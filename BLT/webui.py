"""Copyright (c) 2019 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import subprocess
import ctypes
import sys
import ssl
import csv
import os
import logging
from json import load, dump, dumps, loads
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from time import time, sleep, ctime
from collections import Counter as ct
from ordered_set import OrderedSet
from re import search, findall
from requests import request as rq
from requests import exceptions as ex
from multiprocessing.dummy import Pool as ThreadPool
from flask import Flask, render_template, request, redirect, session, send_file, flash
import cisco_info


def grab_oauth_ccw_order(username, password):
    """function for ccw order api oauth"""

    try:
        with open("ccw_order_cred.json", "r") as f:
            password_creds = load(f)
        cred_tuple = (
            password_creds["client_id"],
            password_creds["client_secret"],
            username,
            password,
        )
        url = "https://cloudsso.cisco.com/as/token.oauth2"
        payload = (
            "client_id=%s&client_secret=%s&grant_type=password&username=%s&password=%s"
            % cred_tuple
        )
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "cache-control": "no-cache",
        }
    except FileNotFoundError:
        print("ccw_order_cred.json is missing...correct this problem")
        return None

    try:
        response = rq("POST", url, data=payload, headers=headers)
        ccwo_access_token = response.json()["access_token"]
        if "profiles" not in os.listdir():
            os.mkdir("profiles")
        if username not in os.listdir("profiles"):
            os.mkdir("profiles//%s" % username)
            os.mkdir("profiles//%s//reports" % username)
        with open("profiles//%s//ccw_order_oauth.json" % username, "w") as f:
            dump({"ts": int(time()), "access_token": ccwo_access_token}, f)
        return ccwo_access_token
    except KeyError:
        return None


def grab_oauth_ccwr(username):
    """Function for ccw-r api oauth"""
    url = "https://cloudsso.cisco.com/as/token.oauth2"
    with open("ccwr_client.json", "r") as f:
        client_creds = load(f)
    print(client_creds)
    payload = "client_id=%s&client_secret=%s&grant_type=client_credentials" % (
        client_creds["client_id"],
        client_creds["client_secret"],
    )
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Host": "cloudsso.cisco.com",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "103",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }
    print(headers)
    response = rq("POST", url, data=payload, headers=headers)
    ccwr_access_token = response.json()["access_token"]
    print(ccwr_access_token)
    with open("profiles//%s//ccwr_oauth.json" % username, "w") as f:
        dump({"ts": int(time()), "access_token": ccwr_access_token}, f)
    return ccwr_access_token


def create_3K_lic_rpt(ccwr_full_list, output_file_list, smart_account):
    """cat3k results report create function
    Create a group on lambda functions to perform RegEx searches
    Creates a CSV formatted Report of 3K licensing content from a file input
    of a CCW-R file export"""
    # Find Header Row based on Serial keyword.
    hr = lambda s: search(".*[Ss][Ee][Rr][Ii][Aa].*", s)
    # Find any SKU containing 3K nomenclature.
    is_3x50 = lambda s: search("3[68]50", s)
    # Find any top level traditonal hardware SKU that also contains license level.
    non_C1_3x50 = lambda s: search("WS-C3[68]50.*-[SEL]", s)
    # Find individual 3K on-box license SKUs.
    lic_C1_3x50 = lambda s: search("C3[68]50-[24][48]-[SL]-[ES]", s)
    # Find any C1 SKU that is less than 24 ports. These have license level
    # as part of the top-level part.
    non_24_48_port_C1 = lambda s: search("C1-WS.*-12.*-[ES]", s)

    # print(dumps(ccwr_full_list[0:5],indent=4))

    # Find CCW-R header row to place into a list
    header = [i for i in ccwr_full_list[0:3] if hr(str(i))]
    # Parse CCW-R lines with any 3x50 SKUs into a list of rows
    dev_3x50 = [i for i in ccwr_full_list if is_3x50(i[0])]
    # Parse CCW-R lines for traditional top-level SKU rows
    non_C1_dev = [i for i in dev_3x50 if non_C1_3x50(i[0])]
    #need to create a list of parent serials for non Cisco ONE devices
    non_C1_dev_parent_serials =[i[3] for i in non_C1_dev]
    # print(dumps(non_C1_dev,indent=4))
    ###Parse CCW-R lines for individual on-box SW upgrade licensing rows
    upg_lics = [i for i in dev_3x50 if lic_C1_3x50(i[0])]
    #need to eliminate duplicate license for newer orders that contain both SW SKU and reflect entitlement at top level.
    upg_lics = [i for i in upg_lics if i[3] not in non_C1_dev_parent_serials]
    # print(dumps(upg_lics,indent=4))
    # Parse C1 SKUs for 3Ks less than 12 ports b/c SW licenses appear in top-level
    non_24_48_port = [i for i in dev_3x50 if non_24_48_port_C1(i[0])]
    # print(dumps(non_24_48_port,indent=4))
    # Concatenate all parsed lists
    parsed_ccwr_rows_list = header + non_C1_dev + upg_lics + non_24_48_port
    # print(dumps(parsed_ccwr_rows_list,indent=4))
    # Perform count of elements in concatenated list and place in dict
    devdict = dict(ct([i[0] for i in parsed_ccwr_rows_list][1:]))
    # Extract top-level SKUs and convert to list of actual licensing SKU that appear in CSSM.
    C3x50 = [
        i[0][3:11] + "-" + i[0][-1]
        for i in parsed_ccwr_rows_list
        if i[0].startswith("WS-C3")
    ]
    C3x50 = C3x50 + [
        i[0][:12].replace(i[0][:5], "C" + "-" + i[0][-1])
        for i in parsed_ccwr_rows_list
        if i[0].startswith("C1-WS")
    ]
    C3x50_E = [i.replace(i[-2:], "-S-E") for i in C3x50 if i.endswith("E")]
    C3x50_S = [i.replace(i[-2:], "-L-S") for i in C3x50 if i.endswith("S")]
    C3x50_L = [i.replace(i[-2:], "-L-L") for i in C3x50 if i.endswith("L")]
    # Extract top-level upgrade license SKUs and convert to list
    upg_lics_indiv = [i[0] for i in upg_lics]
    # Concatenate license lists
    total_upg_lics = C3x50_E + C3x50_S + C3x50_L + upg_lics_indiv
    # Perform count of elements in concatenated list and place in dict
    licdict = dict(ct(total_upg_lics))
    # Create output file
    for i in output_file_list:
        with open(i, "w") as f:
            f.write("Top-Level Device OR License,-----,Count\n")
            for i in devdict:
                f.write(i + ",-----," + str(devdict[i]) + "\n")
            f.write(4 * "\n")
            f.write(
                "LICENSES to be deposited in %s\n\n" % smart_account
                + "License,-----,Count\n"
            )
            for i in licdict:
                f.write(i + ",-----," + str(licdict[i]) + "\n")
            f.write(4 * "\n")
            f.write("Full License/Device Breakout from CCW-R\n\n")
            for i in parsed_ccwr_rows_list:
                for j in i:
                    f.write(j)
                    f.write(",")
                f.write("\n")


def ccwo_order_status(username, so_num):
    try:
        with open("profiles//%s//ccw_order_oauth.json" % username, "r") as f:
            jl = load(f)
        ccwo_access_token = jl["access_token"]
    except Exception as e:
        print(e)

    url = "https://api.cisco.com/commerce/ORDER/v2/sync/checkOrderStatus"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Request-ID": "Type: Integer",
        "Accept-Language": "en_us",
        "Authorization": "Bearer %s" % ccwo_access_token,
        "cache-control": "no-cache",
        "Host": "api.cisco.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }


    if so_num.startswith("8"):
        payload = dumps(
            {
                "GetPurchaseOrder": {
                    "value": {
                        "DataArea": {
                            "PurchaseOrder": [
                                {
                                    "PurchaseOrderHeader": {
                                        "ID": {"value": ""},
                                        "DocumentReference": [
                                            {"ID": {"value": so_num}}
                                        ],
                                        "SalesOrderReference": [{"ID": {"value": ""}}],
                                        "Description": [
                                            {"value": "Yes", "typeCode": "details"}
                                        ],
                                    }
                                }
                            ]
                        },
                        "ApplicationArea": {
                            "CreationDateTime": "datetime",
                            "BODID": {"value": "BoDID-test", "schemeVersionID": "V1"},
                        },
                    }
                }
            }
        )
    else:
        payload = dumps(
            {
                "GetPurchaseOrder": {
                    "value": {
                        "DataArea": {
                            "PurchaseOrder": [
                                {
                                    "PurchaseOrderHeader": {
                                        "ID": {"value": ""},
                                        "DocumentReference": [{"ID": {"value": ""}}],
                                        "SalesOrderReference": [
                                            {"ID": {"value": so_num}}
                                        ],
                                        "Description": [
                                            {"value": "Yes", "typeCode": "details"}
                                        ],
                                    }
                                }
                            ]
                        },
                        "ApplicationArea": {
                            "CreationDateTime": "datetime",
                            "BODID": {"value": "BoDID-test", "schemeVersionID": "V1"},
                        },
                    }
                }
            }
        )
    response = rq("POST", url, data=payload, headers=headers)
    result = response.json()
    result = \
    result["ShowPurchaseOrder"]["value"]["DataArea"]["PurchaseOrder"][0]["PurchaseOrderHeader"]["Extension"][4]["Name"][
        0]["value"]

    result = {so_num: result}
    return result


def ccwr_search_request(username, searchType="serialNumbers", search_list=[]):
    """ccw-r search function"""
    try:
        with open("profiles//%s//ccwr_oauth.json" % username, "r") as f:
            jl = load(f)
        print("ccwr oauth2 token age: " + str(int(time()) - jl["ts"]) + " seconds.")
        if (time() - jl["ts"]) > 3500:
            ccwr_access_token = grab_oauth_ccwr(username)
        else:
            ccwr_access_token = jl["access_token"]
    except:
        ccwr_access_token = grab_oauth_ccwr(username)

    url = "https://api.cisco.com/ccw/renewals/api/v1.0/search/lines"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Request-ID": "Type: Integer",
        "Accept-Language": "en_us",
        "Authorization": "Bearer %s" % ccwr_access_token,
        "Cache-Control": "no-cache",
        "Host": "api.cisco.com",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "113",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }

    offset = 0
    payload = dumps(
        {
            searchType: search_list,
            "limit": 1000,
            "offset": offset,
            "configurations": True,
        }
    )

    with open('counter_dict.json','r') as f:
        counter_dict=load(f)
    current_hr=int(ctime().split()[3].split(':')[0])
    current_dt=ctime().split()[1:3]
    if (current_hr != counter_dict['current_hr']) or (current_dt != counter_dict['current_dt']):
        with open('counter_dict.json','w') as f:
            counter_dict['current_hr']=current_hr
            counter_dict['page_counter']=0
            counter_dict['over']=False
            counter_dict['current_dt']=current_dt
            dump(counter_dict,f)
    if counter_dict['over']==False :
        response = rq("POST", url, data=payload, headers=headers)
        if response.status_code == 403:
            ccwr_access_token = grab_oauth_ccwr()
            headers["Authorization"] = "Bearer %s" % ccwr_access_token
            response = rq("POST", url, data=payload, headers=headers)
        else:
            ccwr_response = response.json()
            try:
                counter_dict['page_counter']=counter_dict['page_counter']+(int(ccwr_response["totalRecords"]/1000)+1)
            except:
                pass
            with open('counter_dict.json','w') as f:
                if counter_dict['page_counter'] > 298:
                    counter_dict['over']=True
                    ts=str(int(time()))
                    with open('jobs/%s.%s'%(username,ts),'w') as job:
                        dump(search_list,job)
                    print('\n\n\nDo some scheduling, the paging counter just went over!\n\n\n')
                    dump(counter_dict,f)
                    ccwr_response='over'
                    return ccwr_response, ccwr_access_token
                dump(counter_dict,f)

    if counter_dict['over']==True:
        ccwr_response='over'
        ts=str(int(time()))
        if search_list != []:
            with open('jobs/%s.%s'%(username,ts),'w') as job:
                dump(search_list,job)
        return ccwr_response, ccwr_access_token


    else:
        response=None

    try:
        if int(ccwr_response["totalRecords"]) > 1000:
            additional_requests = int(int(ccwr_response["totalRecords"]) / 1000)
            for i in range(additional_requests):
                offset += 1000
                payload = dumps(
                    {
                        searchType: search_list,
                        "limit": 1000,
                        "offset": offset,
                        "configurations": True,
                    }
                )
                addtl_response = rq("POST", url, data=payload, headers=headers)
                addtl_response = addtl_response.json()
                ccwr_response["instances"] = (
                    ccwr_response["instances"] + addtl_response["instances"]
                )
        return ccwr_response, ccwr_access_token
    except:
        return None, ccwr_access_token


def ccwr_create_table(username, ccwr_response, sa_list):
    """function to create table for ccw-r results"""
    # with open('contract_response.json','r') as f:
    # jsl=load(f)
    ccwr_full_list = [
        [
            "Product Number",
            "Product Description",
            "Serial Number",
            "Parent Serial Number",
            "Instance Number",
            "Sales Order Number",
            "End Customer Name",
            "Smart Account Name",
        ]
    ]
    ccwr_out_ts=str(time())
    raw_ccwr_output_csv = "profiles/%s/current_raw_CCWR_output.csv" % username
    raw_ccwr_output_csv_report = "profiles/%s/reports/CCWR_raw_output-%s.csv" % (username,ccwr_out_ts)
    ccwr_out_filelist=[raw_ccwr_output_csv,raw_ccwr_output_csv_report]
    # print(dumps(ccwr_response, sort_keys=True, indent=4))
    try:
        for i in ccwr_response["instances"]:
            l = []
            try:
                l.append(i["product"]["number"])
            except:
                l.append("")
            try:
                l.append(i["product"]["description"].lstrip("^").replace(",", ";"))
            except:
                l.append("")
            try:
                l.append(i["serialNumber"])
            except:
                l.append("")
            try:
                l.append(i["parentSerialNumber"])
            except:
                l.append("")
            try:
                l.append(i["instanceNumber"])
            except:
                l.append("")
            try:
                l.append(i["salesOrderNumber"])
            except:
                l.append("")
            try:
                l.append(i["endCustomer"]["name"])
            except:
                l.append("")
            try:
                if not sa_list:
                    l.append("")
                else:
                    for i in sa_list:
                        for k, v in i.items():
                            if k == l[5]:
                                l.insert(7, v)
                            else:
                                l.append("")
            except:
                l.append("")
            l = l[:8]
            ccwr_full_list.append(l)
        for i in ccwr_out_filelist:
            with open(i, "w") as f:
                for i in ccwr_full_list:
                    for j in i:
                        f.write(j + ",")
                    f.write("\n")
        return ccwr_full_list
    except:

        with open(raw_ccwr_output_csv, "w") as f:
            f.write("No Data")
        ccwr_temp_list = []
        return ccwr_temp_list


def file_SN_search(inventory_file):
    """serial number csv parser function"""
    serial_chk = lambda s: search(".*[Ss][Ee][Rr][Ii][Aa].*", s)
    sn_chk = lambda s: search(".*[Ss][Nn].*", s)
    with open(inventory_file) as f:
        rl = f.readlines()
    '''will assume tht the table width is reflected in the first 5 rows AND is the maximum width'''
    col_width=max([len(i.split(",")) for i in rl[0:5]])
    print('%s is the column width'%col_width)
    '''will find the row indices for anything containing [Ss][Ee][Rr][Ii][Aa] or [Ss][Nn]'''
    sn_row_index_list=[rl.index(i) for i in rl[0:5] if serial_chk(i) or sn_chk(i)]
    print('%s is the sn row index list'%sn_row_index_list)
    '''will only consider the first row that matches the column width'''
    sn_row_index=[i for i in sn_row_index_list if len(rl[i].split(","))==col_width][0]
    print('%s is the sn row index'%sn_row_index_list)
    '''create the header'''
    header = rl[sn_row_index].split(",")
    print('%s is the header'%header)
    '''find the column indices that contains [Ss][Ee][Rr][Ii][Aa] or [Ss][Nn]'''
    sn_col_idx_list = [header.index(i) for i in header if serial_chk(i) or sn_chk(i)]
    print('%s : are the column indices'%sn_col_idx_list)
    '''iterate thru column indices and rows in file to create a list of SNs based on column headers'''
    csv_sn_list = [i.split(",")[j] for j in sn_col_idx_list for i in rl[(sn_row_index+1):]]
    return csv_sn_list


def file_SN_search_reg(inventory_file):
    with open(inventory_file) as f:
        data = f.read()
        csv_sn_list_reg = findall(r"[A-Z]{3}[A-Za-z0-9]{8}", data)
        return csv_sn_list_reg


def ccwo_search_request(username, so_list=[]):
    """ccw order search function"""
    try:
        with open("profiles//%s//ccw_order_oauth.json" % username, "r") as f:
            jl = load(f)
        print(
            "ccw order oauth2 token age: " + str(int(time()) - jl["ts"]) + " seconds."
        )

        ccwo_access_token = jl["access_token"]
    except FileNotFoundError as e:
        print(e)
        pass

    url = "https://api.cisco.com/commerce/ORDER/sync/getSerialNumbers"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Request-ID": "Type: Integer",
        "Accept-Language": "en_us",
        "Authorization": "Bearer %s" % ccwo_access_token,
        "cache-control": "no-cache",
        "Host": "api.cisco.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    ccwo_sn_list = []
    ccwo_error_so_list = []
    so_data_matrix_header = [
        ["Sales Order Number", "Line Number", "Part Number", "Quantity"]
    ]
    so_data_matrix = []
    for so_num in so_list:
        try:
            pageNumber = 1
            payload = dumps(
                {
                    "serialNumberRequest": {
                        "salesOrderNumber": so_num,
                        "pageNumber": str(pageNumber),
                    }
                }
            )
            response = rq("POST", url, data=payload, headers=headers)
            rj = response.json()
            so_data_matrix = so_data_matrix + [
                [so_num, i["lineNumber"], i["partNumber"], i["quantity"]]
                for i in rj["serialNumberResponse"]["serialDetails"]["lines"]
            ]
            # print(dumps(rj, sort_keys=True, indent=4))
            total_pages = int(
                rj["serialNumberResponse"]["responseHeader"]["totalPages"]
            )
            if total_pages > 1:
                # print("SO# %s totalPages is great than 1"%str(so_num))
                pageNumber = 2
                for i in range(total_pages - 1):
                    payload = dumps(
                        {
                            "serialNumberRequest": {
                                "salesOrderNumber": so_num,
                                "pageNumber": str(pageNumber),
                            }
                        }
                    )
                    addtl_page = rq("POST", url, data=payload, headers=headers)
                    addtl_page = addtl_page.json()
                    so_data_matrix = so_data_matrix + [
                        [so_num, i["lineNumber"], i["partNumber"], i["quantity"]]
                        for i in addtl_page["serialNumberResponse"]["serialDetails"][
                            "lines"
                        ]
                    ]
                    pageNumber += 1
                    # print(addtl_page)
                    rj["serialNumberResponse"]["serialDetails"]["lines"] = (
                        rj["serialNumberResponse"]["serialDetails"]["lines"]
                        + addtl_page["serialNumberResponse"]["serialDetails"]["lines"]
                    )
            sn_parse1 = [
                i for i in rj["serialNumberResponse"]["serialDetails"]["lines"]
            ]
            sn_parse2 = [i["serialNumbers"] for i in sn_parse1]
            # print(dumps(sn_parse2, indent=4))
            print(
                rj["serialNumberResponse"]["responseHeader"]["totalPages"]
                + " is the total number of pages in the CCWO response for SO#%s"
                % so_num
            )
            for i in sn_parse2:
                for j in i:
                    ccwo_sn_list.append(str(j["serialNumber"]))

        except Exception:
            print(str(so_num) + " SO# could not be retrieved")
            ###logger.debug(so_num + " SO# could not be retrieved")
            ccwo_error_so_list.append(so_num)
            # print(str(so_num)+' cannot be retrieved from ccw.')
            continue

    print(str(len(ccwo_sn_list)) + " is the length of the ccwo sn list.")
    # print(ccwo_sn_list)
    ##logger.debug(ccwo_sn_list)
    so_data_matrix.sort()
    so_data_matrix = so_data_matrix_header + so_data_matrix
    return ccwo_sn_list, ccwo_error_so_list, so_data_matrix


app = Flask(__name__)
app.secret_key = "CHANGE_THIS_KEY_IF_RUNNING_PERSISTENTLY"
app.permanent_session_lifetime = timedelta(minutes=10)
ALLOWED_EXTENSIONS = {"csv"}
#CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#CONTEXT.load_cert_chain("blt.cisco.com-60405.cer", "blt.key")

@app.route("/login", methods=["POST"])
def do_admin_login():
    """Login function"""
    try:
        username = request.form["username"]
        password = request.form["password"]
        sadomain = request.form["SADomain"]
        session["username"] = username
        session["sadomain"] = sadomain
        ccwo_access_token = grab_oauth_ccw_order(username, password)
        if ccwo_access_token:
            session["logged_in"] = True
        else:
            flash("Invalid Credentials...Try again")
            return render_template("login.html")
        return redirect("/")
    except ex.ConnectionError:
        username = request.form["username"]
        sadomain = request.form["SADomain"]
        session["username"] = username
        session["sadomain"] = sadomain
        session["logged_in"] = True
        if username not in os.listdir("profiles"):
            os.mkdir("profiles//%s" % username)
            os.mkdir("profiles//%s//reports" % username)

        with open("profiles//%s//ccwr_oauth.json" % username, "w+") as f:
            f.write("Working Offline")
        return redirect("/")


@app.route("/logout")
def logout():
    """Function to log out of application"""
    session["logged_in"] = False
    return redirect("/")


"""Need to be able to clear the cookie/session data for each data source."""


@app.route("/clearcsv")
def clearcsv():
    """Function to clear SN file names"""
    try:
        session.pop("csv_sn_file_name_list")
        return redirect("/serialnumber")
    except:
        return redirect("/serialnumber")


@app.route("/clearwebsn")
def clearwebsn():
    """Function to clear webform SN input"""
    print('clearing webform SN input.')
    ##logger.debug("cleared webform data in /clearwebsn")
    try:
        session.pop("webform_sn_qty")
    except:
        pass
    try:
        session.pop("raw_sn_input_list")
    except:
        pass
    return redirect("/serialnumber")


@app.route("/clearso")
def clearso():
    """Function to clear sales orders"""
    try:
        session.pop("ccwo_sn_list_name", "so_list")
        return redirect("/")
    except:
        return redirect("/")


@app.route("/clearsn")
def clearsn():
    """Function to clear serial numbers"""
    try:
        session.pop("raw_sn_input_list")
    except:
        pass
    try:
        session.pop("csv_sn_file_name_list")
    except:
        pass
    try:
        session.pop("webform_sn_qty")
    except:
        pass
    return redirect("/")


@app.route("/clearscan")
def clearscan():
    """Function to clear scan results"""
    try:
        session.pop("scan_sn_list_name")
    except:
        pass
    return redirect("/")


@app.route("/")
def webroot():
    """Function for main application page"""
    if not session.get("logged_in"):
        return render_template("login.html")
    username = session["username"]
    try:
        scan_sn_list_name = session["scan_sn_list_name"]
        scan_sn_list = file_SN_search(scan_sn_list_name)
        len_scan_sn_list = str(len(scan_sn_list))
        scan_data = "Network devices scanned: %s" % (len_scan_sn_list)
    except:
        scan_data = "No scan SN Data"
        scan_sn_list = []
    try:
        ccwo_sn_list_name = session["ccwo_sn_list_name"]
        # print(ccwo_sn_list_name)
        ##logger.debug(ccwo_sn_list_name, extra=username)
        # ccwo_sn_list=session['ccwo_sn_list']
        with open(ccwo_sn_list_name, "r") as f:
            ccwo_sn_list = load(f)
        # print(ccwo_sn_list)
        ##logger.debug(ccwo_sn_list, extra=username)

        formatted_so_list = str(session["so_list"]).rstrip("]").lstrip("[")
        len_ccwo_sn_list = str(len(ccwo_sn_list))
        so_data = "SOs %s were searched, returning %s serial numbers." % (
            formatted_so_list,
            len_ccwo_sn_list,
        )
    except:
        ccwo_sn_list = []
        so_data = "No SO Data"

    try:
        raw_sn_input_list = session["raw_sn_input_list"]
        len_raw_sn_input_list = str(len(raw_sn_input_list))
        sn_data_web = "Webform input SN count: %s" % len_raw_sn_input_list

    except:
        sn_data_web = "No Webform SN Data"
        raw_sn_input_list = []
    try:
        csv_sn_file_name_list = session["csv_sn_file_name_list"]
        print('webroot csv sn file name list is: %s'%csv_sn_file_name_list)
        csv_sn_list=[]

        for i in csv_sn_file_name_list:
            try:
                j = file_SN_search(i)
                csv_sn_list=csv_sn_list+j
            except IndexError:
                j = file_SN_search_reg(i)
                csv_sn_list = csv_sn_list + j

        len_csv_sn_list = str(len(csv_sn_list))
        sn_data_csv = "CSV input SN count: %s" % len_csv_sn_list

    except:
        sn_data_csv = "No File SN Data"
        csv_sn_list = []

    ccwr_search_list = csv_sn_list + raw_sn_input_list + ccwo_sn_list + scan_sn_list
    ccwr_search_list = list(set(ccwr_search_list))
    with open("profiles/%s/current_CCWR_input_SNs.json" % username, "w") as f:
        dump(ccwr_search_list, f)
    data_total = str(len(ccwr_search_list))
    return render_template(
        "index.html",
        so_data=so_data,
        sn_data_web=sn_data_web,
        sn_data_csv=sn_data_csv,
        data_total=data_total,
        scan_data=scan_data,
    )


@app.route("/ccwrresults", methods=["GET"])
def ccwrresults_get():
    """Function to display ccw-r final results"""
    start_time = datetime.now()
    session.pop("_flashes", [])
    if not session.get("logged_in"):
        return render_template("login.html")
    try:
        username = session["username"]
        sadomain = session["sadomain"]
        with open("profiles/%s/current_CCWR_input_SNs.json" % username, "r") as f:
            ccwr_search_list = load(f)
        ccwr_response, ccwr_access_token = ccwr_search_request(
            username, "serialNumbers", ccwr_search_list
        )
        if ccwr_response=='over':
            return render_template(
                "apiover.html"
            )
        so_for_sa_list = []
        elapsed_time = datetime.now() - start_time
        print("CCW-R API Time:")
        print(elapsed_time)
        start_time = datetime.now()
        for i in ccwr_response["instances"]:
            so_for_sa_list.append(i["salesOrderNumber"])
        so_for_sa_list = [x for x in so_for_sa_list if x.startswith("1") or x.startswith("8") or x.startswith("9")]
        so_for_sa_list_dedup = []
        [so_for_sa_list_dedup.append(x) for x in so_for_sa_list if x not in so_for_sa_list_dedup]
        threads = []
        sa_list = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            for so_num in so_for_sa_list_dedup:
                threads.append(
                    executor.submit(
                        ccwo_order_status, username, so_num
                    )
                )
        for task in as_completed(threads):
            try:
                result = task.result()
                sa_list.append(result)
            except:
                continue
        elapsed_time = datetime.now() - start_time
        print("CCWO API Time:")
        print(elapsed_time)
        ccwr_temp_list = ccwr_create_table(username, ccwr_response, sa_list)
        os=OrderedSet([dumps(i) for i in ccwr_temp_list])
        ccwr_full_list=[loads(i) for i in os]
        output_file = "profiles/%s/CAT3K_License_Report.csv" % username
        reportstamp=str(int(time()))
        report_output_file ="profiles/%s/reports/CAT3K_License_Report.%s.csv" % (username,reportstamp)
        output_file_list=[output_file,report_output_file]
        create_3K_lic_rpt(ccwr_full_list, output_file_list, sadomain)
        # print(ccwr_full_list)
        ##logger.debug(ccwr_full_list)
        if sadomain == "":
            body = (
                "#### Attach either the CCWR Raw Data or Cat3K License Report to this email####"
                "<--Delete before sending %0D%0A"
                + "%0D%0A"
                + "#### Please make sure to include the smart account and virtual account "
                  "for license deposit####<--Delete before sending%0D%0A"
                + "%0D%0A"
                + "Cisco Licensing Team,%0D%0A"
                + "%0D%0A"
                + "Please convert traditional licensing for products in the attached "
                  "spreadsheet to smart licensing. "
                + "The Smart Account for this action is <Insert your SA here>. "
                + "The Virtual Accouont for this action is <Insert your VA here>."
            )
            mailto = "licensing@cisco.com"
            subject = "Smart Licensing Entitlement Request"
            email = "mailto:{mailto}?subject={subject}&body={body}".format(
                mailto=mailto, subject=subject, body=body
            )
            return render_template(
                "ccwrresults.html", ccwr_full_list=ccwr_full_list, email=email
            )

        body = (
            "#### Attach either the CCWR Raw Data or Cat3K License Report to this email####"
            "<--Delete before sending %0D%0A"
            + "%0D%0A"
            + "#### Please verify the virtual account in {sadomain} for license deposit####"
              "<--Delete before sending%0D%0A".format(
                  sadomain=sadomain)
            + "%0D%0A"
            + "Cisco Licensing Team,%0D%0A"
            + "%0D%0A"
            + "Please convert traditional licensing for products in the attached "
              "spreadsheet to smart licensing. "
            + "The Smart Account for this action is {sadomain}.".format(
                sadomain=sadomain)
            + "The Virtual Accouont for this action is <Insert your VA here>."
        )
        mailto = "licensing@cisco.com"
        subject = "Smart Licensing Entitlement Request"
        email = "mailto:{mailto}?subject={subject}&body={body}".format(
            mailto=mailto, subject=subject, body=body
        )
        elapsed_time = datetime.now() - start_time
        return render_template(
            "ccwrresults.html", ccwr_full_list=ccwr_full_list, email=email
        )

    except FileNotFoundError:
        flash(
            "No data submitted. Gather entitlement data via one of the above methods."
        )
        return render_template("index.html")

    except ex.ConnectionError:
        flash(
            "Connection to Cisco.com can not be established. Check network connectivity."
        )
        return render_template("index.html")

    except TypeError:
        flash(
            "No data submitted. Gather entitlement data via one of the above methods."
        )
        return render_template("index.html")



@app.route("/download3Krpt", methods=["GET"])
def download3Krpt_get():
    """Function to download Cat3K report"""
    username = session["username"]
    file_download = "profiles/%s/CAT3K_License_Report.csv" % username
    return send_file(file_download, as_attachment=True)


@app.route("/downloadccwrraw", methods=["GET"])
def downloadccwrraw_get():
    """Function to download ccw-r raw data"""
    username = session["username"]
    file_download = "profiles/%s/current_raw_CCWR_output.csv" % username
    return send_file(file_download, as_attachment=True)


@app.route("/downloadbltuserguide", methods=["GET"])
def downloadbltuserguide():
    file_download = "docs/BLT-User-Guide.pdf"
    return send_file(file_download, as_attachment=True)


@app.route("/downloadbltinstallguide", methods=["GET"])
def downloadbltinstallguide():
    file_download = "docs/BLT-Install-Guide.pdf"
    return send_file(file_download, as_attachment=True)


@app.route("/serialnumber", methods=["GET", "POST"])
def serialnumber():
    """Function to search serial numbers"""
    if not session.get("logged_in"):
        return render_template("login.html")

    username = session["username"]
    if request.method == "GET":
        try:
            csv_sn_file_name_list=session["csv_sn_file_name_list"]
        except:
            pass
        try:
            webform_sn_qty=session["webform_sn_qty"]
        except:
            pass

    if request.method == "POST":
        try:
            searchsn = str(request.form["searchsn"])
            if searchsn != '':
                form_sn_input_list = searchsn.split(",")
            else:
                form_sn_input_list=[]
            try:
                raw_sn_input_list=session["raw_sn_input_list"]
                print(raw_sn_input_list)
                ##logger.debug(raw_sn_input_list)
            except:
                raw_sn_input_list=[]
            raw_sn_input_list=raw_sn_input_list+form_sn_input_list
            webform_sn_qty=len(raw_sn_input_list)
            session["raw_sn_input_list"] = raw_sn_input_list
            session["webform_sn_qty"] = webform_sn_qty
        except:
            pass
        try:
            snfile = request.files["csvfile"]
            UPLOAD_FOLDER = "profiles/%s/" % username
            app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
            snfile.save(os.path.join(app.config["UPLOAD_FOLDER"], snfile.filename))
            csv_sn_file_name = UPLOAD_FOLDER + snfile.filename
            try:
                csv_sn_file_name_list=session["csv_sn_file_name_list"]
                print(csv_sn_file_name_list)
                ##logger.debug(csv_sn_file_name_list)
            except Exception as E:
                print('Exception: %s'%E)
                ##logger.debug('Exception: %s'%E)
                csv_sn_file_name_list=[]
                pass
            csv_sn_file_name_list.append(csv_sn_file_name)
            print('csv file name list is: %s'%csv_sn_file_name_list)
            session["csv_sn_file_name_list"] = csv_sn_file_name_list
        except:
            pass
    try:
        csv_sn_file_name_list=session["csv_sn_file_name_list"]
    except:
        csv_sn_file_name_list=[]
        pass
    try:
        webform_sn_qty=session["webform_sn_qty"]
    except:
        webform_sn_qty=0
        pass
    return render_template("serialnumber.html", csv_sn_file_name_list=csv_sn_file_name_list, webform_sn_qty=webform_sn_qty)


@app.route("/salesorder", methods=["GET", "POST"])
def salesorder():
    """Function to search sales order numbers"""
    if not session.get("logged_in"):
        return render_template("login.html")

    if request.method == "GET":
        return render_template("salesorder.html")
    try:
        if request.method == "POST":
            username = session["username"]
            searchso = str(request.form["searchso"])
            # print(searchso)
            #logger.debug("searchso")
            so_list = searchso.split(",")
            session["so_list"] = so_list
            with open("profiles//%s//ccw_order_oauth.json" % username, "r") as f:
                jl = load(f)
            # print('ccw order oauth2 token age: '+str(int(time())-jl['ts'])+' seconds.')
            if (time() - jl["ts"]) > 3500:
                session["logged_in"] = False
                return redirect("/")

            ccwo_sn_list, ccwo_error_so_list, so_data_matrix = ccwo_search_request(
                username, so_list
            )
            ccwo_success_so = [i for i in so_list if i not in ccwo_error_so_list]
            ccwo_sn_list_name = "profiles/%s/current_SO_search.json" % username
            session["ccwo_sn_list_name"] = ccwo_sn_list_name
            with open(ccwo_sn_list_name, "w") as f:
                dump(ccwo_sn_list, f)
            # sleep(1)
            return render_template(
                "soresults.html",
                so_data_matrix=so_data_matrix,
                ccwo_success_so=ccwo_success_so,
                ccwo_error_so_list=ccwo_error_so_list,
            )
    except FileNotFoundError:
        flash(
            "Connection to Cisco.com can not be established. Check network connectivity."
        )
        return render_template("salesorder.html")


@app.route("/scan", methods=["GET"])
def scan():
    """Function to scan network for serial numbers"""
    if not session.get("logged_in"):
        return render_template("login.html")
    title = ["Product ID", "Serial Number", "License Entitlement"]
    with open("device_info.csv", "w+") as devFile:
        devwriter = csv.writer(devFile, lineterminator="\n")
        devwriter.writerow(title)

    # Define start time
    start_time = datetime.now()

    # Define the number of threads
    num_threads = int(10)
    pool = ThreadPool(num_threads)

    # Start threads
    pool.starmap(cisco_info.getDevInfo, SWLIST)
    pool.close()
    pool.join()
    username = session["username"]
    UPLOAD_FOLDER = "profiles/%s/" % username
    if os.path.exists(UPLOAD_FOLDER + "device_info.csv"):
        os.remove(UPLOAD_FOLDER + "device_info.csv")
    os.rename("device_info.csv", UPLOAD_FOLDER + "device_info.csv")
    scan_sn_list_name = "profiles/%s/device_info.csv" % username
    session["scan_sn_list_name"] = scan_sn_list_name
    print(session["scan_sn_list_name"])
    print("\nReview collected information in device_info.csv")
    print("\nElapsed time: " + str(datetime.now() - start_time))
    return redirect("/")


@app.route("/scanupload", methods=["GET", "POST"])
def scanupload():
    """Function to accept CSV file for on prem network scanning"""
    if not session.get("logged_in"):
        return render_template("login.html")

    username = session["username"]
    UPLOAD_FOLDER = "profiles/%s/" % username
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    if request.method == "POST":
        f = request.files["csvfile"]
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
        data = cisco_info.getLoginInfo(UPLOAD_FOLDER + f.filename)
        global SWLIST
        SWLIST = cisco_info.convertLoginDict(data)
        if not SWLIST:
            flash("CSV formatted incorrectly...Try again")
            return render_template("scanupload.html")
        return render_template("netscan.html", csvinfo=SWLIST)
    return render_template("scanupload.html")


@app.route("/help", methods=["GET"])
def helppage():
    """Function to return help page"""
    return render_template("help.html")

@app.route("/Reports", methods=["GET"])
def reportpage():
    """Function to return user reports"""
    if not session.get("logged_in"):
        return render_template("login.html")
    username = session["username"]
    files_list = os.listdir('profiles/%s/reports'%username)
    spooledreport_list=[i for i in files_list if 'spooled' in i]
    spooledreport_list.sort()
    report_list=[i for i in files_list if 'spooled' not in i]
    report_list.sort()

    return render_template("Reports.html",report_list=report_list, spooledreport_list=spooledreport_list)

@app.route("/downloadreports/<filename>", methods=["GET"])
def downloadreport(filename):
    """Function to return user reports"""
    if not session.get("logged_in"):
        return render_template("login.html")
    username = session["username"]
    file_download = "profiles/%s/reports/%s" % (username,filename)
    return send_file(file_download, as_attachment=True)

@app.route("/deletereports/<filename>", methods=["GET"])
def deletereport(filename):
    """Function to return user reports"""
    if not session.get("logged_in"):
        return render_template("login.html")
    username = session["username"]
    file_delete = "profiles/%s/reports/%s" % (username,filename)
    os.remove(file_delete)
    files_list = os.listdir('profiles/%s/reports'%username)
    spooledreport_list=[i for i in files_list if 'spooled' in i]
    spooledreport_list.sort()
    report_list=[i for i in files_list if 'spooled' not in i]
    report_list.sort()
    return render_template("Reports.html",report_list=report_list,spooledreport_list=spooledreport_list)



@app.route("/teamsupport", methods=["GET"])
def teamsupport():
    """Function to join teams space for support"""
    return redirect("https://eurl.io/#BkZG3vfeU")


if __name__ == "__main__":
    if sys.platform == "win32":
        app.run(host="127.0.0.1", debug=True, ssl_context="adhoc")
    else:
        app.run(host="0.0.0.0", debug=True, ssl_context="adhoc")

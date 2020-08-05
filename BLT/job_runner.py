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

from os import listdir, remove, mkdir
from json import load, loads, dump, dumps
from time import sleep, time, ctime
from requests import request as rq
from requests import exceptions as ex
from webui import create_3K_lic_rpt
from requests_toolbelt.multipart.encoder import MultipartEncoder


def grab_oauth_ccwr():
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
    with open("ccwr_oauth_age.json", "w") as f:
        dump({"ts": int(time()), "access_token": ccwr_access_token}, f)
    return ccwr_access_token

def ccwr_search_request(username, ccwr_access_token, searchType="serialNumbers", search_list=[]):
    """ccw-r search function"""


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
                    #print('\n\n\nDo some scheduling, the paging counter just went over!\n\n\n')
                dump(counter_dict,f)

    else:
        response=None
        ts=str(int(time()))
        with open('jobs/%s.%s'%(username,ts),'w') as job:
            dump(search_list,job)
        #print('\n\n\nDo some scheduling , the over flag is set!\n\n\n')

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

def ccwr_create_table(username, ccwr_response):
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
        ]
    ]
    report_filename=username+'-'+str(time())
    raw_ccwr_output_csv = "profiles/%s/reports/%s-raw-spooled.csv" % (username,report_filename)
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

            l = l[:8]
            ccwr_full_list.append(l)

        with open(raw_ccwr_output_csv, "w") as f:
            for i in ccwr_full_list:
                for j in i:
                    f.write(j + ",")
                f.write("\n")
        return ccwr_full_list, raw_ccwr_output_csv
    except:

        with open(raw_ccwr_output_csv, "w") as f:
            f.write("No Data")
        ccwr_temp_list = []
        return ccwr_temp_list, raw_ccwr_output_csv


def teams_notification(username, raw_ccwr_output_csv):
    with open("teams_token.json", "r") as f:
        token = load(f)
    token = token["bearer_token"]
    url = "https://api.ciscospark.com/v1/people?email={username}@cisco.com".format(username=username)
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }
    response = rq("GET", url, headers=headers)
    result = response.json()
    id = result["items"][0]["id"]
    url = "https://api.ciscospark.com/v1/messages"
    payload = MultipartEncoder({"toPersonId": id,
                               "text": "Your latest report from blt.cisco.com is ready for download.",
                               "files": (raw_ccwr_output_csv, open(raw_ccwr_output_csv, "rb"),
                               "text/csv")})

    headers = {
        'Authorization': 'Bearer {token}'.format(token=token),
        'Content-Type': payload.content_type
    }
    response = rq("POST", url, headers=headers, data=payload)
    result = response.json()
    print("Notification sent to {username}".format(username=username))
    print(result)


if __name__ =='__main__':

    while True:
        sleep(10)
        with open ('counter_dict.json', 'r') as f:
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

        if counter_dict['over'] != True:
            with open("ccwr_oauth_age.json","r") as f:
                ts=load(f)
            age=int(time()) - int(ts['ts'])
            if age > 3500:
                ccwr_access_token=grab_oauth_ccwr()
            else:
                ccwr_access_token=ts['access_token']

            try:
                jobslist=listdir('jobs')
            except FileNotFoundError:
                mkdir = mkdir("jobs")
                jobslist = listdir('jobs')

            for i in jobslist:
                sleep(5)
                username=i.split('.')[0]
                jobfile='jobs/'+i
                with open(jobfile,'r') as f:
                    search_list=load(f)
                ccwr_response, ccwr_access_token = ccwr_search_request(username,ccwr_access_token,"serialNumbers", search_list)
                ccwr_full_list, raw_ccwr_output_csv = ccwr_create_table(username, ccwr_response)
                filestamp=str(time())
                output_file='profiles/%s/reports/CAT3K_License_Report.%s-spooled.csv'%(username,filestamp)
                output_file_list=[output_file]
                create_3K_lic_rpt(ccwr_full_list, output_file_list, None)
                remove(jobfile)
                teams_notification(username, raw_ccwr_output_csv)

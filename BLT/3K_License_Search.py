from json import load,dumps,dump
from requests import request
from time import time
from re import search
from collections import Counter as ct



def grab_oauth_ccw_order():
    with open ('ccw_order_cred.json','r') as f:
        password_creds=load(f)
    cred_tuple=(password_creds['client_id'],password_creds['client_secret'],password_creds['username'],password_creds['password'])
    url = "https://cloudsso.cisco.com/as/token.oauth2"
    payload = "client_id=%s&client_secret=%s&grant_type=password&username=%s&password=%s"%cred_tuple
    headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "application/json",
    'cache-control': "no-cache",
    }

    response = request("POST", url, data=payload, headers=headers)
    ccwo_access_token=response.json()['access_token']
    with open ('ccw_order_oauth.json','w') as f:
        dump({'ts':int(time()),'access_token':ccwo_access_token},f)
    return ccwo_access_token


def grab_oauth_ccwr():
    url = "https://cloudsso.cisco.com/as/token.oauth2"
    with open ('ccwr_client.json','r') as f:
        client_creds=load(f)
    payload = "client_id=%s&client_secret=%s&grant_type=client_credentials"%(client_creds['client_id'],client_creds['client_secret'])
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "cloudsso.cisco.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "103",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = request("POST", url, data=payload, headers=headers)
    ccwr_access_token=response.json()['access_token']
    with open ('ccwr_oauth.json','w') as f:
        dump({'ts':int(time()),'access_token':ccwr_access_token},f)
    return ccwr_access_token

def file_SN_search(inventory_file):
    with open(inventory_file) as f:
        rl=f.readlines()
    header=rl[0].split(',')
    sn_col_idx=[header.index(i) for i in header if 'erial' in i][0]
    csv_sn_list=[i.split(',')[sn_col_idx] for i in rl[1:]]
    return csv_sn_list


def ccwo_search_request(so_list=[]):

    try:
        with open('ccw_order_oauth.json','r') as f:
            jl=load(f)
        print('ccw order oauth2 token age: '+str(int(time())-jl['ts'])+' seconds.')
        if (time()-jl['ts']) > 3500:
            ccwo_access_token=grab_oauth_ccw_order()
        else:
            ccwo_access_token=jl['access_token']
    except:
        ccwo_access_token=grab_oauth_ccw_order()

    url = "https://api.cisco.com/commerce/ORDER/sync/getSerialNumbers"
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Request-ID': "Type: Integer",
        'Accept-Language': "en_us",
        'Authorization': "Bearer %s"%ccwo_access_token,
        'cache-control': "no-cache",
        'Host': "api.cisco.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }
    ccwo_sn_list=[]
    ccwo_error_so_list=[]
    for so_num in so_list:
        try:
            pageNumber=1
            payload = dumps({'serialNumberRequest':{'salesOrderNumber': so_num, "pageNumber" : str(pageNumber)}})
            response = request("POST", url, data=payload, headers=headers)
            rj=response.json()
            #print(dumps(rj, sort_keys=True, indent=4))
            total_pages=int(rj['serialNumberResponse']['responseHeader']['totalPages'])
            if total_pages>1:
                #print("SO# %s totalPages is great than 1"%str(so_num))
                pageNumber=2
                for i in range(total_pages-1):
                    payload = dumps({'serialNumberRequest':{'salesOrderNumber': so_num, "pageNumber" : str(pageNumber)}})
                    addtl_page=request("POST", url, data=payload, headers=headers)
                    addtl_page=addtl_page.json()
                    pageNumber+=1
                    #print(addtl_page)
                    rj['serialNumberResponse']['serialDetails']['lines']=rj['serialNumberResponse']['serialDetails']['lines']+addtl_page['serialNumberResponse']['serialDetails']['lines']
            sn_parse1=[i for i in rj['serialNumberResponse']['serialDetails']['lines']]
            sn_parse2=[i['serialNumbers'] for i in sn_parse1]
            #print(dumps(sn_parse2, indent=4))
            print(rj['serialNumberResponse']['responseHeader']['totalPages']+' is the total number of pages in the CCWO response for SO#%s'%so_num)
            for i in sn_parse2:
                for j in i:
                    ccwo_sn_list.append(str(j['serialNumber']))
        except Exception as E:
            print(str(so_num)+' SO# could not be retrieved')
            ccwo_error_so_list.append(so_num)
            #print(str(so_num)+' cannot be retrieved from ccw.')
            continue

    print(str(len(ccwo_sn_list))+' is the length of the ccwo sn list.')
    #print(ccwo_sn_list)
    return ccwo_sn_list,ccwo_error_so_list

def ccwr_search_request(searchType='serialNumbers',search_list=[]):
    try:
        with open('ccwr_oauth.json','r') as f:
            jl=load(f)
        print('ccwr oauth2 token age: '+str(int(time())-jl['ts'])+' seconds.')
        if (time()-jl['ts']) > 3500:
            ccwr_access_token=grab_oauth_ccwr()
        else:
            ccwr_access_token=jl['access_token']
    except:
        ccwr_access_token=grab_oauth_ccwr()

    url = "https://api.cisco.com/ccw/renewals/api/v1.0/search/lines"
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Request-ID': "Type: Integer",
        'Accept-Language': "en_us",
        'Authorization': "Bearer %s"%ccwr_access_token,
        'Cache-Control': "no-cache",
        'Host': "api.cisco.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "113",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }


    offset=0
    payload =dumps({searchType:search_list,'limit':1000,'offset':offset,'configurations':True})
    response = request("POST", url, data=payload, headers=headers)
    if response.status_code == 403:
        ccwr_access_token=grab_oauth_ccwr()
        headers['Authorization']='Bearer %s'%ccwr_access_token
        response = request("POST", url, data=payload, headers=headers)
    else:
        pass
    ccwr_response=response.json()
    if int(ccwr_response['totalRecords']) > 1000:
        additional_requests=(int(int(ccwr_response['totalRecords'])/1000))
        for i in range(additional_requests):
            offset+=1000
            payload =dumps({searchType:sn_list,'limit':1000,'offset':offset,'configurations':True})
            addtl_response = request("POST", url, data=payload, headers=headers)
            addtl_response=addtl_response.json()
            ccwr_response['instances']=ccwr_response['instances']+addtl_response['instances']
    return ccwr_response,ccwr_access_token

def ccwr_create_table(ccwr_response,raw_ccwr_output_csv=''):
    with open('contract_response.json','r') as f:
        jsl=load(f)

    ccwr_full_list=[['Product Number', 'Product Description','Serial Number',
    'Parent Serial Number','Instance Number','Sales Order Number',
    'End Customer Name']]

    #print(dumps(ccwr_response, sort_keys=True, indent=4))

    for i in ccwr_response['instances']:
        l=[]
        try:
            l.append(i['product']['number'])
        except:
            l.append('')
            pass
        try:
            l.append(i['product']['description'].lstrip('^').replace(',',';'))
        except:
            l.append('')
            pass
        try:
            l.append(i['serialNumber'])
        except:
            l.append('')
            pass
        try:
            l.append(i['parentSerialNumber'])
        except:
            l.append('')
            pass
        try:
            l.append(i['instanceNumber'])
        except:
            l.append('')
            pass
        try:
            l.append(i['salesOrderNumber'])
        except:
            l.append('')
            pass
        try:
            l.append(i['endCustomer']['name'])
        except Exception as E:
            l.append('')
            pass
        ccwr_full_list.append(l)
    if raw_ccwr_output_csv!='':
        with open(raw_ccwr_output_csv,'w') as f:
            for i in ccwr_full_list:
                for j in i:
                    f.write(j+',')
                f.write('\n')

    return ccwr_full_list
    #print('\n\n\n'+80*'#'+'\n\n\n')
    #print(dumps(jsl['instances'][0], sort_keys=True, indent=4))




def create_3K_lic_rpt(ccwr_full_list, output_file, smart_account):
    '''Create a group on lambda functions to perform RegEx searches'''
    ###Find Header Row based on Serial keyword.
    hr = lambda s: search('.*[Ss][Ee][Rr][Ii][Aa].*',s)
    ###Find any SKU containing 3K nomenclature.
    is_3x50 = lambda s: search('3[68]50',s)
    ###Find any top level traditonal hardware SKU that also contains license level.
    non_C1_3x50 = lambda s: search('WS-C3[68]50.*-[SE]',s)
    ###Find individual 3K on-box license SKUs.
    lic_C1_3x50 = lambda s: search('C3[68]50-[24][48]-[SL]-[ES]',s)
    ###Find any C1 SKU that is less than 24 ports. These have license level as part of the top-level part.
    non_24_48_port_C1 = lambda s: search('C1-WS.*-12.*',s)
    '''Creates a CSV formatted Report of 3K licensing content from a file input
    of a CCW-R file export'''

    #print(dumps(ccwr_full_list[0:5],indent=4))

    ### Find CCW-R header row to place into a list
    header=[i for i in ccwr_full_list[0:3] if hr(str(i))]
    ###Parse CCW-R lines with any 3x50 SKUs into a list of rows
    dev_3x50=[i for i in ccwr_full_list if is_3x50(str(i))]
    ###Parse CCW-R lines for traditional top-level SKU rows
    non_C1_dev=[i for i in dev_3x50 if non_C1_3x50(str(i))]
    #print(dumps(non_C1_dev,indent=4))
    ###Parse CCW-R lines for individual on-box SW upgrade licensing rows
    upg_lics=[i for i in dev_3x50 if lic_C1_3x50(str(i))]
    #print(dumps(upg_lics,indent=4))
    ###Parse C1 SKUs for 3Ks less than 12 ports b/c SW licenses appear in top-level
    non_24_48_port=[i for i in dev_3x50 if non_24_48_port_C1(str(i))]
    #print(dumps(non_24_48_port,indent=4))
    ###Concatenate all parsed lists
    parsed_ccwr_rows_list=header+non_C1_dev+upg_lics+non_24_48_port
    #print(dumps(parsed_ccwr_rows_list,indent=4))
    ###Perform count of elements in concatenated list and place in dict
    devdict=dict(ct([i[0] for i in parsed_ccwr_rows_list][1:]))
    ###Extract top-level SKUs and convert to list of actual licensing SKU that appear in CSSM.
    C3x50=[i[0][3:11]+'-'+i[0][-1] for i in parsed_ccwr_rows_list if i[0].startswith('WS-C3')]
    C3x50=C3x50+[i[0][:12].replace(i[0][:5],'C'+'-'+i[0][-1]) for i in parsed_ccwr_rows_list if i[0].startswith('C1-WS')]
    C3x50_E=[i.replace(i[-2:],'-S-E') for i in C3x50 if i.endswith('E')]
    C3x50_S=[i.replace(i[-2:],'-L-S') for i in C3x50 if i.endswith('S')]
    ###Extract top-level upgrade license SKUs and convert to list
    upg_lics_indiv=[i[0] for i in upg_lics]
    ###Concatenate license lists
    total_upg_lics=C3x50_E+C3x50_S+upg_lics_indiv
    ###Perform count of elements in concatenated list and place in dict
    licdict=dict(ct(total_upg_lics))
    ###Create output file
    with open (output_file,'w') as f:
        f.write('Top-Level Device OR License,-----,Count\n')
        for i in devdict:
            f.write(i+',-----,'+str(devdict[i])+'\n')
        f.write(4*'\n')
        f.write("LICENSES to be deposited in %s\n\n"%smart_account+'License,-----,Count\n')
        for i in licdict:
            f.write(i+',-----,'+str(licdict[i])+'\n')
        f.write(4*'\n')
        f.write("Full License/Device Breakout from CCW-R\n\n")
        for i in parsed_ccwr_rows_list:
            for j in i:
                f.write(j)
                f.write(',')
            f.write('\n')



if __name__=='__main__':
    so_list=['106620939','107280782','107204872','106141383','107194712','102389156','107104430','106647394','107220873','107130438','106792196','12345']
    ccwo_sn_list,ccwo_error_so_list=ccwo_search_request(so_list)
    #print(ccwo_sn_list, ccwo_error_so_list)
    csv_sn_list=file_SN_search('final_list.csv')
    #csv_sn_list=[]
    #print(str(len(csv_sn_list))+' is the number of SNs from the file.')
    webform_sn_list=[]
    raw_ccwr_output_csv='test.csv'
    sn_list=list(set(csv_sn_list+ccwo_sn_list+webform_sn_list))
    ccwr_response,ccwr_access_token=ccwr_search_request('serialNumbers',sn_list)
    print(str(len(ccwr_response['instances']))+' is the length of the unparsed response instances.')
    #print(dumps(ccwr_response['instances'], sort_keys=True, indent=4))
    ccwr_full_list=ccwr_create_table(ccwr_response,raw_ccwr_output_csv)
    create_3K_lic_rpt(ccwr_full_list, '3Klicrpt-1DEC.csv', 'swannynet.com')
    print(dumps(ccwr_full_list[-5:-1],indent=4))
    print(str(len(sn_list))+' is the length of the final ccwr serial number input.')
    print(str(len(ccwr_full_list))+' is the length of the final ccwr report/list output.')

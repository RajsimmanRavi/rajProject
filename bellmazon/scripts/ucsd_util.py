#mini version for creating sa VM instance 
import urllib2
import json
import logging
import time
import sys

from datetime import datetime

logging.basicConfig(filename='example.log',level=logging.DEBUG)

def request2json(url):

    # Set the request authentication headers
    headers = {'X-Cloupia-Request-Key': '71E929B152DC44F7AE9F0184EA1F9CB0'}

    url = url.replace(' ', "%20")

    logging.debug('url:[' + url + ']')
    req = urllib2.Request(url, None, headers)

    resp = urllib2.urlopen(req).read()

    logging.debug('resp:[' + resp + ']')


    return json.loads(resp.decode('utf8'))


def userAPIGetWorkflowInputs(workflow_name):
    url = 'http://198.235.64.34/app/api/rest?formatType=json&opName=userAPIGetWorkflowInputs&opData={param0:' \
          + str(workflow_name) + '}'
    
    return request2json(url)

    

def userAPISubmitWorkflowServiceRequest(inputsDict):
    logging.info("inside 'userAPISubmitWorkflowServiceRequest' fn!")
     
    workflow_name = 'Deply Multiple Standard VM Raj' # always will be hardcoded to this workflow name
    
    paramlist = '{"list":['
    lenDict = len(inputsDict)
    counter = 1
    for key, value in inputsDict.iteritems():
        if counter != lenDict:
            paramlist += '{"name":"'+str(key)+'","value":"'+str(value)+'"},'
        else:
            paramlist += '{"name":"'+str(key)+'","value":"'+str(value)+'"}'
        counter += 1
    paramlist += ']}'
    
    logging.debug(paramlist)
    
    """
    k_Catalog_Item = 'Catalog Item'
    k_vDC = 'vDC'
    k_hdd1_size_GB = 'HDD1 size GB'
    k_vm_name = 'VM Name'
    k_memory = 'Memory'
    k_cpu = 'CPU'

    v_Catalog_Item = '40'
    v_vDC = 'SDN_vDC'
    v_hdd1_size_GB = '150'
    v_vm_name = 'RajVM01'
    v_memory = '2560'
    v_cpu = '2'

     
    url_req = 'https://198.235.64.34/app/api/rest?formatType=json&opName=userAPISubmitWorkflowServiceRequest&opData={param0:"' + workflow_name +\
         '","param1":{"list":[{' + \
         '"name":"' + k_Catalog_Item + '","value":"' + v_Catalog_Item  + '"},{' + \
         '"name":"' + k_vDC + '","value":"' + v_vDC + '"},{' + \
         '"name":"' + k_hdd1_size_GB + '","value":"' + v_hdd1_size_GB + '"},{' + \
         '"name":"' + k_vm_name + '","value":"' + v_vm_name + '"},{' + \
         '"name":"' + k_memory + '","value":"' + v_memory + '"},{' + \
         '"name":"' + k_cpu + '","value":"' + v_cpu + '"}]},"param2":1141}'
    """

    url_req = 'https://198.235.64.34/app/api/rest?formatType=json&opName=userAPISubmitWorkflowServiceRequest&opData={param0:"' + workflow_name +\
         '","param1":' + paramlist + ',"param2":1141}' 

    return request2json(url_req)


def userAPIGetServiceRequestDetails(requestId):

    url = 'http://198.235.64.34/app/api/rest?formatType=json&opName=userAPIGetServiceRequestDetails&opData={param0:' \
          + str(requestId) + '}'

    return request2json(url)

def userAPIGetVMsForServiceRequest(requestId):
    url = 'http://198.235.64.34/app/api/rest?formatType=json&opName=userAPIGetServiceRequestDetails&opData={param0:' \
          + str(requestId) + '}'

    return request2json(url)



def wait_for_after_in_progress(requestId):
    logging.info("inside 'wait_for_after_in_progrss' fn!")
    status = 'Undefined'
    response = 1
    while response != 0:
        data = userAPIGetServiceRequestDetails(requestId)
        logging.info('data2: ' + str(data))
        serviceResult = data['serviceResult']
        status = serviceResult['status']
        logging.info('status: ' + str(status))
        statusStr = 'RequestId:[' + str(requestId) + ']; ' + str(status)
        logging.info('statusStr is: '+str(statusStr))
        response = 1
        if status == "Submitted":
            response = 1
        elif status == "In Progress":
            response = 1
        else:
            response = 0
        time.sleep(5)
        
    return status

def get_status(requestId):
    data = userAPIGetServiceRequestDetails(requestId)
    serviceResult = data['serviceResult']
    status = serviceResult['status']
    logging.info('status: ' + str(status))
    statusStr = 'RequestId:[' + str(requestId) + ']; ' + str(status)
    logging.info('statusStr is: '+str(statusStr))
    return status


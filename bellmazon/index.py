#!/usr/bin/python
'''
A basic bottle app skeleton
'''
import bottle, os
from bottle import route, run, debug, template, request, static_file, error
from subprocess import Popen
from ConfigParser import SafeConfigParser
from app_packages import configfileutils, mongoutils, ucsd_util_mini
import logging
import urllib2

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

app = application = bottle.Bottle()

''' global paths for CSS files '''
static_bs_min = "/static/css/bootstrap.min.css"
static_ss = "/static/css/simple-sidebar.css"
static_custom = "/static/css/custom_upd.css"
static_jquery='/static/js/jquery.js'

'''
Variables containing vcpe info for
progress polling
'''
rootPath = os.path.abspath(os.path.dirname(__file__))

"""
** Not sure what this is about **
@app.route('/static/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    return static_file(filename, root='static')
"""

@app.route('/')
@app.route('/login')
def show_index():
    '''
        The login page (currently, everybody can login (i.e. authenticattion yet to be implemented)
        
    '''

    skeleton = template('templates/index.html', 
               static_custom=static_custom)                    
    logging.warning('entered show_index')
    return skeleton

@app.route('/home', method="GET")
def show_home():
    skeleton = template('templates/home.html',
               static_custom=static_custom)

    return skeleton

@app.route('/createVM', method='POST')
def createVM():
    logging.debug('inside Create_VM() fn!')
    data = request.body.read()
    logging.debug(data)
    CatalogItem = request.forms.get('vmImage')
    vDC = request.forms.get('vDC')
    hdd1_size_gb = request.forms.get('hdd1_size_gb')
    vmName = request.forms.get('vmName')
    memory =  request.forms.get('memory')
    cpu = request.forms.get('cpu')

    inputsDict = {'Catalog Item': CatalogItem, 'vDC': vDC, 'HDD1 size GB': hdd1_size_gb, 'VM Name': vmName, 'Memory': memory, 'CPU': cpu} 
    logging.debug(inputsDict)
    
    serviceReqDetails =  ucsd_util_mini.userAPISubmitWorkflowServiceRequest(inputsDict)
    logging.debug(serviceReqDetails)
    
    
    serviceReqId = serviceReqDetails['serviceResult']
    logging.debug("serviceRequestId is: "+str(serviceReqId))

    wait_for_progress = ucsd_util_mini.wait_for_after_in_progress(serviceReqId)

    logging.debug("wait_for_progress returns: "+str(wait_for_progress))
    
    return wait_for_progress

if __name__ == '__main__':
    bottle.run(host='0.0.0.0')


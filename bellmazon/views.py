from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User #for creating users
from django.template import RequestContext
from scripts import ucsd_util
from models import Username, InstanceInfo

import random
import string

# Create your views here.
def signIn(request):
    request.session.set_test_cookie()
    return render(request, 'bellmazon/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'bellmazon/login.html')

def auth(request):
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()

    username =  request.POST.get("username","")
    password =  request.POST.get("password","")
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            fullName = user.get_full_name()
        
            try:
                pk_id = Username.objects.get(username=username).id
                vmInfo = InstanceInfo.objects.filter(uid=pk_id)

                for info in vmInfo:
                    check_status = ucsd_util.get_status(info.serviceReqId)
                    info.status = check_status
                    print info.status
                    info.save()
            except:
                 vmInfo = ""
            
            logout_url = "http://127.0.0.1:8888/bellmazon/logout"
            return  render_to_response('bellmazon/home.html',{'fullName':fullName, 'logout_url':logout_url, 'vmInfo': vmInfo}, context_instance=RequestContext(request))
        else:
            state = "Your account is not active, please contact the site admin."
            return  HttpResponse(state)
    else:
        state = "The username and/or password is incorrect."
        return HttpResponse(state)

def createAccount(request):
    fName =  request.POST.get("fName","")
    lName =  request.POST.get("lName","")
    emailAddr =  request.POST.get("emailAddr","")
    
    """ Create a random password """
    char_set = string.ascii_uppercase + string.digits
    password = ''.join(random.sample(char_set*6, 6))

    username = fName.lower()+"."+lName.lower()

    """ Since, sending email is in a stall, I will create a temp password 'bell'. Remove this later"""
    password = 'bell'
    
    try: 
        
        """ Save it on main Admin Django module """
        user = User.objects.create_user(username=username, email=emailAddr, password=password)
        user.first_name = fName
        user.last_name = lName
        user.save()
        
        """ Save it in our database model"""
        username = Username(username=str(user)) # store the curent logged-in user to database
        username.save()

        """ TODO: Send Email """

        #print "sendingEmail"
        #print sendEmail.createdAccount(emailAddr,username,password)

    except:
        return HttpResponse("Couldn't create an account, please Try Again!")

    else:
        return HttpResponse("An email has been sent regarding the user credentials.")
    
def launchInstance(request):
    vmImage =  request.POST.get("vmImage","")
    vDC =  request.POST.get("vDC","")
    vmSize =  request.POST.get("vmSize","")
    vmName =  request.POST.get("vmName","")
    
    if vmSize == "xSmall":
        cpu = "1"
        memory = "1024"
        hdd1_size_gb = "150"
    elif vmSize == "Small":
        cpu = "2"
        memory = "2048"
        hdd1_size_gb = "150"
    elif vmSize == "Medium":
        cpu = "4"
        memory = "8192"
        hdd1_size_gb = "200"
    else:
        cpu = "8"
        memory = "16384"
        hdd1_size_gb = "200"

    inputsDict = {'Catalog Item': vmImage, 'vDC': vDC, 'HDD1 size GB': hdd1_size_gb, 'VM Name': vmName, 'Memory': memory, 'CPU': cpu}
    
    """
    TODO: Assign IP Address to VM
    """
    ipAddr = "not assigned"
    #status = "building"
    
    user = request.user
    
    try:
        username = Username.objects.get(username=str(user))
    except:
        return HttpResponse("Couldn't get user. Please try again!!")
    else:
        serviceReqDetails =  ucsd_util.userAPISubmitWorkflowServiceRequest(inputsDict)
        serviceReqId = serviceReqDetails['serviceResult']
    
        status = ucsd_util.get_status(serviceReqId)
        
        instanceInfo = InstanceInfo(uid=username,name=vmName,image=vmImage,size=vmSize,ipAddr=ipAddr,status=status,serviceReqId=serviceReqId) # stores instance info to database
        instanceInfo.save()

        pk_id = Username.objects.get(username=username).id
        vmInfo = InstanceInfo.objects.filter(uid=pk_id)

        logout_url = "http://127.0.0.1:8888/bellmazon/logout"     
        return render_to_response('bellmazon/home.html',{'vmInfo': vmInfo, 'logout_url':logout_url}, context_instance=RequestContext(request))



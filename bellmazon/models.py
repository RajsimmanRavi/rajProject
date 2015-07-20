from django.db import models

# Create your models here.
"""
Create 2 models - Username and InstanceInfo

The Username model has 1 field:
    -- username

The InstanceInfo model has 5 fields:
    -- name
    -- image
    -- size
    -- IP Address
    -- status
"""

class Username(models.Model):
    username = models.CharField(max_length=200)
   
    def __str__(self):
        return self.username

class InstanceInfo(models.Model):
    uid = models.ForeignKey(Username) # This maps the instance info to the username. Thus we have 1-to-many relationship
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    ipAddr = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    serviceReqId = models.CharField(max_length=200, default='0000')

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.name, self.image, self.size, self.ipAddr, self.status , self.serviceReqId)


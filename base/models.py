from django.db import models
from django.contrib.auth.models import AbstractUser


import time
from datetime import datetime

class User(AbstractUser):
    name = models.CharField(max_length=100, null = True)
    email = models.EmailField(unique=True, null = True)
    bio = models.TextField(null = True, blank = True)
    participant = models.BooleanField(default=True, null = True)
    avatar = models.ImageField(default='avatar.png', upload_to='.')

    USERNAME_FIELD = 'email'   # Auth with EmailField
    REQUIRED_FIELDS=['username']

class Event(models.Model):
    name = models.CharField(max_length  = 255)
    description = models.TextField(max_length =1000, null = True, blank = True)
    participants = models.ManyToManyField(User , blank = True, related_name = "events")
    start_date = models.DateTimeField(null = True, blank = True)
    end_date = models.DateTimeField(null = True, blank = True)

    created = models.DateField(auto_now_add = True) #Create 
    updated  = models.DateField(auto_now = True) #Update

    def __str__ (self):
        return self.name
    
    class Meta:
        ordering = ['-end_date']

    @property
    def event_status(self):
        status = None
        
        present = datetime.now().timestamp()
        deadline = self.start_date.timestamp()
        past_deadline = (present > deadline)

        if past_deadline:
            status = 'Finished'
        else:
            status = 'Ongoing'

        return status

class Submission(models.Model):
    participant = models.ForeignKey(User, on_delete = models.SET_NULL , null = True , related_name="submission")
    event = models.ForeignKey(Event, on_delete = models.SET_NULL, null = True)
    details = models.TextField(max_length =255, null = True, blank = True)
    
    def __str__(self):
        return str(self.participant.name) + '-----' + str(self.event)
# str(self.participant.name)

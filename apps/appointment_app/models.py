from __future__ import unicode_literals

from django.db import models
from ..main_app.models import User
from datetime import datetime, timedelta
import re  # import python regex module
# Create your models here.

DATE_REGEX = re.compile(r'^((?:19|20)\d\d)[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$')
TIME_REGEX = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')


class AppointmentManager(models.Manager):

    def validate(self, data):
        print data['date']
        errors = []
        print "@@@@@@@@@@@@@@@@@@@@@@@ datetime.today"
        # datetime.today()
        # strdatetime =  data['date'] + data['time']
        # print "@@@@@@@@@@@@@@@@@@@@@@@ strdatetime"

        # print strdatetime
        # date = datetime.strptime(strdatetime, "%Y-%m-%d")
        # time = datetime.strptime(strdatetime, "%H:%M")
        # datetime = datetime.strptime(strdatetime, "%Y-%m-%d%H:%M")
        # print "@@@@@@@@@@@@@@@@@@@@@@@ x"
        # print x
        # print type(u'2014-03-06T04:38:51Z') is types.UnicodeType

        if len(data['date']) < 1:
            errors.append(" Date is empty")
        if not DATE_REGEX.match(data['date']):
            errors.append("date is not valid")
        if len(data['time']) < 1:
            errors.append("Time is empty")
        if not TIME_REGEX.match(data['time']):
            errors.append("Time is not valid")
        if len(data['task']) < 1:
            errors.append("Task info is empty")
        if len(data['status']) < 1:
            errors.append("Missing status")

        if len(errors) == 0:
            strdatetime =  data['date'] + " " + data['time']
            print strdatetime
            # d == datetime.combine(d.date(), d.timetz())
            datetime_object = datetime.strptime(strdatetime, '%Y-%m-%d %H:%M')
            print datetime_object
            # d == datetime.combine(d.date(), d.timetz())
            # then = datetime.strptime(u'04:38:51Z', "%H:%M:%SZ")
            # print then
            # d = datetime.combine(data['date'], data['time'])
            # print d
            # d = datetime.strptime(strdatetime, "%Y-%m-%dT%H:%M:%SZ")
            # print "@@@@@@@@@@@@@@@@@@@@@@@"
            # print d
            # print "@@@@@@@@@@@@@@@@@@@@@@@"
            if datetime_object < datetime.utcnow()-timedelta(hours=5):
                errors.append("appointment must be the future.")

        if len(errors):
            return {'status':True, 'errors':errors}
        else:
            return {'status':False, 'datetime':datetime_object}
    def currentTasks(self, user_id):
        today = datetime.utcnow()
        tasks =  self.filter(user_id=user_id, taskdatetime__year=today.year,taskdatetime__month=today.month, taskdatetime__day=today.day).order_by('-taskdatetime')
        return tasks

    def futureTasks(self, user_id):
        today = datetime.utcnow()
        tasks =  self.filter(user_id=user_id).exclude(taskdatetime__year=today.year,taskdatetime__month=today.month, taskdatetime__day=today.day).order_by('-taskdatetime')
        return tasks

    def getTask(self, task_id):
        user_task = self.get(id=task_id)
        return user_task

    def addTask(self,user_id, postData):
        response = self.validate(postData)
        # print response
        if response['status'] :
            return response
        else :
            try  :
                date_time = response['datetime']
                user = User.objects.get(id=user_id)
                task = self.create(task=postData['task'], user=user, taskdatetime=date_time,  status=postData['status'])
                print task
            except:
                response['status'] = True
                response['errors'] = ["Duplicate error."]
            return response

    def updateTask(self,user_id, task_id, postData):
        response = self.validate(postData)
        if response['status'] :
            return response
        else :
            date_time = response['datetime']
            user = User.objects.get(id=user_id)
            try :
                user_task = self.get(id=task_id)
                user_task.task=postData['task']
                user_task.user=user
                user_task.taskdatetime=date_time
                user_task.status=postData['status']
                user_task.save()
            except :
                response['status'] = True
                response['errors'] = ["something wrong, fix it!."]
            return response

    def deleteTask(self, task_id):
        user_task = self.get(id=task_id)
        user_task.delete()
        return

class Appointment(models.Model):
    user = models.ForeignKey(User, related_name='task')
    status = models.CharField(max_length=255)
    task = models.CharField(max_length=500)
    taskdatetime = models.DateTimeField(auto_now=False, auto_now_add=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()

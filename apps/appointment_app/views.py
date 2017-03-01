from django.shortcuts import render ,redirect
from models import Appointment
from django.contrib import messages
from datetime import datetime

# Create your views here.
def index(request):
    print Appointment.objects.futureTasks(request.session['user_id'])
    # print Appointment.objects.futureTasks(request.session['user_id'])[1]
    # print Appointment.objects.futureTasks(request.session['user_id'])[1].user.id
    # print Appointment.objects.futureTasks(request.session['user_id'])[2].user.id
    # print Appointment.objects.futureTasks(request.session['user_id'])[3].user.id
    # print Appointment.objects.futureTasks(request.session['user_id'])[4].user.id
    # print Appointment.objects.futureTasks(request.session['user_id'])[5].user.id
    # print Appointment.objects.futureTasks(request.session['user_id'])[6].user.id
    print request.session['user_id']
    try:
        context = {
            'name': request.session['user'],
            'status': request.session['user_status'],
            'task_date':datetime.now(),
            'current_appointments': Appointment.objects.currentTasks(request.session['user_id']),
            'other_appointments':Appointment.objects.futureTasks(request.session['user_id'])
            }
        return render(request, 'appointment_app/index.html', context)
    except KeyError:
            return redirect('main:mainindex')
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def add(request):
    if request.method == 'POST':
        try:
            context = {
                'name': request.session['user'],
                'status': request.session['user_status'],
                }
            # print context
            response = Appointment.objects.addTask(request.session['user_id'], request.POST)
            print response
            if response['status'] :
                for error in response['errors']:
                    messages.error(request, error)
            return redirect('promise:index')
        except KeyError:
                return redirect('main:mainindex')
############################################################
def showUpdate(request, task_id):

    try:
        context = {
            'name': request.session['user'],
            'status': request.session['user_status'],
            'appointment':Appointment.objects.getTask(task_id)
            }
        # print context
        return render( request, 'appointment_app/update.html', context)
    except KeyError:
            return redirect('main:mainindex')
###############################################################
def showDelete(request, task_id):
    try:
        context = {
            'name': request.session['user'],
            'status': request.session['user_status'],
            'appointment':Appointment.objects.getTask(task_id)
            }
        # print context
        return render( request, 'appointment_app/delete.html', context)
    except KeyError:
            return redirect('main:mainindex')
######################################################################
def update(request, task_id):
   if request.method == 'POST':
        try:
            context = {
                'name': request.session['user'],
                'status': request.session['user_status'],
                }
            print context
            response = Appointment.objects.updateTask(request.session['user_id'], task_id, request.POST)
            print response
            if response['status'] :
                for error in response['errors']:
                    messages.error(request, error)
            return redirect('promise:index')
        except KeyError:
                return redirect('main:mainindex')
#######################################################################
def delete(request, task_id):
    if request.method == 'POST':
        try:
            context = {
                'name': request.session['user'],
                'status': request.session['user_status'],
                }
            response = Appointment.objects.deleteTask(task_id)
            return redirect('promise:index')
        except KeyError:
            return redirect('main:mainindex')

from django.shortcuts import render, redirect,HttpResponse
from models import User

from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'main_app/index.html')

def registration(request):
    if request.method == "POST":
        response_from_model = User.objects.registration(request.POST)
        if  response_from_model['status']:
            request.session['user_id'] = response_from_model['user'].id
            request.session['user'] = response_from_model['user'].name
            return redirect('main:success')
        else:
            for error in response_from_model['errors']:
                messages.error(request, error)
    return redirect('main:mainindex')

def login(request):

    if request.method == 'POST':
        response_from_model = User.objects.login(request.POST)
        if  response_from_model['status']:
            request.session['user_id'] = response_from_model['user'].id
            request.session['user'] = response_from_model['user'].name
            return redirect('main:success')
        else:
            for error in response_from_model['errors']:
                messages.error(request, error)
    return redirect('main:mainindex')

def logout(request):

    if request.method == "POST":
        if 'user_id' in request.session:
           request.session.pop('user_id')
           request.session.pop('user')
    request.session['user_status'] = 'logged out'
    return redirect("main:mainindex" )

def success(request):
    if 'user_id' in request.session:
        request.session['user_status']  = 'logged in'
        return redirect('promise:index')
    else :
        return redirect('main' )

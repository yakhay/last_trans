
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from urllib.parse import urlencode
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import TaskSerializer
import requests 
import secrets
import os
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from .forms import CustomUserForm 
from .models import *
from .forms import CustomUserForm
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse

state = secrets.token_urlsafe(16)
client_id =  os.environ.get('client_id')
redirect_uri = os.environ.get('redirect_uri')
client_secret = os.environ.get('client_secret')

def SignIn(request):
    if request.user.is_authenticated:
        return JsonResponse({'alert': 'ok', 'redirect_url': '/home/'}, status=200)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user :
            token ,_ = Token.objects.get_or_create(user=user)
            request.session['user_id'] = user.id
            request.session['token'] = token.key
            return JsonResponse({'alert': 'ok', 'redirect_url': '/home/'}, status=200)
        else:
            return JsonResponse({'alert': 'Username or Password is incorrect'}, status=401)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def SignUp(request):
    # if request.user.is_authenticated:
    #     return JsonResponse({'alert': 'ok', 'redirect_url': '/home/'}, status=200)
    if request.method == "POST":
        user_form = CustomUserForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return JsonResponse({'status': True}, status=200)
        else:
            return JsonResponse({"status": False,"error": user_form.errors}, status=200)
    return JsonResponse({'status': False}, status=200)


def redirect_to_42(request):
    data = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'public',
        'state': state
    }
    authorize_url = f"https://api.intra.42.fr/oauth/authorize?{urlencode(data)}"
    return redirect(authorize_url)


def exchange_code_for_token(code):
    token_url = "https://api.intra.42.fr/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(token_url,data=data)
    response_data = response.json()
    if 'access_token' in response_data :
        return response_data['access_token']
    else:
        return None
 
def store_data_in_database(request,access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        """ checking if user already exists in database"""
        login = user_data['login']
        user, created = CustomUser.objects.get_or_create(username=login, email=user_data['email'])
        if  created:
            user.first_name = user_data['displayname'].split(' ')[0]
            user.last_name = user_data['displayname'].split(' ')[1]
            user.save()
        token,_,= Token.objects.get_or_create(user=user)
        request.session['user_id'] = user.id
        request.session['token'] = token.key

def callback(request):
    code = request.GET.get('code')
    state_req = request.GET.get('state')
    if state_req != state :
        return HttpResponseBadRequest("invalid state parameter")
    access_token = exchange_code_for_token(code)
    if access_token :
        store_data_in_database(request,access_token)
        return redirect('/home/')    
    else:
        return HttpResponseBadRequest("Failed to authenticate")
    

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)




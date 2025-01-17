from django.contrib.auth import logout as log
from django.http import HttpResponseBadRequest
from .models import CustomUser
from django.shortcuts import  redirect
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from . serializers import TaskSerializer

def login_required(request):
    access_token = request.session.get('user_id')
    try:
        user = CustomUser.objects.get(id=access_token)
    except CustomUser.DoesNotExist:
        return None
    return user

def logout(request):
    log(request)
    return redirect('/')

def already_logged(request):
    user = login_required(request)
    if user:
        return JsonResponse({'logged': True}, status=200)
    return JsonResponse({'logged': False}, status=200)

def exit():
    return redirect('/game/')

def calculate_ranking(user):
    all_users = CustomUser.objects.all()
    all_users = sorted(all_users, key=lambda x: x.score, reverse=True)
    for i in range(len(all_users)):
        if all_users[i].id == user.id:
            return i + 1
    return 0

def leadrboard(request):
    all_users = CustomUser.objects.all()
    all_users = sorted(all_users, key=lambda x: x.score, reverse=True)
    data = []
    for user in all_users:
        user.ranking = calculate_ranking(user)
        user.total_match = user.win + user.lose
        data.append(user)
        if len(data) == 5:
            break
    dataseriaser = TaskSerializer(data, many=True)
    return JsonResponse(dataseriaser.data, safe=False)

def data(request):
    user = login_required(request)
    if not user:
        return HttpResponseBadRequest("Forbidden", status=403)
    user.ranking = calculate_ranking(user)
    user.total_match = user.win + user.lose
    user.save()
    dataseriaser = TaskSerializer(user)
    return JsonResponse(dataseriaser.data)

def token(request):
    user = login_required(request)
    if not user:
        return HttpResponseBadRequest("Forbidden", status=403)
    token = request.session.get('token')
    contex = {'token': token}
    return JsonResponse(contex)


def update_profile(request):
    if request.method == 'POST':
        user = login_required(request)
        user.photo_profile = request.FILES.get('image')
        new_username = request.POST.get('username')
        if CustomUser.objects.filter(username=new_username).exclude(id=user.id).exists():
            return JsonResponse({'status': False, 'message': 'Username already taken'}, status=200)
        user.username = new_username
        user.save()
        return JsonResponse({'status': True}, status=200)
    else:
        return JsonResponse({'status': False, 'message': 'Invalid request method'}, status=405)

def update_username(request):
    if request.method == 'POST':
        user = login_required(request)
        user.username = request.POST.get('username')
        user.save()
    return redirect('/home/')

@csrf_exempt
def csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})
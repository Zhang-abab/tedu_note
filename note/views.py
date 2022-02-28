from tkinter import N
from turtle import title
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

from .models import User
from .models import Note

# Create your views here.

def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)
    return wrap

@check_login
def add_note(request):
    if request.method == 'GET':
        return render(request, 'note/add_note.html')
    elif request.method == 'POST':
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']

        Note.objects.create(title=title, content=content, user_id=uid)
        return  HttpResponse('---提交成功---')

@check_login
def list_note(request,uid):
    if request.method == 'GET':
        try:
            #唯一索引，注意并发写入问题
            user = User.objects.get(id = uid)
        except Exception as e:
            return HttpResponse('用户不存在')

        notes = Note.objects.filter(user_id = 3)            
        dict = {}
        titles = [1,1]
        contents = [1,1]
        i = 0
        dict['uesrname'] = user.username
        for note in notes:
            titles[i] = note.title
            contents[i] = note.content
            i += 1
        dict['titles'] = titles
        dict['contents'] = contents
        print(dict)

        return render(request, 'note/list_note.html', dict)
        
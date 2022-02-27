from calendar import c
from crypt import methods
import re
from sre_constants import CH_UNICODE
from tkinter import E
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render 
from .models import User
import hashlib
# Create your views here.

def reg_view(request):
    #注册 GET 返回页面 POST 提交数据 
    #1.密码一致 2.用户名可用 3.插入数据
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']

        if password_1 != password_2:
            return HttpResponse('两次密码输入不一致')
        old_users = User.objects.filter(username = username)
        if old_users:
            return HttpResponse('用户名已注册')

        m = hashlib.md5()
        m.update(password_1.encode())
        password = m.hexdigest()

        try:
            #唯一索引，注意并发写入问题
            user = User.objects.create(username = username, password = password)
        except Exception as e:
            return HttpResponse('用户名已注册')
        
        request.session['username'] = username
        request.session['uid'] = user.id
        

        return HttpResponse('注册成功')

def login_view(request):
    if request.method == 'GET':
        #检查登陆状态

        #检查session
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index')
        #检查cookies
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')

        if c_username and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect('/index')

        return render(request, 'user/login.html')
    elif request.method == 'POST':
        #处理数据
        username = request.POST['username']
        password = request.POST['password']

        #比对账号
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print('--login user error %s'%(e))
            return HttpResponse('---用户名或密码有误---')
        
        #比对密码
        m = hashlib.md5()
        m.update(password.encode())
        if m.hexdigest() != user.password:
            return HttpResponse('---用户名或密码有误---')

        #记录对话状态
        request.session['username'] = username
        request.session['uid'] = user.id

        return HttpResponseRedirect('/index')

        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600*24*3)
            resp.set_cookie('uid', user.id, 3600*24*3)
        

        return resp
        

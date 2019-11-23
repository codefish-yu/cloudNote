from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *

# Create your views here.
def reg_view(request):
    #如果是get请求，拿页面
    if request.method == 'GET':
        #渲染页面
        return render(request,'user/register.html')
    elif request.method == 'POST':
        #处理注册逻辑
        username = request.POST.get('username')
        if not username:
            return HttpResponse('请输入用户名')

        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if not password_1 or not password_2:
            return HttpResponse('两次输入密码不一致')
        #判断用户名
        old_users = User.objects.filter(username=username)
        #如果有，则证明已注册
        if old_users:
            return HttpResponse('当前用户名已注册')

        try:
            #创建用户,这个对象user直接关联到数据库
            user = User.objects.create(username=username,password=password_1)
        except Exception as e:
            print('reg error')
            return HttpResponse('当前用户名已注册')

        #存cookies，在cookies中存下字段username和主键id的值
        resp = HttpResponse('注册成功')
        resp.set_cookie('username',username)
        resp.set_cookie('uid',user.id)  #存下主键用于索引
        return resp

    return HttpResponse('test is ok')

#登录功能
def login(request):
    #拿页面
    if request.method == 'GET':
        #1.检查session，若有session则直接跳转到首页
        if 'username' in request.session and 'uid' in request.session:

            return HttpResponseRedirect('/user/index')
        #2.无session,检查cookies
        if 'username' in request.COOKIES and 'uid' in request.COOKIES:
            #有cookies，回写session
            request.session['username'] = request.COOKIES['username']
            request.session['uid'] = request.COOKIES['uid']
            return HttpResponseRedirect('/user/index')
        #若session和cookies都无，去登录页面
        return render(request,'user/login.html')

    #处理数据
    elif request.method == 'POST':




        username = request.POST.get('username')
        if not username:
            #传给html必须是字典，现拼一个字典，传给html
            dic = {'msg':'请提交用户名'}
            return render(request,'user/login.html',dic)

        password = request.POST.get('password')
        if not password:
            dic = {'msg':'请提交密码'}
            return render(request,'user/login.html',dic)

        #查找用户
        user = User.objects.filter(username=username)#filter()返回queryset对象[obj]
        if not user:
            #提示自己
            print('-----user login %s 用户名不存在'%(username))
            #给用户返模棱两可的
            dic = {'msg':'用户名或密码错误'}
            return render(request,'user/login.html',dic)
        if user[0].password != password:    #用索引将对象从queryset中取出来
            print('----user login %s 密码不正确'%(username))
            dic = {'msg':'用户名或密码错误'}
            return render(request,'user/login.html',dic)

        #验证到这一步，用户名和密码都正确
        #记录登录状态(session版本）
        request.session['username'] = username
        request.session['uid'] = user[0].id

        # 重定向到首页,写的是首页的url，触发该url链接的试图函数的逻辑
        resp = HttpResponseRedirect('/user/index')

        print(dict(request.POST))
        save_cookies = False
        # 判断用户是否点下次免登陆，若点了，帮他存个３０天的cookies
        if 'save_cookies' in request.POST.keys():
            save_cookies = True

        if save_cookies:
            resp.set_cookie('username',username,60*60*24*30)
            resp.set_cookie('uid',user[0].id,60*60*24*30)

        return resp




#返回首页
def index(request):
    username = request.session.get('username')
    #验证是否登陆过，若登陆过就无需再登录
    if 'username' in request.session and 'uid' in request.session:
        is_login = True
    else:
        is_login = False

    return render(request,'user/index.html',locals())   #locals()收集该试图函数中所有的变量传给html

#退出功能
# 需求：
#1.删除session
#2.删除cookies
#3.跳转到登录页面
def logout(request):
    if 'username' in request.session and 'uid' in request.session:
        #删除session
        del request.session['username']
        del request.session['uid']
    resp = HttpResponseRedirect('user/index.html')

    if 'username' in request.COOKIES and 'uid' in request.COOKIES:
        resp.delete_cookie('username')
        resp.delete_cookie('uid')

    return resp

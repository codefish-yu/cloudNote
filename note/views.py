from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page

from note.models import Note
from user.models import User

#检查当前用户是否登录的装饰器函数
def check_logging(fn):
    def wrap(request,*args,**kwargs):
        #检查当前用户是否登录
        #检查session
        if 'username' not in request.session or 'uid' not in request.session:
            #检查cookies
            if 'username' not in request.COOKIES or 'uid' not in request.COOKIES:
                #肯定没登录
                return HttpResponseRedirect('/user/login')
            else:
                #回写session
                request.session['username'] = request.COOKIES['username']
                request.session['uid'] = request.COOKIES['uid']

        return fn(request,*args,**kwargs)
    return wrap




@check_logging  #装饰器，检查用户是否登录的功能
def add_view(request):
    if request.method == 'GET':
        return render(request,'note/add_note.html')

    #提交自己写的笔记，提交成功后跳转到笔记列表页面
    elif request.method == 'POST':
        #处理数据
        #考虑登录状态
        uid = request.session.get('uid')
        print(uid)
        if not uid:
            return HttpResponse('请先登录')
        #TODO 检查用户是否能发言(user表中isactive=True)

        user = User.objects.filter(id=uid)
        user = user[0]
        title = request.POST.get('title')
        content = request.POST.get('content')
        #TODO 检查title content 是否提交
        note = Note(title=title,content=content,user=user)
        note.save()
        return HttpResponseRedirect('/note/')

@cache_page(30)
#用户笔记列表
@check_logging
def list_view(request):
    uid = request.session.get('uid')
    ##查询方案１
    # all_notes = Note.objects.filter(isActive=True,user_id=uid)
    #＃查询方案２　user 一表　note　多表[外键],反向查询
    user = User.objects.get(id=uid)
    all_notes = user.note_set.filter(isActive=True)    #queryset[obj1,obj2]
    print(111)
    print(all_notes)
    return render(request,'note/list_note.html',locals())

#删除笔记
@check_logging
def del_view(request,id):   #文章的编号,从list_view中传递给前端，再从前端传给后端的另一个试图函数
    #将session中的uid取出来，用于确定这个文章是你自己的才能删
    uid = request.session.get('uid')
    #方案１
    notes = Note.objects.filter(id=id,user_id=uid)
    # #方案２
    # user = User.objects.get(id=uid)
    # note = user.note_set.filter(id=id,user=user)
    note = notes[0]
    note.isActive = False
    note.save()
    #修改isActive之后，相当于重新进入了这个页面，又触发了list_view()试图函数
    return HttpResponseRedirect('/note/')




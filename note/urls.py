from django.conf.urls import url
from . import views

urlpatterns = [
    #http://127.0.0.1:8000/note/add
    url(r'^add$',views.add_view),
    # http://127.0.0.1:8000/note/ -->笔记的主页
    url(r'^$', views.list_view),
    # http://127.0.0.1:8000/note/del/某个笔记的编号(路由也是可以用正则变化的?)
    url(r'^del/(\d+)$',views.del_view)

]
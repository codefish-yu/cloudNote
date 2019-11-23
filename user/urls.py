from django.conf.urls import url
from . import views

urlpatterns = [
    #http://127.0.0.1:8000/user/reg
    url(r'^reg$',views.reg_view),
    # http://127.0.0.1:8000/user/login
    url(r'^login$',views.login),
    # http://127.0.0.1:8000/user/logout
    url(r'^logout$', views.logout),
    # http://127.0.0.1:8000/user/index
    url(r'^index$',views.index)
    ]
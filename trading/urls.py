from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^trade.do/', views.trade),
    url(r'^cancel_order.do/', views.cancel_order),
]
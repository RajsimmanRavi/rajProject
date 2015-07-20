from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^$', views.signIn, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^auth/$', views.auth, name="auth"),
    url(r'^createAccount/$', views.createAccount, name="createAccount"),
    url(r'^launchInstance/$', views.launchInstance, name="launchInstance"),
    
]

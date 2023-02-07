from django.urls import path
from . import views as proxy_views
from django.contrib.auth.views import LoginView

urlpatterns = [
   # path("",proxy_views, name = "home-page"),
    ##(template_name = "proxymodel/loginPage.html"), name = "login-user"),
]

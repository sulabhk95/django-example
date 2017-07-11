from p_app import views
from django.conf.urls import url,include

app_name = 'p_app'

urlpatterns = [
url(r'^usr_login/$',views.usr_login,name='usr_login'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^users/$',views.users,name='users'),
    ]

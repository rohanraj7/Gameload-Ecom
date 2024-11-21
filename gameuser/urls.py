from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name='index'),
    path("login/",views.login_view,name="login_view"),
    path('signup/',views.signup,name="signup"),
    # path('loginwithphone/',views.loginwithphone,name="loginwithphone"),
    path('loginwithemail/',views.loginwithemail,name="loginwithemail"),
    path('phoneotp/',views.phoneotp,name="phoneotp"),
    path('otplogin/',views.otplogin,name="otplogin"),
    path('profile/',views.profile,name="profile"),
    path('changepassword/',views.change_password,name="change_password"),
    path('logout/',views.Logout,name="logout"),
    path('forgot/',views.forgot_password,name="forgot"),
    path('filter/<int:id>',views.filter,name="filter"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('adminlogin/',views.adminlogin,name="adminlogin"),
    path('userlist/',views.userlist,name="userlist"),
    path('block/<int:id>',views.block,name="block"),
    path('orders/',views.orders,name='orders'),
    path('banner/',views.banner,name="banner"),
    path('delete_banner/<int:id>',views.delete_banner,name="delete_banner"),
    path('removecoupon/<int:id>',views.delete_coupon,name="delete_coupon"),
    path('orderstatus/<int:id>',views.orderstatus,name="orderstatus"),
    path('salesreport/',views.salesreport,name="salesreport"),
    path('date_wise/',views.date_wise,name="date_wise"),
    path('adminlogout/',views.adminlogout,name="adminlogout"),
]
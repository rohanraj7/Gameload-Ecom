from django.urls import path
from . import views

urlpatterns = [
    # path("checkouts/",views.checkout,name="checkout"),
    path("address/<str:source>",views.address,name="address"),
    path("delete_address/<int:id>",views.delete_address,name="delete_address"),
    path('cart_to_checkout/',views.cart_to_checkout,name="cart_to_checkout"),
    path('razor_success/',views.razor_success,name="razor_success"),
    path('successpage/',views.success_page,name="success_page"),
    path('myorders/',views.myorders,name="myorders"),
    path('cancelorder/<int:id>',views.cancelorder,name="cancelorder"),
    path('return/<int:id>',views.return_order,name="return_order"),
    path('coupons/',views.coupon_generator,name="coupon_generator"),
    path('removecoupon/<int:id>',views.delete_coupon,name="delete_coupon"),
]




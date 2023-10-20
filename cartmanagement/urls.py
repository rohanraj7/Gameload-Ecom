from django.urls import path
from . import views

urlpatterns = [
    path('cart_view/',views.cart_view,name="cart_view"),
    path('wishlist/addto_cart/<int:id>',views.wishlist_addto_cart,name="wishlist_addto_cart"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('addwishlist/<int:id>/<str:source>',views.addto_wishlist,name="addto_wishlist"),
    path('remove_wishlist/<int:id>',views.remove_wishlist,name="remove_wishlist"),
    path('product_addto_cart/<int:id>/<str:source>',views.product_addtocart,name="product_addtocart"),
    path('cart_remove/<int:id>',views.cart_remove,name="cart_remove"),
    path('dquantity/',views.dquantity,name='dquantity'),
    path('iquantity/',views.iquantity,name="iquantity"),
    # path('cat_to_checkout/',views.cart_to_checkout,name="cat_to_checkout"),
    path('remove_appiled/',views.remove_appiled,name="remove_appiled"),
]
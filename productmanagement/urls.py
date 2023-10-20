from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.products,name="products"),
    path('addproducts/',views.addproducts,name='addproducts'),
    path('categories/',views.categories,name='categories'),
    path("productview_admin/",views.productview_admin,name="productview_admin"),
    path("edit_product/<int:id>",views.edit_product,name="edit_product"),
    path('deletecategories/<int:id>',views.delete_categories,name="delete_categories"),
    path('single_product/<int:id>',views.single_product,name='single_product'),
]
from django.shortcuts import render,redirect
from django.contrib import messages
from gameadmin.models import Categories
from . models import Stock
from cartmanagement.models import Cart,Wishlist
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db.models import Q 



# Create your views here.


def products(request):
    if request.user.is_authenticated:
        all_products = Stock.objects.all()
        categories = Categories.objects.all()
        cart_counts = Cart.objects.filter(userid = request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user = request.user.id).count()
        search = request.GET.get('search')

        if search:
            search_products = all_products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
            categories = Categories.objects.all()
            context={'searchfound':search_products,'categories':categories}
            return render(request , 'products.html',context)

        products = []
        for i in all_products:
            products.append({
                 "id"    : i.id,                              
                "name"  : i.name,
                "price" : i.price,
                "quantity" : i.quantity,
                "stock"  : i.stock,
                "description":i.description,
                "image1"    : i.image1,
                "image2"    : i.image2,
                "image3"    : i.image3,
                "image4"    : i.image4,
                "proOffer"  : i.proOffer,
                "offeredprice" :i.price -  i.price * (i.proOffer/100)
            })

        paginator = Paginator(products,6)
        page_number = request.GET.get('page')
        productdata = paginator.get_page(page_number)
        totalpage = productdata.paginator.num_pages
        
        context = {'all_products':all_products,'categories':categories,'cart_counts':cart_counts,'wishlist_counts':wishlist_counts,'product_data':productdata,'last_page':totalpage,'list':[n+1 for n in range(totalpage)]}
        return render(request, 'products.html',context)
    
# _________________GUEST_USER_______________________
    else:
        all_products = Stock.objects.all()
        categories = Categories.objects.all()
        cart_counts = Cart.objects.filter(userid = request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user = request.user.id).count()
        search = request.GET.get('search')

        if search:
            search_products = all_products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
            categories = Categories.objects.all()
            context={'searchfound':search_products,'categories':categories}
            return render(request , 'products.html',context)

        products = []
        for i in all_products:
            products.append({
                 "id"    : i.id,                              
                "name"  : i.name,
                "price" : i.price,
                "quantity" : i.quantity,
                "stock"  : i.stock,
                "description":i.description,
                "image1"    : i.image1,
                "image2"    : i.image2,
                "image3"    : i.image3,
                "image4"    : i.image4,
                "proOffer"  : i.proOffer,
                "offeredprice" :i.price -  i.price * (i.proOffer/100)
            })

        paginator = Paginator(products,2)
        page_number = request.GET.get('page')
        productdata = paginator.get_page(page_number)
        totalpage = productdata.paginator.num_pages
        context = {'all_products':all_products,'categories':categories,'cart_counts':cart_counts,'wishlist_counts':wishlist_counts,'product_data':productdata,'last_page':totalpage,'list':[n+1 for n in range(totalpage)]}
        return render(request, 'products.html',context)


def single_product(request,id):
    if request.user.is_authenticated:
        single_stock = Stock.objects.get(id=id)
        cat_offer = Categories.objects.values('offer').get(id=single_stock.category.id)
        product_offer = single_stock.proOffer
        category_offer = cat_offer['offer']
        cart_counts = Cart.objects.filter(userid = request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user = request.user.id).count()
        if category_offer >= product_offer:
            offered_price = single_stock.price - (single_stock.price * category_offer)/100
        else:
            offered_price = single_stock.price - (single_stock.price * product_offer)/100

        context={'single_stock':single_stock,'offered_price':offered_price,'cart_counts':cart_counts,'wishlist_counts':wishlist_counts}
        return render(request, 'productdetails.html',context)
    else:
        single_stock = Stock.objects.get(id=id)
        cat_offer = Categories.objects.values('offer').get(id=single_stock.category.id)
        product_offer = single_stock.proOffer
        category_offer = cat_offer['offer']
        cart_counts = Cart.objects.filter(userid = request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user = request.user.id).count()
        if category_offer >= product_offer:
            offered_price = single_stock.price - (single_stock.price * category_offer)/100
        else:
            offered_price = single_stock.price - (single_stock.price * product_offer)/100

        context={'single_stock':single_stock,'offered_price':offered_price,'cart_counts':cart_counts,'wishlist_counts':wishlist_counts}
        return render(request, 'productdetails.html',context)
    

def addproducts(request):
    if request.method == 'POST':
        name = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        quantity = request.POST['quantity']
        categories = request.POST['categories']
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')
        stocks = Stock(name=name,price=price,quantity=quantity,stock=stock,description=description,image1=img1,image2=img2,image3=img3,image4=img4,category_id=categories)
        stocks.save()
        messages.success(request, "Product Added!")
    cat = Categories.objects.all()
    context = {"cat":cat}

    return render(request, 'admin/addproducts.html',context)


def categories(request):
    if request.method== 'POST':
        name = request.POST['categories']
        offer = request.POST['offer']
        img1 = request.FILES.get('img1')
        categories = Categories(name=name,offer=offer,image=img1)
        categories.save()
    cat = Categories.objects.all()
    context = {"cat":cat}
    return render(request, 'admin/categories.html',context)


def productview_admin(request):
    all_products = Stock.objects.all()
    context = {'all_products':all_products}
    return render(request, 'admin/productview_admin.html',context)

def edit_product(request,id):
    categories = Categories.objects.all()
    product = Stock.objects.get(id=id)
    context = {'categories':categories,'product':product}

    if request.method == 'POST':
        renaming = Stock.objects.get(id=id)
        name = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        quantity = request.POST['quantity']
        category = request.POST['categories']
        renaming.name = name
        renaming.description = description
        renaming.price = price
        renaming.stock = stock
        renaming.quantity = quantity
        renaming.category_id = category
        renaming.save()
        messages.info(request, "Product Edited")
        return redirect(productview_admin)
    return render(request, 'admin/editproduct.html',context)

def delete_categories(request,id):
    cat = Categories.objects.get(id=id)
    cat.delete()
    return redirect(categories)
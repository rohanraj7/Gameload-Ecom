from django.shortcuts import render,redirect
from .models import Wishlist,Cart
from django.contrib import messages
from gameuser.views import home
from productmanagement.models import Stock,Categories
from productmanagement.views import products,single_product
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from cartmanagement.models import Guestcart
from ordermanagement.views import cart_to_checkout

# Create your views here.


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(userid=request.user.id).order_by('id')
        category = Categories.objects.values('offer')
        subtotal = sum(item.price *item.quantity for item in cart_items)
        total = 0
        for ob in cart_items:
            total = total + ob.amount
        discount = 0
        total_price = total - discount
        counts = Cart.objects.filter(userid=request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user=request.user.id).count()
        carts = Cart.objects.all()
        context={'total':total,'cart_counts':counts,'carts':carts,'wishlist_counts':wishlist_counts,"subtotal":subtotal,"total_price":total_price}
        return render(request, 'cart.html',context)
    else:
        if not request.session.session_key:
            request.session.create()
        request.session['guest_key'] = request.session.session_key
        cart_items = Guestcart.objects.filter(userreference=request.session.session_key).order_by('id')
        category = Categories.objects.values('offer')
        subtotal = sum(item.price *item.quantity for item in cart_items)
        total = 0
        for ob in cart_items:
            total = total + ob.amount
        discount = 0
        total_price = total - discount
        counts = Guestcart.objects.filter(userreference=request.session.session_key).count()
        wishlist_counts = Wishlist.objects.filter(user=request.user.id).count()
        carts = Guestcart.objects.all()
        context={'total':total,'cart_counts':counts,'carts':carts,'wishlist_counts':wishlist_counts,"subtotal":subtotal,"total_price":total_price}
        return render(request, 'cart.html',context)


def product_addtocart(request,id,source):
    if request.user.is_authenticated:
        stock_item = Stock.objects.get(id=id)
        if source == 'index':
            if Cart.objects.filter(productid = stock_item, userid = request.user).exists():
                messages.info(request,"The products is already Exists")
                return redirect(home)
            else:
                if stock_item.stock != 0:
                    cart_item = Cart(
                        userid = request.user,
                        productid = stock_item,
                        productname = stock_item.name, 
                        price = stock_item.price,
                        image = stock_item.image1,
                        quantity = 1,
                        amount = stock_item.price - (stock_item.price * stock_item.proOffer)/100
                    )
                    cart_item.save()
                    messages.success(request, "Added to Cart")
                    return redirect(home)
                else:
                    messages.error(request,"Product Out of Stock")
                    return redirect(home)
        if source == 'products':
            if Cart.objects.filter(productid = stock_item, userid = request.user).exists():
                messages.info(request,"The products is already Exists")
                return redirect(products)
            else:
                if stock_item.stock != 0:
                    cart_item = Cart(
                        userid = request.user,
                        productid = stock_item,
                        productname = stock_item.name, 
                        price = stock_item.price,
                        image = stock_item.image1,
                        quantity = 1,
                        amount = stock_item.price - (stock_item.price * stock_item.proOffer)/100
                    )
                    cart_item.save()
                    messages.success(request, "Added to Cart")
                    return redirect(products)
                else:
                    messages.error(request,"Product Out of Stock")
                    return redirect(products)
        if source == 'single_products':
            if Cart.objects.filter(productid = stock_item, userid = request.user).exists():
                messages.info(request,"The products is already Exists")
                return redirect('single_product', id=id)
            else:
                if request.method == "POST":
                    offered_price = request.POST['offered_price']
                    quantity = request.POST['quantity']
                    if int(quantity) <= stock_item.stock: 
                        cart_item = Cart(
                        userid = request.user,
                        productid = stock_item,
                        productname = stock_item.name, 
                        price = stock_item.price,
                        image = stock_item.image1,
                        quantity = quantity,
                        amount = offered_price
                        )
                        cart_item.save()
                        messages.success(request, "Added to Cart")
                        return redirect(cart_view)
                    else:
                        messages.info(request, f"Only {stock_item.stock} product is Left")
                        return redirect('single_product', id=id)
# ________________GUEST_USER________________________
    else:
        stock_item = Stock.objects.get(id=id)
        if not request.session.session_key:
            request.session.create()
        request.session['guest_key']=request.session.session_key
        key = request.session['guest_key']
        if source == 'index':
            if Guestcart.objects.filter(productid = stock_item, userreference = key).exists():
                messages.info(request,"The products is already Exists")
                return redirect(home)
            else:
                if stock_item.stock != 0:
                    cart_item = Guestcart(
                        userreference = key,
                        productid = stock_item,
                        productname = stock_item.name, 
                        price = stock_item.price,
                        image = stock_item.image1,
                        quantity = 1,
                        amount = stock_item.price - (stock_item.price * stock_item.proOffer)/100
                    )
                    cart_item.save()
                    messages.success(request, "Added to Cart")
                    return redirect(home)
                else:
                    messages.error(request, "Product is Out of stock!")
                    return redirect(home)
        if source == 'products':
            if Guestcart.objects.filter(productid = stock_item, userreference = key).exists():
                messages.info(request,"The products is already Exists")
                return redirect(products)
            else:
                if stock_item.stock != 0:
                    cart_item = Guestcart(
                        userreference = key,
                        productid = stock_item,
                        productname = stock_item.name, 
                        price = stock_item.price,
                        image = stock_item.image1,
                        quantity = 1,
                        amount = stock_item.price - (stock_item.price * stock_item.proOffer)/100
                    )
                    cart_item.save()
                    messages.success(request, "Added to Cart")
                    return redirect(products)
                else:
                    messages.error(request, "Product is Out of stock!")
                    return redirect(products)
        if source == 'single_products':
            if Guestcart.objects.filter(productid = stock_item, userreference = key).exists():
                messages.info(request,"The products is already Exists")
                return redirect(products)
            else:
                if request.method == "POST":
                    offered_price = request.POST['offered_price']
                    quantity = request.POST['quantity']
                    if int(quantity) <= stock_item.stock:
                        cart_item = Guestcart(
                        userreference = key,
                        productid = stock_item,
                        productname = stock_item.name, 
                        price = stock_item.price,
                        image = stock_item.image1,
                        quantity = quantity,
                        amount = offered_price
                        )
                        cart_item.save()
                        messages.success(request, "Added to Cart")
                        return redirect(cart_view)
                    else:
                        messages.info(request, f"Only {stock_item.stock} product is Left")
                        return redirect('single_product', id=id)   
    return render(request, 'login_signup/login.html')


def wishlist_addto_cart(request,id):
    if request.user.is_authenticated:
        stock_item = Wishlist.objects.get(id=id)
        stock = Stock.objects.get(id=stock_item.productid.id)
        wish = Cart(userid=request.user,productid=stock,productname=stock.name,price=stock.price,image=stock.image1,quantity=stock.quantity,amount=stock.price)
        wish.save()
        stock_item.delete()
        messages.success(request, "Product added to Cart")
        return redirect(wishlist)
    return render(request, 'login_signup/login.html')




def wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.all()
        counts = Cart.objects.filter(userid =request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user =request.user.id).count()
        context={'wishlist':wishlist,'cart_counts':counts,'wishlist_counts':wishlist_counts}
        return render(request, 'wishlist.html',context)
    return render(request, 'login_signup/login.html')

def addto_wishlist(request,id,source):
    if request.user.is_authenticated:
        stock = Stock.objects.get(id=id)
        wishlist = Wishlist.objects.all()
        if source == "index":
            if Wishlist.objects.filter(productid = stock, user=request.user).exists():
                messages.info(request,"Product is ALready Exists in The Wishlist")
                return redirect(home)
            else:
                wish = Wishlist(productname=stock.name,user=request.user,productid=stock,description=stock.description,image=stock.image1,price=stock.price)
                wish.save()
                messages.success(request, "Product added to wishlist")
                return redirect(home)
        if source == "products":
            if Wishlist.objects.filter(productid = stock, user=request.user).exists():
                messages.info(request,"Product is ALready Exists in The Wishlist")
                return redirect(products)
            else:
                wish = Wishlist(productname=stock.name,user=request.user,productid=stock,description=stock.description,image=stock.image1,price=stock.price)
                wish.save()
                messages.success(request, "Product added to wishlist")
                return redirect(products)
    else:
        messages.success(request, 'Please Signin then only Create WishList..!')  
        return render(request, 'login_signup/login.html')

def remove_wishlist(request,id):
    if request.user.is_authenticated:
        wish = Wishlist.objects.get(id=id)
        wish.delete()
        messages.success(request, 'Removed From the Wishlist')
        return redirect(wishlist)
    return render(request, 'login_signup/login.html')

def cart_remove(request,id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(id=id)
        cart.delete()
        messages.success(request, 'Removed from the Cart')
        return redirect(cart_view)
    else:
        cart = Guestcart.objects.get(id=id)
        cart.delete()
        messages.success(request, 'Removed from the Cart')
        return redirect(cart_view)

@csrf_exempt
def dquantity(request):
    if request.user.is_authenticated:
        if request.method == "POST":    
            id = request.POST['id']
            car = Cart.objects.get(id=id)
            ob = Cart.objects.values('quantity').get(id=id)
            quantity = ob['quantity']
            if quantity >= 2:
                # Decrease the quantity by 1
                Cart.objects.filter(id=id).update(quantity=ob['quantity'] - 1)
                
                # Calculate the offered price based on the discount percentage
                cat = Categories.objects.values('offer').get(id=car.productid.category_id)
                offered_price = car.productid.price - (car.productid.price * cat['offer']) / 100
                
                # Update the amount based on the new quantity and offered price
                Cart.objects.filter(id=id).update(amount=offered_price * (ob['quantity'] - 1))
            
            ob = Cart.objects.values('quantity').get(id=id)
            o = Cart.objects.values('quantity', 'price', 'amount').get(id=id)
            
            

            cart_items = Cart.objects.filter(userid=request.user)

            # Subtotal is the actuall prices of the products 
            subtotal = sum(item.price *item.quantity for item in cart_items)

            amount = o['amount']
            q = ob['quantity']
            total = 0
            for j in cart_items:
                total = total + j.amount
            
            # Total prices of the with the offered prices the discount is not now defined
            discount = 0
            total_price = total - discount 

            cart1 = car.productid.stock
        return JsonResponse({'amount': amount, 'q': q, 'total': total, 'cart1': cart1,'subtotal':subtotal,'total_price':total_price})
    else:
        if request.method == "POST":    
            id = request.POST['id']
            car = Guestcart.objects.get(id=id)
            ob = Guestcart.objects.values('quantity').get(id=id)
            quantity = ob['quantity']
            if quantity >= 2:
                # Decrease the quantity by 1
                Guestcart.objects.filter(id=id).update(quantity=ob['quantity'] - 1)
                
                # Calculate the offered price based on the discount percentage
                cat = Categories.objects.values('offer').get(id=car.productid.category_id)
                offered_price = car.productid.price - (car.productid.price * cat['offer']) / 100
                
                # Update the amount based on the new quantity and offered price
                Guestcart.objects.filter(id=id).update(amount=offered_price * (ob['quantity'] - 1))
            
            ob = Guestcart.objects.values('quantity').get(id=id)
            o = Guestcart.objects.values('quantity', 'price', 'amount').get(id=id)
            
            

            cart_items = Guestcart.objects.filter(userreference=request.session.session_key)

            # Subtotal is the actuall prices of the products 
            subtotal = sum(item.price *item.quantity for item in cart_items)

            amount = o['amount']
            q = ob['quantity']
            total = 0
            for j in cart_items:
                total = total + j.amount
            
            # Total prices of the with the offered prices the discount is not now defined
            discount = 0
            total_price = total - discount 

            cart1 = car.productid.stock
        return JsonResponse({'amount': amount, 'q': q, 'total': total, 'cart1': cart1,'subtotal':subtotal,'total_price':total_price})
    

@csrf_exempt
def iquantity(request):
    if request.user.is_authenticated and request.user.is_active:
        if request.method == "POST":
            id = request.POST['id']
            car = Cart.objects.get(id=id)
            
            # Retrieve the Cart object
            ob = Cart.objects.get(id=id)

            # Calculate the offered price based on the discount percentage
            cat = Categories.objects.values('offer').get(id=ob.productid.category_id)
            offered_price = ob.productid.price - (ob.productid.price * cat['offer']) / 100

            # Update the quantity
            # Cart.objects.filter(id=id).update(quantity=ob.quantity + 1)

            # Update the amount based on the offered price and quantity
            # Cart.objects.filter(id=id).update(amount=offered_price * ob.quantity)

            # Update the quantity
            new_quantity = ob.quantity + 1
            Cart.objects.filter(id=id).update(quantity=new_quantity)
            
            # Calculate the new amount based on the updated quantity
            new_amount = offered_price * new_quantity
            Cart.objects.filter(id=id).update(amount=new_amount)
            

            updated_cart_item = Cart.objects.get(id=id)

            cart_items = Cart.objects.filter(userid=request.user)

            # total is the discounted prices of the products 
            total = sum(item.amount for item in cart_items)

            # Subtotal is the actuall prices of the products 
            subtotal = sum(item.price *item.quantity for item in cart_items)

            discount = 0
            total_price = total - discount 

            cart1 = car.productid.stock
        return JsonResponse({'amount': updated_cart_item.amount, 'q': updated_cart_item.quantity, 'total': total, 'cart1': cart1,"subtotal":subtotal,'total_price':total_price})
    else:
        if request.method == "POST":
            id = request.POST['id']
            car = Guestcart.objects.get(id=id)
            
            # Retrieve the Cart object
            ob = Guestcart.objects.get(id=id)

            # Calculate the offered price based on the discount percentage
            cat = Categories.objects.values('offer').get(id=ob.productid.category_id)
            offered_price = ob.productid.price - (ob.productid.price * cat['offer']) / 100

            # Update the quantity
            # Cart.objects.filter(id=id).update(quantity=ob.quantity + 1)

            # Update the amount based on the offered price and quantity
            # Cart.objects.filter(id=id).update(amount=offered_price * ob.quantity)

            # Update the quantity
            new_quantity = ob.quantity + 1
            Guestcart.objects.filter(id=id).update(quantity=new_quantity)
            
            # Calculate the new amount based on the updated quantity
            new_amount = offered_price * new_quantity
            Guestcart.objects.filter(id=id).update(amount=new_amount)
            

            updated_cart_item = Guestcart.objects.get(id=id)

            cart_items = Guestcart.objects.filter(userreference=request.session.session_key)

            # total is the discounted prices of the products 
            total = sum(item.amount for item in cart_items)

            # Subtotal is the actuall prices of the products 
            subtotal = sum(item.price *item.quantity for item in cart_items)

            discount = 0
            total_price = total - discount 

            cart1 = car.productid.stock
        return JsonResponse({'amount': updated_cart_item.amount, 'q': updated_cart_item.quantity, 'total': total, 'cart1': cart1,"subtotal":subtotal,'total_price':total_price})
    
def remove_appiled(request):
    if request.user.is_authenticated:
        request.session['coupon_offer'] = None
        messages.success(request, 'Appiled Coupon Removed')
        return redirect(cart_to_checkout)
    return render(request, 'login_signup/login.html')
    
    



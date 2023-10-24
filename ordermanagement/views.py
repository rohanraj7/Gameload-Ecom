from django.shortcuts import render,redirect
from .models import Address,Payment
from django.contrib import messages
from gameuser.views import profile
from django.views.decorators.cache import never_cache
from cartmanagement.models import Wishlist,Cart,Guestcart
from gameadmin.models import Coupon
from django.utils import timezone
from productmanagement.models import Stock
from ordermanagement.models import Myorders
from datetime import datetime
from gameuser.views import home
from datetime import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator



# Create your views here.

def address(request,source):
    if request.user.is_authenticated:
        if request.method == "POST":
            firstname = request.POST['firstname']
            lastname =  request.POST['lastname']
            state = request.POST['state']
            address = request.POST['address']
            city = request.POST['city']
            postcode = request.POST['postcode']
            phoneno =  request.POST['phoneno']
            email =  request.POST['email']
            data = Address(user_id=request.user.id,firstname=firstname,lastname=lastname,state=state,city=city,postcode=postcode,phoneno=phoneno,email=email,address=address)
            data.save()
            context = {
             "firstname":firstname,
             "lastname":lastname,
             "state":state,
             "address":address,
             "city": city,
             "postcode": postcode,
             "phoneno": phoneno,
             "email": email
            }
            messages.success(request, 'Address Added')
            if source == 'profile':
                return redirect(profile)
            if source == 'checkout':
                return redirect(cart_to_checkout)
        return render(request, 'address.html')
    return render(request, 'login_signup/login.html')

def delete_address(request,id):
    if request.user.is_authenticated:
        address_data = Address.objects.get(id=id)
        address_data.delete()
        messages.success(request, "Address Deleted")
        return redirect(profile)
    return render(request, 'login_signup/login.html')



@never_cache
def cart_to_checkout(request):
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(userid=request.user)
            product = Cart.objects.filter(userid=request.user.id).values()
            subtotal = sum(amount.price*amount.quantity for amount in cart_items)
            total_price = sum(item.amount for item in cart_items)
            total = total_price

            cart_counts = Cart.objects.filter(userid=request.user.id).count()
            wishlist_counts = Wishlist.objects.filter(user=request.user.id).count()
            address_data = Address.objects.filter(user=request.user)
            coupons = Coupon.objects.filter(status="Active")
            discount = 0
            previous_amount = 0
            applied = None  # Initializing applied as None

            # The ORDER ID REPRESENTS THE FORMAT OF YEAR/MONTH/MINUTE/HOURS/MINUTES/SECONDS 


            ord1 = datetime.now().strftime('%Y%m%d%H%M%S') + str(request.user.id)
            # ord2 = str(datetime.now())+str(request.user.id)
            # ord1 = ord2.translate({ord(':'): None,ord('-'): None, ord(' '): None, ord('.'): None})
            request.session['order_id'] = ord1

        except:
            cart_items = None
        if not cart_items:
            return redirect(home)

                    
        # FOR THE RAZORPAY GETTING 
        request.session['total_price'] = str(total_price)

        # # COUPONS_MANAGEMENT 
        # now = timezone.now()
        # if 'coupon_filled' in request.POST:
        #     code = request.POST['coupon']
        #     try:
        #         coupon_details = Coupon.objects.get(
        #             coupon_code=code,
        #             added_date__lt=now,
        #             validtill__gte=now,  # Ensure the coupon is not expired.
        #             minimum_price__lte=total_price  # Ensure the total price meets the minimum requirement.
        #         )
                
        #         request.session['coupon_offer'] = coupon_details.discount
        #         request.session['coupon_code'] =coupon_details.coupon_code
        #         applied = request.session['coupon_code']
        #         if request.session['coupon_offer'] is not None:
        #             previous_amount = total
        #             discount = (total*request.session['coupon_offer'])/100
        #             total = total-(total*request.session['coupon_offer'])/100
        #             total_price = total
        #             n = ' Coupon APPLIED successfully '
        #             messages.success(request,n)
        #     except Coupon.DoesNotExist:
        #         messages.error(request, "Coupon Not Valid, Enter Valid Coupon..!")
        #         return redirect(cart_to_checkout)
            
        if request.method == "POST":
            # COUPONS_MANAGEMENT 
            now = timezone.now()
            if 'coupon_filled' in request.POST:
                code = request.POST['coupon']
                try:
                    coupon_details = Coupon.objects.get(
                        coupon_code=code,
                        added_date__lt=now,
                        validtill__gte=now,  # Ensure the coupon is not expired.
                        minimum_price__lte=total_price  # Ensure the total price meets the minimum requirement.
                    )

                    request.session['coupon_offer'] = coupon_details.discount
                    request.session['coupon_code'] =coupon_details.coupon_code
                    applied = request.session['coupon_code']
                    if request.session['coupon_offer'] is not None:
                        previous_amount = total
                        discount = (total*request.session['coupon_offer'])/100
                        total = total-(total*request.session['coupon_offer'])/100
                        total_price = total
                        n = ' Coupon APPLIED successfully '
                        messages.success(request,n)
                        context = {
                            "product":product,
                            "subtotal": subtotal,
                            "total":total,
                            "total_price":total_price,
                            "cart_counts": cart_counts,
                            "wishlist_counts":wishlist_counts,
                            "address_data": address_data,
                            "coupons":coupons,
                            "discount":discount,
                            "previous_amount":previous_amount,
                            "applied":applied
                        }
                        return render(request, 'checkout.html',context)
                except Coupon.DoesNotExist:
                    messages.error(request, "Coupon Not Valid, Enter Valid Coupon..!")
                    return redirect(cart_to_checkout)
            if 'address' in request.POST and 'method' in request.POST:
                address_details = request.POST['address']
                payment_method = request.POST['method']
                address_data_id= Address.objects.get(id=address_details)
                request.session['address'] = address_details

                if payment_method == "COD":
                    for ob in product:
                        product_data = Stock.objects.get(id=ob['productid_id'])
                        if product_data.stock >= ob['quantity']:
                            new_order = Myorders(userid=request.user,productid=product_data,address=address_data_id,quantity=ob['quantity'],amount=ob['price'],method=payment_method,productname=ob['productname'],image=ob['image'],totalamount=ob['amount'],orderid=ord1)
                            new_order.save()
                            del_cart = Cart.objects.filter(userid=request.user.id)
                            del_cart.delete()
                            Stock.objects.filter(id=ob['productid_id']).update(stock=(product_data.stock - ob['quantity']))
                            return render(request, 'success.html',{'payment_method':payment_method})
                        else:
                            messages.warning(request, 'PRODUCT OUT OF STOCK')
                            return redirect(cart_to_checkout)
                elif payment_method == "razorpay":
                    amount = float(total_price*100)
                    order_currency = 'INR'
                    client = razorpay.Client(
                        # auth=('rzp_test_SwupBK06DEvv6V', 'P6DCiW5gkQke1e4uxcTkE5VE')
                        auth=('rzp_test_VSbB1GJYXzzZKh', 'IAg647QdqxBOszNtyVHvCr4I')
                    )
                    payment = client.order.create({'amount':amount,'currency':order_currency,'payment_capture':'0'})
                    payment_id = payment['id']
                    request.session['payment'] = payment
                    payment_status = payment['status']
                    if payment_status == "created":
                        return render(request, 'payments/razorpay.html',{'payment':payment,"amount":amount, "product":product,"total_price":total_price,"address":address_data_id,"order_id":ord1})
                    return render(cart_to_checkout)
                
                elif payment_method == "paypal_money":
                    total_price_amount = request.session['total_price']
                    orderid = request.session['order_id']
                    for ob in product:
                        product_data = Stock.objects.get(id=ob['productid_id'])
                        if product_data.stock >= ob['quantity']:
                            new_order = Myorders(userid=request.user,productid=product_data,address=address_data_id,quantity=ob['quantity'],amount=ob['price'],method=payment_method,productname=ob['productname'],image=ob['image'],totalamount=ob['amount'],orderid=ord1)
                            new_order.save()
                            del_cart = Cart.objects.filter(userid=request.user.id)
                            del_cart.delete()
                            Stock.objects.filter(id=ob['productid_id']).update(stock=(product_data.stock - ob['quantity']))
                            context = {'total':total_price,'orderid':orderid,'ob':product,'m':total_price_amount,'ord1':ord1}
                            return render(request,'payments/paypal.html', context)
                else:
                    del_cart = Cart.objects.filter(userid=request.user.id)
                    del_cart.delete()
        context = {
            "product":product,
            "subtotal": subtotal,
            "total":total,
            "total_price":total_price,
            "cart_counts": cart_counts,
            "wishlist_counts":wishlist_counts,
            "address_data": address_data,
            "coupons":coupons,
            "discount":discount,
            "previous_amount":previous_amount,
            "applied":applied
        }
        return render(request, 'checkout.html',context)
    else:
        messages.success(request, 'Please Signin then only Place Order..!')   
        return render(request, 'login_signup/login.html')


def coupon_generator(request):
    if request.user.is_superuser:
        if request.method == "POST":
            coupon_name = request.POST['coupon_name']
            coupon_code = request.POST['coupon_code']
            date_form = request.POST['date_form']
            date_form_datetime = timezone.make_aware(datetime.strptime(date_form, "%Y-%m-%d"))  # Convert to aware datetime
            minimum_price = request.POST['minimum_price']
            minimum_price = request.POST['minimum_price']
            discount = request.POST['discount']
            current_date = timezone.now() 

             # Check if the coupon is active or expired
            status = "Active" if date_form_datetime >= current_date else "Expired"  # Compare date_form_datetime with current_date


            coupon_data = Coupon(coupon_name=coupon_name,coupon_code=coupon_code,validtill=date_form_datetime,minimum_price=minimum_price,discount=discount,status=status)
            coupon_data.save()
            messages.success(request, 'The Coupon Added Successfully')
            return redirect(coupon_generator)
        coupons = Coupon.objects.all()
        context = {'coupons':coupons}
        return render(request, 'admin/coupon.html',context)
    return render(request, 'admin/adminlogin.html')
    

def delete_coupon(request,id):
    if request.user.is_superuser:
        coupon_data = Coupon.objects.get(id=id)
        coupon_data.delete()
        messages.success(request, "Coupon Deleted")
        return redirect(coupon_generator)
    return render(request, 'admin/adminlogin.html')
        
        


@csrf_exempt
def razor_success(request):
    response = request.POST
    try:
        product = Cart.objects.filter(userid=request.user.id).values()
    except:
        product = None
    if not product:
        return redirect(home)
    total_price = request.session['total_price']
    new_orderid = request.session['order_id']

    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature'],
    }

    payment_details = Payment(user=request.user, paymentid=params_dict["razorpay_payment_id"], paymentmethod='razor', totalamount=float(total_price),status='paid',
                    orderid=new_orderid)
    payment_details.save()


     # Fetch the necessary data to create the Myorders instance
    product = Cart.objects.filter(userid=request.user.id).values()
    address_id = request.session['address']
    address_data_id = Address.objects.get(id=address_id)
    for ob in product:
        product_data = Stock.objects.get(id=ob['productid_id'])
        if product_data.stock >= ob['quantity']:
            new_order = Myorders(userid=request.user,productid=product_data,address=address_data_id,quantity=ob['quantity'],amount=ob['price'],method='razorpay',productname=ob['productname'],image=ob['image'],totalamount=ob['amount'],orderid=params_dict['razorpay_order_id'])
            new_order.save()
            client = razorpay.Client(auth=("rzp_test_VSbB1GJYXzzZKh", "IAg647QdqxBOszNtyVHvCr4I"))
            del_cart = Cart.objects.filter(userid=request.user.id)
            del_cart.delete()
            Stock.objects.filter(id=ob['productid_id']).update(stock=(product_data.stock - ob['quantity']))
            client.utility.verify_payment_signature(params_dict)
            return render(request, 'success.html')
        else:
            messages.info(request, "product Out of Stock")
            return redirect(cart_to_checkout)


def myorders(request):
    if request.user.is_authenticated:
        order_list = Myorders.objects.filter(userid=request.user.id).order_by('-id')
        cart_counts = Cart.objects.filter(userid = request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user = request.user.id).count()
        order_listed = []
        orderdata = None  # Initialize orderdata here
        totalpage = None  # Initialize totalpage here
        for ob in order_list:
            order_listed.append({
                "id": ob.id,
                "userid"       :ob.userid,
                "productid"    :ob.productid ,
                "address"      :ob.address   ,
                "quantity"     :ob.quantity  ,
                "amount"       :ob.amount    ,
                "method"       :ob.method    ,
                "productname"  :ob.productname ,
                "image"        :ob.image      ,
                "status"       :ob.status     ,
                "totalamount"  :ob.totalamount ,
                "orderid"      :ob.orderid   ,
                "orderdate"    :ob.orderdate ,
                "orderstatus"  :ob.orderstatus , 
            })
            paginator = Paginator(order_listed,6)
            page_number = request.GET.get('page')
            orderdata = paginator.get_page(page_number)
            totalpage = orderdata.paginator.num_pages

        context={"order_list":order_list,"wishlist_counts":wishlist_counts,"cart_counts":cart_counts,'order_data':orderdata,'last_page':totalpage,'list':[n+1 for n in range(totalpage)] if totalpage is not None else []}
        return render(request, 'myorders.html',context)
    return render(request, 'login_signup/login.html')


def coupon_generator(request):
    if request.user.is_superuser:
        if request.method == "POST":
            coupon_name = request.POST['coupon_name']
            coupon_code = request.POST['coupon_code']
            date_form = request.POST['date_form']
            date_form_datetime = timezone.make_aware(datetime.strptime(date_form, "%Y-%m-%d"))  # Convert to aware datetime
            minimum_price = request.POST['minimum_price']
            minimum_price = request.POST['minimum_price']
            discount = request.POST['discount']
            current_date = timezone.now() 

             # Check if the coupon is active or expired
            status = "Active" if date_form_datetime >= current_date else "Expired"  # Compare date_form_datetime with current_date


            coupon_data = Coupon(coupon_name=coupon_name,coupon_code=coupon_code,validtill=date_form_datetime,minimum_price=minimum_price,discount=discount,status=status)
            coupon_data.save()
            messages.success(request, 'The Coupon Added Successfully')
            return redirect(coupon_generator)
        coupons = Coupon.objects.all()
        context = {'coupons':coupons}
        return render(request, 'admin/coupon.html',context)
    return render(request, 'admin/adminlogin.html')


def cancelorder(request,id):
    if request.user.is_authenticated:
        order_list = Myorders.objects.get(id=id)
        if order_list.orderstatus == "Placed":
            if order_list.status == True:
                Myorders.objects.filter(id=id).update(status=False)
                Myorders.objects.filter(id=id).update(orderstatus='Cancelled')
                messages.success(request, f"{order_list.productname} is cancelled...!")
                return redirect(myorders)
        messages.info(request, 'Something Went Wrong...!')
        return redirect(myorders)
    return render(request, 'login_signup/login.html')

def success_page(request):
    if request.user.is_authenticated:
        return render(request, 'success.html')
    return render(request, 'login_signup/login.html')

def return_order(request,id):
    if request.user.is_authenticated:
        order_list = Myorders.objects.get(id=id)
        order_list.orderstatus = "Return Pending"
        order_list.save()
        messages.error(request, "The Product Returned")
        return redirect(myorders)
    return render(request, 'login_signup/login.html')

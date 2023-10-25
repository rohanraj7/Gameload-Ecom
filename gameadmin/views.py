from django.shortcuts import render,redirect
from gameadmin.models import Banner,Categories
from gameadmin.models import Coupon
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate,login
import datetime
from ordermanagement.views import coupon_generator
from django.contrib.auth import logout
from ordermanagement.models import Myorders
from django.core.paginator import Paginator
from ordermanagement.models import Payment
from productmanagement.models import Stock
from gameuser.models import User
from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth
import calendar

# Create your views here.
def dashboard(request):
    if request.user.is_superuser:
        product = Stock.objects.all()
        placed_count = Myorders.objects.filter(orderstatus='Placed').count()
        bb = Myorders.objects.filter(orderstatus='Deliverd')
        order_cancelled = Myorders.objects.filter(orderstatus='Cancelled').count()
        pending_return = Myorders.objects.filter(orderstatus='Return Pending').count()
        revenue = 0
        for i in bb:
            revenue = revenue + int(i.totalamount)                    

        use = Stock.objects.count()
        ob = Myorders.objects.filter(orderstatus='Deliverd').count()
        pending = Myorders.objects.filter(orderstatus='Placed').count() 
        categories = Categories.objects.all().count()        
        product = Stock.objects.all()
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=365))
        yearly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        mmax = timezone.now()
        mmin = (timezone.now() - datetime.timedelta(days=30))
        monthly = Myorders.objects.filter(orderdate__lte=mmax, orderdate__gte=mmin,orderstatus='Deliverd')
        monthy_revenue = 0
        for ob in monthly.values():
            monthy_revenue += ob['totalamount']
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=7))
        weekly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        a = []
        n = 1
        subm = timezone.now()
        n = 4
        for i in range(4):
            k = 0
            for i in monthly:
                if i.orderdate <= subm and i.orderdate >= (subm - datetime.timedelta(days=7)):      #type: ignore
                    k += 1
            
            # Get the name of the month for the current date
            month_name = calendar.month_name[subm.month]

            a.append({'name': month_name, 'value': k})
            n -= 1
            subm = subm - datetime.timedelta(days=7)

        subw = timezone.now()
        n = 7
        b = []
        for i in range(7):
            k = 0
            for i in weekly:
                if i.orderdate <= subw and i.orderdate >= (subw - datetime.timedelta(days=1)):      #type: ignore
                    k += 1
            b.append({'name': 'day' + str(n), 'value': k})
            n -= 1
            subw = subw - datetime.timedelta(days=1)
        monthly_sales = list(reversed(a))
        weekly_sales = list(reversed(b))
        user_count = User.objects.all().count()
        order_price = Payment.objects.all().aggregate(Sum('totalamount'))
        total_income = order_price['totalamount__sum']
        order_count = Myorders.objects.all().count()
        product_count = product.count()
        payment = Payment.objects.all()

        obje = Myorders.objects.filter(orderdate__year=2022)
        
        obje1 = Myorders.objects.values('orderdate','orderid','amount','orderstatus').annotate(month=TruncMonth('orderdate')).values('month','orderdate','orderid','amount','orderstatus').annotate(c=Count('id')).values('month','c','orderdate','orderid','amount','orderstatus')
        
        lol=[]
        for i in obje1:
            lol.append({'order_id':i['orderid'],'delivery_status':i['orderstatus'],'month':i['month'].month,'year':i['month'].year,'total_price':i['amount']})
            
        return render(request, 'admin/chart.html',
                    context={'monthly': monthly, 'yearly': yearly, 'monthly_sales': monthly_sales,
                            'weekly_sales': weekly_sales, 'user_count': user_count, 'total_income': total_income,
                            'order_count': order_count, 'product_count': product_count, 'payment': payment, 'lol':lol,'revenue':revenue,'product':product,'use':use,'ob':ob,'bb':bb,'pending':pending,"monthy_revenue":monthy_revenue,'categories':categories,"order_cancelled":order_cancelled,"pending_return":pending_return,"placed_count":placed_count})
    return render(request, 'admin/adminlogin.html')
    
    
def banner(request):
    if request.user.is_superuser:
        if request.method == "POST":
            img = request.FILES.get('img1')
            banner = Banner(image=img)
            banner.save()   
        ban = Banner.objects.all()
        return render(request, 'admin/banner.html',{'ban':ban})
    return render(request, 'admin/adminlogin.html')
    

def delete_banner(request,id):
    banner = Banner.objects.get(id=id)
    banner.delete()
    return redirect('banner')



def adminlogin(request):
    if request.user.is_superuser:
        return redirect(dashboard)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully")
            return redirect(dashboard)
        else:
            messages.error(request, 'wrong credentials enter valid details!!')
            return redirect(adminlogin)  
    return render(request, 'admin/adminlogin.html')
    

def orders(request):
    if request.user.is_superuser:
        categories_list = Categories.objects.all()
        order_list = Myorders.objects.all().order_by('-id')
        order_listed = []
        orderdata = None  # Initialize orderdata here
        totalpage = None  # Initialize totalpage here
        for ob in order_list:
            order_listed.append({
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
        context={"categories_list":categories_list,'order_list':order_list,'order_data':orderdata,'last_page':totalpage,'list':[n+1 for n in range(totalpage)] if totalpage is not None else []}
        return render(request, 'admin/orders.html',context)
    return render(request, 'admin/adminlogin.html')




    

def delete_coupon(request,id):
    if request.user.is_superuser:
        coupon_data = Coupon.objects.get(id=id)
        coupon_data.delete()
        messages.success(request, "Coupon Deleted")
        return redirect(coupon_generator)
    return render(request, 'admin/adminlogin.html')
    

def orderstatus(request,id):
    if request.user.is_superuser:
        ob = Myorders.objects.values('status','orderstatus').get(id=id)
        if ob['status'] == True:
            if ob['orderstatus'] == "Placed":
                Myorders.objects.filter(id=id).update(orderstatus="Shipped")
                messages.success(request, 'Order Shipped')
                return redirect(orders)
            if ob['orderstatus'] == "Shipped":
                Myorders.objects.filter(id=id).update(orderstatus="Out for Delivery")
                messages.success(request, 'Order is at Nearest Hub')
                return redirect(orders)
            if ob['orderstatus'] == "Out for Delivery":
                Myorders.objects.filter(id=id).update(orderstatus="Deliverd")
                messages.success(request, 'Order is Deliverd To Customer!')
                return redirect(orders) 
            if ob['orderstatus'] == "Return Pending":
                Myorders.objects.filter(id=id).update(orderstatus="Return Intiated")
                messages.success(request, 'Return Accepted')
                return redirect(orders)
        else:
            messages.failed(request, "Something Went Wrong..!")
            return redirect(orders)
    return render(request, 'admin/adminlogin.html')



def userlist(request):
    if request.user.is_superuser:
        all_users = User.objects.all().order_by('id').exclude(admin=True)
        context = {'all_users':all_users}
        return render(request,"admin/userlist.html",context)
    return render(request, 'admin/adminlogin.html')
    

def block(request,id):
    if request.user.is_superuser:
        find_one = User.objects.values('active').get(id=id)
        if find_one['active'] == True:
            User.objects.filter(id=id).update(active=False)
            messages.error(request, "User is Blocked..!")
            return redirect(userlist)
        else:
            User.objects.filter(id=id).update(active=True)
            messages.success(request, "User is UnBlocked..!")
            return redirect(userlist)
    return render(request, 'admin/adminlogin.html')

        


def salesreport(request):
    if request.user.is_superuser:
        product = Stock.objects.all()
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=365))
        yearly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        mmax = timezone.now()
        mmin = (timezone.now() - datetime.timedelta(days=30))
        monthly = Myorders.objects.filter(orderdate__lte=mmax, orderdate__gte=mmin)
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=7))
        weekly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        a = []
        n = 1
        subm = timezone.now()
        n = 4
        for i in range(4):
            k = 0
            for i in monthly:
                if i.orderdate <= subm and i.orderdate >= (subm - datetime.timedelta(days=7)):  # type: ignore
                    k += 1
            a.append({'name': 'week' + str(n), 'value': k})
            n -= 1
            subm = subm - datetime.timedelta(days=7)
        subw = timezone.now()
        n = 7
        b = []
        for i in range(7):
            k = 0
            for i in weekly:
                if i.orderdate <= subw and i.orderdate >= (subw - datetime.timedelta(days=1)):    # type: ignore
                    k += 1
            b.append({'name': 'day' + str(n), 'value': k})
            n -= 1
            subw = subw - datetime.timedelta(days=1)
        monthly_sales = list(reversed(a))
        weekly_sales = list(reversed(b))
        user_count = User.objects.all().count()
        order_price = Payment.objects.all().aggregate(Sum('totalamount'))
        total_income = order_price['totalamount__sum']
        order_count = Myorders.objects.all().count()
        product_count = product.count()
        payment = Payment.objects.all()
        obje = Myorders.objects.filter(orderdate__year=2022)
        obje1 = Myorders.objects.values('orderdate','orderid','amount','orderstatus').annotate(month=TruncMonth('orderdate')).values('month','orderdate','orderid','amount','orderstatus').annotate(c=Count('id')).values('month','c','orderdate','orderid','amount','orderstatus')
        lol=[]
        for i in obje1:
            lol.append({'orderid':i['orderid'],'orderdate':i['orderdate'].date,'orderstatus':i['orderstatus'],'month':i['month'].month,'year':i['month'].year,'totalamount':i['amount']})
        return render(request, 'admin/salesreport.html',
                      context={'monthly': monthly,'yearly': yearly, 'monthly_sales': monthly_sales,
                               'weekly_sales': weekly_sales, 'user_count': user_count, 'total_income': total_income,
                               'order_count': order_count,'product_count': product_count,'payment':payment,'lol':lol})
    return render(request, 'admin/adminlogin.html')



def date_wise(request):
    if request.user.is_superuser:
        if request.method=="POST":
            start = request.POST['start_date']
            end = request.POST['end_date']
            if len(start)<1:
                messages.error(request,"choose correct Date")
                return redirect(salesreport)
            if len(end)<1:
               messages.error(request,"choose correct Date")
               return redirect(salesreport)
            order = Myorders.objects.filter(orderdate__range=[start,end])
            o_count =len(order)
            return render(request, 'admin/salesreport.html',{'lol':order,'o_count':o_count})
    return render(request, 'admin/adminlogin.html')


def adminlogout(request):
    if request.user.is_superuser:
        logout(request)
        messages.success(request, 'Logout Successfully!')
        return redirect(adminlogin) 
    return render(request, 'admin/adminlogin.html')

    
    
    


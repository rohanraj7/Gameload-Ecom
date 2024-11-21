from urllib import response
from django.shortcuts import render,redirect
from productmanagement.models import Stock
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gameuser.models import User
from gameuser.mixins import MessageHandler
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from gameadmin.models import Banner,Categories
from cartmanagement.models import Cart,Wishlist,Guestcart
import random
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from ordermanagement.models import Address
from django.core.exceptions import ObjectDoesNotExist



@never_cache 
def home(request):
    if request.user.is_authenticated:
        all_products = Stock.objects.all()
        categories = Categories.objects.all()
        banner = Banner.objects.all()
        cart_counts = Cart.objects.filter(userid=request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user=request.user.id).count()
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
        paginator = Paginator(products,4)
        page_number = request.GET.get('page')
        productdata = paginator.get_page(page_number)
        totalpage = productdata.paginator.num_pages
        context = {'all_products':all_products,'banner':banner,'categories':categories,'cart_counts':cart_counts,'wishlist_counts':wishlist_counts,'product_data':productdata,'last_page':totalpage,'list':[n+1 for n in range(totalpage)]}
        return render(request, 'index.html',context)
    
# ___________________________GUEST_USER________________________

    else:
        all_products = Stock.objects.all()
        categories = Categories.objects.all()
        banner = Banner.objects.all()
        cart_counts = Guestcart.objects.filter(userreference=request.session.session_key).count()
        wishlist_counts = Wishlist.objects.filter(user=request.user.id).count()

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

        context = {'all_products':all_products,'banner':banner,'categories':categories,'cart_counts':cart_counts,'wishlist_counts':wishlist_counts,'product_data':productdata,'last_page':totalpage,'list':[n+1 for n in range(totalpage)]}
        return render(request, 'index.html',context)
    

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(login_view)

@never_cache 
def login_view(request): 
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user is not None:
            if user.active:
                messages.success(request,"Successfully login")
                login(request, user)
                return redirect(home)
            else:
                messages.error(request, "The user is Blocked..!")
                return redirect(login_view)
        else:
            n = "invalid credentials"
            messages.error(request,n)
            return redirect(login_view)
    return render(request, "login_signup/login.html")

def signup(request):
    if request.method == 'POST':
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        phoneno = request.POST.get('number')
        password1 = request.POST.get('password')
        password2 = request.POST.get('re-password')
        if password1 != password2:
            messages.error(request, ('password not Matching'))
            return redirect(signup)
        if User.objects.filter(phoneno = phoneno).exists():
            messages.info(request, 'Phone no Already Exists')
            return redirect(signup)
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email is Already Taken')
            return redirect(signup)
        
        otp = str(random.randint(100000, 999999))
        print("1st stage")
        request.session['signup_data'] = {
            'name': fullname,
            'email': email,
            'phoneno': phoneno,
            'password': password1,
            'otp': otp,
        }
        print("2nd stage")
        # Send OTP via email
        subject = 'Signup OTP Verification'
        message = f'Your OTP for signup is: {otp}'
        from_email = 'rohanraj9645@gmail.com'
        recipient_list = [email]
        
        print("Completedd")

        try:
            print("Here")
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'OTP sent to your email.')
            return redirect('phoneotp')  # Redirect to OTP verification page
        except Exception as e:
            print("Declined Here!!!")
            messages.error(request, f'Error sending OTP: {e}')
            return redirect(signup)

        # if '+91' not in phoneno:
        #     phoneno = '+91' + phoneno
        # otp = 1234
        # message_handler = MessageHandler(phoneno,otp)
        # response = message_handler.send_otp_to_phone(request)
        # if "Succesfully send OTP" in response:
        #     context = {
        #         "name": fullname,
        #         "email": email,
        #         "phoneno": phoneno,
        #         "password1": password1,
        #         "password2": password2
        #     }
        #     messages.success(request, 'Otp successfully Sented..!')
        #     return render(request, 'otp/otp.html', context)
        # elif "Failed to send OTP" in response:
        #         messages.error(request, 'This PhoneNo is Not verified In Twilio. Use This Username: rohanraj.py@gmail.com and Password: 123 for Login..')
        #         return redirect(signup)
        # else:
        #     print("Noneee..!------------------------------------------------")
    return render(request, 'login_signup/register.html')


def profile(request):
    if request.user.is_authenticated:
        address = Address.objects.all()
        cart_counts = Cart.objects.filter(userid=request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user=request.user.id).count()
        context = {
            "cart_counts":cart_counts,
            "wishlist_counts":wishlist_counts,
            "address":address
        }
        return render(request, 'profile.html',context)
    return render(request, 'login_signup/register.html')

def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            current = request.POST['password']
            newpassword = request.POST['newpassword']
            confirmpassword = request.POST['confirmpassword']
            verify = check_password(current, request.user.password)
            if verify:
                if newpassword == confirmpassword:
                    user_data = User.objects.get(id=request.user.id)
                    user_data.set_password(newpassword)
                    user_data.save()
                    # Log the user back in with updated credentials
                    updated_user = authenticate(request, email=user_data.email, password=newpassword)
                    if updated_user is not None:
                        login(request, updated_user)
                    messages.success(request, 'NEW PASSWORD UPDATED')
                    return redirect(profile)
                else:
                    messages.error(request,"THE PLEASE CONFIRM PASSWORD CORRECTLY")
                    return redirect(change_password)
            else:
                messages.error(request,"THE CURRENT PASSWORD IS NOT MATCHING")
                return redirect(change_password)
        cart_counts = Cart.objects.filter(userid=request.user.id).count()
        wishlist_counts = Wishlist.objects.filter(user=request.user.id).count()
        context = {
            "cart_counts":cart_counts,
            "wishlist_counts":wishlist_counts,
        }
        return render(request, 'changepassword.html',context)
    return render(request, 'login_signup/register.html')



def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            reset_token = str(random.randint(10000,99999))
            user.set_password(reset_token)
            user.save()

            subject = 'Password Reset Request'
            message = f' Use this Token for password For Login...! Your Password reset Token is: {reset_token}'
            from_email = 'rohanraj9645@gmail.com'
            recipient_list = [email]
            send_mail(subject,message,from_email,recipient_list)
            messages.success(request, 'Password reset email sent. Please Check your inbox.')
            return redirect(login_view)
        except User.DoesNotExist:
            messages.error(request, 'Email Not Found Please Enter a Valid email address.!')
    return render(request, 'login_signup/forgot.html')

# This Function is temperally hashed because of the limitation of the twilio for the newly joined Members

# for the registeration otp 
# def phoneotp(request):
#     if request.method == "POST":
#         fullname = request.POST.get('name')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password')
#         phoneno = request.POST.get('phoneno')
#         code = request.POST.get('code')
#         verify = MessageHandler(phoneno,code).validate()
#         if verify:
#             print(phoneno,"WONDERFULL CAMED HERE MAN......!")
#             user=User.objects.filter(phoneno=phoneno)
#             print(user,"ARA NIKKALLUUEKKB MACHUUUU")
#             # user = User.objects.get(phoneno=phoneno)
#             # print(ob.user, "ARARA NIKKALUE TELL MEE........!")
#             # print(user,"------------------->>>>")
#             if not user.exists():
#                 user = User.objects.create_user(fullname=fullname,email=email,phoneno=phoneno,password=password1)
#                 user.save()
#                 login(request, user)
#                 messages.success(request,'User Created Successfully')
#                 return redirect(home)
#             else:
#                 messages.error(request,"The Phone Number Already Exists...!")
#                 return redirect(signup)
#     return render(request, 'otp/otp.html')

def phoneotp(request):
    if request.method == 'POST':
        entered_otp = request.POST['code']
        signup_data = request.session.get('signup_data')
        print(signup_data, "value is Here!!!!!!!")
        print(entered_otp,"enteredotp")
        print(signup_data['otp'],"the otp from the session")
        if not signup_data:
            messages.error(request, 'Session expired. Please sign up again.')
            return redirect('signup')

        if entered_otp == signup_data['otp']:
            user = User.objects.create_user(fullname=signup_data['name'],email=signup_data['email'],phoneno=signup_data['phoneno'],password=signup_data['password'])
            user.save()
            messages.success(request, 'Signup successful! Please log in.')
            del request.session['signup_data']  # Clear session data
            return redirect('login_view')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'otp/otp.html')

def loginwithemail(request):
    if request.method == "POST":
        email = request.POST['email']
        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP

        # Save the OTP in the session
        request.session['email_otp'] = otp
        # request.session['email'] = email

        subject = 'Login OTP Verification'
        message = f"Your OTP for login is: {otp}"
        from_email = 'rohanraj9645@gmail.com'  # Replace with your actual email
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'OTP sent to your email.')
            return render(request, 'otp/phoneotp.html', {'email': email})  # Redirect to OTP form page
        except Exception as e:
            messages.error(request, f"Error sending OTP: {e}")
            return redirect('loginwithemail')

    return render(request, 'otp/phonelogin.html')

# This Function is temperally hashed because of the limitation of the twilio for the newly joined Members

# def loginwithphone(request):
#     if request.method == "POST":
#         number = request.POST['number']
#         if '+91' in number:
#             pass
#         else:
#             number = '+91' + number
#         otp = 1234
#         message_handler = MessageHandler(number,otp).send_otp_to_phone()
#         return render(request, 'otp/phoneotp.html',{'phoneno':number})
#     return render(request, 'otp/phonelogin.html')


def otplogin(request):
    if request.method == "POST":
        email = request.POST['email']
        otp = request.POST['otp']

        # Retrieve the stored OTP from session
        session_otp = request.session.get('email_otp')
        
        # Ensure that both the email and OTP are provided
        if not email or not otp:
            messages.error(request, "Email and OTP are required.")
            return render(request, 'otp/emailotp.html', {'email': email})

        try:
            user = User.objects.get(email=email)

            # Validate the OTP
            if str(session_otp) == str(otp):
                # Clear the OTP and email from session after successful login
                del request.session['email_otp']
                # del request.session['email']
                
                # Log in the user
                login(request, user)
                messages.success(request, f"{user.email} successfully logged in.")
                return redirect('index')  # Redirect to your home page after login
            else:
                messages.error(request, 'Incorrect OTP. Please try again.')
                return render(request, 'otp/phoneotp.html', {'email': email})

        except ObjectDoesNotExist:
            messages.error(request, 'User not found. Please sign up.')
            return redirect('signup')

    return render(request, 'otp/phoneotp.html')

# This Function is temperally hashed because of the limitation of the twilio for the newly joined Members

# def otplogin(request):
#     if request.method == "POST":
#         phone = request.POST['phoneno']
#         if '+91' in phone:
#             pass
#         else:
#             phone = "+91" + phone
#         otp = int(request.POST['otp'])
#         try:
#             user = User.objects.get(phoneno=phone)

#             validate = MessageHandler(phone, otp).validate()

#             if validate == "approved":
#                 if user is not None:
#                     login(request, user)
#                     messages.success(request, f"{user} Logged In")
#                     return redirect('index') 
#             else:
#                 messages.info(request, 'Incorrect OTP. Please try again.')
#                 return render(request, 'otp/phoneotp.html', {'phoneno': phone})

#         except ObjectDoesNotExist:
#             messages.error(request, 'User not found , Please sign up.')
#             return redirect('signup') 
        
#     return render(request, 'otp/phoneotp.html')
# This Method is For Filter the values through the categories 
 
def filter(request,id):
    if request.user.is_authenticated:
        search_product = Stock.objects.filter(category=id)
        categories = Categories.objects.all()
        user_search = []
        for ob in search_product:
            user_search.append(
                {
                    "id": ob.id,
                    "name": ob.name,
                    "price": ob.price,
                    "quantity": ob.quantity,
                    "stock": ob.stock,
                    "description": ob.description,
                    "image1": ob.image1,
                    "proOffer": ob.proOffer,
                    "offeredprice": ob.price - ob.price * (ob.proOffer/100)
                }
            )
        context ={'user_categorie_search':user_search,'categories':categories}
        return render(request, 'products.html',context)
    return render(request, 'login_signup/login.html')


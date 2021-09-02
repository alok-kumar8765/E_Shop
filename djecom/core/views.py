from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from core.models import Product
from .models import Category
from .models import Customer
from .models import Orders
from django.contrib.auth.hashers import make_password, check_password
from django.views import View

def index(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();
    data ={}
    data['products'] = products
    data['categories'] = categories
    #print(products)
    print('You are: ',request.session.get('email'))
    return render(request,'index.html',data)

# Class base Index
class Index(View):
    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print('cart ',request.session['cart'])
        return redirect('homepage')
    
    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        #request.session.get('cart').clear()
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products();
        data ={}
        data['products'] = products
        data['categories'] = categories
        #print(products)
        print('You are: ',request.session.get('email'))
        return render(request,'index.html',data)

def ValidateCustomer(customer):
    error_message = None;
    if(not customer.first_name):
        error_message = "First Name Required !"
    elif len(customer.first_name) < 4:
        error_message = "First Name Must Be 4 Character"
    elif not customer.last_name:
        error_message = 'Last Name Required !'
    elif len(customer.last_name) < 4 :
        error_message = 'Last Nmae must be 4 character long'
    elif not customer.phone:
        error_message = ' Phone Number Required !'
    elif len(customer.phone) < 10 :
        error_message = 'Phone Number must be 10 character long'
    elif not customer.email:
        error_message = 'example@gmail.com'
    elif len(customer.email) < 4 :
        error_message = 'Email must be 5 character long'
    elif len(customer.password) < 4:
        error_message = 'Password must be 6 charater long'
    elif customer.isExists():
        error_message = 'Email Aready Registered !'
    #saving data
    return error_message

def registerUser(request):
    postData = request.POST
    first_name = postData.get('first_name')
    last_name = postData.get('last_name')
    phone = postData.get('phone')
    email = postData.get('email')
    password = postData.get('password')
    #validation
    value = {
        'first_name' : first_name,
        'last_name' : last_name,
        'phone' : phone,
        'email' : email
    }
    error_message = None
    customer = Customer(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)
    error_message = ValidateCustomer(customer)
    if not error_message:    
        customer.password = make_password(customer.password)        
        customer.register()
        return redirect('homepage')
    else:
        data = {
            'error_message' : error_message,
            'values' : value
        }
        #return HttpResponse('Account Created Successfully ')
        return render(request,'signup.html',data)

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    else:
        return registerUser(request)

class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    
    def post(self,request):
        postData = request.POST
        first_name = postData.get('first_name')
        last_name = postData.get('last_name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        #validation
        value = {
            'first_name' : first_name,
            'last_name' : last_name,
            'phone' : phone,
            'email' : email
        }
        error_message = None
        customer = Customer(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)
        error_message = self.ValidateCustomer(customer)
        if not error_message:    
            customer.password = make_password(customer.password)        
            customer.register()
            return redirect('homepage')
        else:
            data = {
            'error_message' : error_message,
            'values' : value
            }
        #return HttpResponse('Account Created Successfully ')
            return render(request,'signup.html',data)

    def ValidateCustomer(self,customer):
        error_message = None;
        if(not customer.first_name):
            error_message = "First Name Required !"
        elif len(customer.first_name) < 4:
            error_message = "First Name Must Be 4 Character"
        elif not customer.last_name:
            error_message = 'Last Name Required !'
        elif len(customer.last_name) < 4 :
            error_message = 'Last Name must be 4 character long'
        elif not customer.phone:
            error_message = ' Phone Number Required !'
        elif len(customer.phone) < 10 :
            error_message = 'Phone Number must be 10 character long'
        elif not customer.email:
            error_message = 'example@gmail.com'
        elif len(customer.email) < 4 :
            error_message = 'Email must be 5 character long'
        elif len(customer.password) < 4:
            error_message = 'Password must be 6 charater long'
        elif customer.isExists():
            error_message = 'Email Aready Registered !'
        #saving data
        return error_message
#Login Class Base
class Login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag =check_password(password,customer.password)
            if flag:
                request.session['customer'] = customer.id
                #request.session['email'] = customer.email
                return redirect('homepage')
            else:
                error_message = 'Email or Password is invalid !'
        else:
            error_message = 'Email Or Password Is Invalid !'
        print(customer)
        print(email,password)
        return render(request,'login.html',{'error_message':error_message})
# Loging Part  function  
#def login(request):    
    #if request.method == 'GET':
        #return render(request,'login.html')
   # else:
    #    email = request.POST.get('email')
     #   password = request.POST.get('password')
      #  customer = Customer.get_customer_by_email(email)
       # error_message = None
       # if customer:
       #     flag =check_password(password,customer.password)
        #    if flag:
         #       return redirect('homepage')
          #  else:
           #     error_message = 'Email or Password is invalid !'
        #else:
         #   error_message = 'Email Or Password Is Invalid !'
        p#rint(customer)
        #print(email,password)
        #return render(request,'login.html',{'error_message':error_message})
        
def logout(request):
    request.session.clear()
    return redirect('login')
class cart(View):
    def get(self,request):
        print(list(request.session.get('cart').keys()))
        ids = list(request.session.get('cart').keys())
        products = Product.get_product_by_id(ids)
        print(products)
        return render(request,'cart.html',{'products':products})

class CheckOut(View):
    def post(self,request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        print(customer,address,phone,cart,products)
        for product in products:
            order = Orders(customer=Customer(id=customer),product=product,price=product.price,address=address,phone=phone,quantity=cart.get(str(product.id)))
            #order.placeOrder();
        request.session['cart'] ={}
        return redirect('cart')
    

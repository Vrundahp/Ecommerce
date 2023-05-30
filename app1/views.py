from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

# Create your views here

def demo_all(request):
    data=user.objects.all()
    return render(request,'table.html',{'abc':data})

def demo_filter(request):
    data=user.objects.filter(email="vrunda@gmail.com")
    return render(request,'table.html',{'abc':data})

def demo_get(request):
    data=user.objects.get(username="vrunda")
    return render(request,'table_get.html',{'abc':data})

def index(request):
    if 'email' in request.session:
        a=request.session['email']
        data=Category.objects.all()
        return render(request,'index.html',{'abc':data,'a':a})
    else:
        data=Category.objects.all()
        return render(request,'index.html',{'abc':data})

def login(request):
    if request.method=="POST":
        try:
            data=user.objects.get(email=request.POST['email'],password=request.POST['Password'])
            if data:
                request.session['email']=data.email
                return redirect('index')
            else:
                return render(request,'login.html',{'message':'Invalid Email Or Password'})
        except:
                return render(request,'login.html',{'message':'Invalid Email Or Password'})

    return render(request,'login.html')


def logout(request):
    if 'email' in request.session:
        del request.session['email']
        return redirect('login')
    else:
        return redirect('login')

def productall(request):
    data=Product.objects.all()
    return render(request,'productall.html',{'abc':data})

def product_categorywise(request,id):
    data=Product.objects.filter(category=id)
    return render(request,'productall.html',{'abc':data})

def product_get(request,id):
    data=Product.objects.get(id=id)
    return render(request,'singleproduct.html',{'abc':data})

def register(request):
    if request.method=='POST':
        name1=request.POST['name']
        email1=request.POST['email']
        phone1=request.POST['phone']
        password1=request.POST['password']
        data=user()
        data.username=name1
        data.email=email1
        data.phone=phone1
        data.password=password1
        a=user.objects.filter(email=email1)
        if len(a)==0:
            data.save()
            return redirect('login')
        else:
            return render(request,'register.html',{'message':"user alredy exist"})

    return render(request,'register.html')

def contactus(request):
        return render(request,'contactus.html')

def profile(request):
    if 'email' in request.session:
        a=request.session['email']
        data=user.objects.get(email=a)
        if request.method=='POST':
            data.username=request.POST['name']
            data.phone=request.POST['phone']
            data.save()
            return render(request,'profile.html',{'data':data,'a':a,'message':"profile updated.."})
        return render(request,'profile.html',{'data':data,'a':a})
    else:
        return redirect('login')
    
def changeps(request):
    if 'email' in request.session:
        a=request.session['email']
        data=user.objects.get(email=a)
        if request.method=='POST':
            if data.password==request.POST['Password']:
                if request.POST['Password1']==request.POST['Password2']:

                    data.password=request.POST['Password1']
                    data.save()
                    return render(request,'changeps.html',{'data':data,'a':a,'message':"password updated.."})
                else:
                    return render(request,'changeps.html',{'data':data,'a':a,'message':"password mitchmitched.."})
            else:
                    return render(request,'changeps.html',{'data':data,'a':a,'message':"old password mitchmachted.."})

        return render(request,'changeps.html',{'data':data,'a':a})
    else:
        return redirect('login')
    

import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

def buynow(request):
    if 'email' in request.session:
        a=register.objects.get(email=request.session['email'])
        if request.method=='POST':
            request.session['productid']=request.POST['id']
            request.session['quantity']='1'
            request.session['userid']=a.pk
            request.session['username']=a.username
            request.session['userEmail']=a.email
            request.session['usercontact']=a.phone
            request.session['address']=a.address
            b=Product.objects.get(id=request.POST['id'])
            request.session['productamount']=b.price
            request.session['paymentmethod']='Razorpay'
            request.session['transcationId']=""
            return redirect('razorpayView')
        else:
            return redirect('login')
        
RAZOR_KEY_ID='rzp_test_jLoZ3B0yiYIMrI'
RAZOR_KEY_SECRET='4fsTggaouFMTBT8C4PsGMMhF'

client=razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))

def razorpayView(request):
    currency='INR'
    amount=int(request.session['orderamount'])*100
    razorpay_order=client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'razorpayDemo.html',context=context)

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            amount = int(request.session['orderAmount'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)

            #Order Save Code
            orderModel = Ordermodel()
            orderModel.productid=request.session['productid']
            orderModel.productqty=request.session['quantity']
            orderModel.userId = request.session['userid']
            orderModel.userName = request.session['username']
            orderModel.userEmail = request.session['userEmail']
            orderModel.userContact = request.session['userContact']
            orderModel.address = request.session['address']
            orderModel.orderAmount = request.session['orderAmount']
            orderModel.paymentMethod = request.session['paymentMethod']
            orderModel.transactionId = payment_id
            productdata=Product.objects.get(id=request.session['productid'])
            productdata.quantity=productdata.quantity-int(request.session['quantity'])
            productdata.save()
            orderModel.save()
            del request.session['productid']
            del request.session['quantity']
            del request.session['userid']
            del request.session['username']
            del request.session['userEmail']
            del request.session['userContact']
            del request.session['address']
            del request.session['orderAmount']
            del request.session['paymentMethod']
            # render success page on successful caputre of payment
            return redirect('orderSuccessView')
        except:
            print("Hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("Hello123")
       # if other than POST request is made.
        return HttpResponseBadRequest()

def successview(request):
    if 'email' in request.session:
        a=request.session['email']
        return render(request,'order_sucess.html',{'a':a})
    else:
        return HttpResponseBadRequest()
    
def orderview(request):
    if 'email' in request.session:
        a=request.session['email']
        data=Ordermodel.objects.filter(userEmail=a)
        prolist=[]
        for i in data:
            pro={}
            productdata=Product.objects.get(id=i.productid)
            pro['name']=productdata.name
            pro['img']=productdata.img
            pro['price']=i.orderAmount
            pro['quantity']=i.productqty
            pro['date']=i.orderDate
            pro['TransactionId']=i.transactionId
            prolist.append(pro)
        return render(request,'ordertable.html',{'a':a,'prolist':prolist})
    else:
        return HttpResponseBadRequest()

from django.urls import path
from app1.views import *

urlpatterns=[
    path('all/',demo_all),
    path('filter/',demo_filter),
    path('get/',demo_get),
    path('',index,name='index'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('product-all/',productall,name='productall'),
    path('product-filter/<int:id>',product_categorywise,name='productcat'),
    path('product-get/<int:id>',product_get,name='productget'),
    path('register/',register,name='register'),
    path('contactus/',contactus,name='contactus'),
    path('profile_change/',profile,name='profilechange'),
    path('changeps/',changeps,name='changeps'),
    path('buy-now/',buynow,name='buy'),
    path('razorpayview/',razorpayView,name='razorpayview'),
    path('paymenthandler/',paymenthandler,name='paymenthandler'),
    path('successview/',successview,name='ordersuccessview'),
    path('orderlist/',orderview,name='orderlist')
]
from django.shortcuts import render , redirect
from django.views.generic import ListView , View , DetailView
from .models import Product , Cart , Order , Adresse , Payment, Coupon, Refund , User_profile, Category
from django.shortcuts import get_object_or_404 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, CouponCodeForm, refundForm , PaymentForm
from django.utils import timezone
import stripe
import string
import random
stripe.api_key = "sk_test_vE5AoHAcAujqNog95BYXXXXXXXXXXXXXXXX"

# Create your views here.

def OrderNumber():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def CartView(request):
    user= request.user
    carts = Cart.objects.filter(user=user,ordered=False)
    orders = Order.objects.filter(user=user, ordered=False)
    if carts.exists():
        if orders : 
            order = orders[0]
            return render(request, 'products/cart.html', {'carts':carts, 'order':order})
        else:
            messages.warning(request, 'you dont have any item in the cart')
            return redirect('core:home')   
            
    else:
        messages.warning(request, " you don't have an active order  ")
        return redirect('core:home')     
    
@login_required
def AddToCartView(request , id):
    item = get_object_or_404(Product , id=id)
    order_item , created = Cart.objects.get_or_create(item=item , user=request.user)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'this item quantity was apdated')
            return redirect('core:cart')
        else:
            order.order_items.add(order_item)
            messages.info(request, 'this item was added to your cart')
            return redirect('core:cart')
    else:
        order = Order.objects.create(user=request.user)
        order.order_items.add(order_item)
        messages.info(request, 'this item was added to your cart')
        return redirect('core:cart')
        
@login_required
def RemoveFromCartView(request , id):
    item = get_object_or_404(Product, id=id)
    cart_qs = Cart.objects.filter(item=item ,user=request.user)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.quantity > 1 :
            cart.quantity -= 1
            cart.save()
            messages.info(request, 'this item was added to your cart')
            return redirect('core:cart')
        else:
            cart.delete()
            messages.info(request, 'this item was removed from your cart')
            return redirect('core:cart')
    order_qs = Order.objects.filter(item=item, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__id=item.id).exists():
            order_item = Cart.objects.filter(item=item , user=request.user)[0]
            order.order_item.remove()
            messages.info(request, 'this item was removed from your cart')
            return redirect('core:cart')
    else :
        messages.info(request, 'you don\'t have active order')
        return redirect('core:cart')


@login_required
def DeleteItem(request , id):
   
    item = get_object_or_404(Product, id=id)
    cart_qs = Cart.objects.filter(item=item ,user=request.user)
    if cart_qs.exists():
        cart = cart_qs[0]
        cart.delete()
        messages.info(request, 'this item was removed from your cart')
        return redirect('core:cart')
    order_qs = Order.objects.filter(item=item, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item__id=item.id).exists():
            order_item = Cart.objects.filter(item=item , user=request.user)[0]
            order.order_item.remove()
            messages.info(request, 'this item was removed from your cart')
            return redirect('core:cart')
    else :
        messages.info(request, 'you don\'t have active order')
        return redirect('core:cart')

def validation(values):
    valid = True
    for value in values:
        if value == '':
           valid = False
    return valid
    
@login_required
def CheckoutView(request):  
    myform = CheckoutForm(request.POST or None)
    try:
        order = Order.objects.get(user=request.user, ordered = False)
        print(request.POST)
        if myform.is_valid():
            use_same_shipping_adresse = myform.cleaned_data.get('use_same_shipping_adresse')
            save_billing_adress = myform.cleaned_data.get('save_adress_as_default')
            save_shipping_adress = myform.cleaned_data.get('save_shipping_adress')
            use_default = myform.cleaned_data.get('use_default')
            use_default_shipping_adress = myform.cleaned_data.get('use_default_shipping_adress')
            payment_method = myform.cleaned_data.get('payment_method')
            adress1 = myform.cleaned_data.get('adress1')
            adress2 = myform.cleaned_data.get('adress2')
            country = myform.cleaned_data.get('country')
            zip_code = myform.cleaned_data.get('zip_code')
            shipping_adress1 = myform.cleaned_data.get('shipping_adress1')
            shipping_adress2 = myform.cleaned_data.get('shipping_adress2')
            shipping_country = myform.cleaned_data.get('shipping_country')
            shipping_zip_code = myform.cleaned_data.get('shipping_zip_code')
            Billing_adresse = Adresse(
                        user = request.user,
                        adress1 = adress1,
                        adress2 = adress2,
                        country = country,
                        zip_code = zip_code,
                        adresse_type = 'B'      
                    )
            shipping_adresse = Adresse(
                        user = request.user,
                        adress1 = shipping_adress1,
                        adress2 = shipping_adress2,
                        country = shipping_country,
                        zip_code = shipping_zip_code,
                        adresse_type = 'S'      
                    )
            if use_default_shipping_adress :
                shipping_adresse_qs = Adresse.objects.filter(
                user = request.user,
                adresse_type = 'S',
                defualt = True
                )
                if shipping_adresse_qs.exists():
                    shipping_adresse = shipping_adresse_qs[0]
                    order.shipping_adress = shipping_adresse
                    order.save()
                else:
                    messages.warning(request, 'you dont have a default Shipping adresse')
                    return redirect('core:checkout')             
            else : 
                if validation([shipping_adress1, shipping_country, shipping_zip_code]):
                    if save_shipping_adress :
                        shipping_adresse.defualt = True
                        shipping_adresse.save()
                    order.shipping_adress = shipping_adresse
                    shipping_adresse.save()
                    order.save()
                else:
                    messages.warning(request , 'sorry but you need to enter you informations')
                    return redirect('core:checkout')

            if use_same_shipping_adresse :
                Billing_adresse = shipping_adresse
                Billing_adresse.pk = None
                Billing_adresse.save()
                Billing_adresse.adresse_type='B'
                Billing_adresse.save()
                order.billing_adress= Billing_adresse
                order.save()
                       
            elif use_default :
                billing_adresse_qs = Adresse.objects.filter(
                user = request.user,
                adresse_type = 'B',
                defualt = True
                    )
                if billing_adresse_qs.exists():
                    billing_adresse = billing_adresse_qs[0]
                    order.billing_adress = billing_adresse
                    order.save()
                else:
                    messages.warning(request, 'you dont have a default billing adresse')
                    return redirect('core:checkout')             
            else : 
                if validation([adress1, country, zip_code]):
                    if save_billing_adress :
                        Billing_adresse.defualt = True
                        Billing_adresse.save()
                    order.billing_adress = Billing_adresse
                    order.save()
                else:
                    messages.warning(request , 'sorry but you need to enter you informations')
                    return redirect('core:checkout')

            if payment_method == 'S':
                return redirect('core:payment')  
            elif payment_method == 'P':
                return redirect('core:payment')  
            else:
                return redirect('core:home')  
                       
    except ObjectDoesNotExist:
        messages.info(request, 'you dont have any active order')
        return redirect ('/')
    context={
        'form':myform,
        'order':order
    }
    billing_adresse_qs = Adresse.objects.filter(
        user = request.user,
        adresse_type = 'B',
        defualt = True
    )
    if billing_adresse_qs.exists():
        context.update({'default_billing_adress':billing_adresse_qs[0]})

    shipping_adresse_qs = Adresse.objects.filter(
        user = request.user,
        adresse_type = 'S',
        defualt = True
    )
    if shipping_adresse_qs.exists():
        context.update({'default_shipping_adress':shipping_adresse_qs[0]})
    return render(request, 'products/checkout-page.html', context)

@login_required
def PaymentView(request): 
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    order = order_qs[0]
    try : 
        order = Order.objects.get(user=request.user, ordered = False)
        if request.method == 'POST':
            #get token that cames from striep
            token = request.POST.get('stripeToken')
            #get order
            order = Order.objects.get(user=request.user, ordered = False)
            amount = int(order.get_total() * 100) 
              
            try:
                #creat charge
                charge = stripe.Charge.create( 
                    amount = amount,
                    currency="usd",
                    source= token, 
                    description="My First Test Charge (created for API docs)",
                )
                #create payment
                payment = Payment()
                payment.strip_charg_id = charge['id']
                payment.user = request.user
                payment.amount = order.get_total()
                payment.save()
                #assign payment to order 
                the_order_items = Cart.objects.filter(user=request.user)
                for item in the_order_items:
                    item.ordered=True
                    item.save()
                order.ordered = True
                order.number = OrderNumber()
                order.payment = payment
                cart_qs = Cart.objects.filter(user=request.user)
                order.save()
                messages.info(request, 'your order was succes')
                return redirect("/")
                



            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                print('Status is: %s' % e.http_status)
                print('Type is: %s' % e.error.type)
                print('Code is: %s' % e.error.code)
                # param is '' in this case
                print('Param is: %s' % e.error.param)
                print('Message is: %s' % e.error.message)
                return redirect("/")
            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(request, 'Rate limit error')
                return redirect("/")
            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                messages.warning(request, 'invalid paramiters')
                return redirect("/")
            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(request, 'not authenticated')
                return redirect("/")
            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(request, 'network error')
                return redirect("/")
            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(request, 'something wents worng you will not charged please try again')
                return redirect("/")
            except Exception as e:
                # send email to ouselves
                messages.warning(request, 'there is some thing to fix in our website you will not charged please try again later')
                return redirect("/")
    except ObjectDoesNotExist:
        messages.warning(request, 'Sorry you don\'t have any active order')
        return redirect('core:home')

    return render(request, 'products/charge.html', {'couponform':CouponCodeForm(),'order':order})
    

def AddCouponCodeView(request):
    if request.method=='POST':
        couponform = CouponCodeForm(request.POST)
        if couponform.is_valid():        
            try: 
                code = couponform.cleaned_data['code']
                order = Order.objects.get(user=request.user, ordered=False)
                now = timezone.now()
                couponcode = Coupon.objects.get(
                    code=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True,
                        )
                order.coupon = couponcode
                order.save()
                messages.info(request, 'code successfully added')
                return redirect('core:payment')
            except ObjectDoesNotExist:
                messages.warning(request, 'This coupon is not exists')
                return redirect('core:payment')

class RefunView(View):
    def get(self, *args, **kwargs):
        form = refundForm()
        context = {
            'form': form,
        }
        return render(self.request,'products/refund.html', context)

    def post(self, *args, **kwargs): 
        form = refundForm(self.request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            order_number = form.cleaned_data['order_number']
            reason = form.cleaned_data['reason']
            try :
                order = Order.objects.get(number=order_number, ordered=True)
                order.refunded_requested = True
                order.save()

                refund = Refund()
                if email == self.request.user.email:
                    refund.reson = reason
                    refund.order = order
                    refund.email = email
                    refund.save()

                    messages.info(self.request , 'refund has been successfully submited')
                    return redirect('core:refund')
                else:
                    messages.warning(self.request , 'the email is not the same as your email')
                    return redirect('core:refund')


            except ObjectDoesNotExist:
                messages.warning(self.request,'you dont have any order match that number')
                return redirect('core:refund')

def DetiailsView(request , pk):
    product = get_object_or_404(Product, id=pk)
    other_products_list = []
    other_products = Product.objects.all()
    for item in other_products:
        if item.id == product.id:
            pass
        else:
            other_products_list.append(item)
    context = {
        'product':product,
        'other_products':other_products_list[0:3]
    }
    return render (request, 'products/product-page.html', context)
    

class ProductView(ListView):
    model = Product
    template_name='products/products_list.html'
    paginate_by = 8
    



def ProductlistOnCategoryView(request, name):
    items = Product.objects.filter(category__name=name)

    context = {
        'items':items,
    }
    return render(request, 'products/productslistoncategory.html', context)

def ProfileView(request, pk):
    profile = get_object_or_404(User_profile , id=pk)
    orders = Order.objects.filter(user=profile.user, ordered=True )
    arrived_orders = Order.objects.filter(user=profile.user, ordered=True, arrived=True)
    purshase_history = Payment.objects.filter(user=profile.user)
    refund_requests = Refund.objects.filter(email=profile.user.email)
    refunded_orders = Refund.objects.filter(email=profile.user.email, accepted=True)
    print(orders)

    context = {
        'profile':profile,
        'purshase_history':purshase_history,
        'refund_requests':refund_requests,
        'orders':orders,
        'arrived_orders':arrived_orders
    }

    return render(request, 'products/profile_page.html', context)


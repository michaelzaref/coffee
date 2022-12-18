from django.shortcuts import redirect, render
from django.utils import timezone
from orders.models import Order
from orders.models import OrderDetails
from products.models import Product
from products.views import product

# Create your views here.
def order(request):
    if 'pro_id' in request.GET and 'qnt' in request.GET and 'price' in request.GET and request.user.is_authenticated and  not request.user.is_anonymous :
        pro_id=request.GET['pro_id']
        qnt=request.GET['qnt']

        order=Order.objects.all().filter(user=request.user,is_finished=False)
        
        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('/products/')

    
        pro=Product.objects.get(id=pro_id)
        if order:
            old_order=Order.objects.get(user=request.user, is_finished=False)
            if OrderDetails.objects.filter(order=old_order ,product=pro).exists():
                order_details=OrderDetails.objects.get(product=pro,order=old_order)
                order_details.quantity += int(qnt)
                order_details.save()
            else:
                order_details=OrderDetails.objects.create(product=pro,order=old_order,price=pro.price,quantity=qnt)
            
            
            print(1)

        else:
            new_order=Order()
            new_order.user=request.user
            new_order.order_date=timezone.now()
            new_order.is_finished=False
            new_order.save()
            order_ditails=OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qnt)
        return redirect('/products/' + request.GET['pro_id'])

        

    else:
        return redirect('/products/')


def cart(request):
    context=None

    if request.user.is_authenticated and not request.user.is_anonymous :
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order= Order.objects.get(user=request.user,is_finished=False)
            orderditails=OrderDetails.objects.all().filter(order=order)
            total=0
            print(5)
            for sub in orderditails:
                
                total +=sub.price * sub.quantity
                print(total)
            context={
                'order': order,
                'orderditails':orderditails,
                'total':total,

            }
        print(1)
    return render(request,'orders/cart.html',context=context)

def remove(request,id):
    if request.user.is_authenticated and not request.user.is_anonymous and id:
        dell = OrderDetails.objects.get(id=id)
        if dell.order.user.id ==request.user.id:
            dell.delete()
        
        print(1)

    return redirect('cart')

from django.shortcuts import render, get_object_or_404, redirect
from .models import FoodItem, Order

# FoodItem Views
def index(request):
    return render(request, 'food/index.html')

def food_list(request):
    food_items = FoodItem.objects.all()
    return render(request, 'food/food_list.html', {'food_items': food_items})

def food_detail(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    return render(request, 'food/food_detail.html', {'food_item': food_item})

def food_create(request):
    if request.method == 'POST':
        food_item = FoodItem(
            name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price']
        )
        food_item.save()
        return redirect('food_list')
    return render(request, 'food/food_form.html')

def food_update(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        food_item.name = request.POST['name']
        food_item.description = request.POST['description']
        food_item.price = request.POST['price']
        food_item.save()
        return redirect('food_list')
    return render(request, 'food/food_form.html', {'food_item': food_item})

def food_delete(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        food_item.delete()
        return redirect('food_list')
    return render(request, 'food/food_confirm_delete.html', {'food_item': food_item})

# Order Views
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'food/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'food/order_detail.html', {'order': order})

def order_create(request):
    if request.method == 'POST':
        food_items = FoodItem.objects.filter(pk__in=request.POST.getlist('food_items'))
        total_price = sum(item.price for item in food_items)
        order = Order(
            customer_name=request.POST['customer_name'],
            customer_email=request.POST['customer_email'],
            total_price=total_price
        )
        order.save()
        order.food_items.set(food_items)
        return redirect('order_list')
    food_items = FoodItem.objects.all()
    return render(request, 'food/order_form.html', {'food_items': food_items})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'food/order_confirm_delete.html', {'order': order})

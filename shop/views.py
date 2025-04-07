from django.shortcuts import render, redirect
from .models import Cart  # Make sure this is the correct model
from shop.form import CustomUserForm
from .models import Category, Product,favourite
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


def home(request):
    products = Product.objects.filter(trending=1)
    return render(request, "shop/index.html", {"products": products})


def favviewpage(request):
    if request.user.is_authenticated:
      fav=favourite.objects.filter(user=request.user)
      return render(request,"shop/fav.html",{"fav":fav})
    else:
      return redirect("/")  


def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewcart") 
# def cart_page(request):
#      if request.user.is_authenticated:  
#         cart=Cart.objects.filter(user=request.user)
#         return render(request,"shop/cart.html",{"carts":cart})
#      else:
#         return redirect("/")  


# def cart_page(request):
#     if request.user.is_authenticated:
#         cart = Cart.objects.filter(user=request.user)  # Ensure you're getting the user's cart items
#         return render(request, "shop/cart.html", {"carts": cart})
#     else:
#         return redirect("/")


def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        for item in cart:
            item.total_price = item.Product.selling_price * item.Product_qty
        total_amount = sum(item.Product.selling_price * item.Product_qty for item in cart)  # Calculate total in view
        return render(request, "shop/cart.html", {"carts": cart, "total_amount": total_amount})
    else:
        return redirect("/")

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart") 
# def fav_page(request):
#     if request.headers.get('x-requested-with')=='XMLHTTpRequest':
#      if request.user.is_authenticated:
#        data=json.load(request)
#        product_qty(data['product_qty'])
#        product_id(data['pid'])
#        product_status=Product.objects.get(id=product_id)
#        if product_status:
#            if Favourite.objects.filter(user=request.user.id,product_id=product_id):
#             return jsonResponse({'status':'Product Already in Cart'},status=200) 
#            else:
#              Favourite.objects.filter(user=request.user.id,product_id=product_id)
#              return jsonResponse({'status':'Product Already in Cart'},status=200) 
#        Favourite.objects.create(user=request.user,product_id=product_id)   
#        return jsonResponse({'status':'Product Added to Favourite'}, status=200)
    
       
       
#      else:
#       return jsonResponse({'status':'Login to Add Favourite'}, status=200)
#     else:
#      return jsonResponse({'status':'Invalid Access'}, status=200)
     




# def add_to_cart(request):
#     if request.headers.get('x-requested-with')=='XMLHTTpRequest':
#      if request.user.is_authenticated:
#        data=json.load(request)
#        product_qty(data['product_qty'])
#        product_id(data['pid'])
#        #print(data['request.user.id'])
#        product_status=Product.objects.get(id=product_id)
#        if product_status:
#          if Cart.objects.filter(user=request.user.id,product_id=product_id):
#             return jsonResponse({'status':'Product Already in Cart'},status=200) 
#          else:
#             if product_status.quantity>=Product_qty:
#               Cart.objects.create(user=request.user,product_id=product_id,Product_qty=Product_qty)   
#               return jsonResponse({'status':'Product Added to Cart'},status=200) 
#             else:
#              return jsonResponse({'status':'Product Stock Not Available'}, status=200)
       
#      else:
#       return jsonResponse({'status':'Login to Add Cart'}, status=200)
#     else:
#      return jsonResponse({'status':'Invalid Access'}, status=200)
     
# from django.http import JsonResponse
# from django.shortcuts import render
# from .models import Cart, Product

# def add_to_cart(request):
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         if request.user.is_authenticated:
#             # Read data from the request
#             data = json.loads(request.body)  # Make sure to use `json.loads` instead of `json.load`
#             product_qty = data.get('product_qty')
#             product_id = data.get('pid')

#             # Check if the required data exists
#             if not product_qty or not product_id:
#                 return JsonResponse({'status': 'Error', 'message': 'Missing product quantity or product ID'}, status=400)

#             try:
#                 product_status = Product.objects.get(id=product_id)
#             except Product.DoesNotExist:
#                 return JsonResponse({'status': 'Error', 'message': 'Product not found'}, status=404)

#             if product_status:
#                 # Check if product is already in cart
#                 if Cart.objects.filter(user=request.user, product_id=product_id).exists():
#                     return JsonResponse({'status': 'Product Already in Cart'}, status=200)

#                 # Check stock availability
#                 if product_status.quantity >= product_qty:
#                     # Add to cart
#                     Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
#                     return JsonResponse({'status': 'Product Added to Cart'}, status=200)
#                 else:
#                     return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
#             else:
#                 return JsonResponse({'status': 'Error', 'message': 'Product not found in the inventory'}, status=404)

#         else:
#             return JsonResponse({'status': 'Error', 'message': 'Please login to add items to cart'}, status=401)
#     else:
#         return JsonResponse({'status': 'Error', 'message': 'Invalid access method'}, status=400)
          
import json
from django.http import JsonResponse
from .models import Cart, Product

# # View to add product to cart
# def add_to_cart(request):
#     if request.method == 'POST':
#         try:
#             # Get JSON data from the body
#             data = json.loads(request.body)
#             product_qty = data.get('product_qty')
#             product_id = data.get('pid')

#             # Ensure the quantity and product ID are present
#             if not product_qty or not product_id:
#                 return JsonResponse({'status': 'Error', 'message': 'Missing product_qty or pid'}, status=400)

#             # Fetch the product from the database
#             try:
#                 product = Product.objects.get(id=product_id)
#             except Product.DoesNotExist:
#                 return JsonResponse({'status': 'Error', 'message': 'Product not found'}, status=404)

#             # Check if the product is already in the user's cart
#             if Cart.objects.filter(user=request.user, product=product).exists():
#                 return JsonResponse({'status': 'Product already in cart'}, status=200)

#             # Check if there is enough stock for the requested quantity
#             if product.quantity >= product_qty:
#                 Cart.objects.create(user=request.user, product=product, product_qty=product_qty)
#                 return JsonResponse({'status': 'Product added to cart'}, status=200)
#             else:
#                 return JsonResponse({'status': 'Not enough stock'}, status=400)

#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'Error', 'message': 'Invalid JSON data'}, status=400)

#     return JsonResponse({'status': 'Error', 'message': 'Invalid request method'}, status=400)
     

def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)  # Parse the incoming JSON data
            product_qty = data.get('product_qty')
            product_id = data.get('pid')

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'status': 'Product not found'}, status=400)

            if Cart.objects.filter(user=request.user, id=product_id).exists():
                return JsonResponse({'status': 'Product Already in Cart'}, status=200)
            else:
                if product.quantity >= product_qty:
                    Cart.objects.create(user=request.user, Product=product, Product_qty=product_qty)
                    return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                else:
                    return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)
     
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("/")



def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else: 
     if request.method == 'POST':
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in Successfully")
            return redirect("/")
        else:
            messages.error(request,"Invalid User Name or Password")
            return render(request, "shop/login.html")
    return render(request,"shop/login.html")



def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success! You can now login.")
            return redirect('/login')  # Redirect to login after successful registration
    else:
        form = CustomUserForm()  # Empty form for GET requests

    return render(request, "shop/register.html", {'form': form})


def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, "shop/collections.html", {"category": category})


def collectionsview(request, name):
    # Corrected to reference 'Category' model and check for valid category
    if Category.objects.filter(name=name, status=0):
        products = Product.objects.filter(Category__name=name)
        return render(request, "shop/products/index.html", {"products": products, "category_name": name})
    else:
        messages.warning(request, "No such category found.")
        return redirect('collections')  # Corrected to use 'collections' path name


def product_details(request, cname, pname):
    # Corrected to reference 'Category' model and 'Product' model
    if Category.objects.filter(name=cname, status=0):
        product = Product.objects.filter(name=pname, status=0).first()
        if product:
            return render(request, "shop/products/product_details.html", {"product": product})
        else:
            messages.error(request, "No such product found.")
            return redirect('collections')  # Redirect to collections if product is not found
    else:
        messages.error(request, "No such category found.")
        return redirect('collections')  # Redirect to collections if category is not found

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Product, favourite
import json

# View to add product to favorites

def add_to_favorites(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_id = data['pid']
                product_qty = data['product_qty']

                # Fetch the product by ID
                product = Product.objects.get(id=product_id)
                
                # Check if the product is already in the favorites for the user
                if favourite.objects.filter(user=request.user, product=product).exists():
                    return JsonResponse({'status': 'Product already in favorites'}, status=200)

                # Add product to favorites
                favourite.objects.create(user=request.user, product=product)

                return JsonResponse({'status': 'Product added to favorites'}, status=200)

            except Product.DoesNotExist:
                return JsonResponse({'status': 'Product not found'}, status=404)
            except Exception as e:
                return JsonResponse({'status': f'Error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'status': 'You need to log in first'}, status=403)
    else:
        return JsonResponse({'status': 'Invalid request'}, status=400)

def fav_page(request):
    if request.user.is_authenticated:
        # Fetch the favorite items of the logged-in user
        fav_items = favourite.objects.filter(user=request.user)
        return render(request, "shop/fav.html", {"fav": fav_items})
    else:
        return redirect('login')  # Redirect to login page if user is not authenticated

def remove_from_favorites(request, fav_id):
    if request.user.is_authenticated:
        try:
            fav_item = favourite.objects.get(id=fav_id, user=request.user)  # Fetch the favorite item
            fav_item.delete()  # Remove the item from favorites
            # return JsonResponse({'status': 'Product removed from favorites'}, status=200)
            return redirect('favviewpage')  # Redirect to favorites page
        except favourite.DoesNotExist:
            return JsonResponse({'status': 'Product not in your favorites'}, status=404)
    else:
        return JsonResponse({'status': 'You need to log in first'}, status=403)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Max, Min
from .models import Category, Product, ProductLine, Comment, ProductImage, Chart, Compare
from .forms import CommentForm, ReplyForm, SearchForm
from cart.models import Cart
from cart.forms import CartForm
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from urllib.parse import urlencode

from .filters import ProductFilter



def home(request):
    category = Category.objects.filter(sub_category=False)
    context = {'category':category}
    return render(request, 'home/home.html', context)


def all_products(request,id=None):
    products = Product.objects.all()

    min = Product.objects.aggregate(price=Min('price'))
    min_price = int(min['price'])
    max = Product.objects.aggregate(price=Max('price'))
    max_price = int(max['price'])
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs

    paginator = Paginator(products, 10)
    page_num = request.GET.get('page')
    filters = request.GET.copy()
    if 'page' in filters:
        del filters['page']
    page_obj = paginator.get_page(page_num)

    form = SearchForm()
    category = Category.objects.filter(sub_category=False)
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data['search']
            products = products.filter(Q(name__icontains=data)|Q(description__icontains=data))
    
    if id:
        data = get_object_or_404(Category,id=id)
        page_obj = Product.objects.filter(category=data)
        paginator = Paginator(page_obj,10)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

    context = {'products':page_obj, 'category':category, 'form':form, 'page_num':page_num, 'filter':filter,
               'min_price':min_price, 'max_price':max_price, 'filters':urlencode(filters)}
    return render(request, 'home/products.html', context)


def product_info(request,id):
    product = get_object_or_404(Product,id=id)
    images = ProductImage.objects.filter(product_id=id)
    cart_form = CartForm()
    Comment_form = CommentForm()
    reply_form = ReplyForm()
    comments = Comment.objects.filter(product_id=id,is_reply=False)
    update = Chart.objects.filter(product_id=id)
    change = Chart.objects.all()
    similar = product.tags.similar_objects()[:2]
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True

    is_dislike = False
    if product.dislike.filter(id=request.user.id).exists():
        is_dislike = True

    is_favorite = False
    if product.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    if product.status != 'None':
        if request.method == 'POST':
            product_line = ProductLine.objects.filter(product_id=id)
            pl_id = request.POST.get('select')
            chosen_product_line = ProductLine.objects.get(id=pl_id)
        else:
            product_line = ProductLine.objects.filter(product_id=id)
            chosen_product_line = ProductLine.objects.get(id=product_line[0].id)
        context = {'product':product,'product_line':product_line,'chosen_product_line':chosen_product_line,
                   'similar':similar,'is_like':is_like,'is_dislike':is_dislike,'comment_form':Comment_form,
                   'comments':comments,'reply_form':reply_form,'images':images,'cart_form':cart_form,
                   'is_favorite':is_favorite,'update':update,'change':change}
        
        return render(request, 'home/product_info.html', context)
    else:

        return render(request, 'home/product_info.html', {'product':product,'similar':similar,'is_like':is_like,
                                                          'is_dislike':is_dislike,'comment_form':Comment_form,'comments':comments,
                                                          'reply_form':reply_form,'images':images,'cart_form':cart_form,
                                                          'is_favorite':is_favorite,'update':update,'change':change})
    


def product_like(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
    else:
        product.like.add(request.user)
        is_like = True
    #return redirect('product_info', product.id)
    #return the same page
    return redirect(url)



def product_dislike(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_dislike = False
    if product.dislike.filter(id=request.user.id).exists():
        product.dislike.remove(request.user)
        is_dislike = False
    else:
        product.dislike.add(request.user)
        is_dislike = True
    #return redirect('product_info', product.id)
    #return the same page
    return redirect(url)



def product_comment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'],rate=data['rate'],user_id=request.user.id,product_id=id)
            messages.success(request,'thanks for your comment','success')
            return redirect(url)
        else:
            return redirect(url)
    

def product_comment_reply(request,id,comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(comment=data['comment'],product_id=id,user_id=request.user.id,reply_id=comment_id,is_reply=True)
            messages.success(request,'thanks for your reply','success')
            return redirect(url)
        else:
            return redirect(url)
        

def product_comment_like(request,id):
    url = request.META.get('HTTP_REFERER')
    comment = Comment.objects.get(id=id)
    if comment.like.filter(id=request.user.id).exists():
        comment.like.remove(request.user)
    else:
        comment.like.add(request.user)

    return redirect(url)


def product_search(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data.isdigit():
                products = products.filter(Q(discount__icontains=data)|Q(sale_price__icontains=data))
            else:
                #products = products.filter(name__icontains=data)
                products = products.filter(Q(name__icontains=data)|Q(description__icontains=data))
            return render(request, 'home/products.html', {'products':products,'form':form})



def product_favorite(request,id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    is_favorite = False
    if product.favorite.filter(id=request.user.id).exists():
        product.favorite.remove(request.user)
        product.total_favorite -= 1
        product.save()
        is_favorite = False
    else:
        product.favorite.add(request.user)
        product.total_favorite += 1
        product.save()
        is_favorite = True
    return redirect(url)



def contact(request):
    if request.method == 'POST':
        #if dont want to use forms
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        body = subject + '\n' + email + '\n' + message
        form = EmailMessage(
            'contact form',
            body,
            'test',
            ('hamidhaghverdi12345@gmail.com',),
        )
        form.send(fail_silently=False)

    return render(request, 'account/contact.html')



def compare(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        item = get_object_or_404(Product,id=id)
        qs = Compare.objects.filter(user_id=request.user.id,product_id=id)
        if qs.exists():
            messages.success(request,'the product is already submitted!')
        else:
            Compare.objects.create(user_id=request.user.id,product_id=item.id,session_key=None)

    else:
        item = get_object_or_404(Product,id=id)
        qs = Compare.objects.filter(user_id=None,product_id=id,session_key=request.session.session_key)
        if qs.exists():
            messages.success(request,'the product is already submitted!')
        else:
            if not request.session.session_key:
                request.session.create()
            Compare.objects.create(user_id=None,product_id=item.id,session_key=request.session.session_key)
    return redirect(url)




def compare_list(request):
    if request.user.is_authenticated:
        data = Compare.objects.filter(user_id=request.user.id)
        return render(request, 'home/compare.html')
    
    else:
        data = Compare.objects.filter(session_key__exact=request.session.session_key,user_id=None)
        return render(request, 'home/compare.html', {'data':data})


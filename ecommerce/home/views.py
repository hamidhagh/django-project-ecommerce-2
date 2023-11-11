from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product, ProductLine, Comment
from .forms import CommentForm, ReplyForm



def home(request):
    category = Category.objects.filter(sub_category=False)
    context = {'category':category}
    return render(request, 'home/home.html', context)


def all_products(request,id=None):
    products = Product.objects.all()
    category = Category.objects.filter(sub_category=False)
    if id:
        data = get_object_or_404(Category,id=id)
        products = Product.objects.filter(category=data)

    context = {'products':products, 'category':category}
    return render(request, 'home/products.html', context)


def product_info(request,id):
    product = get_object_or_404(Product,id=id)
    Comment_form = CommentForm()
    reply_form = ReplyForm()
    comments = Comment.objects.filter(product_id=id,is_reply=False)
    similar = product.tags.similar_objects()[:2]
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True

    is_dislike = False
    if product.dislike.filter(id=request.user.id).exists():
        is_dislike = True

    if product.status != 'None':
        if request.method == 'POST':
            product_line = ProductLine.objects.filter(product_id=id)
            pl_id = request.POST.get('select')
            chosen_product_line = ProductLine.objects.get(id=pl_id)
        else:
            product_line = ProductLine.objects.filter(product_id=id)
            chosen_product_line = ProductLine.objects.get(id=product_line[0].id)
        context = {'product':product,'product_line':product_line,'chosen_product_line':chosen_product_line,'similar':similar,'is_like':is_like,'is_dislike':is_dislike,'comment_form':Comment_form,'comments':comments,'reply_form':reply_form}
        return render(request, 'home/product_info.html', context)
    else:

        return render(request, 'home/product_info.html', {'product':product,'similar':similar,'is_like':is_like,'is_dislike':is_dislike,'comment_form':Comment_form,'comments':comments,'reply_form':reply_form})
    


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
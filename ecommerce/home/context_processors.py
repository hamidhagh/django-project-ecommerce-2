from .models import Category

def get_category(request):
    category = Category.objects.filter(sub_category=False)
    context = {'category':category}
    return context
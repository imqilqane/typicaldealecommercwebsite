from django import template
from products.models import Category

register = template.Library()
@register.inclusion_tag('products/navbar.html')
def Ctegories():
    context = {
        'tagscategories': Category.objects.all(),
         }
    return context
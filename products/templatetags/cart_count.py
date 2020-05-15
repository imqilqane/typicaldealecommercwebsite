from django import template
from products.models import Order

register = template.Library()
@register.filter
def counter(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].order_items.count()
    else:
        return 0
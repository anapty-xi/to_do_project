from django import template
from django.db.models import Model 
from account.models import UserProxy 

register = template.Library()

@register.simple_tag
def get_number_todos_status(user_proxy: UserProxy, status: str) -> int | str:
    if not isinstance(user_proxy, Model):
         return ""
    if not hasattr(user_proxy, 'get_number_todos_status'):
         return ""

    amount = user_proxy.get_number_todos_status(status)
    return amount
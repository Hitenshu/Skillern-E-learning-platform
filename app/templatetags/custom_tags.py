from django import template
import math
from app.models import UserCourse , Video, UserVideo
from django.contrib.auth import get_user
register = template.Library()

@register.simple_tag
def dis_price(price,discount):
    if discount is None or discount == 0:
        return price
    sellprice = price
    sellprice = price - (price * discount * 0.01)
    return math.floor(sellprice)

@register.filter
def rupee(price):
    return f'₹  {price}'

@register.simple_tag
def is_enrolled(request , course):
   
    user = None
    if not request.user.is_authenticated:
        return False
        # if you are enrooled in this course you can watch every video
    user = request.user
    try:
        user_course = UserCourse.objects.get(user = user  , course = course)
        return True
    except:
        return False
    

@register.simple_tag
def has_completed_course(user, course):
    total = Video.objects.filter(course=course).count()
    completed = UserVideo.objects.filter(user=user, video__course=course, is_completed=True).count()
    return total == completed and total > 0    


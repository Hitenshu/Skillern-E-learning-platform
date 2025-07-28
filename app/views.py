
from time import time
from django.shortcuts import render,HttpResponse, redirect
from psutil import users
from .models import Courses, Video , Payment , UserCourse , UserVideo
from django.contrib.auth.forms import UserCreationForm
from app.forms.registrationForm import RegistrationForm
from app.forms.loginForm import LoginForm
from django.contrib.auth import login
from django.contrib import auth
from LMS.settings import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import razorpay # type: ignore
import datetime
from django.contrib.auth import get_user
from django.db.models import Q

import warnings
import traceback


# Create your views here.
def home(request):
    course = Courses.objects.filter(active = True)[:8]

    features = [
        {
            'icon': 'bi bi-person-lines-fill',
            'title': 'Professional Instruction',
            'desc': 'Learn from certified and experienced instructors across multiple fields.',
        },
        {
            'icon': 'bi bi-patch-check-fill',
            'title': 'Certified Courses',
            'desc': 'Receive verified certifications upon successful course completion.',
        },
        {
            'icon': 'bi bi-laptop-fill',
            'title': 'Learn Online',
            'desc': 'Flexible learning from anywhere, at any time, on any device.',
        },
        {
            'icon': 'bi bi-book-fill',
            'title': 'Diverse Learning Paths',
            'desc': 'Wide variety of professional and personal development courses available.',
        },
        {
            'icon': 'bi bi-journal-richtext',
            'title': 'Free eBooks',
            'desc': 'Access supplementary reading material at no extra cost.',
        },
        {
            'icon': 'bi bi-globe2',
            'title': 'Global Community',
            'desc': 'Connect and learn with peers across 100+ countries worldwide.',
        },
    ]

    context = {
        'course':course,
        'features':features,
    }
    return render(request, 'course/home.html' ,context)

from django.contrib.auth import get_user

def course_page(request, slug):
    course = Courses.objects.get(slug=slug)
    serial_no = request.GET.get('lecture')
    if serial_no is None:
        serial_no = 1

    video = Video.objects.get(serial_no=serial_no, course=course)

    user = get_user(request)  # ✅ safely resolve LazyObject

    if not video.is_preview:
        if not user.is_authenticated:
            return redirect("login")

        # check if the user is enrolled
        if not UserCourse.objects.filter(user=user, course=course).exists():
            return redirect("enroll", slug=course.slug)

    # Only get completed videos if user is authenticated
    completed_video_ids = []
    if user.is_authenticated:
        completed_video_ids = UserVideo.objects.filter(
            user=user,
            video__in=Video.objects.filter(course=course),
            is_completed=True
        ).values_list('video_id', flat=True)

    context = {
        'course': course,
        'video': video,
        'completed_video_ids': list(completed_video_ids),
    }
    return render(request, 'course/course_page.html', context)



def register(request):
    if request.method == 'POST':
        form =RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # or home page
    else:
        form = UserCreationForm()
    return render(request, 'course/register.html', {'form': form})

def login_view(request):  # Rename to `login_view` to avoid conflicts with auth.login
    if request.method == "POST":
        form = LoginForm(data=request.POST)  # Pass `request`
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('/')
            

    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'course/login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def my_course(request):
    user = request.user
    user_course = UserCourse.objects.filter(user = user)
    context = {
        "user_course" : user_course,
    }
    return render(request, 'course/my_course.html', context)



client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

@login_required(login_url='/login/')
def enroll(request, slug):
    course = Courses.objects.get(slug=slug)
    user = request.user
    action = request.GET.get('action')
    order = None
    payment = None

    try:
        user_course = UserCourse.objects.get(user=user, course=course)
        error = "YOU ARE ALREADY ENROLLED IN THIS COURSE"
       
    except:
        error = None
        amount = int(course.price * (1 - course.discount / 100) * 100)

        # If course is free, enroll directly
        if amount == 0:
            userCourse = UserCourse.objects.create(user=user, course=course)
            userCourse.save()
            return redirect('my_course')

    if action == 'create_payment' and error is None:
        currency = "INR"
        notes = {
            "email": user.email,
            "name": f'{user.first_name} {user.last_name}'
        }
        receipt = f"Skillern-{int(time())}"
        order = client.order.create({
            'receipt': receipt,
            'notes': notes,
            'amount': amount,
            'currency': currency
        })

        payment = Payment()
        payment.user = user
        payment.course = course
        payment.order_id = order.get('id')
        payment.save()

    context = {
        'course': course,
        'order': order,
        'payment': payment,
        'error': error
    }
    return render(request, 'course/enroll.html', context)

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id  = razorpay_payment_id
            payment.status =  True
            
            userCourse = UserCourse(user = payment.user , course = payment.course)
            userCourse.save()

            payment.user_course = userCourse
            payment.save()
            return redirect('my_course')
        except:
            return redirect('home')    

@login_required(login_url='/login/')
def mark_video_completed(request, video_id):
    video = Video.objects.get(id=video_id)
    UserVideo.objects.update_or_create(
        user=request.user,
        video=video,
        defaults={'is_completed': True}
    )
    return redirect('course_page', slug=video.course.slug)


@login_required(login_url='/login/')
def generate_certificate(request, course_id):
    user = request.user
    name = user.get_full_name() or user.username
    course = Courses.objects.get(id=course_id)
    date = datetime.date.today().strftime("%d %B %Y")

    context = {
        'name': name,
        'course': course.name,  # or course.title
        'date': date,
    }

    return render(request, 'certificate_template.html', context)


def about(request):
    return render(request,"course/about.html")

def search(request):
    keyword = request.GET.get('keyword')
    course = Courses.objects.filter(Q(name__icontains=keyword) | Q(description__icontains = keyword) , active = True)
    content={
        'course': course,
        'keyword': keyword,
    }
    return render(request, 'course/search.html',content)
from django.contrib import admin
from .models import Courses,Tag,Prerequiste,Learning,Video, UserCourse, Payment, UserVideo
from django.utils.html import format_html

# Register your models here.

class TagAdmin(admin.TabularInline):
    model = Tag

class PrerequisteAdmin(admin.TabularInline):
    model =  Prerequiste

class LearningAdmin(admin.TabularInline):
    model = Learning   

class VideoAdmin(admin.TabularInline):
    model = Video   
      

class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, PrerequisteAdmin, LearningAdmin,VideoAdmin]   
    list_display = ('name', 'get_price','get_discount','active')
    list_filter = ('price','discount','active')

    def get_price(self , Courses):
        return f'₹ {Courses.price}'
    def get_discount(self , Courses):
        return f'{Courses.discount} %'
    
    get_price.short_description = 'Price'
    get_discount.short_description = 'Discount'

    prepopulated_fields = {'slug':('name',)}


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ('order_id','get_user','get_course','status')   
    list_filter = ('course','status') 

    def get_user(self, payment):
        return format_html( f"<a target='_blank' href='/adminauth/user/{payment.user.id}'>{payment.user}</a>")
    def get_course(self, payment):
        return format_html( f"<a target ='_blank' href= '/adminapp/courses/{payment.course.id}'> {payment.course}</a>")
    
    get_user.short_description = 'User'
    get_course.short_description = 'Course'


class UserCourseAdmin(admin.ModelAdmin):
    model = UserCourse
    list_display = ('get_item','get_user','get_course',)   
    list_filter = ('user','course')

    def get_item(self, UserCourse ):
        return f"{str(UserCourse.user)[:3]}-{str(UserCourse.course)[:3]}"
    def get_user(self, UserCourse):
        return format_html( f"<a target='_blank' href='/adminauth/user/{UserCourse.user.id}'>{UserCourse.user}</a>")
    def get_course(self, UserCourse):
        return format_html( f"<a target ='_blank' href= '/adminapp/courses/{UserCourse.course.id}'> {UserCourse.course}</a>")
    
    get_user.short_description = 'User'
    get_course.short_description = 'Course'
    get_item.short_description = 'Object'


class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display = ('title','course','is_preview')
    list_filter = ('course','is_preview')






admin.site.register(Courses,CourseAdmin)
admin.site.register(Video,VideoAdmin)
admin.site.register(UserCourse,UserCourseAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(UserVideo)

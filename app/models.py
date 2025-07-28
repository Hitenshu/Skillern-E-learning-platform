from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Courses(models.Model):
    name = models.CharField(max_length=50,null=False)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=500,null=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='files/thumbnails')
    date =models.DateTimeField(auto_now_add=True)
    resource = models.FileField(upload_to='files/resources')
    length =models.IntegerField(null=False)

    class Meta:
        verbose_name = "Course"  # Singular name
        verbose_name_plural = "Courses"  # Plural name

    def __str__(self):
        return self.name

class CourseProperties(models.Model):
    description = models.CharField(max_length=20,null = False)
    course = models.ForeignKey(Courses,null= False,on_delete=models.CASCADE)

    class Meta:
        abstract = True 

class Tag(CourseProperties):
    pass

class Prerequiste(CourseProperties):
    pass

class Learning(CourseProperties):
    pass   

class Video(models.Model):
    title = models.CharField(max_length=100, null= False)
    course = models.ForeignKey(Courses, null=False, on_delete=models.CASCADE)
    serial_no = models.IntegerField(null=False)    
    video_id = models.CharField(max_length=500, null= False)
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class UserCourse(models.Model):
    user = models.ForeignKey(User, null = False , on_delete=models.CASCADE)    
    course = models.ForeignKey(Courses, null = False , on_delete=models.CASCADE)    
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'
    

class Payment(models.Model):
    order_id = models.CharField(max_length=50, null = False)
    payment_id = models.CharField(max_length=50) 
    user_course = models.ForeignKey(UserCourse, null = True , on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    course  = models.ForeignKey(Courses, on_delete=models.CASCADE) 
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


class UserVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'video')    
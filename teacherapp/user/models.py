from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.base import Model
from django.db.models.fields.related import OneToOneField
from .manager import CustomUserManager
from .utils import *
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from phonenumber_field.modelfields import PhoneNumberField
import json

class User(AbstractBaseUser,PermissionsMixin):
    
    user_id     = models.CharField(max_length=10,unique=True)
    username    = models.CharField(max_length=50,unique=True,verbose_name="username")
    is_staff    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    is_active   = models.BooleanField(('active'), default=True)
    email       = models.EmailField(('email address'),unique=True)
    date_joined = models.DateTimeField(('date_joined'), auto_now_add=True)
    is_teacher   = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

class Profile(models.Model):
    gender_choise = (
        ("Male","Male"),
        ("Female","Female")
    )
    profile     = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=50,verbose_name="First Name",blank=True)
    last_name   = models.CharField(max_length=50,verbose_name="Last Name",blank=True)
    gender      = models.CharField(choices=gender_choise,max_length=10,verbose_name="Gender",default="Male")
    profile_img = models.URLField(blank=True,default="https://picsum.photos/seed/picsum/200/300")
    location    = models.CharField(max_length=255,verbose_name="Address",blank=True)
    description = models.TextField()
    dob         = models.DateField(verbose_name="Date Of Birth",null=True)
    mobile_no   = PhoneNumberField(blank=True,null=True)

    # last_name           = models.CharField(max_length=25,verbose_name="Last Name")
    # is_online           = models.BooleanField(default=False)
    # got_projects        = models.ManyToManyField("activity.Project_Request",related_name="Project_Request",blank=True)
    # title               = models.CharField(max_length=100,verbose_name="Title")
    # description         = models.CharField(max_length=100,verbose_name="Title")
    # profile_img         = models.URLField(blank=True)
    # keywords            = models.CharField(max_length=200,verbose_name="Keywords")
    # user_plan           = models.ForeignKey(User_Plans,on_delete=models.CASCADE,null=True)




    def __str__(self) -> str:
        return self.profile.username

    def set_keyword(self, x):
        self.keywords = json.dumps(x)

    def get_keyword(self):
        key = json.loads(self.keywords)
        print(key)
        return key

        
    def get_absolute_url(self):
        return reverse("profile",kwargs={"username":self.profile.username})

    class Meta:
        ordering = ["pk"]
class Greade(models.Model):
    grade_id = models.CharField(max_length=10,unique=True,blank=True)
    std = models.PositiveIntegerField(verbose_name="Grade or Standard")
    subject = models.CharField(max_length=60,verbose_name="Siubject Name")
    topic = models.CharField(max_length=500,verbose_name="Topic")

    def __str__(self) -> str:
        return self.grade_id


class Teacher(models.Model):
    teacher = models.OneToOneField(User,on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10,decimal_places=2)
    cover_img = models.URLField(blank=True,default="https://i.picsum.photos/id/1000/5626/3635.jpg")
    grade = models.ForeignKey(Greade,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return  self.teacher.email

class Student(models.Model):
    student = models.OneToOneField(User,on_delete=models.CASCADE)
    father_name = models.CharField(max_length=100,verbose_name="Father Name")
    father_mobile_no = PhoneNumberField(verbose_name="Father Mobile Number")
    father_email = models.EmailField(verbose_name="Father Email Id")
    grade = models.ForeignKey(Greade,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return  self.student.email




class BankAccont(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100,verbose_name="Bank Name")
    iban = models.CharField(max_length=30,verbose_name="IBAN Number")
    bank_address = models.CharField(max_length=255,verbose_name="Bank Address")

    def __str__(self) -> str:
        return self.bank_name


class SocialHandles(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=20,verbose_name="Platform Name",blank=True)
    link = models.URLField(blank=True,default="https://facebook.com")

    def __str__(self) -> str:
        return self.platform_name

class Session(models.Model):
    payment_choise = (
        ("online","online"),
        ("offline","offline")
    )
    session_id = models.CharField(max_length=10,unique=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    grade = models.ForeignKey(Greade,on_delete=models.CASCADE)
    session_title = models.CharField(max_length=50,verbose_name="Session Title")
    session_des = models.TextField(verbose_name="Description",blank=True)
    duration = models.DurationField(verbose_name="Duration",blank=True)
    time = models.DateTimeField(verbose_name="Time")
    no_of_student_allowed = models.PositiveIntegerField(verbose_name="No of Students allowed in session",blank=True,null=True)
    price_per_student = models.DecimalField(max_digits=10,decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=20,choices=payment_choise,default="online")
    custom_session = models.BooleanField(default=False,verbose_name="Negotiation")

    def __str__(self) -> str:
        return self.session_id
    





# id pre save here

def pre_save_create_user_id(sender, instance, *args, **kwargs):
    if not instance.user_id:
        instance.user_id= unique_user_id_generator(instance)


pre_save.connect(pre_save_create_user_id, sender=User)



def pre_save_create_session_id(sender, instance, *args, **kwargs):
    if not instance.session_id:
        instance.session_id= unique_session_id_generator(instance)

pre_save.connect(pre_save_create_session_id, sender=Session)

def pre_save_create_grade_id(sender, instance, *args, **kwargs):
    if not instance.grade_id:
        instance.grade_id= unique_grade_id_generator(instance)

pre_save.connect(pre_save_create_grade_id, sender=Greade)
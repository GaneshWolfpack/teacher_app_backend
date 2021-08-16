from django.contrib import admin
from .models import *
admin.site.register([User,Profile,BankAccont,SocialHandles,Greade,Teacher,Student,Session])

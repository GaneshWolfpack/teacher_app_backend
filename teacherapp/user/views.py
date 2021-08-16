from django.shortcuts import render
from rest_framework.views import APIView
import random
from rest_framework import generics
from django.core.mail import send_mail
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.template.loader import get_template
from rest_framework.validators import ValidationError
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

class EmailVarification(APIView):
    gen_otp = random.randint(100000,999999)
    def get(self,request):
        user = User.objects.get(user_id=request.user.user_id)
        email = user.email
        subject, from_email, to = 'Varification',None,email
        context = {
            "username":user.username,
            "otp":self.gen_otp
        }

        subject = "verify your email"
        sent = send_mail(
            subject=subject,
            message = "hello",
            html_message=get_template('email.html').render(context),
            from_email = None,
            recipient_list = [email])
        if sent:
            return Response({"msg":"email has been sent"})
        raise ConnectionError()
        

    def post(self,request):
        user = User.objects.filter(user_id=request.user.user_id)
        data = request.data
        otp = data["otp"]
        if str(otp) == str(self.gen_otp):
            user.update(is_verified=True)
            return Response({"msg":"email is verified"})
        return ValidationError(detail="you are entering wrong otp",code=400)

class Profile_View(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(profile=user)
class MakeTeacherOrStudent(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        user = request.user
        if data["profile"] == "teacher" or data["profile"]== "Teacher" or data["profile"]== "TEACHER":
            teacher = User.objects.get(user_id=user.user_id)
            teacher_profile = Teacher.objects.create(
                teacher = user,
                hourly_rate = data["hourly_rate"],
                cover_img = data["cover_img_url"],
                grade = data["grade"]
            )
            if teacher_profile:
                teacher.is_teacher = True
                serialize = TeacherSerializer(teacher_profile)
                return Response(data=serialize.data,status=HTTP_201_CREATED)
        else:
            student = User.objects.get(user_id=user.user_id)
            student_profile = Student.objects.create(
                student = user,
                father_name = data["father_name"],
                father_mobile_no = data["father_mobile_no"],
                father_email = data["father_email"],
                grade = data["grade"]
            )
            if student_profile:
                student.is_teacher = False
                serialize = StudentSerializer(student_profile)
                return Response(data=serialize.data,status=HTTP_201_CREATED)

        return Response({"msg":"somthing went wrong"},status=HTTP_400_BAD_REQUEST)

class GradeCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer

    def get_queryset(self):
        user = self.request.user
        return Greade.objects.filter(teacher=user)   



class SocialCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SocialSerializer

    def get_queryset(self):
        user = self.request.user
        return SocialHandles.objects.filter(teacher=user) 


class SessionCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer

    def get_queryset(self):
        user = self.request.user
        return Session.objects.filter(teacher=user)

class SessionReadUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    lookup_field= "session_id"

    def get_queryset(self):
        user = self.request.user
        return Session.objects.filter(teacher=user)


class TeacherProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    lookup_field = "pk"
    def get_queryset(self):
        user = self.request.user
        return Teacher.objects.filter(teacher=user)


class StudentProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(student=user)
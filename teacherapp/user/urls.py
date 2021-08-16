from django.urls import path,include
from .views import *

urlpatterns = [
    path("verification/",EmailVarification.as_view(),name="verification"),
    path("profile/<str:pk>",Profile_View.as_view(),name="profile"),
    path("teacher_profile/<str:pk>",TeacherProfileView.as_view(),name="teacher_profile"),
    path("session/",SessionCreateAPIView.as_view(),name="session"),
    path("session/<str:session_id>",SessionReadUpdateDeleteAPIView.as_view(),name="read_session"),
    path("student_profile/<str:pk>",StudentProfileView.as_view(),name="student_profile"),
    path("create_teacher_or_student/",MakeTeacherOrStudent.as_view(),name="create_teacher"),
    path("grade_create/",GradeCreateAPIView.as_view(),name="grade_create"),
    path("social_account/",SocialCreateAPIView.as_view(),name="social_account")

]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('exam/create/', views.ExamCreateView.as_view(), name='exam-create'),
    path('exam/<int:pk>', views.ExamDetailView.as_view(), name='exam-detail'),
    path('take/<int:report_id>/<int:pk>/<int:ques_num>', views.TakeExamView.as_view(), name='exam-take'),
    path('report', views.ReportView.as_view(), name='report'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question-create'),
    
]
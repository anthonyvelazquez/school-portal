from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  prompt = models.CharField(max_length=255)
  answer = models.CharField(max_length=255)

class Exam(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  title = models.CharField(max_length=255)
  questions = models.ManyToManyField(Question, related_name='questions')
  teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')

class StudentReport(models.Model):
  score = models.FloatField(default=0)
  correct_answers = models.IntegerField(default=0)
  exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam')
  student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
  
  def save(self, *args, **kwargs):
        self.score = (self.correct_answers / self.exam.questions.count()) * 100
        super(StudentReport, self).save(*args, **kwargs)
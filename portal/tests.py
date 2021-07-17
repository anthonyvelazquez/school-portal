from django.test import TestCase
from django.contrib.auth.models import User
from .models import StudentReport, Exam, Question

# models test
class StudentReportTest(TestCase):

  def create_report(self, correct=1):
    student = User.objects.create(username='student')
    teacher = User.objects.create(username='teacher')
    quest1 = Question.objects.create(prompt='quest1')
    quest2 = Question.objects.create(prompt='quest2')
    exam = Exam.objects.create(teacher=teacher)
    exam.questions.add(quest1)
    exam.questions.add(quest2)
    return StudentReport.objects.create(correct_answers=correct, student=student, exam=exam)

  def test_report_score_tracking(self):
      report = self.create_report()
      self.assertTrue(isinstance(report, StudentReport))
      self.assertEqual(report.score, 50.0)
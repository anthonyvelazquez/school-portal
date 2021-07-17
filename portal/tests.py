from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import StudentReport, Exam, Question
from django.urls import reverse_lazy 

# models test
class StudentReportTest(TestCase):

  def create_report(self, correct=1):
    student = User.objects.create(username='student')
    student.set_password('student')
    teacher = User.objects.create(username='teacher')
    teacher.set_password('teacher')
    quest1 = Question.objects.create(prompt='quest1', answer='quest1')
    quest2 = Question.objects.create(prompt='quest2', answer='quest2')
    exam = Exam.objects.create(teacher=teacher)
    exam.questions.add(quest1)
    exam.questions.add(quest2)
    return StudentReport.objects.create(correct_answers=correct, student=student, exam=exam)

  def test_report_score_tracking(self):
    report = self.create_report()
    self.assertTrue(isinstance(report, StudentReport))
    self.assertEqual(report.score, 50.0)

  def test_index_view_no_reports(self):
    user = User.objects.create(username='student')
    user.set_password('student')
    user.save()
    c = self.client
    c.force_login(User.objects.get(username='student'))
    url = reverse_lazy('index')
    resp = c.get(url)
    self.assertEqual(resp.context['new_report_id'], 1)

  def test_index_view_previous_reports(self):
    c = self.client
    report = self.create_report()
    c.force_login(User.objects.get(username='student'))
    url = reverse_lazy('index')
    resp = c.get(url)
    self.assertEqual(resp.context['new_report_id'], 2)

  def test_take_exam_view_get_404(self):
    c = self.client
    report = self.create_report()
    c.force_login(User.objects.get(username='student'))
    url = reverse_lazy('exam-take', kwargs={'report_id': '2', 'pk': '1', 'ques_num': '1'})
    resp = c.get(url)
    self.assertEqual(resp.status_code, 404)

  def test_take_exam_view_get_200(self):
    c = self.client
    report = self.create_report()
    c.force_login(User.objects.get(username='student'))
    url = reverse_lazy('exam-take', kwargs={'report_id': '2', 'pk': '1', 'ques_num': '1'})
    resp = c.get(url, {}, HTTP_REFERER='http://google.com')
    self.assertEqual(resp.status_code, 200)

  def test_take_exam_view_post_404(self):
    c = self.client
    report = self.create_report()
    c.force_login(User.objects.get(username='student'))
    url = reverse_lazy('exam-take', kwargs={'report_id': '2', 'pk': '1', 'ques_num': '1'})
    resp = c.post(url)
    self.assertEqual(resp.status_code, 404)

  def test_take_exam_view_post_200(self):
    c = self.client
    report = self.create_report()
    c.force_login(User.objects.get(username='student'))
    url = reverse_lazy('exam-take', kwargs={'report_id': '2', 'pk': '1', 'ques_num': '1'})
    resp = c.post(url, {'answer': 'quest1'}, HTTP_REFERER='http://google.com')
    fetched_report = StudentReport.objects.get(pk=2)
    fetched_report.correct_answers
    self.assertEqual(fetched_report.correct_answers, 1)
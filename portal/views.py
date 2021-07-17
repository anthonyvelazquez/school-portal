from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Exam, Question, StudentReport

from textblob import TextBlob

def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer

class IndexView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'portal/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        reports = StudentReport.objects.filter(student=self.request.user)
        if reports.count() > 0:
          ctx['new_report_id'] = StudentReport.objects.filter(student=self.request.user).last().pk + 1
        return ctx

class ExamDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('user.is_staff', )
    model = Exam
    template_name = 'portal/detail.html'
    context_object_name = 'exam'

class ExamCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('user.is_staff', )
    model = Exam
    template_name = 'portal/create.html'
    fields = ('title', )
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

class QuestionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('user.is_staff', )
    model = Question
    template_name = 'portal/create.html'
    fields = ('prompt', 'answer')
    success_url = reverse_lazy('index')

    def get_success_url(self):
        exam_id = self.request.GET.get('exam', None)
        exam = Exam.objects.get(pk=exam_id)
        exam.questions.add(self.object)
        return reverse_lazy('exam-detail',args=(exam_id,))

class TakeExamView(LoginRequiredMixin, View):
    def get(self, request, report_id, pk, ques_num):
        if not get_referer(request):
            raise Http404("Cannot navigate between questions. Exam is finalized")
        exam = Exam.objects.get(pk=pk)
        question = exam.questions.all()[ques_num-1]
        prompt_tokens = word_tokenize(question.prompt)
        report = StudentReport.objects.get_or_create(pk=report_id, student=request.user, exam=exam)
        return render(request, 'portal/take.html', {'exam': exam, 'question': question, 'ques_num': ques_num, 'report_id': report_id, 'prompt_tokens': prompt_tokens})

    def post(self, request, report_id, pk, ques_num):
        if not get_referer(request):
            raise Http404("Cannot navigate between questions. Exam is finalized")
        exam = Exam.objects.get(pk=pk)
        question = exam.questions.all()[ques_num-1]
        answer = request.POST.get('answer', '')
        report, created = StudentReport.objects.get_or_create(pk=report_id, student=request.user)
        if question.answer == answer:
            report.correct_answers += 1
        ques_num += 1
        report.save()
        if ques_num > exam.questions.count():
            return redirect('report')
        return redirect('exam-take', report_id=report_id, pk=pk, ques_num=ques_num)

class ReportView(LoginRequiredMixin, ListView):
    model = StudentReport
    template_name = 'portal/score.html'
    def get_queryset(self):
          return StudentReport.objects.filter(student=self.request.user)
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.http import HttpResponseRedirect

from .forms import StudentForm, ImageForm
from .models import *



class MainPageView(ListView):
    model = Student
    template_name = 'index.html'
    context_object_name = 'students'
    paginate_by = 2

    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        if search:
            template_name = 'search.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            context['students'] = Student.objects.filter(Q(student_name__icontains=search) |
                                                         Q(description__icontains=search))
        elif filter:
            start_date = timezone.now() - timedelta(days=1)
            context['students'] = Student.objects.filter(posted_date__gte=start_date)

        else:
            context['students'] = Student.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category-detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.filter(category_id=self.slug)
        return context

class StudentDetailview(DetailView):
    model = Student
    template_name = 'student-detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.get_object().get_image
        context['images'] = self.get_object().images.exclude(id=image.id)
        return context


@login_required(login_url='login')
def add_student(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=1)
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if student_form.is_valid() and formset.is_valid():
            student = student_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                Image.objects.create(image=image, student=student)
            return redirect(student.get_absolute_url())
    else:
        student_form = StudentForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add-student.html', locals())


def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=3)
    student_form = StudentForm(request.POST or None, instance=student)
    formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(student=student))
    if student_form.is_valid() and formset.is_valid():
        student = student_form.save()

        for form in formset:
            image = form.save(commit=False)
            image.student = student
            image.save()
        return redirect(student.get_absolute_url())
    return render(request, 'update-student.html', locals())


class DeleteStudentView(DeleteView):
    model = Student
    template_name = 'delete-student.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted')
        return HttpResponseRedirect(success_url)

from datetime import datetime

from django import forms
from .models import Student, Image


class StudentForm(forms.ModelForm):
    posted_date=forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)
    class Meta:
        model=Student
        fields='__all__'


class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=('image',)
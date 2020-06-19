from django import forms
from django.forms import ModelForm
from .models import Job
from django.core import validators

# Job form to allow use of widgets
class JobForm(ModelForm):

    date_applied = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Job
        fields = ('name','status','location','date_applied','notes')
        widgets = {
            'notes': forms.Textarea(attrs={'class':'editable medium-editor-textarea job_description'})
        }

# Update job form to allow use of widgets
class UpdateJobForm(ModelForm):

    date_applied = forms.DateField(widget=forms.SelectDateWidget())
    date_online_assessment = forms.DateField(required=False,widget=forms.SelectDateWidget(empty_label="---"))
    date_phone_interview = forms.DateField(required=False,widget=forms.SelectDateWidget(empty_label="---"))
    date_video_interview = forms.DateField(required=False,widget=forms.SelectDateWidget(empty_label="---"))
    date_onsite_interview = forms.DateField(required=False,widget=forms.SelectDateWidget(empty_label="---"))
    date_final_decision = forms.DateField(required=False,widget=forms.SelectDateWidget(empty_label="---"))
    date_rejected = forms.DateField(required=False,widget=forms.SelectDateWidget(empty_label="---"))

    class Meta:
        model = Job
        fields = ('location','status','date_applied','date_online_assessment',
        'date_phone_interview','date_video_interview','date_onsite_interview',
        'date_final_decision','date_rejected','notes')
        widgets ={
            'notes': forms.Textarea(attrs={'class':'editable medium-editor-textarea job_description'})
        }

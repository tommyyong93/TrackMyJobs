from django.core import serializers
from django import forms
from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib import messages
from braces.views import SelectRelatedMixin
from jobs.models import Job
from . import models
from .forms import JobForm, UpdateJobForm
from .filters import JobFilter
import django_filters

from django.contrib.auth import get_user_model
User = get_user_model()

# View for creating a new job
class CreateJob(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    login_url = 'login'
    def get_redirect_url(self,*args,**kwargs):
        return reverse('home')

    model = Job
    form_class = JobForm

    def get_success_url(self):
        return reverse('jobs:filter')

    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

# View using filter use this instead of JobList
def job_list_filter(request):
    queryset = queryset=User.objects.prefetch_related("jobs").get(
        username__iexact=request.user.get_username()
    )
    print(queryset)
    filter = JobFilter(request.GET,queryset=queryset.jobs.all())
    return render(request, 'jobs/job_filter.html', {'filter': filter})

# View for the job list (applied jobs)
class JobList(LoginRequiredMixin,SelectRelatedMixin,generic.ListView):
    login_url = 'login'
    model = Job
    template_name = 'jobs/job_list.html'
    select_related = ('user',)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["job_user"] = self.job_user
        return context

    def get_queryset(self):
        try:
            self.job_user = User.objects.prefetch_related("jobs").get(
                username__iexact=self.request.user.get_username()
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.job_user.jobs.all()

# View for one job -- includes update and delete button
class JobDetail(LoginRequiredMixin,SelectRelatedMixin,generic.DetailView):
    model = Job
    select_related = ('user',)
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact = self.request.user.get_username())

# View for updating job
class JobUpdate(LoginRequiredMixin,SelectRelatedMixin,generic.UpdateView):
    login_url = 'login'
    select_related = ('user',)
    template_name = 'jobs/job_edit.html'
    form_class = UpdateJobForm
    model = Job

    def get_success_url(self):
        return reverse_lazy('jobs:filter')

# View for deleting job
class JobDelete(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    login_url = 'login'
    model = Job
    select_related = ('user',)

    def get_success_url(self):
        return reverse_lazy('jobs:filter')

# Dashboard view -- inlcudes more data in query set
class JobDashboard(LoginRequiredMixin,SelectRelatedMixin,generic.ListView):
    login_url = 'login'
    model = Job
    template_name = 'jobs/job_dashboard.html'
    select_related = ('user',)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["job_user"] = self.job_user
        context["online_jobs"] = self.online_jobs
        context["phone_jobs"] = self.phone_jobs
        context["video_jobs"] = self.video_jobs
        context["onsite_jobs"] = self.onsite_jobs
        context["final_jobs"] = self.final_jobs
        context["rejection_jobs"] = self.rejection_jobs
        context["no_response"] = self.no_response
        return context

    def get_queryset(self):
        try:
            self.job_user = User.objects.prefetch_related("jobs").get(
                username__iexact=self.request.user.get_username()
            )
            self.online_jobs = Job.online_jobs.all().filter(user=self.request.user)
            self.phone_jobs = Job.phone_jobs.all().filter(user=self.request.user)
            self.video_jobs = Job.video_jobs.all().filter(user=self.request.user)
            self.onsite_jobs = Job.onsite_jobs.all().filter(user=self.request.user)
            self.final_jobs = Job.final_jobs.all().filter(user=self.request.user)
            self.rejection_jobs = Job.rejection_jobs.all().filter(user=self.request.user)
            self.no_response = Job.no_response.all().filter(user=self.request.user)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.job_user.jobs.all()

# View for plots - data has been serialized to be used in js
class JobPlots(LoginRequiredMixin,SelectRelatedMixin,generic.ListView):
    login_url = 'login'
    model = Job
    template_name = 'jobs/job_plots.html'
    select_related = ('user',)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        JSONSerializer = serializers.get_serializer("json")
        json_serializer = JSONSerializer()
        json_serializer.serialize(self.online_jobs)
        context["job_user"] = self.job_user
        context["online_jobs"] = self.online_jobs
        context["phone_jobs"] = self.phone_jobs
        context["video_jobs"] = self.video_jobs
        context["onsite_jobs"] = self.onsite_jobs
        context["final_jobs"] = self.final_jobs
        context["rejection_jobs"] = self.rejection_jobs
        context["no_response"] = self.no_response
        ### serialize querysets to use in javascript
        json_serializer.serialize(self.job_user.jobs.all())
        context['applied_jobs_dict'] = json_serializer.getvalue()
        json_serializer.serialize(self.online_jobs)
        context["online_jobs_dict"] = json_serializer.getvalue()
        json_serializer.serialize(self.phone_jobs)
        context["phone_jobs_dict"] = json_serializer.getvalue()
        json_serializer.serialize(self.video_jobs)
        context["video_jobs_dict"] = json_serializer.getvalue()
        json_serializer.serialize(self.onsite_jobs)
        context["onsite_jobs_dict"] = json_serializer.getvalue()
        json_serializer.serialize(self.final_jobs)
        context["final_jobs_dict"] = json_serializer.getvalue()
        json_serializer.serialize(self.rejection_jobs)
        context["rejection_jobs_dict"] = json_serializer.getvalue()
        json_serializer.serialize(self.no_response)
        context["no_response_dict"] = json_serializer.getvalue()
        return context

    def get_queryset(self):
        try:
            self.job_user = User.objects.prefetch_related("jobs").get(
                username__iexact=self.request.user.get_username()
            )
            self.online_jobs = Job.online_jobs.all().filter(user=self.request.user)
            self.phone_jobs = Job.phone_jobs.all().filter(user=self.request.user)
            self.video_jobs = Job.video_jobs.all().filter(user=self.request.user)
            self.onsite_jobs = Job.onsite_jobs.all().filter(user=self.request.user)
            self.final_jobs = Job.final_jobs.all().filter(user=self.request.user)
            self.rejection_jobs = Job.rejection_jobs.all().filter(user=self.request.user)
            self.no_response = Job.no_response.all().filter(user=self.request.user)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.job_user.jobs.all()

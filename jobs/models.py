from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Q
# Create your models here.
import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()

# Gets jobs which are under status 'online'
class OnlineManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(date_online_assessment__isnull = False)
                                            | Q(status__iexact='Online Assessment 1')
                                            | Q(status__iexact='Online Assessment 2')
                                            | Q(status__iexact='Online Assessment 3'))

# Gets jobs which are under status 'phone'
class PhoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(date_phone_interview__isnull = False)
                                            | Q(status__iexact='Phone Interview 1')
                                            | Q(status__iexact='Phone Interview 2'))

# Gets jobs which are under status 'video'
class VideoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(date_video_interview__isnull = False)
                                            | Q(status__iexact='Video Interview 1')
                                            | Q(status__iexact='Video Interview 2'))

# Gets jobs which are under status 'onsite'
class OnsiteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(date_onsite_interview__isnull = False)
                                            | Q(status__iexact='Onsite Interview'))

# Gets jobs which are under status 'final decision'
class FinalDecisionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(date_final_decision__isnull = False)
                                            | Q(status__iexact='Offer')
                                            | Q(status__iexact='Accepted Offer')
                                            | Q(status__iexact='Declined Offer')
                                            )

# Gets jobs which are under status 'rejection'
class RejectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status__iexact='Rejection')
                                            |Q(date_rejected__isnull=False))

# Gets jobs which are under status 'no response'
class NoResponseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status__iexact='No Response'))

# Job model
class Job(models.Model):
    # Categories for status
    STATUS = (('Applied','Applied'),
    ('Online Assessment 1','Online Assessment 1'),
    ('Online Assessment 2','Online Assessment 2'),
    ('Online Assessment 3','Online Assessment 3'),
    ('Phone Interview 1','Phone Interview 1'),
    ('Phone Interview 2','Phone Interview 2'),
    ('Video Interview 1','Video Interview 1'),
    ('Video Interview 2','Video Interview 2'),
    ('Onsite Interview','Onsite Interview'),
    ('Offer','Offer'),
    ('Rejection','Rejection'),
    ('Accepted Offer','Accepted Offer'),
    ('Declined Offer','Declined Offer'),
    ('No Response','No Response'))

    user = models.ForeignKey(User,related_name='jobs',on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    slug = models.SlugField(allow_unicode=True)
    status = models.CharField(blank=True,choices=STATUS,max_length=30)
    location = models.CharField(blank=True,max_length=255)
    date_applied = models.DateField(null=True)
    date_online_assessment = models.DateField(null=True)
    date_phone_interview = models.DateField(null=True)
    date_video_interview = models.DateField(null=True)
    date_onsite_interview = models.DateField(null=True)
    date_final_decision = models.DateField(null=True)
    date_rejected = models.DateField(null=True)
    notes = models.TextField(blank=True,default='')
    notes_html = models.TextField(editable=False,default='',blank=True,null=True)

    objects = models.Manager()
    online_jobs = OnlineManager()
    phone_jobs = PhoneManager()
    video_jobs = VideoManager()
    onsite_jobs = OnsiteManager()
    final_jobs = FinalDecisionManager()
    rejection_jobs = RejectionManager()
    no_response = NoResponseManager()

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.notes_html = misaka.html(self.notes)
        super().save(*args,**kwargs)

    class Meta:
        ordering = ['date_applied']
        unique_together = ['user','name']

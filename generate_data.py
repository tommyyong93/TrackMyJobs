import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobtracker.settings')
import django
django.setup()

from faker import Faker
import random
from account.models import User
from jobs.models import Job

def populate(N=1,M=1):
    generator = Faker()

    STATUS = (('Applied','Applied'),
    ('Online Assessment 1','Online Assessment 1'),
    ('Online Assessment 2','Online Assessment 2'),
    ('Online Assessment 3','Online Assessment 3'),
    ('Phone Interview 1','Phone Interview 1'),
    ('Phone Interview 1','Phone Interview 1'),
    ('Video Interview 1','Video Interview 1'),
    ('Video Interview 2','Video Interview 2'),
    ('Onsite Interview','Onsite Interview'),
    ('Offer','Offer'),
    ('Rejection','Rejection'),
    ('Accepted Offer','Accepted Offer'),
    ('Declined Offer','Declined Offer'))

    for i in range(N):
        fakeName = generator.user_name()
        fakeEmail = generator.ascii_safe_email()
        fakePass = generator.password()

        newUser = User.objects.get_or_create(username=fakeName,email=fakeEmail,password=fakePass)[0]
        newUser.save()

        for i in range(M):
            fakeJob = generator.bs()
            fakeStatus = STATUS[random.randint(0,12)][0]
            fakeDate = generator.date_this_century()

            newJob = Job.objects.get_or_create(user=newUser,name=fakeJob,status=fakeStatus,date_applied=fakeDate)[0]
            newJob.save()

if __name__ == '__main__':
    print("Populating Script!")
    populate(5,10)
    print("Populating complete!")

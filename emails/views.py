from django.shortcuts import render,redirect

from emails.tasks import send_email_task
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscribers

 
# Create your views here.
def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form=email_form.save()
            # Send an email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            # Acces the selected email_list
            email_list = email_form.email_list 
            
            # Extract email address
            subscribers = Subscribers.objects.filter(email_list=email_list)
            to_email =[email.email_address for email in subscribers]  

            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                attachment = None 

            # handover to celery    
            send_email_task(mail_subject,message, to_email, attachment)       
            # send_email_notification(mail_subject,message, to_email, attachment)  

            # to_email = settings.DEFAULT_TO_EMAIL
            # send_email_notification(mail_subject,message,to_email)
            #Display a success message
            messages.success(request, 'Email sent successfully')
            return redirect('send_email')
    else:
        email_form = EmailForm()
        context = {
            'email_form' : email_form 
        }
        return render(request, 'emails/send_email.html', context)
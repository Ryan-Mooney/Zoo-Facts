from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.urls import reverse
from django.views import generic
from django.template import Context, Template, loader, RequestContext
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.conf import settings
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests, ast, urllib.request, smtplib, random
from .functions import *
from .forms import *

def index(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		if 'submit' in request.POST:
			form=ZooSpamForm(request.POST)
			if form.is_valid():
				#This is the code to get the picture from the API
					#get_request=requests.get('https://dog.ceo/api/breeds/image/random')
					#decoded_picture=get_request.content.decode("utf-8")
					#picture_dic=ast.literal_eval(decoded_picture)
					#picture_url=picture_dic["message"]
					#new_picture_url=remove_forward_slashes(picture_url)

				#Import facts and picture URL arrays and randomly choose one
				facts_array=get_facts()
				urls_array=get_pic_urls()
				new_form=form.save()

				#Initialize loop variables and fact holder
				i=new_form.number_messages
				sent_facts=''

				#Sends a different fact for each message desired
				while i>0:
					random_index=random.randrange(0,len(urls_array)-1,1)
					picture_url=urls_array[random_index]
					fact=facts_array[random_index]
					fact=fact[0].lower()+fact[1:].rstrip('.')
					text='Did you know ' + fact + '?' 
					sent_facts=sent_facts+'<img src="'+picture_url+'" width=400></br>'+'<p class="fact-zoospam">'+text+'</p>'

					#Save the picture url we are sending
					new_form.picture_url=picture_url
					new_form.save()

					#Create container for message
					msgRoot=MIMEMultipart('related')
					msgRoot['From']='zoospam@mailgun.org'
					msgRoot['To']=new_form.email_recipient
					msgRoot['Subject']='Zoo Spam'
					message = text + '<br />' + '<img src="cid:image1">'
					msgText=MIMEText(message, 'html')
					msgRoot.attach(msgText)

					#Retrieve image and attach to message
					msg_data=urllib.request.urlopen(picture_url)
					msg_img=MIMEImage(msg_data.read(), _subtype="jpeg + png + gif")
					msg_img.add_header('Content-ID', '<image1>')
					msgRoot.attach(msg_img)

					#Create SMS array for recipient
					SMS_array = create_sms_array(new_form.email_recipient)

					#Send message via smtp server
					smtp = smtplib.SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT)
					smtp.starttls()
					smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
					smtp.sendmail(settings.EMAIL_HOST_USER, new_form.email_recipient, msgRoot.as_string())
					smtp.quit()

					i=i-1

				#Reinitialize form (comment next line out to prevent form refreshing)
				form=ZooSpamForm()
				picture_url=picture_url+" width=400"
				message_sent='Your message was successfully sent to '+new_form.email_recipient + '!'
				args={'form': ZooSpamForm(), 'message_sent': message_sent, 'sent_facts': sent_facts,}
				return render(request, './ZooSpam/index.html', args)
		
		#Does all the features of submit without sending anything
		elif 'test' in request.POST:
			form=ZooSpamForm(request.POST)
			#Import facts and picture URL arrays and randomly choose one for each request
			facts_array=get_facts()
			urls_array=get_pic_urls()
			new_form=form.save()
			new_form.email_recipient='Test'
			i=new_form.number_messages
			sent_facts=''
			while i>0:
				random_index=random.randrange(0,len(urls_array)-1,1)
				picture_url=urls_array[random_index]
				fact=facts_array[random_index]
				fact=fact[0].lower()+fact[1:].rstrip('.')
				text='Did you know ' + fact + '?' 
				sent_facts=sent_facts+'<img src="'+picture_url+'" width=400></br>'+'<p class="fact-zoospam">'+text+'</p>'
				i=i-1
			
			#Reinitialize form (comment next line out to prevent form refreshing)
			form=ZooSpamForm()
			confirmation_text='This is what your friend would get!'
			args={'form': ZooSpamForm(), 'sent_facts': sent_facts, 'message_sent': confirmation_text,}
			return render(request, './ZooSpam/index.html', args)
			
	#Otherwise, we render a blank form to be filled
	else:
		form=ZooSpamForm()
		template=loader.get_template('./ZooSpam/index.html')
		return render(request, './ZooSpam/index.html', {'form': form})

def attributions(request):
	template=loader.get_template('./ZooSpam/attributions.html')
	attribution_list=get_attributions()
	args={'attribution_list': attribution_list,}
	return render(request, './ZooSpam/attributions.html', args,)
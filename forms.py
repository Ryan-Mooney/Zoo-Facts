from django import forms
from .models import ZooSpamForm

class ZooSpamForm(forms.ModelForm):
	class Meta:
		model = ZooSpamForm
		email_recipient=ZooSpamForm.email_recipient
		number_messages=ZooSpamForm.number_messages
		widgets = {
			'email_recipient': forms.TextInput(attrs={'placeholder': 'sample@email.com'}),
		}
		fields = ('email_recipient','number_messages',)
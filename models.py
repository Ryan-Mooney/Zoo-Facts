from django.db import models

class ZooSpamForm(models.Model):
	email_recipient=models.CharField(max_length=500, null=True)
	numbers_choices=((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10'))
	number_messages=models.IntegerField(choices=numbers_choices, default=1)
	picture_url=models.CharField(max_length=500)
	def __str__(self):
		return self.email_recipient
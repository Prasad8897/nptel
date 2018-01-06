# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.


class Email(models.Model):
	email = models.EmailField(unique=True)

	def __str__(self):
		return self.email


class MailingList(models.Model):

	list_id = models.EmailField(unique=True)
	contact = models.EmailField()

	def __str__(self):
		return self.list_id


class EmailData(models.Model):

	date = models.DateTimeField()
	from_email = models.ForeignKey(Email, related_name='from_email')
	to_email = models.ManyToManyField(Email, related_name='to_email')
	cc = models.ManyToManyField(Email, related_name='cc')
	subject = models.CharField(max_length=10000)
	mailing_list = models.ForeignKey(MailingList)
	mail_id = models.IntegerField(default=0, unique=True)

	def __str__(self):
		return self.mail_id

	def __unicode__(self):
		return unicode(self.mail_id)

	class Meta:
		ordering = ('-mail_id',)


class EmailBody(models.Model):

	email_data = models.ForeignKey(EmailData)
	contentType = models.CharField(max_length=20)
	body = models.TextField()

class  FullEmail(models.Model):
	
	mail_id = models.IntegerField(default=0)
	data = models.TextField()
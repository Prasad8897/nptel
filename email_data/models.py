# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
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


class Threads(models.Model):
    message_ids = models.TextField(null=True)

    def getIds(self):
        return json.loads(self.message_ids)

    def saveIds(self, ids):
        self.message_ids = json.dumps(ids)


class EmailData(models.Model):

    date = models.DateTimeField()
    from_email = models.ForeignKey(Email, related_name='from_email',
                                   on_delete=models.CASCADE)
    to_email = models.TextField()
    cc = models.TextField()
    subject = models.CharField(max_length=10000)
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    mail_id = models.IntegerField(default=0, unique=True)
    thread = models.ForeignKey(Threads)
    
    def __str__(self):
        return self.mail_id

    def __unicode__(self):
        return unicode(self.mail_id)

    class Meta:
        ordering = ('-mail_id',)

    def save_to_emails(self, emails):
        self.to_email = json.dumps(emails)

    def get_to_emails(self):
        return Email.objects.filter(email__in=json.load(self.to_email))

    def save_cc(self, emails):
        self.cc = json.dumps(emails)

    def get_cc(self):
        return Email.objects.filter(email__in=json.load(self.cc))


class EmailBody(models.Model):

    email_data = models.ForeignKey(EmailData)
    message_id = models.CharField(max_length=1000, default='')
    in_reply_to = models.CharField(max_length=1000, null=True)
    contentType = models.CharField(max_length=20)
    body = models.TextField()

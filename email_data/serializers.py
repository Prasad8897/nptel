from email_data.models import EmailData
from rest_framework import serializers


class EmailDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = EmailData
		fields = (
			'mail_id', 'date', 'from_email', 'to_email', 'cc', 'subject',
			'mailing_list'
			)

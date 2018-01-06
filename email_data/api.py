from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from email_data.models import Email, EmailData, MailingList, EmailBody
from django.db.models import Count
from django.template.loader import get_template


MAILINGLIST_NOT_FOUND = 'Discussion group nocXX-XXXX-discuss@nptel.iitm.ac.in does not exists'
ADMIN_EMAIL_NOT_FOUND = 'Admin Email not of form nocXX-XXXX@nptel.iitm.ac.in'

@api_view(["GET"])
def CourseMetaData(request, courseId):
	if request.method == 'GET':
		group = courseId+"-discuss@nptel.iitm.ac.in"
		m = MailingList.objects.filter(list_id=group)
		if not m.exists():
			return JsonResponse(status=404, data={'status':'404','message':MAILINGLIST_NOT_FOUND})
		
		admin_email = Email.objects.filter(email=courseId+"@nptel.iitm.ac.in")
		if not admin_email.exists():
			return JsonResponse(status = 404,data={'status':'404','message':ADMIN_EMAIL_NOT_FOUND})
		
		allEmails = EmailData.objects.filter(mailing_list=m).order_by('-date')
		totalPosts = allEmails.count()
		
		adminPosts = allEmails.filter(from_email=admin_email).order_by('-date')
		
		subjects = allEmails.order_by('subject').values('subject').distinct()
		count=0
		for s in subjects:
			fe = allEmails.filter(subject=s['subject']).order_by('from_email').values('from_email').distinct()
			for e in fe:
				if e['from_email'] == admin_email[0].id:
					count+=1
		print count
		print subjects.count()-count

		return JsonResponse({
			'totalPosts': totalPosts,
			"lastAdminPostDate": adminPosts[0].date.strftime('%Y-%m-%d %H:%M:%S'),
			'lastUserPostDate': allEmails[0].date.strftime('%Y-%m-%d %H:%M:%S'),
			})

@api_view(['GET'])
def AllEmailData(request, courseId):
	if request.method == 'GET':
		group = courseId+"-discuss@nptel.iitm.ac.in"
		m = MailingList.objects.filter(list_id=group)
		if not m.exists():
			return JsonResponse(status=404, data={'status':'404','message':MAILINGLIST_NOT_FOUND})

		ed = EmailData.objects.filter(subject__icontains='introduce yourself').filter(mailing_list=m)
		body = EmailBody.objects.filter(email_data__in=ed).values('email_data__mail_id','body')
		#t = get_template('index.html');html = t.render({'email_data':ed})
		t = get_template('body.html');html = t.render({'body':body})
		return HttpResponse(html)

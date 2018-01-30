from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from email_data.models import Email, EmailData, MailingList, EmailBody
from django.db.models import Count, Q
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
		
		userPosts = allEmails.exclude(from_email=admin_email).order_by('date')
		adminPosts = allEmails.filter(from_email=admin_email).order_by('-date')
		
		count=allEmails.filter(from_email=admin_email).order_by('thread').values('thread').distinct().count()
		threads = allEmails.order_by('thread').values('thread').distinct().count()
		print threads
		print count
		return JsonResponse({
			'totalPosts': totalPosts,
			"lastAdminPostDate": adminPosts[0].date.strftime('%Y-%m-%d %H:%M:%S'),
			'lastUserPostDate': userPosts[0].date.strftime('%Y-%m-%d %H:%M:%S'),
			'unanswered': threads-count,
			})

@api_view(['GET', 'PATCH', 'DELETE'])
def AllEmailData(request, courseId):
	group = courseId+"-discuss@nptel.iitm.ac.in"
	m = MailingList.objects.filter(list_id=group)
	allEmails = EmailData.objects.filter(mailing_list=m).order_by('-date')
	if not m.exists():
		return JsonResponse(status=404, data={'status':'404','message':MAILINGLIST_NOT_FOUND})
	if request.method == 'GET':
		ed = EmailData.objects.filter(subject__icontains='introduce yourself').filter(mailing_list=m)
		body = EmailBody.objects.filter(email_data__in=ed).values('id','body')
		d = []
		for b in body:
			d.append({'id':b['id'],'body':b['body']})
		return JsonResponse({'data':d})
	elif request.method == 'PATCH':
		inputdict = request.data
		e = ""
		try:
			e = EmailBody.objects.get(id=inputdict['id'],email_data__in=allEmails)
		except:
			return JsonResponse(status=404, data={'status':'404','message':"Operation not possible"})
		e.body = inputdict['body']
		e.save()
		data = {'id':e.id,'body':e.body}
		return JsonResponse(data)
	elif request.method == 'DELETE':
		inputdict = request.data
		e= ""
		try:
			e = EmailBody.objects.get(id=inputdict['id'],email_data__in=allEmails)
		except:
			return JsonResponse(status=404, data={'status':'404','message':"Operation not possible"})
		e.delete()
		return JsonResponse({})

@api_view(['GET'])
def mostAnsweredPeople(request, courseId):
	if request.method == 'GET':
		group = courseId+"-discuss@nptel.iitm.ac.in"
		m = MailingList.objects.filter(list_id=group)
		if not m.exists():
			return JsonResponse(status=404, data={'status':'404','message':MAILINGLIST_NOT_FOUND})
		
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from email_data.models import Email, EmailData, MailingList, EmailBody, Threads

MAILINGLIST_NOT_FOUND = 'Discussion group nocXX-XXXX-discuss@nptel.iitm.ac.in'
MAILINGLIST_NOT_FOUND += 'does not exists'
ADMIN_EMAIL_NOT_FOUND = 'Admin Email not of form nocXX-XXXX@nptel.iitm.ac.in'


@api_view(["GET"])
def CourseMetaData(request, courseId):
    if request.method == 'GET':
        group = courseId+"-discuss@nptel.iitm.ac.in"
        m = MailingList.objects.filter(list_id=group)
        results = {}
        if not m.exists():
            return JsonResponse(status=404,
                                data={'status': '404',
                                      'message': MAILINGLIST_NOT_FOUND})
        admin_email = Email.objects.filter(email=courseId+"@nptel.iitm.ac.in")
        if admin_email.exists():
            allEmails = EmailData.objects.filter(from_email=admin_email,
                                                 mailing_list=m)
            allEmails = allEmails.order_by('-date')
            query = allEmails[0].date
            results['lastAdminPostDate'] = query.strftime("%Y-%m-%d %H:%M:%S")
        else:
            results['lastAdminPostDate'] = 'Not Found'
        allEmails = EmailData.objects.filter(mailing_list=m).order_by('-date')
        query = allEmails[0].date
        results['lastUserPostDate'] = query.strftime("%Y-%m-%d %H:%M:%S")
        totalPosts = allEmails.count()
        results['totalPosts'] = totalPosts
        threads = allEmails.values('thread').order_by('thread').distinct()
        count = 0
        for thread in threads:
            threadDetails = Threads.objects.get(id=thread.values()[0])
            if len(threadDetails.getIds()) == 1:
                count += 1
        results['unanswered'] = count
        return JsonResponse({'result': results})


@api_view(['GET', 'PATCH', 'DELETE'])
def AllEmailData(request, courseId):
    group = courseId+"-discuss@nptel.iitm.ac.in"
    m = MailingList.objects.filter(list_id=group)
    allEmails = EmailData.objects.filter(mailing_list=m).order_by('-date')
    if not m.exists():
        return JsonResponse(status=404,
                            data={'status': '404',
                                  'message': MAILINGLIST_NOT_FOUND})
    if request.method == 'GET':
        ed = EmailData.objects.filter(subject__icontains='introduce yourself')
        ed = ed.filter(mailing_list=m)
        body = EmailBody.objects.filter(email_data__in=ed).values('id', 'body')
        d = []
        for b in body:
            d.append({'id': b['id'], 'body': b['body']})
        return JsonResponse({'result': d})
    elif request.method == 'PATCH':
        inputdict = request.data
        e = ""
        try:
            e = EmailBody.objects.get(id=inputdict['id'],
                                      email_data__in=allEmails)
        except EmailBody.DoesNotExist:
            return JsonResponse(status=404,
                                data={'status': '404',
                                      'message': "Operation not possible"})
        e.body = inputdict['body']
        e.save()
        data = {'id': e.id, 'body': e.body}
        return JsonResponse(data)
    elif request.method == 'DELETE':
        inputdict = request.data
        e = ""
        try:
            e = EmailBody.objects.get(id=inputdict['id'],
                                      email_data__in=allEmails)
        except EmailBody.DoesNotExist:
            return JsonResponse(status=404,
                                data={'status': '404',
                                      'message': "Operation not possible"})
        e.delete()
        return JsonResponse({})


@api_view(['GET'])
def mostAnsweredPeople(request, courseId, count):
    if request.method == 'GET':
        group = courseId+"-discuss@nptel.iitm.ac.in"
        m = MailingList.objects.filter(list_id=group)
        if not m.exists():
            return JsonResponse(status=404,
                                data={'status': '404',
                                      'message': MAILINGLIST_NOT_FOUND})
        emailFreq = {}
        emailFreq2 = {}
        allEmails = EmailData.objects.filter(mailing_list=m)
        allEmails = allEmails.values('from_email_id')
        dist = allEmails.order_by('from_email_id').distinct()
        for e in allEmails:
            try:
                emailFreq[e['from_email_id']] += 1
            except KeyError:
                emailFreq[e['from_email_id']] = 1
        for i in emailFreq.keys():
            emailFreq2[Email.objects.get(id=i).email] = emailFreq[i]
        value = sorted(emailFreq2.items(), key=lambda x: x[1], reverse=True)
        emailFreq = dict((x, y) for x, y in value[:int(count)])
        print emailFreq
        return JsonResponse({'result': emailFreq})

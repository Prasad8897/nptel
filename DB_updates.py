from email_data.models import Email, MailingList, EmailData, EmailBody, Threads


def addToDB(data):
    try:
        EmailData.objects.get(mail_id=data['id'])
        raise ValueError("done till here")
    except EmailData.DoesNotExist:
        from_email = EmailInstance(data['from'])
        m = MailingListInstance(data['mailing-list'])
        ed = EmailData()
        ed.from_email = from_email
        ed.mailing_list = m
        to = []
        for e in data['to']:
            to.append(EmailInstance(e).id)
        ed.save_to_emails(to)
        cc = []
        for e in data['cc']:
            cc.append(EmailInstance(e).id)
        ed.save_cc(cc)
        ed.date = data['date']
        ed.mail_id = data['id']
        t = ThreadInstance(data['in-reply-to'], data['message-id'])
        ed.thread = t
        ed.subject = data['subject']
        ed.save()
        print str(data['id'])
        if data['body']:
            body = EmailBody(
                email_data=ed,
                message_id=data['message-id'],
                in_reply_to=data['in-reply-to'],
                contentType='text/plain',
                body=data['body'])
            body.save()


def EmailInstance(email):
    obj, create = Email.objects.get_or_create(email=email)
    if not create:
        return obj
    else:
        return Email.objects.get(email=email)


def MailingListInstance(data):
    obj, create = MailingList.objects.get_or_create(
        list_id=data[0], contact=data[1])
    if not create:
        return obj
    else:
        return MailingList.objects.get(list_id=data[0])


def ThreadInstance(in_reply_to, message_id):
    thread = Threads.objects.filter(message_ids__icontains=message_id)
    if in_reply_to is not None:
        thread = thread | Threads.objects.filter(
            message_ids__icontains=in_reply_to)
    if thread.exists():
        thread = thread[0]
        l = thread.getIds()
        addToList(in_reply_to, l)
        thread.saveIds(l)
        thread.save()
        return thread
    else:
        thread = Threads()
        l = []
        addToList(in_reply_to, l)
        addToList(message_id, l)
        thread.saveIds(l)
        thread.save()
        return thread


def addToList(a, l):
    if a is not None:
        if a not in l:
            l.append(a)

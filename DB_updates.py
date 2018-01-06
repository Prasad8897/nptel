from email_data.models import Email, MailingList, EmailData, EmailBody


def addToDB(data):
    try:
        EmailData.objects.get(mail_id=data['id'])
        raise ValueError("done till here")
    except EmailData.DoesNotExist:
        from_email = EmailInstance(data['from'])
        m = MailingListInstance(data['mailing-list'])
        ed = EmailData(
            date=data['date'],
            from_email=from_email,
            subject=data['subject'],
            mailing_list=m,
            mail_id=data['id']
        )
        ed.save()
        if data['body']:
            b = EmailBody(
                email_data=ed,
                body=data['body'])
            b.save()
        for e in data['to']:
            ed.to_email.add(EmailInstance(e))
        for e in data['cc']:
            ed.cc.add(EmailInstance(e))
        print "Email data: " + str(ed.id)


def EmailInstance(email):
    try:
        return Email.objects.get(email=email)
    except Email.DoesNotExist:
        e = Email(email=email)
        e.save()
        return e


def MailingListInstance(data):
    try:
        return MailingList.objects.get(list_id=data[0])
    except MailingList.DoesNotExist:
        m = MailingList(list_id=data[0], contact=data[1])
        m.save()
        return m

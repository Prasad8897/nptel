import sys
import imaplib
import email
import time
from datetime import date
from data_organiser import date_formatting, email_formating, email_set, subject_formatting, mailing_list_formating, body_formatting, message_id_formatting
from DB_updates import addToDB


reload(sys)
sys.setdefaultencoding('utf-8')


def process1(msg, ids, body):
    if msg['mailing-list']:
        data = {}
        data['date'] = date_formatting(msg['date'])
        data['id'] = ids
        data['from'] = email_formating(msg['from'])
        data['to'] = email_set(msg['to'])
        data['cc'] = email_set(msg['cc'])
        data['subject'] = subject_formatting(msg['subject'])
        data['mailing-list'] = mailing_list_formating(msg['mailing-list'])
        data['body'] = body_formatting(body)
        data['message-id'] = message_id_formatting(msg['message-id'])
        data['in-reply-to'] = message_id_formatting(msg['in-reply-to'])
        # print message_id_formatting(msg['message-id'])
        addToDB(data)


FROM_EMAIL = "reviewer1@nptel.iitm.ac.in"
FROM_PWD = "1reviewer"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def read_email_from_gmail():
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    i = len(id_list) - 1
    while i >= 0:
        try:
            typ, data = mail.fetch(id_list[i], '(BODY.PEEK[])')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(
                        response_part[1].decode("utf-8", errors='ignore'))
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain' and part.get_filename() is None:
                            process1(
                                msg,
                                i,
                                part.get_payload(decode=True).decode(part.get_charsets()[0]))
                            break
            i -= 1
        except mail.abort:
            mail.logout()
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(FROM_EMAIL, FROM_PWD)
            mail.select('inbox')
        except ValueError:
            break
        except Exception as e:
            print e
            i -= 1

# read_email_from_gmail()

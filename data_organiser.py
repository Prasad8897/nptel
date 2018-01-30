import re
from datetime import datetime, timedelta


def email_formating(email):
    email = email.lower()
    index = email.find('<')
    index2 = email.find('>')
    if index != -1:
        email = email[index + 1:index2]
    return email.strip('\t\r\n')


def subject_formatting(subject):
    if subject is None:
        return ""
    p = subject.split()
    for i in range(len(p)):
        if 'Re:' in p[i]:
            p[i] = p[i][3:]
        if 'Fwd:' in p[i]:
            p[i] = p[i][4:]
    subject = ' '.join(p)
    subject = subject.lstrip(' ')
    subject = subject.rstrip(' ')
    subject = list(subject)
    for i in range(len(subject)):
        if subject[i] == '"':
            subject[i] = "\\\""
        elif subject[i] == "'":
            subject[i] = "\\\'"
    return ''.join(subject)


def mailing_list_formating(mailing_list):
    notWanted = '\t\r\n'
    mailing_list = list(mailing_list)
    for i in range(len(mailing_list)):
        if mailing_list[i] in notWanted:
            mailing_list[i] = ''
    mailing_list = ''.join(mailing_list)
    matches = re.findall('list (.+);.*contact (.+).*', mailing_list)
    return matches[0]


def date_formatting(date):
    if ord(date[0]) >= 65:
        if len(date) == 36 or len(date) == 30:
            date = date[:5] + '0' + date[5:]
        date1 = datetime.strptime(date[5:25], '%d %b %Y %H:%M:%S')
        return date_to_IST(date1, date[26:31])
    else:
        if len(date) == 25:
            date = '0' + date
        date1 = datetime.strptime(date[0:20], '%d %b %Y %H:%M:%S')
        return date_to_IST(date1, date[21:26])


def date_to_IST(date, timezone):
    if timezone[0] == '-':
        date += timedelta(hours=int(timezone[1:3]), minutes=int(timezone[3:5]))
        date += timedelta(hours=5, minutes=30)
    if timezone[0] == '+':
        date -= timedelta(hours=int(timezone[1:3]), minutes=int(timezone[3:5]))
        date += timedelta(hours=5, minutes=30)
    return date


def email_set(data):
    e_set = []
    if not (data is None or data == ''):
        e_set = data.split(', ')
        for i in range(len(e_set)):
            e_set[i] = email_formating(e_set[i])
    return e_set


def body_formatting(message):
    if message is None:
        return ''
    lines = message.split('\n')
    editing = []
    for line in lines:
        line = line[:-1]
        if "On " in line and "wrote:" in line:
            break
        if line.find('>') == -1:
            editing.append(line)
    message = "\n".join(editing).rstrip('\n')
    index = message.find('You received this message because you')
    if index != -1:
        message = message[:index - 3]
    return message


def message_id_formatting(message):
    if message is not None:
        message = message[1:-1]
    return message

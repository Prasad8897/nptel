
Instructions for Setup

1) Install django-admin (Refernce-http://django-admin-tools.readthedocs.io/en/latest/installation.html)
2) Pull this Git Repository
3) Open file nptel-services/nptel-services/settings.py
4) Search for "DATABASES"
5) Create a database of your choice and write the name of the database in "NAME"
6) Change "USER", "PASS", "HOST", "PORT" according to your requirements.
7) In terminal, after the opening this folder run the commands 
   -> python manage.py makemigrations
   -> python manage.py migrate
   The above two commands will check for changes in data structure an apply them to the database
8) To start the server run the command
   -> python manage.py runserver 0.0.0.0:<port>
   The <port> refers to port number you want it run on


Instruction for Usage:

1) Start the server
   -> python manage.py runserver 0.0.0.0:<port>

2) GET request to "<domainName>:<port>/admin_login/<course id>" would give you meta data request for
	the course

3) GET request to "<domainName>/allEmails/<course id>" would return an array of dictionary in JSON
	format with each element as {'id':email_id, 'body':email_body}

4) PATCH request to "<domainName>/allEmails/<course id>" would edit the body of email which has the id 
	that has been sent. the email body of email with id = email_id would set to email_body
	data format -> {'id':email_id, 'body':email_body}

5) Delete request to "<domainName>/allEmails/<course id>" would delete the email body for the email
	which has id = email_id
	data format -> {'id':email_id}
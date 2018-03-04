
Instructions for Setup

1) Install django-admin (Refernce: http://django-admin-tools.readthedocs.io/en/latest/installation.html).
2) Pull this Git Repository.
3) Open file nptel-services/nptel-services/settings.py.
4) Search for "DATABASES".
5) Create a database of your choice and write the name of the database in "NAME".
6) Change "USER", "PASS", "HOST", "PORT" according to your requirements.
7) In terminal, after the opening this folder run the commands:
   -> python manage.py makemigrations
   -> python manage.py migrate
   The above two commands will check for changes in data structure an apply them to the database.
8) To start the server run the command
   -> python manage.py runserver 0.0.0.0:<port>
   The <port> refers to port number you want it run on.


Instruction on Request to be sent:

1) Start the server
   -> python manage.py runserver 0.0.0.0:<port>

2) GET request to "<domainName>:<port>/admin_login/<course id>" would give you meta data request for the course.

3) GET request to "<domainName>:<port>/allEmails/<course id>" would return an array of dictionary in JSON format with each element as {'id':email_id, 'body':email_body}

4) PATCH request to "<domainName>:<port>/allEmails/<course id>" would edit the body of email which has the id that has been sent. The email body of email with id = email_id would set to email_body.
	data format -> {'id':email_id, 'body':email_body}

5) Delete request to "<domainName>:<port>/allEmails/<course id>" would delete the email body for the email which has id = email_id.
	data format -> {'id':email_id}

6) Get request to "<domainName>:<port>/number_of_posts/<course id>/<num>/" would return the top "num" number of contributors of the course(emailId and number of posts by that user).
    Eg: num = 10 means it will return top 10 contributors of the discussion forum.

7) If a request cant be processed then a response with status 404 would be sent back with a JSON object with it containing the message of error.

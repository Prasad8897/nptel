"""nptel_services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from email_data.api import CourseMetaData, AllEmailData, mostAnsweredPeople
from mail_reader import read_email_from_gmail
# read_email_from_gmail()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_login/(?P<courseId>noc\d\d-[a-z][a-z]\d\d)',
        CourseMetaData),
    url(r'^allEmails/(?P<courseId>noc\d\d-[a-z][a-z]\d\d)', AllEmailData),
    url(r'^number_of_posts/(?P<courseId>noc\d\d-[a-z][a-z]\d\d)/(?P<count>\d+)/'
        , mostAnsweredPeople)
]

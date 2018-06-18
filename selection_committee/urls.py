"""JA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

app_name = 'selection_committee'
urlpatterns = [
    # start page with choice
    url(r'^$', views.selection_committee, name='selection_committee'),
    # registration form for youngling
    url(r'^youngling.html/$', views.youngling, name='youngling'),
    # before answering
    url(r'^genering.html/(?P<young_id>[0-9]+)/$', views.before_testing, name='before'),
    # younglings answering
    url(r'^answering.html/(?P<personal_test_id>[0-9]+)/$', views.testing, name='testing'),
    # jedies list
    url(r'^jedies.html/$', views.jedies, name='jedies'),
    # candidates list
    url(r'j_y_choosing.html/(?P<selected_jedi_id>[0-9]+)/$', views.j_y_choosing, name='j_y_choosing'),
]

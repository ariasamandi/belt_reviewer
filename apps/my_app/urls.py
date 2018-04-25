from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^books/add$', views.book_add),
    url(r'^books/add/process$', views.book_add_process),
    url(r'^books/(?P<book_id>\d+)$', views.review),
    url(r'^logout$', views.logout), 
          # This line has changed!
]

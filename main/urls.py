from django.conf.urls import url

from main.views import UserView, UserDetailView, \
    HospitalListView, HospitalDetailView, \
    VisitListView, VisitDetailView, UserVisitView

urlpatterns = [
    url(r'^user/$', UserView.as_view()),
    url(r'^user/details/$', UserDetailView.as_view()),
    url(r'^user/visits/$', UserVisitView.as_view()),
    url(r'^hospital/$', HospitalListView.as_view()),
    url(r'^hospital/(?P<pk>[0-9]+)/$', HospitalDetailView.as_view()),
    url(r'^visit/$', VisitListView.as_view()),
    url(r'^visit/(?P<pk>[0-9]+)/$', VisitDetailView.as_view()),
]

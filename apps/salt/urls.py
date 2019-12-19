from rest_framework.routers import DefaultRouter
from .views import ListKeyView, AddKeyView, MinonStatusViewSet, RejectKeyView, DeleteKeyView, JobsHistoryView, \
    JobsManagerView
from django.conf.urls import include, url

salt_router = DefaultRouter()
salt_router.register(r'minion/status', MinonStatusViewSet, base_name="minion_status")

urlpatterns = [
    url(r'^', include(salt_router.urls)),
    # key管理
    url(r'^get_key/$', ListKeyView.as_view()),
    url(r'^add_key/$', AddKeyView.as_view()),
    url(r'^reject_key/$', RejectKeyView.as_view()),
    url(r'^delete_key/$', DeleteKeyView.as_view()),

    # Job管理
    url(r'^jobs_history/$', JobsHistoryView.as_view()),
    url(r'^jobs_manager/$', JobsManagerView.as_view()),
]

from rest_framework.routers import DefaultRouter
from .views import ListKeyView, AddKeyView, AclViewSet, SlsViewSet, MdlViewSet, MinonStatusViewSet, RejectKeyView, DeleteKeyView, JobsHistoryView, \
    JobsActiveView, JobsKillView, JobsScheduleView, JobsDetailView, GrainsView, PillarView
from django.conf.urls import include, url

salt_router = DefaultRouter()
salt_router.register(r'minion/status', MinonStatusViewSet, base_name="minion_status")
salt_router.register(r'acl', AclViewSet, base_name="salt_acl")
salt_router.register(r'sls', SlsViewSet, base_name="salt_sls")
salt_router.register(r'mdl', MdlViewSet, base_name="salt_mdl")
salt_router.register(r'arg', MdlViewSet, base_name="salt_arg")

urlpatterns = [
    url(r'^', include(salt_router.urls)),
    # key管理
    url(r'^key/$', ListKeyView.as_view()),
    url(r'^key/add/$', AddKeyView.as_view()),
    url(r'^key/reject/$', RejectKeyView.as_view()),
    url(r'^key/delete/$', DeleteKeyView.as_view()),

    # Job管理
    url(r'^jobs/history/$', JobsHistoryView.as_view()),
    url(r'^jobs/active/$', JobsActiveView.as_view()),
    url(r'^jobs/detail/$', JobsDetailView.as_view()),
    url(r'^jobs/kill/$', JobsKillView.as_view()),
    url(r'^jobs/schedule/$', JobsScheduleView.as_view()),

    # 数据管理
    url(r'^minion/grains/$', GrainsView.as_view()),
    url(r'^minion/pillar/$', PillarView.as_view()),
]

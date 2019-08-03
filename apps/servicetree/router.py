from rest_framework.routers import DefaultRouter
from .views import NodeInfoManageViewSet


user_router = DefaultRouter()
pms_router.register("nodeinfo", NodeInfoViewSet, base_name='nodeinfo')
pms_router.register("nodeinfomanage", NodeInfoManageViewSet, base_name='nodeinfomanage')

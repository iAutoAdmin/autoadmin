from rest_framework.routers import DefaultRouter
from .views import NodeInfoManageViewSet, NodeInfoViewSet


servicetree_router = DefaultRouter()
servicetree_router.register("nodeinfo", NodeInfoViewSet, base_name='nodeinfo')
servicetree_router.register("nodeinfomanage", NodeInfoManageViewSet, base_name='nodeinfomanage')
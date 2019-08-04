from rest_framework.routers import DefaultRouter
from .views import NodeInfoManageViewSet, NodeInfoViewSet


servicetree_router = DefaultRouter()
servicetree_router.register("servicetree/node", NodeInfoViewSet, base_name='node')
servicetree_router.register("servicetree/nodemanage", NodeInfoManageViewSet, base_name='nodemanage')
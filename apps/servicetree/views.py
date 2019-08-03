from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins, response, status, permissions
from .models import NodeInfo
from .serializers import NodeInfoSerializer
from rest_framework.pagination import PageNumberPagination
from .filter import NodeinfoFilter


class NodeInfoViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    返回指定Node信息
    list:
    返回Node列表
    update:
    更新Node信息
    destroy:
    删除Node记录
    create:
    创建Node资源
    partial_update:
    更新部分字段
    """
    queryset = NodeInfo.objects.all()
    serializer_class = NodeInfoSerializer
    filter_class = NodeinfoFilter
    filter_fields = ("node_name")


class NodeInfoManageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Nodeinfo信息展示
    """
    pagination_class = PageNumberPagination
    queryset = NodeInfo.objects.all()

    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        data = self.get_nodeinfo()
        return response.Response(data)

    def get_nodeinfo(self):
        ret = []

        for obj in self.queryset.filter(pid=0):
            # print(obj.id, obj.node_name)
            node = self.get_node(obj)
            node["children"] = self.get_children(obj.id)
            ret.append(node)
        return ret

    def get_children(self, pid):
        ret = []
        nodes = NodeInfo.objects.filter(pid=pid)
        if len(nodes) == 0:
            return ret

        for child in NodeInfo.objects.filter(pid=pid):
            node = self.get_node(child)
            ret.append(node)
            children = self.get_children(child.id)
            if children:  # 如果存在子节点则加入列表
                node["children"] = children
            elif len(children) == 0:
                del node["children"]  # 删除node字典中children字段
        return ret

    def get_node(self, product_obj):
        node = {}
        node["id"] = product_obj.id
        node["label"] = product_obj.node_name
        node["pid"] = product_obj.pid
        node["path_node"] = product_obj.path_node
        node["children"] = []
        return node

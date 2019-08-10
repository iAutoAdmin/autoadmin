from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins, response, status, permissions
from .models import Node
from .serializers import NodeSerializer


class NodeViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    retrieve:
    返回指定Node信息
    update:
    更新Node信息
    destroy:
    删除Node记录
    create:
    创建Node资源
    partial_update:
    更新部分字段
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer



class ServiceTreeViewSet(viewsets.GenericViewSet):
    """
    list:
    返回所有服务树列表信息
    """

    def list(self, request, *args, **kwargs):
        data = self.get_tree()
        return response.Response(data)

    def get_tree(self):
        return self.get_child_node(0)

    def get_child_node(self, pid):
        ret = []
        for obj in Node.objects.filter(pid__exact=pid):
            node = self.get_node(obj)
            node["children"] = self.get_child_node(obj.id)
            ret.append(node)
        return ret

    def get_node(self, obj):
        node = {}
        node["id"] = obj.id
        node["label"] = obj.name
        node["pid"] = obj.pid
        return node

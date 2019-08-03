import django_filters
from servicetree.models import NodeInfo


class NodeinfoFilter(django_filters.FilterSet):
    '''
    NodeName 搜索类
    '''
    node_name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤node节点名称')

    class Meta:
        model = NodeInfo
        fields = ['node_name']

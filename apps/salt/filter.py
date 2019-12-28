import django_filters
from .models import SaltArg, SaltMdl, SaltSls, SaltAcl


class SaltSlsFilter(django_filters.FilterSet):
    """
    搜索状态文件名称
    """
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤状态文件名称')

    class Meta:
        model = SaltSls
        fields = ['name']


class SaltArgFilter(django_filters.FilterSet):
    """
    搜索模块参数
    """
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤参数名称')

    class Meta:
        model = SaltArg
        fields = ['name']


class SaltMdlFilter(django_filters.FilterSet):
    """
    搜索模块名称
    """
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤模块名称')

    class Meta:
        model = SaltMdl
        fields = ['name']


class SaltAclFilter(django_filters.FilterSet):
    """
    搜索模块名称
    """
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤ACL名称')

    class Meta:
        model = SaltAcl
        fields = ['name', 'deny']
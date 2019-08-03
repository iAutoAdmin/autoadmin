from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegSerializer
from .filters import UserFilter

User = get_user_model()



class UserRegViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    create:
    创建用户

    update:
    修改密码
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer


class UserInfoViewset(viewsets.ViewSet):
    """
    获取当前登陆的用户信息
    """
    def list(self, request, *args, **kwargs):
        data = {
            "username": self.request.user.username,
            "name": self.request.user.name,
        }
        return Response(data)


class UsersViewset(viewsets.ModelViewSet):
    """
    retrieve:
    获取用户信息
    list:
    获取用户列表
    update:
    更新用户信息
    delete:
    删除用户
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_fields = ("username",)

    def get_queryset(self):
        queryset = super(UsersViewset, self).get_queryset()
        queryset = queryset.order_by("id")
        return queryset
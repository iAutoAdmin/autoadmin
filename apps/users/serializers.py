from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    username    = serializers.CharField(required=False, read_only=False, max_length=32, label="用户名", help_text="用户名")
    name        = serializers.CharField(required=False, read_only=False, label="姓名", help_text="姓名")
    is_active   = serializers.BooleanField(required=False, read_only=True, label="登陆状态", default=True, help_text="登陆状态")
    email       = serializers.CharField(read_only=True, help_text="联系邮箱")
    last_login  = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="上次登录时间")
    phone       = serializers.CharField(required=False, max_length=11, min_length=11, allow_null=True, help_text="手机号",
                                        error_messages={"max_length":"手机号错误","min_length":"手机号错误"},
                                        )
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            return serializers.ValidationError("用户已存在")
        except User.DoesNotExist:
            return username

    class Meta:
        model = User
        fields = ("id", "username", "name", "phone", "email", "is_active","last_login")

class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列化类
    """
    id       = serializers.IntegerField(read_only=True)
    name     = serializers.CharField(max_length=32, label="姓名", help_text="用户姓名，中文姓名")
    username = serializers.CharField(max_length=32, label="用户名", help_text="用户名，用户登陆名")
    password = serializers.CharField(style={"input_type": "password"}, label="密码", write_only=True, help_text="密码")
    phone    = serializers.CharField(max_length=11, min_length=11, label="手机号", required=False,
                                     allow_null=True, allow_blank=True, help_text="手机号")

    def create(self, validated_data):
        validated_data["is_active"] = False
        instance = super(UserRegSerializer, self).create(validated_data=validated_data)
        instance.email = "{}{}".format(instance.username, settings.DOMAIN)

        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password =  validated_data.get("password", None)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ("username", "password", "name", "id", "phone")
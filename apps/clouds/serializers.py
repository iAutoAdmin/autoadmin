from rest_framework import serializers
from clouds.models import Instances, Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    """
    厂商列化类
    """

    class Meta:
        model = Manufacturer
        fields = '__all__'


class InstanceSerializer(serializers.ModelSerializer):
    """
    主机序列化类
    """

    class Meta:
        model = Instances
        fields = '__all__'

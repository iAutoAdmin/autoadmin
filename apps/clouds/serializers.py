from rest_framework import serializers
from clouds.models import CloudHost


class HostInfoSerializer(serializers.ModelSerializer):
    """
    主机信息
    """

    class Meta:
        model = CloudHost
        fields = '__all__'

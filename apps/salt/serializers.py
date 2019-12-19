from rest_framework import serializers
from .models import Minions_status


class MinionStausSerializer(serializers.Serializer):
    """
    AppName序列化类
    """
    minion_id = serializers.CharField(max_length=32, label="主机名", help_text="主机名", read_only=True)
    minion_status = serializers.CharField(required=True, max_length=32, label="minion状态", help_text="minion状态")

    class Meta:
        model = Minions_status
        fields = '__all__'

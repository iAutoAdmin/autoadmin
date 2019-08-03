from rest_framework import serializers
from .models import NodeInfo

class NodeInfoSerializer(serializers.ModelSerializer):
    """
    NodeInfo序列化类
    """

    def to_representation(self, instance):
        ret = super(NodeInfoSerializer, self).to_representation(instance)
        return ret

    def validate_pid(self, pid):
        """
        Check that the per_pid is or not parent
        """
        if pid > 0:
            try:
                node_obj = NodeInfo.objects.get(pk=pid)
                if node_obj.pid != 0 or node_obj:
                    # return serializers.ValidationError("上级菜单错误")
                    return pid
            except NodeInfo.DoesNotExist:
                return serializers.ValidationError("上级菜单不存在")
            return pid
        else:
            return 0

    def update(self, instance, validated_data):
        instance.node_name = validated_data.get("node_name", instance.node_name)
        instance.pid = validated_data.get("pid", instance.pid)
        instance.path_node = validated_data.get("path_node", instance.path_node)
        instance.save()
        return instance

    class Meta:
        model = NodeInfo
        fields = ('id', 'node_name', 'pid', 'path_node')
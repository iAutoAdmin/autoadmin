from django.db import models
from django.contrib.auth.models import Group


# Create your models here.
class NodeInfo(models.Model):
    node_name = models.CharField("节点名称", max_length=32, db_index=True, help_text="service名称")
    pid = models.IntegerField("节点pid", db_index=True, help_text="pid")
    path_node = models.CharField("节点中文path", max_length=32, db_index=True, help_text="node中文path")
    groups = models.ManyToManyField(Group, verbose_name="用户组关联节点", related_name="node_group", help_text="用户组关联节点")

    def __str__(self):
        return self.node_name

    class Meta:
        db_table = "pms_node"
        ordering = ["id"]

from django.db import models
from django.contrib.auth.models import Group
from orgs.models import Organization


# Create your models here.
class Node(models.Model):
    name = models.CharField("节点名称", max_length=32, db_index=True, help_text="service名称")
    pid = models.IntegerField("节点pid", db_index=True, help_text="pid")
    path = models.CharField("节点中文path", max_length=32, db_index=True, help_text="node中文path")
    rd = models.CharField("业务负责人", max_length=255, null=True, blank=True, help_text="业务负责人")
    op = models.CharField("运维负责人", max_length=255, null=True, blank=True, help_text="运维负责人")
    groups = models.ManyToManyField(Organization, verbose_name="用户组关联节点", related_name="node_group",
                                    help_text="用户组关联节点")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "servicetree_node"
        ordering = ["id"]

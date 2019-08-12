from django.db import models
from django.contrib.auth.models import Group


class Manufacturer(models.Model):
    vendor_name = models.CharField("厂商名称", max_length=32, db_index=True, help_text="厂商名称")
    remark = models.CharField("备注", max_length=300, null=True, blank=True, help_text="备注")

    def __str__(self):
        return self.vendor_name

    class Meta:
        db_table = 'clouds_manufacturer'
        ordering = ["id"]


class Instances(models.Model):
    created_at = models.DateTimeField("创建时间", help_text="创建时间")
    updated_at = models.DateTimeField("更新时间", auto_now=True, help_text="更新时间")
    deleted_at = models.DateTimeField("删除时间", help_text="删除时间")
    cloud_id = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="云厂商", help_text="云厂商")
    resource_id = models.CharField("资源id", max_length=255, default=None, unique=True, help_text="资源id")
    region_id = models.CharField("地域名称", max_length=255, default=None, help_text="地域名称")
    instance_id = models.CharField("实例ID", max_length=255,  default=None, help_text="实例ID")
    instance_name = models.CharField("实例名称", max_length=255,  default=None, help_text="实例名称")
    os_name = models.CharField("操作系统", max_length=64, default=None, help_text="操作系统")
    zone_id = models.CharField("可用区", max_length=255, default=None, help_text="可用区")
    public_ip = models.CharField("公网ip", max_length=64, db_index=True, null=True, help_text="公网ip")
    private_ip = models.CharField("私有ip", max_length=64, db_index=True, null=True, help_text="私有ip")
    e_ip = models.CharField("弹性ip", max_length=64, null=True, help_text="弹性ip")
    instance_status = models.CharField("实例状态", max_length=64, db_index=True, null=True, help_text="实例状态")
    vpc_id = models.CharField("专有网络", max_length=64, null=True, help_text="专有网络")
    cpu_num = models.CharField("CPU数", max_length=64, default=1, help_text="CPU数")
    memory_size = models.CharField("内存大小", max_length=64, default=1024, help_text="内存大小")
    instance_type = models.CharField("实例类型", max_length=64, default=None, help_text="实例类型")
    band_width_out = models.CharField("网络出口带宽", max_length=64, null=True, blank=True, help_text="网络出口带宽")
    instance_charge_type = models.CharField("付费类型", max_length=64, default="包年包月", help_text="付费类型")
    host_name = models.CharField("主机名称", max_length=64, default=None, help_text="主机名称")
    gpu = models.CharField("GPU", max_length=64,  default=None, help_text="GPU")
    create_time = models.CharField("创建时间", max_length=64,  help_text="创建时间")
    expire_time = models.CharField("过期时间", max_length=64, help_text="过期时间")
    status = models.IntegerField(default=1, null=False, verbose_name=u'状态,1:存在,2:已删除')

    def __str__(self):
        return "{}".format(self.host_name)

    class Meta:
        db_table = "clouds_instance"
        ordering = ["id"]

from django.db import models
from django.contrib.auth.models import Group


# Create your models here.
class CloudHost(models.Model):
    CLOUDS_NAME = (
        (1, u'阿里云'),
        (2, u'腾讯云'),
        (3, u'AWS'),
    )
    created_at = models.DateTimeField("创建时间", help_text="创建时间")
    updated_at = models.DateTimeField("更新时间", auto_now=True, help_text="更新时间")
    deleted_at = models.DateTimeField("删除时间", help_text="删除时间")
    cloud_id = models.CharField("云厂商", max_length=255, choices=CLOUDS_NAME, default=1, help_text="云厂商")
    resource_id = models.CharField("资源id", max_length=255, default=None, unique=True, help_text="资源id")
    gpu = models.IntegerField("GPU", max_length=12, default=None, help_text="GPU")
    instance_id = models.CharField("实例ID", max_length=255,  default=None, help_text="实例ID")
    instance_name = models.CharField("实例名称", max_length=255,  default=None, help_text="实例名称")
    instance_status = models.CharField("实例状态", max_length=64, db_index=True, default=None, help_text="实例状态")
    instance_type = models.CharField("实例类型", max_length=64, default=None, help_text="实例类型")
    instance_network_type_code = models.CharField("网络类型", max_length=64, default="vpc", help_text="网络类型")
    instance_charge_type_code = models.CharField("付费类型", max_length=64, default=None, help_text="付费类型")
    internet_charge_type_code = models.CharField("弹性IP付费类型", max_length=64, default=None, help_text="弹性IP付费类型")
    band_width_out = models.CharField("网络出口带宽", max_length=64, default=None, help_text="网络出口带宽")
    region_id = models.CharField("地域名称", max_length=255, default=None, help_text="地域名称")
    zone_info = models.CharField("可用区", max_length=255, default=None, help_text="可用区")
    cpu_num = models.CharField("CPU数", max_length=64, default=1, help_text="CPU数")
    memory_size = models.CharField("内存大小", max_length=64, default=1024, help_text="内存大小")
    system_disk_size = models.CharField("系统盘大小", max_length=64, default=None, help_text="系统盘大小")
    system_disk_type = models.CharField("系统盘类型", max_length=64, default=None, help_text="系统盘类型")
    disk_size = models.CharField("数据盘大小", max_length=64, default=None, help_text="数据盘大小")
    disk_type = models.CharField("数据盘类型", max_length=64, default=None, help_text="数据盘类型")
    vpc_id = models.CharField("专有网络", max_length=64, default=None, help_text="专有网络")
    public_ip = models.CharField("公网ip", max_length=64, db_index=True, default=None, help_text="公网ip")
    private_ip = models.CharField("私有ip", max_length=64, db_index=True, default=None, help_text="私有ip")
    e_ip = models.CharField("弹性ip", max_length=64, default=None, help_text="弹性ip")
    os = models.CharField("操作系统", max_length=64, default=None, help_text="操作系统")
    host_name = models.CharField("主机名称", max_length=64, default=None, help_text="主机名称")
    create_time = models.CharField("创建时间",  help_text="创建时间")
    expire_time = models.CharField("过期时间", help_text="过期时间")
    image_id = models.CharField("系统镜像id", max_length=64, default=None, help_text="系统镜像id")

    def __str__(self):
        return "{}[{}]".format(self.host_name, self.public_ip)

    class Meta:
        db_table = "clouds_hostinfo"
        ordering = ["id"]

#!/usr/bin/env python
# coding=utf-8
import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoadmin.settings")
django.setup()

import hashlib
from clouds.aliyun.common import ALiYun
from clouds.models import Instances, Manufacturer


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


def sync_instances(manufacturer):
    """
    在同步主机之前还需对比阿里云侧和本地机器，来修改status的状态，用来标记已删除或存在
    :param manufacturer: ALY, TXY, AWS
    :return:
    """
    ali = ALiYun()
    instances = ali.get_ecs()
    for instance in instances:
        for manfu_obj in Manufacturer.objects.all():
            if manfu_obj.vendor_name == manufacturer:
                try:
                    resource_id = md5(instance.get('InstanceId'))
                    host_obj = Instances.objects.get(resource_id=resource_id)
                    host_obj.resource_id = md5(instance.get('InstanceId'))
                    host_obj.region_id = instance.get('RegionId')
                    host_obj.cloud_id_id = manfu_obj.id
                    host_obj.instance_id = instance.get('InstanceId')
                    host_obj.instance_name = instance.get('InstanceName')
                    host_obj.os_name = instance.get('OSName')
                    host_obj.zone_id = instance.get("ZoneId")
                    host_obj.public_ip = instance.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress', "")[
                        0]
                    host_obj.private_ip = instance.get('PublicIpAddress').get('IpAddress', "")[0]
                    host_obj.e_ip = instance.get("EipAddress", "")
                    host_obj.instance_status = instance.get('Status')
                    host_obj.vpc_id = instance.get('InstanceNetworkType')
                    host_obj.cpu_num = instance.get('Cpu')
                    host_obj.memory_size = instance.get('Memory')
                    host_obj.ioOptimized = instance.get('IoOptimized')
                    host_obj.instance_type = instance.get('InstanceType')
                    host_obj.band_width_out = instance.get('InternetMaxBandwidthOut')
                    host_obj.instance_charge_type = instance.get('InstanceChargeType')
                    host_obj.host_name = instance.get('HostName')
                    host_obj.gpu = instance.get('GPUAmount')
                    host_obj.create_time = instance.get('CreationTime')
                    host_obj.expire_time = instance.get('ExpiredTime')
                    host_obj.save()

                except Instances.DoesNotExist:
                    Instances.objects.create(resource_id=md5(instance.get('InstanceId')),
                                             region_id=instance.get('RegionId'),
                                             cloud_id_id=manfu_obj.id,
                                             instance_name=instance.get('InstanceName'),
                                             os_name=instance.get('OSName'),
                                             zone_id=instance.get("ZoneId"),
                                             instance_id=instance.get('InstanceId'),
                                             public_ip=
                                             instance.get('VpcAttributes').get('PrivateIpAddress').get(
                                                 'IpAddress', "")[0],
                                             private_ip=instance.get('PublicIpAddress').get('IpAddress', "")[0],
                                             e_ip=instance.get("EipAddress", ""),
                                             instance_status=instance.get('Status'),
                                             vpc_id=instance.get('InstanceNetworkType'),
                                             cpu_num=instance.get('Cpu'),
                                             memory_size=instance.get('Memory'),
                                             ioOptimized=instance.get('IoOptimized'),
                                             instance_type=instance.get('InstanceType'),
                                             band_width_out=instance.get('InternetMaxBandwidthOut'),
                                             instance_charge_type=instance.get('InstanceChargeType'),
                                             host_name=instance.get('HostName'),
                                             gpu=instance.get('GPUAmount'),
                                             create_time=instance.get('CreationTime'),
                                             expire_time=instance.get('ExpiredTime')
                                             )


if __name__ == '__main__':
    sync_instances("ALY")

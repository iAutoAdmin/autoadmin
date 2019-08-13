#!/usr/bin/env python
# coding=utf-8

import hashlib
import os
import django
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoadmin.settings")
django.setup()
from clouds.aliyun.common import ALiYun
from clouds.models import Instances, Manufacturer


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


def rsync_instances():
    ali = ALiYun()
    instances = ali.get_ecs()

    for instance in instances:
        instance_obj = Instances()
        for manfu_obj in Manufacturer.objects.all():
            if manfu_obj.vendor_name == "阿里云":
                instance_obj.resource_id = md5(instance.get('InstanceId'))
                instance_obj.region_id = instance.get('RegionId')
                instance_obj.cloud_id_id = manfu_obj.id
                instance_obj.instance_id = instance.get('InstanceId')
                instance_obj.instance_name = instance.get('InstanceName')
                instance_obj.os_name = instance.get('OSName')
                instance_obj.zone_id = instance.get("ZoneId")
                instance_obj.public_ip = instance.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress', "")[0]
                instance_obj.private_ip = instance.get('PublicIpAddress').get('IpAddress', "")[0]
                instance_obj.e_ip = instance.get("EipAddress").get('IpAddress', "")[0]
                instance_obj.instance_status = instance.get('Status')
                instance_obj.vpc_id = instance.get('InstanceNetworkType')
                instance_obj.cpu_num = instance.get('Cpu')
                instance_obj.memory_size = instance.get('Memory')
                instance_obj.ioOptimized = instance.get('IoOptimized')
                instance_obj.instance_type = instance.get('InstanceType')
                instance_obj.band_width_out = instance.get('InternetMaxBandwidthOut')
                instance_obj.instance_charge_type = instance.get('InstanceChargeType')
                instance_obj.host_name = instance.get('HostName')
                instance_obj.gpu = instance.get('GPUAmount')
                instance_obj.create_time = instance.get('CreationTime')
                instance_obj.expire_time = instance.get('ExpiredTime')
                instance_obj.save()
        # print(instance.get('CreationTime'))

if __name__ == '__main__':
    rsync_instances()

#!/usr/bin/env python
# coding=utf-8

import hashlib
import os
import django
import sys
from clouds.aliyun.common import ALiYun
from clouds.models import Instances
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoadmin.settings")
django.setup()


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


def rsync_instances():
    ali = ALiYun()
    instances = ali.get_ecs()
    for instance in instances:
        instance_obj = Instances()
        instance_obj.resource_id = md5(instance.get('InstanceId'))
        instance_obj.region_id = instance.get('RegionId')
        instance_obj.instance_id = instance.get('InstanceId')
        instance_obj.instance_name = instance.get('InstanceName')
        instance_obj.os_name = instance.get('OSName')
        instance_obj.zone_id = instance.get("ZoneId")
        instance_obj.public_ip = instance.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress', "")[0]
        instance_obj.private_ip = instance.get('PublicIpAddress').get('IpAddress', "")[0]
        instance_obj.e_ip = instance.get("E_IP", "")
        instance_obj.instance_status = instance.get('Status')
        instance_obj.vpc_id = instance.get('InstanceNetworkType')
        instance_obj.cpu_num = instance.get('Cpu')
        instance_obj.memory_size = instance.get('Memory')
        instance_obj.instance_type = instance.get('IoOptimized')
        instance_obj.band_width_out = instance.get('InternetMaxBandwidthOut')
        instance_obj.instance_charge_type = instance.get('InstanceChargeType')
        instance_obj.host_name = instance.get('HostName')
        instance_obj.gpu = instance.get('GPUAmount')
        instance.create_time = instance.get('CreationTime')
        instance_obj.expire_time = instance.get('ExpiredTime')


if __name__ == '__main__':
    rsync_instances()

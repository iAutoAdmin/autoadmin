#!/usr/bin/env python
# coding=utf-8

import hashlib
import datetime
from clouds.aliyun.common import ALiYun


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


def rsync_instances():
    starttime = datetime.datetime.now()
    ali = ALiYun()
    instances = ali.get_ecs()
    for instance in instances:
        print(instance.get('InstanceId'))
        print(md5(instance.get('InstanceId')))
        print(instance.get('InstanceName'))
        print(instance.get('HostName'))
        RegionId = instance.get('RegionId')
        print(RegionId)
        print(instance.get("ZoneId"))
        zones = ali.get_zone(RegionId)
        for zone in zones:
            if instance.get("ZoneId") == zone["ZoneId"]:
                print(zone["LocalName"])
        disks = ali.get_instance_disk_info(RegionId, instance.get("ZoneId"), instance.get('InstanceId'))
        for disk in disks:
            print(disk.get('Size'))
            print(disk.get('Type'))
        print(instance['OSName'])
        print(instance.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[0])
        print(instance.get('PublicIpAddress').get('IpAddress')[0], "")
        print(instance.get('Status'))
        print(instance.get('InstanceNetworkType'))
        print(instance.get('Cpu'))
        print(instance.get('Memory') / 1024)
        print(instance.get('IoOptimized'))
        print(instance.get('GPUAmount'))
        print(instance.get('InternetMaxBandwidthOut'))
        print(instance.get('InstanceType'))
        print(instance.get('InstanceChargeType'))
        print(instance.get('CreationTime'))
        print(instance.get('ExpiredTime'))
    endtime = datetime.datetime.now()
    print(endtime - starttime)


if __name__ == '__main__':
    # str = "aly" + "i-2ze4wxcyl324952q8m7b"
    # print(md5(str))
    rsync_instances()

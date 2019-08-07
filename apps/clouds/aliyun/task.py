#!/usr/bin/env python
# coding=utf-8

import hashlib
from clouds.aliyun.common import ALiYun


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


def rsync_instances():
    ali = ALiYun()
    instances = ali.get_ecs()
    for instance in instances:
        print(md5(instance['InstanceId']))
        print(instance['InstanceName'])
        regionid = instance.get("ZoneId").split("-")[0]+"-" + instance.get("ZoneId").split("-")[1]
        zones = ali.get_zone(regionid)
        for i in zones:
            if instance.get("ZoneId") == i["ZoneId"]:
                print(i["LocalName"])
        print(instance['VpcAttributes']['PrivateIpAddress']['IpAddress'][0])
        print(instance.get('PublicIpAddress').get('IpAddress')[0])
        print(instance['InstanceNetworkType'])
        print(instance['InstanceType'])
        print(instance['Cpu'])
        print(instance['Memory']/1024)
        print(instance['Status'])
        print(instance['ExpiredTime'])
        print(str(instance['InternetMaxBandwidthOut']))




if __name__ == '__main__':
    # str = "aly" + "i-2ze4wxcyl324952q8m7b"
    # print(md5(str))
    rsync_instances()

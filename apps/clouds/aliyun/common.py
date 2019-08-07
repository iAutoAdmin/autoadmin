#!/usr/bin/env python
# coding=utf-8
import json
from autoadmin.settings import accessKeyId, accessSecret
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeZonesRequest import DescribeZonesRequest
from aliyunsdkecs.request.v20140526.DescribeAvailableResourceRequest import DescribeAvailableResourceRequest
from aliyunsdkslb.request.v20140515.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancerAttributeRequest import DescribeLoadBalancerAttributeRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceTypesRequest import DescribeInstanceTypesRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceTypeFamiliesRequest import DescribeInstanceTypeFamiliesRequest

class ALiYun(object):
    def __init__(self):
        self.accessKeyId = accessKeyId
        self.accessSecret = accessSecret

    def get_zone(self, RegionId):
        """
        查询RegionId下的可用区，根据ZoneId判断LocalName
        :param RegionId:
        :return:
        """
        client = AcsClient(self.accessKeyId, self.accessSecret, RegionId)
        request = DescribeZonesRequest()
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        res = str(response, encoding='utf-8')
        return json.loads(res).get("Zones").get("Zone")

    def get_regions(self):
        """
        获取所有地域regionId
        :return:
        """
        regions = []
        client = AcsClient(self.accessKeyId, self.accessSecret)
        request = DescribeRegionsRequest()
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        res = (str(response, encoding='utf-8'))
        for region in (eval(res)['Regions']['Region']):
            regions.append(region['RegionId'])
        return regions

    def get_slb(self):
        """
        获取所有地域下slb负载均衡实例
        :return:
        """
        balancers = []
        regionids = self.get_regions()
        try:
            for rid in regionids:
                client = AcsClient(self.accessKeyId, self.accessSecret, rid, connect_timeout=30)
                request = DescribeLoadBalancersRequest()
                request.set_accept_format('json')
                response = client.do_action_with_exception(request)
                res = eval(str(response, encoding='utf-8'))
                balancers += res.get("LoadBalancers").get("LoadBalancer")
            return balancers
        except Exception as ex:
            print(ex)

    def get_slb_detail(self, loadbalancerid, regionid):
        """
        返回lb详细信息
        :param loadbalancerid: lb-2zeqx4f9qglel963dmdzv
        :param regionid: cn-beijing
        :return:
        """
        client = AcsClient(self.accessKeyId, self.accessSecret, regionid)
        request = DescribeLoadBalancerAttributeRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(loadbalancerid)
        response = client.do_action_with_exception(request)
        return eval(str(response, encoding='utf-8'))

    def get_ecs(self):
        """
        获取所有区域ECS信息
        :return:
        """
        instances = []
        regionids = self.get_regions()
        try:
            for rid in regionids:
                client = AcsClient(self.accessKeyId, self.accessSecret, rid, connect_timeout=30)
                request = DescribeInstancesRequest()
                request.set_accept_format('json')
                response = client.do_action_with_exception(request)
                # print(str(response, encoding='utf-8'))
                res = json.loads(str(response, encoding='utf-8'))
                instances += res['Instances']['Instance']
            return instances
        except Exception as ex:
            return ex

    def get_instancetype(self, RegionId):
        """
        查看ECS实例规格信息
        :param RegionId:
        :return:
        """
        client = AcsClient(self.accessKeyId, self.accessSecret, RegionId)
        request = DescribeInstanceTypesRequest()
        request.set_accept_format('json')
        request.set_InstanceTypeFamily("ecs.t5")
        response = client.do_action_with_exception(request)
        res = str(response, encoding='utf-8')
        return json.loads(res).get("InstanceTypes").get("InstanceType")

if __name__ == '__main__':
    ali = ALiYun()
    # ali.get_regions()
    # print(ali.get_slb())
    # print(ali.get_slb_detail("lb-2zeqx4f9qglel963dmdzv", "cn-beijing"))
    # print(ali.get_ecs())
    # res = ali.get_zone("cn-beijing")
    # ali.get_instancetype()
    # res = ali.get_instancetype("cn-beijing")
    # for i in res:
    #     print(i["CpuCoreCount"],i["MemorySize"])
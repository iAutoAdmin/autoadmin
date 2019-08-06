#!/usr/bin/env python
# coding=utf-8
import json
from autoadmin.settings import accessKeyId, accessSecret
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkslb.request.v20140515.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancerAttributeRequest import DescribeLoadBalancerAttributeRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest


class ALiYun(object):
    def __init__(self):
        self.accessKeyId = accessKeyId
        self.accessSecret = accessSecret

    def get_regions(self):
        """
        获取所有可用区regionId
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
                res = json.loads(str(response, encoding='utf-8'))
                instances += res['Instances']['Instance']
            return instances
        except Exception as ex:
            return ex


if __name__ == '__main__':
    ali = ALiYun()
    # ali.get_regions()
    # print(ali.get_slb())
    # print(ali.get_slb_detail("lb-2zeqx4f9qglel963dmdzv", "cn-beijing"))
    print(ali.get_ecs())

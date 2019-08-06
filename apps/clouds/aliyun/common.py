#!/usr/bin/env python
# coding=utf-8
import json
from autoadmin.settings import accessKeyId, accessSecret
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkslb.request.v20140515.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest

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
        regions = self.get_regions()
        try:
            for region in regions:
                client = AcsClient(self.accessKeyId, self.accessSecret, region, connect_timeout=30)
                request = DescribeLoadBalancersRequest()
                request.set_accept_format('json')
                response = client.do_action_with_exception(request)
                res = eval(str(response, encoding='utf-8'))
                # print(res.get("LoadBalancers").get("LoadBalancer"))
                balancers += res.get("LoadBalancers").get("LoadBalancer")
            return balancers
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    ali = ALiYun()
    # ali.get_regions()
    print(ali.get_slb())

from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from salt.api import SaltAPI
from salt.serializers import MinionStausSerializer, AclSerializer, ArgSerializer, SlsSerializer, MdlSerializer
from .models import MinionsStatus, SaltAcl, SaltMdl, SaltSls, SaltArg
from .filter import SaltAclFilter, SaltArgFilter, SaltMdlFilter, SaltSlsFilter, MinionStatusFilter
from django.http import Http404
from rest_framework.schemas import AutoSchema
from rest_framework.exceptions import APIException
import logging
import json
import coreapi
import re

logger = logging.getLogger('default')


class MinonStatusViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    list: 查看salt-minion的状态
    """
    serializer_class = MinionStausSerializer
    queryset = MinionsStatus.objects.all()
    filter_class = MinionStatusFilter
    search_fields = ['minion_id', 'minion_status']


class AclViewSet(viewsets.ModelViewSet):
    """
    list: 获取ACL列表名称
    create: 添加salt拒绝权限名称
    retrieve: 查看ACL名称
    update: 更新ACL名称
    partial_update: 部分更新ACL名称
    destroy: 删除ACL名称
    """
    serializer_class = AclSerializer
    queryset = SaltAcl.objects.all()
    filter_class = SaltAclFilter
    search_fields = ['name', 'deny']


class SlsViewSet(viewsets.ModelViewSet):
    """
    list: 获取salt状态文件列表
    create: 添加salt状态文件
    retrieve: 查看salt状态文件
    update: 更新salt状态文件
    partial_update: 部分更新salt状态文件
    destroy: 删除salt状态文件
    """
    serializer_class = SlsSerializer
    permission_classes = []
    queryset = SaltSls.objects.all()
    filter_class = SaltSlsFilter
    search_fields = ['name']


class MdlViewSet(viewsets.ModelViewSet):
    """
    list: 获取salt模块列表
    create: 添加salt模块
    retrieve: 查看salt模块
    update: 更新salt模块
    partial_update: 部分更新salt模块
    destroy: 删除salt模块件
    """
    serializer_class = MdlSerializer
    permission_classes = []
    queryset = SaltMdl.objects.all()
    filter_class = SaltMdlFilter
    search_fields = ["name"]


class ArgViewSet(viewsets.ModelViewSet):
    """
    list: 获取模块参数列表
    create: 添加模块参数
    retrieve: 查看模块参数
    update: 更新模块参数
    partial_update: 部分模块参数
    destroy: 删除模块参数
    """
    serializer_class = ArgSerializer
    permission_classes = []
    queryset = SaltArg.objects.all()
    filter_class = SaltArgFilter
    search_fields = ["name"]


class ListKeyView(APIView):
    """
    列出所有的key
    """

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name='hostname', required=False, location='query', description='主机名称', type='sting'),
        ]
    )

    def get(self, request, *args, **kwargs):
        hostname = request.query_params.get('hostname', None)
        sapi = SaltAPI()
        result = sapi.list_all_key()
        minion_key = []
        if hostname:
            for minions_rejected in result.get("minions_rejected"):
                if self.filter_hostname(hostname, minions_rejected):
                    minion_key.append({"minions_status": "Accepted", "minions_id": minions_rejected})
            for minions_denied in result.get("minions_denied"):
                if self.filter_hostname(hostname, minions_denied):
                    minion_key.append({"minions_status": "Accepted", "minions_id": minions_denied})
            for minions in result.get("minions"):
                if self.filter_hostname(hostname, minions):
                    minion_key.append({"minions_status": "Accepted", "minions_id": minions})
            for minions_pre in result.get("minions_pre"):
                if self.filter_hostname(hostname, minions_pre):
                    minion_key.append({"minions_status": "Accepted", "minions_id": minions_pre})
            return Response({"data": minion_key, "status": True, "message": ""}, 200)

        if isinstance(result, dict):
            if result.get("status") is False:
                return result, 500
            for minions_rejected in result.get("minions_rejected"):
                minion_key.append({"minions_status": "Rejected", "minions_id": minions_rejected})
            for minions_denied in result.get("minions_denied"):
                minion_key.append({"minions_status": "Denied", "minions_id": minions_denied})
            for minions in result.get("minions"):
                minion_key.append({"minions_status": "Accepted", "minions_id": minions})
            for minions_pre in result.get("minions_pre"):
                minion_key.append({"minions_status": "Unaccepted", "minions_id": minions_pre})
        else:
            logger.error("Get minion key error: %s" % result)
        return Response({"data": minion_key, "status": True, "message": ""}, 200)

    def filter_hostname(self, hostname, minion_id):
        if re.search(hostname, minion_id):
            return True


class AddKeyView(APIView):
    """
    接受key
    """

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name='hostname', required=True, location='form', description='主机列表', type='array'),
        ]
    )

    def check_object(self, hostname):
        try:
            obj = MinionsStatus.objects.get(minion_id=hostname)
            return obj.minion_id
        except MinionsStatus.DoesNotExist:
            # raise Http404
            contenxt = hostname + " doesn't exist"
            raise APIException(contenxt)

    def post(self, request):
        hostnames = request.data.get('hostname', None)
        for hostname in hostnames:
            minion_id = self.check_object(hostname)
            sapi = SaltAPI()
            sapi.accept_key(minion_id)
        return Response({"status": 1})


class RejectKeyView(APIView):
    """
    拒绝key
    """

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name='hostname', required=True, location='form', description='主机列表', type='array'),
        ]
    )

    def check_object(self, hostname):
        try:
            obj = MinionsStatus.objects.get(minion_id=hostname)
            return obj.minion_id
        except MinionsStatus.DoesNotExist:
            contenxt = hostname + " doesn't exist"
            raise APIException(contenxt)

    def post(self, request):
        hostnames = request.data.get('hostname', None)
        for hostname in hostnames:
            minion_id = self.check_object(hostname)
            sapi = SaltAPI()
            sapi.reject_key(minion_id)
        return Response({"status": 1})


class DeleteKeyView(APIView):
    """
    删除key
    """

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name='hostname', required=True, location='form', description='主机列表', type='array'),
        ]
    )

    def check_object(self, hostname):
        try:
            obj = MinionsStatus.objects.get(minion_id=hostname)
            return obj.minion_id
        except MinionsStatus.DoesNotExist:
            contenxt = hostname + " doesn't exist"
            raise APIException(contenxt)

    def delete(self, request):
        hostnames = request.data.get('hostname', None)
        for hostname in hostnames:
            minion_id = self.check_object(hostname)
            sapi = SaltAPI()
            sapi.delete_key(minion_id)
        return Response({"status": 1})


class JobsHistoryView(APIView):
    """
    查看jobs历史
    """

    def get(self, request):
        sapi = SaltAPI()
        jids = sapi.runner("jobs.list_jobs")
        return Response(jids)


class JobsActiveView(APIView):
    """
    get:
    获取正在运行的jobs
    """

    def get(self, request):
        job_active_list = []
        sapi = SaltAPI()
        result = sapi.runner("jobs.active")
        if request:
            for jid, info in result.items():
                # 不能直接把info放到append中
                info.update({"Jid": jid})
                job_active_list.append(info)
        return Response({"data": job_active_list, "status": 1, "message": ""}, 200)


class JobsKillView(APIView):
    """
    delete:
    杀掉运行的job
    :parameter action: kill
    :parameter minion_ids: {"v-zpgeek-01": 12345,"v-zpgeek-02": 2345}
    """
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name='action', required=True, location='query', description='kill', type='string'),
            coreapi.Field(name='jid', required=True, location='query', description='20191220141748273576',
                          type='string'),
            coreapi.Field(name='minion_ids', required=True, location='query', description='json字符串', type='string')
        ]
    )

    def delete(self, request):
        action = request.query_params.get('action', None)
        jid = request.query_params.get('jid', None)
        minion_ids = request.query_params.get('minion_ids', None)
        print(json.loads(minion_ids))
        if action and jid and minion_ids:
            for minion in json.loads(minion_ids):
                for minion_id, ppid in minion.items():
                    # 获取pgid 并杀掉
                    kill_ppid_pid = r'''ps -eo pid,pgid,ppid,comm |grep %s |grep salt-minion |
                                         awk '{print "kill -- -"$2}'|sh''' % ppid
                    try:
                        # 通过kill -- -pgid 删除salt 相关的父进程及子进程
                        sapi = SaltAPI()
                        pid_result = sapi.shell_remote_execution(minion_id, kill_ppid_pid)
                        logger.info("kill %s %s return: %s" % (minion, kill_ppid_pid, pid_result))
                    except Exception as e:
                        logger.info("kill %s %s error: %s" % (minion, jid, e))
            return Response({"status": 1, "message": ""}, 200)
        else:
            return Response({"status": 0, "message": "The specified jid or action or minion_id "
                                                     "parameter does not exist"}, 400)


class JobsDetailView(APIView):
    """
    get:
    查看单个具体job
    """
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name='jid', required=True, location='query', description='20191220141748273576',
                          type='string'),
        ]
    )

    def get(self, request, *args, **kwargs):
        jid = request.query_params.get('jid', None)
        sapi = SaltAPI()
        result = sapi.jobs_info(jid)
        return Response(result)


class JobsScheduleView(APIView):
    """
    get: 查看定时任务
    """

    def get(self, request):
        sapi = SaltAPI()
        result = sapi.runner("jobs.active")
        return Response(result)


class GrainsView(APIView):
    """
    post: 同步grains数据
    :type list
    """
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name='minion_ids', required=True, location='form', description='v-test-01,v-test-02',
                          type='array'),
        ]
    )

    def post(self, request):
        minion_ids = request.data.get('minion_ids', None)
        sapi = SaltAPI()
        result = sapi.sync_grains(minion_ids)
        return Response(result)


class PillarView(APIView):
    """
    post: 同步pillar数据
    :type list
    """
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name='minion_ids', required=True, location='form', description='v-test-01,v-test-02',
                          type='array'),
        ]
    )

    def post(self, request):
        minion_ids = request.data.get('minion_ids', None)
        sapi = SaltAPI()
        result = sapi.sync_grains(minion_ids)
        return Response(result)

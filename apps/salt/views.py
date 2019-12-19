import coreapi
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from salt.api import SaltAPI
from salt.serializers import MinionStausSerializer
from .models import Minions_status
from django.http import Http404
from rest_framework.schemas import AutoSchema
from rest_framework.exceptions import APIException
import logging
import os

logger = logging.getLogger('default')


class MinonStatusViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    list:
    查看salt-minion的状态
    """
    serializer_class = MinionStausSerializer
    queryset = Minions_status.objects.all()


class ListKeyView(APIView):
    """
    列出所有的key
    """

    def get(self, request, *args, **kwargs):
        sapi = SaltAPI()
        result = sapi.list_all_key()
        minion_key = []
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
            obj = Minions_status.objects.get(minion_id=hostname)
            return obj.minion_id
        except Minions_status.DoesNotExist:
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
            obj = Minions_status.objects.get(minion_id=hostname)
            return obj.minion_id
        except Minions_status.DoesNotExist:
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
    拒绝key
    """

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name='hostname', required=True, location='form', description='主机列表', type='array'),
        ]
    )

    def check_object(self, hostname):
        try:
            obj = Minions_status.objects.get(minion_id=hostname)
            return obj.minion_id
        except Minions_status.DoesNotExist:
            contenxt = hostname + " doesn't exist"
            raise APIException(contenxt)

    def post(self, request):
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


class JobsManagerView(APIView):
    """
    get:
    获取运行的jobs
    post:
    杀掉正在运行的job
    """

    def get(self, request):
        sapi = SaltAPI()
        jids_running = sapi.runner("jobs.active")
        return Response(jids_running)

    def post(self, request):
        schema = AutoSchema(
            manual_fields=[
                coreapi.Field(name='action', required=True, location='query', description='kill', type='string'),
            ]
        )
        jid = request.query_params.get('kill', None)
        kill = "salt '*' saltutil.kill_job" + " " + jid
        os.popen(kill)
        return Response({"status": 0})

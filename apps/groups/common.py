from django.contrib.auth import get_user_model
from pms.models import Permission
User = get_user_model()

def get_user_obj(uid):
    try:
        for id in uid:
            if User.objects.get(pk=id):
                pass
        return uid
    except User.DoesNotExist:
        return None

def get_permission_obj(pid):
    try:
        for id in pid:
            if Permission.objects.get(pk=id):
                pass
        return pid
    except User.DoesNotExist:
        return None
from django.db import models
import django.utils.timezone as timezone


class SaltAcl(models.Model):
    name = models.CharField(max_length=64, verbose_name=u"ACL名称")
    description = models.CharField(max_length=128, verbose_name=u"描述")
    deny = models.CharField(max_length=64, verbose_name=u"拒绝权限")
    add_time = models.DateTimeField('添加日期', default=timezone.now)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        db_table = 'salt_acl'
        verbose_name = u'salt权限控制'


class SaltSls(models.Model):
    name = models.CharField(max_length=64, verbose_name=u"状态文件名称")
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"描述")
    add_time = models.DateTimeField('添加日期', default=timezone.now)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        db_table = 'salt_sls'
        verbose_name = u'salt状态文件'


class SaltMdl(models.Model):
    name = models.CharField(max_length=64, verbose_name=u"模块名称")
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"描述")
    add_time = models.DateTimeField('添加日期', default=timezone.now)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        db_table = 'salt_mdl'
        verbose_name = u'salt模块名称'


class SaltArg(models.Model):
    name = models.CharField(max_length=64, verbose_name=u"cmd.run模块参数名称")
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"描述")
    add_time = models.DateTimeField('添加日期', default=timezone.now)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        db_table = 'salt_arg'
        verbose_name = u'salt参数名称'


class MinionsStatus(models.Model):
    minion_id = models.CharField(max_length=128, null=True, blank=True)
    minion_status = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = "salt_minions_status"

    def __unicode__(self):
        return u'%s %s' % (self.minion_id, self.minion_status)

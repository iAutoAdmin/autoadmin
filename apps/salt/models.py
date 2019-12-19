from django.db import models


class Minions_status(models.Model):
    minion_id = models.CharField(max_length=128, null=True, blank=True)
    minion_status = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = "salt_minions_status"

    def __unicode__(self):
        return u'%s %s' % (self.minion_id, self.minion_status)

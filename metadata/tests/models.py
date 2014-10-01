from django.db import models

from metadata.mixins import MetadataMixin


class Poll(MetadataMixin, models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question

    def refresh(self):
        return self.__class__._default_manager.get(pk=self.pk)

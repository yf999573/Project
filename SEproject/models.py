# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class people(models.Model):
    user = models.CharField(max_length=20)
    psd = models.CharField(max_length=15)


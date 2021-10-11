from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey
import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Role(models.Model):
  '''
  The Role entries are managed by the system,
  automatically created via a Django data migration.
  '''

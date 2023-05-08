from datetime import datetime
import pytz
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import slugify


def created_now_tz():
    tz_info = pytz.timezone(settings.TIME_ZONE)
    return datetime.now(tz_info)


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(
            is_deleted=True,
            deleted_at=created_now_tz(),
        )

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None, is_deleted=False)

    def dead(self):
        return self.exclude(deleted_at=None, is_deleted=False)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        qs = SoftDeletionQuerySet(self.model)
        return qs.filter(is_deleted=False) if self.alive_only else qs

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class AbstractModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False)
    enabled = models.BooleanField(
        default=True,
        verbose_name="Enabled?",
        help_text="Objects not enabled can't be show.")
    created_at = models.DateTimeField(
        default=created_now_tz,
        editable=False,
        verbose_name="Created at",
        help_text="The object date creation.")
    updated_at = models.DateTimeField(
        default=created_now_tz,
        editable=False,
        verbose_name="Updated at",
        help_text="The object last update.")
    deleted_at = models.DateTimeField(
        blank=True,
        null=True)
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Is deleted?",
        help_text="Object checked as is_deleted can't be show.")
    created_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        verbose_name="Created by",
        related_name='created_by_%(class)s_related'.lower(),
        null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        now = datetime.now(pytz.timezone(settings.TIME_ZONE))
        if self.created_at is None:
            self.created_at = now
        self.updated_at = now
        super(AbstractModel, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """ soft delete a model instance """
        """ we never delete a object! Instead we mark he as deleted. """
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(AbstractModel, self).delete()

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

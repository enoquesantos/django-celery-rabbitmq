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

from tinymce.models import HTMLField

# Create your models here.
# classe abstrata para as páginas estáticas que contém:
# um título, uma descrição (conteúdo), um campo observações (opcional de
# uso interno) e campos timestamp.
class PostModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False)
    title = models.CharField(
        max_length=80,
        verbose_name="Title",
        help_text="The page title")
    slug = models.SlugField(
        max_length=50,
        null=True,
        unique=True,
        editable=False)
    brief = models.TextField(
        max_length=150,
        verbose_name="A brief",
        help_text="A brief with 150 characters limit.",
        blank=True,
        null=True)
    content = HTMLField(
        verbose_name="The page body",
        help_text="The body text in HTML format.",
        blank=True,
        null=True)
    comment = models.TextField(
        max_length=2000,
        verbose_name="Comments",
        help_text="A private area with comments for this post.",
        null=True,
        blank=True)
    deleted_at = models.DateTimeField(
        blank=True,
        null=True)
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Is deleted")
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Created at")
    updated_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Updated at")

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.slug)

    def delete(self, using=None, keep_parents=False):
        """ soft delete a model instance """
        """ we never delete a object! Instead we mark he as deleted. """
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(PostModel, self).delete()

    # before saving the object we need to create the slug
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title)[0:49])
        if not self.brief:
            self.brief = "%s..." % (str(self.content)[0:147])
        super(PostModel, self).save(*args, **kwargs)

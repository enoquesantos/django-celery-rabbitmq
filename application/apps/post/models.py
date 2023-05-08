from django.db import models
from django.utils.text import slugify

from tinymce.models import HTMLField

from apps.abstract.models import AbstractModel


# Create your models here.
# classe abstrata para as páginas estáticas que contém:
# um título, uma descrição (conteúdo), um campo observações (opcional de
# uso interno) e campos timestamp.
class PostModel(AbstractModel):
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

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.slug)

    def save(self, *args, **kwargs):
        '''
        before saving the object we need to create/updated the slug and brief
        '''
        self.slug = slugify(str(self.title)[0:49])

        if not self.brief:
            self.brief = "%s..." % (str(self.content)[0:147])

        super(PostModel, self).save(*args, **kwargs)

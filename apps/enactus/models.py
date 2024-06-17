from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from django_resized import ResizedImageField

from apps.utils.models import TimeStampAbstractModel


class Advertisement(TimeStampAbstractModel):
    theme = models.CharField(
        _("Тема"),
        max_length=300,
        )
    description = RichTextField(
        _("Описание"),
        )
    teams = models.ManyToManyField(
        'teams.Team',
        verbose_name=_("Компании"),
        blank=True,   
    )
    users = models.ManyToManyField(
        'users.User',
        verbose_name=_("Пользователи"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Объявления")
        verbose_name_plural = _("Объявления")
        ordering = ['-created_at', '-updated_at']


    def __str__(self) -> str:
        return self.theme    



class Project(models.Model):
    image = ResizedImageField(
        upload_to='projects_images/',
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        )
    name = models.CharField(
        _("Название"),
        max_length=300,
        )
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.SET_NULL,
        verbose_name=_("Регион"),
        blank=True,
        null=True,
    )
    start_date = models.DateField(
        _('Дата начала'),
    )
    end_date = models.DateField(
        _('Дата окончания'),
        blank=True,
        null=True,
    )
    description = RichTextField(
        _('Описание'),
        blank=True,
        null= True
    )
    criterias = RichTextField(
        _('Критерии'),
        blank=True,
        null=True,
    )
    is_for_students = models.BooleanField(
        _('Для студентов'),
        default=False,
    )


    class Meta:
        verbose_name = _("Проект")
        verbose_name_plural = _("Проекты")
        ordering = ['name', '-id']



class NewsCategory(models.Model):
    name = models.CharField(
        _("Название"),
        max_length=300,
        )
    description = RichTextField(
        _("Описание"),
        blank=True,
        null=True
        )
    
    class Meta:
        verbose_name = _("Категория новостей")
        verbose_name_plural = _("Категории новостей")

    def __str__(self) -> str:
        return self.name



class News(TimeStampAbstractModel):
    title = models.CharField(
        _("Заголовок"),
        max_length=300,
        )
    description = RichTextField(
        _("Описание"),
        )
    short_description = models.TextField(
        _("Краткое описание"),
    )
    image = ResizedImageField(
        upload_to='news_images/',
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        )
    
    category = models.ForeignKey(
        'NewsCategory',
        on_delete=models.CASCADE,
        verbose_name=_("Категория"),
        blank=True,
        )
    video_url = models.URLField(
        _("Ссылка на видео"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")
        ordering = ['-created_at', '-updated_at']

    def __str__(self) -> str:
        return self.title    
    


class NewsPhoto(models.Model):
    news = models.ForeignKey(
        'News',
        on_delete=models.CASCADE,
        verbose_name=_("Новость"),
        related_name="photos"
    )
    image = ResizedImageField(
        upload_to='news_photos/',
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        )
    
    class Meta:
        verbose_name = _("Фото новости")
        verbose_name_plural = _("Фото новостей")
        ordering = ['id']

    def __str__(self) -> str:
        return self.news.title    
    


class Event(models.Model):
    name = models.CharField(
        _("Название"),
        max_length=300,
        )
    short_description = models.TextField(
        _("Краткое описание"),
    )
    description = RichTextField(
        _("Описание"),
        )
    start_date = models.DateField(
        _('Дата начала'),
    )
    end_date = models.DateField(
        _('Дата окончания'),
    )
    start_time = models.TimeField(
        _('Время начала'),
    )
    end_time = models.TimeField(
        _('Время окончания'),
    )
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.SET_NULL,
        verbose_name=_("Регион"),
        blank=True,
        null=True,
    )
    address = models.CharField(
        _("Адрес"),
        max_length=300,
    )
    video_url = models.URLField(
        _("Ссылка на видео"),
        blank=True,
        null=True,
    )
    image = ResizedImageField(
        upload_to='events_images/',
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        )
    
    class Meta:
        verbose_name = _("Мероприятие")
        verbose_name_plural = _("Мероприятия")
        ordering = ['name', '-id']

    def __str__(self) -> str:
        return self.name    
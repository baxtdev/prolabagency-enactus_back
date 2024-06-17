import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField

from apps.utils.models import TimeStampAbstractModel,SoccialNetworks
from apps.utils.utils import build_absolute_url
from apps.users.models import User



# Create your models here.
class Team(SoccialNetworks):
    image = ResizedImageField(
        upload_to='teams/',
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(
        _("Дата основания"),
        auto_now_add=True,
        blank=True,
        null=True,
        )
    name = models.CharField(
        _("Название команды"),
        max_length=400
        )
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.SET_NULL,
        verbose_name=_("Регион"),
        blank=True,
        null=True,
        )
    university = models.ForeignKey(
        'university.University',
        verbose_name=_("Университет команды"),
        on_delete=models.CASCADE,
    )
    mission = RichTextField(
        _("Миссия"),
        blank=True,
        null=True,
    )
    goals = RichTextField(
        _("Цели"),
        blank=True,
        null=True,
    )
    tasks = RichTextField(
        _("Задачи"),
        blank=True,
        null=True,
    )
    phone = PhoneNumberField(
        _("Телефон"),
        unique=True,
    )
    phone_two = PhoneNumberField(
        _("Телефон 2"),
        blank=True,
        null=True,
    )
    phone_three = PhoneNumberField(
        _("Телефон 3"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self) -> str:
        return f"Команда {self.name} Университет {self.university}"    



class TeamMembers(TimeStampAbstractModel):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='team',
    )
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_('Команда'),
    )
    position = models.CharField(
        _('Должность'),
        max_length=255,
        blank=True,
        null=True,
        )
    company = models.CharField(
        _('Компания'),
        max_length=255,
        blank=True,
        null=True,
    )
    departament = models.CharField(
        _('Отдел'),
        max_length=255,
        blank=True,
        null=True,
        choices=User.DEPARTAMENT_CHOICES
    )
    start_date = models.DateTimeField(
        _('Дата начала'),
    )
    end_date = models.DateTimeField(
        _('Дата окончания'),
        blank=True,
        null=True,
    )
    is_current = models.BooleanField(
        _('Текущий участник'),
        default=False,
    )

    class Meta:
        db_table = 'team_members_tab'
        managed = True
        verbose_name = 'Участник Команды'
        verbose_name_plural = 'Участники Команды'
        ordering = ('-id',)

    def __str__(self) -> str:
        return f"{self.team}-Участник {self.user}"


def team_document_upload_path(instance,filename:str):
    _format = filename.split('.')[-1]
    return f'team_documents/{instance.team.name}_{instance.name}_.{_format}'



class TeamDocuments(TimeStampAbstractModel):
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('Команада')
    )
    name = models.CharField(
        _('Название документа'),
        max_length=300,
    )
    document_file = models.FileField(
        upload_to=team_document_upload_path,
        verbose_name=_('Файл документа'),
    )
    document_url = models.URLField(
        _('Ссылка на документ'),
        blank=True,
        null=True,
    )
    class Meta:
        db_table = 'docs_tab'
        managed = True
        verbose_name = 'Документ Команды'
        verbose_name_plural = 'Документы Команды'
        ordering = ['-id','-created_at']

    def __str__(self) -> str:
        return f"Команда {self.team.name}-{self.name} "    



class TeamProject(models.Model):
    image = ResizedImageField(
        upload_to='team_projects_images/',
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    )
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='projects',
    )
    name = models.CharField(
        _('Название Проекта'),
        max_length=300,
    )
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.SET_NULL,
        verbose_name=_("Регион"),
        blank=True,
        null=True,
        )
    start_date = models.DateTimeField(
        _('Дата начала'),
    )
    end_date = models.DateTimeField(
        _('Дата окончания'),
        blank=True,
        null=True,
    )
    is_current = models.BooleanField(
        _('Текущий проект'),
        default=False,
    )
    project_url = models.URLField(
        _('Ссылка на проект'),
        blank=True,
        null=True,
    )
    count_of_beneficiaries = models.PositiveBigIntegerField(
        _('Количество бенефициаров'),
        blank=True,
        null=True,
    )
    budget = models.PositiveSmallIntegerField(
        _('Бюджет'),
        blank=True,
        null=True,
    )
    income = models.PositiveSmallIntegerField(
        _('Прибыль'),
        blank=True,
        null=True,
    )
    investments = models.PositiveSmallIntegerField(
        _('Инвестиции'),
        blank=True,
        null=True,
    )
    description = RichTextField(
        _('Описание'),
    )
    problem = RichTextField(
        _('Проблема'),
        blank=True,
        null=True,
    )
    decision = RichTextField(
        _('Решение'),
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'projects_tab'
        managed = True
        verbose_name = 'Проект Команды'
        verbose_name_plural = 'Проекты Команд'
        ordering = ['id','name']

    def __str__(self) -> str:
        return f"Команда {self.team.name}-Проект {self.name}"



def document_upload_path(instance,filename:str):
    _format = filename.split('.')[-1]
    return f'team_prjects_documents/{instance.team_project.name}_{instance.name}_.{_format}'



class TeamProjectDocuments(TimeStampAbstractModel):
    team_project = models.ForeignKey(
        'TeamProject',
        on_delete=models.CASCADE,
        related_name='documents',
    )
    name = models.CharField(
        _('Название документа'),
        max_length=300,
    )
    document_url = models.URLField(
        _('Ссылка на документ'),
        blank=True,
        null=True,
    )
    document_file =models.FileField(
        _('Файл документа'),
        upload_to=document_upload_path,
        )
    
    class Meta:
        db_table = 'projetc_docs_tab'
        managed = True
        verbose_name = 'Документ Проекта'
        verbose_name_plural = 'Документы Проектов'


    def __str__(self) -> str:
        return f"Команда-{self.team_project.team.name}-Проект {self.team_project.name}"    

    def image_absolute_url(self):
        return build_absolute_url(self.document_file)



class TeamProjectPhotos(models.Model):
    team_project = models.ForeignKey(
        'TeamProject',
        on_delete=models.CASCADE,
        related_name='photos',
    )
    image = ResizedImageField(
        upload_to='team_project_photos/',
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'project_photos_tab'
        managed = True
        verbose_name = 'Фото Проекта'
        verbose_name_plural = 'Фото Проектов'
        ordering = ['id']

    def __str__(self) -> str:
        return f"Проект {self.team_project}-{self.id}"    

    def image_absolute_url(self):
        return build_absolute_url(self.image)
    


class InvitationToMembers(TimeStampAbstractModel):
    token = models.UUIDField(
        _('Токен'),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    invited_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='invitations',
        blank=True,
        null=True
    )
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='invitations',
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=300,
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=300,
    )
    email = models.EmailField(
        _('Email'),
        max_length=300,
    )
    role = models.CharField(
        _('Роль'),
        max_length=300,
        choices=User.ROLE_CHOICE
    )
    departament = models.CharField(
        _('Отдел'),
        max_length=300,
        choices=User.DEPARTAMENT_CHOICES
    )
    status = models.BooleanField(
        _('Статус'),
        default=False,
    )

    class Meta:
        db_table = 'invitation_to_members_tab'
        managed = True
        verbose_name = 'Приглашение в команду'
        verbose_name_plural = 'Приглашения в команды'
        ordering = ['id','status']

    def __str__(self) -> str:
        return f"Приглашение в команду {self.team}-Приглашенный {self.email}"
    
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

from apps.utils.models import TimeStampAbstractModel,SoccialNetworks
from apps.utils.utils import generate_code
from .managers import UserManager

from asgiref.sync import sync_to_async


class User(AbstractUser,TimeStampAbstractModel,SoccialNetworks):
    IT="IT"
    HR="HR"
    FIN="FIN"
    MKT="MKT"
    SMM="SMM"
    DEPARTAMENT_CHOICES = (
    (IT, 'ИТ'),
    (HR, 'HR'),
    (FIN, 'Финансы'),
    (MKT, 'Маркетинг'),
    ('PRD', 'Продукты'),
    ('SALES', 'Продажи'),
    ('FIN', 'Финансы'),
    (SMM, 'SMM'),
    ('OTHER', 'Другое'),
    )
    departament = models.CharField(
        _('Отдел'),
        max_length=300,
        choices=DEPARTAMENT_CHOICES,
        blank=True,
        null=True
    )
    phone=PhoneNumberField(
        'Телефон',
        unique=True,
        blank=True, 
        null=True
    )
    image = ResizedImageField(
        upload_to='avatars/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    ) 
    username = None
    middle_name = models.CharField(
        max_length=255, 
        verbose_name='Отчество',
        blank=True,
        null=True
        )
    last_activity = models.DateTimeField(
        verbose_name=_('last'),
        editable=True,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _("Эл.почта"), 
        max_length=254,
        unique = True,
        )
    CORDINATOR = 'CORD'
    SIMPLE_MEMBER = 'MEMR'
    MANAGER = 'MANG'
    CAPTAIN = 'CAPT'
    ADVISER = 'ADVS'	
    ALUMNI ='ALUM'
    ROLE_CHOICE=(
        (CORDINATOR,"Координатор"),
        (SIMPLE_MEMBER,"Участники"),
        (MANAGER,"Менеджер"),
        (CAPTAIN,"Капитан"),
        (ADVISER,"Эдвайзер"),
        (ALUMNI,"Аламник"),
    )
    role = models.CharField(
        choices = ROLE_CHOICE,
        max_length = 50,
        default = SIMPLE_MEMBER,
    )
    GENDER_CHOICE = (
        ("M","Мужчина"),
        ("W","Женщина"),
        ("OTHER","Дугое"),
        ("NONE","Не указан"),
    )
    gender = models.CharField(
        _("Пол"),
        choices = GENDER_CHOICE,
        max_length = 50,
        default = "NONE",
        blank=True,
        )
    is_notifications = models.BooleanField(
        _('Отправлять уведомления'),
        default=False,
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()
    
    class Meta:
        db_table = 'main_table'
        managed = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def get_full_name(self) -> str:
        if self.first_name or self.last_name or self.middle_name:
            return f"{self.first_name} {self.last_name} {self.middle_name}"
        return f"{self.email.split('@')[0]}"
    
    @sync_to_async
    def _last_activity(self):
        from django.utils import timezone
        self.last_activity = timezone.now()
        self.save()



class UserActivities(models.Model):
    role = models.CharField(
        _('Роль'),
        max_length=255,
        default=User.ALUMNI,
        choices=User.ROLE_CHOICE
    )
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Команда'),
        related_name='activities',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities',
    )
    department = models.CharField(
        _('Отдел'),
        max_length=255,
        blank=True,
        null=True,
        choices=User.DEPARTAMENT_CHOICES,
        default=User.SMM,
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
    project = models.ManyToManyField(
        'teams.TeamProject',
        verbose_name=_('Проект'),
    )

    class Meta:
        db_table = 'activities_table'
        managed = True
        verbose_name = 'Активность Пользователя'
        verbose_name_plural = 'Активности Ползователей'
        ordering = ['-start_date']

    def __str__(self) -> str:
        return f"Пользователь {self.user}-Проект {self.project}"    



class ResetPasword(TimeStampAbstractModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='codes',
    )
    is_active = models.BooleanField()
    code = models.IntegerField(
        unique=True,
        blank=True,
        null=True
    )
    data = models.DateField(
        auto_now_add=True,
        auto_created=True,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        code = generate_code()
        if not self.code:
            self.code = code
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.email}---{self.data}"
        
    class Meta:
        db_table = 'codes_res_password_table'
        managed = True
        verbose_name = 'Код для сброса пароля'
        verbose_name_plural = 'Коды для  сброса пароля'  


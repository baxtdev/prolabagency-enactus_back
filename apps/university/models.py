from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
from drf_extra_fields.fields import Base64ImageField,Base64FileField


from apps.utils.models import TimeStampAbstractModel,SoccialNetworks
# Create your models here.

class University(models.Model):
    image = ResizedImageField(
        upload_to='universities/',
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
        blank=True,
        null=True,
    )
    name = models.CharField(
        _("Название Университета"),
        max_length=400
        )    
    rectors_first_name = models.CharField(
        _("ИМЯ Ректора"),
        max_length=400,
    )
    rectors_second_name = models.CharField(
        _("ФАМИЛИЯ Ректора"),
        max_length=400,
    )
    rectors_middle_name = models.CharField(
        _("ОТЧЕСТВО Ректора"),
        max_length=400,
        blank=True,
        null=True,
    )
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.SET_NULL,
        verbose_name=_("Регион"),
        blank=True,
        null=True,
        )
    abbreviation = models.CharField(
        _("Аббревиатура"),
        max_length=20,
    )
    info = RichTextField(
        _("Информация"),
        blank=True,
        null=True,
    )


    class Meta:
        db_table = 'universities_tab'
        managed = True
        verbose_name = 'Университет'
        verbose_name_plural = 'Университеты'
        ordering = ['id','name']

    def __str__(self) -> str:
        return f"Университет Имени {self.name}- Ректор {self.rectors_first_name}"



def document_upload_path(instance,filename:str):
    _format = filename.split('.')[-1]
    return f'university_documents/{instance.university.name}_{instance.name}_.{_format}'



class UniversityDocuments(TimeStampAbstractModel):
    university = models.ForeignKey(
        'University',
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
        db_table = 'university_docs_tab'
        managed = True
        verbose_name = 'Документ Университета'
        verbose_name_plural = 'Документы Университета'

    def __str__(self) -> str:
        return f"Университет {self.university.name}-Документ {self.name}" 





    



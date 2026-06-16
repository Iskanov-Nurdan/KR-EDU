import os
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from PIL import Image as PilImage

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_file_size(value):
    if value.size > MAX_UPLOAD_SIZE:
        raise ValidationError('Файл слишком большой (максимум 10 МБ).')


def _compress_image_file(path, quality=82, max_size=(1920, 1080)):
    """Resize and recompress an image in-place after it has been saved to disk."""
    try:
        with PilImage.open(path) as img:
            fmt = (img.format or 'JPEG').upper()
            if fmt == 'JPG':
                fmt = 'JPEG'
            if fmt not in ('JPEG', 'PNG', 'WEBP'):
                return

            if img.mode == 'RGBA' and fmt == 'JPEG':
                bg = PilImage.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg
            elif img.mode not in ('RGB', 'RGBA', 'L'):
                img = img.convert('RGB')

            img.thumbnail(max_size, PilImage.LANCZOS)

            save_kw = {'optimize': True}
            if fmt in ('JPEG', 'WEBP'):
                save_kw['quality'] = quality

            img.save(path, format=fmt, **save_kw)
    except Exception:
        pass


class _CompressImageMixin:
    """Mixin that auto-compresses an image field on save.

    Set ``image_field = 'photo'`` (or any field name) on the subclass
    to compress a field other than the default ``'image'``.
    """
    image_field = 'image'

    def _image_name_in_db(self):
        if not self.pk:
            return None
        try:
            return (
                self.__class__.objects
                .filter(pk=self.pk)
                .values_list(self.image_field, flat=True)
                .first()
            )
        except Exception:
            return None

    def save(self, *args, **kwargs):
        old_name = self._image_name_in_db()
        super().save(*args, **kwargs)
        field = getattr(self, self.image_field, None)
        if field and field.name != old_name:
            try:
                _compress_image_file(field.path)
            except (ValueError, OSError):
                pass


# ── Site-wide settings ────────────────────────────────────────────────────────

class SiteSettings(models.Model):
    logo = models.ImageField(
        upload_to='site/', blank=True, null=True,
        verbose_name='Логотип колледжа',
        help_text='Загрузите PNG или JPG файл логотипа',
        validators=[validate_file_size],
    )
    favicon = models.ImageField(
        upload_to='site/', blank=True, null=True,
        verbose_name='Фавикон (иконка вкладки)',
        help_text='PNG или ICO, рекомендуемый размер 32×32 или 64×64 пикселей',
        validators=[validate_file_size],
    )
    college_name = models.CharField(
        max_length=255,
        default='Кочкор-Атинский региональный колледж',
        verbose_name='Название колледжа',
    )
    subtitle = models.CharField(
        max_length=255,
        default='Министерство науки, высшего образования и инноваций КР',
        verbose_name='Подзаголовок (под названием)',
    )
    mission = models.TextField(
        blank=True,
        verbose_name='Миссия колледжа',
        help_text='Текст миссии — отображается на странице «О колледже»',
    )

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'


# ── Ministry page ─────────────────────────────────────────────────────────────

class MinistryPage(models.Model):
    title = models.CharField(
        max_length=500,
        default='Министерство науки, высшего образования и инноваций Кыргызской Республики',
        verbose_name='Название министерства',
    )
    description = models.CharField(
        max_length=1000, blank=True,
        verbose_name='Краткое описание',
    )
    content = models.TextField(
        blank=True,
        verbose_name='Содержание страницы',
    )
    logo = models.ImageField(
        upload_to='ministry/', blank=True, null=True,
        verbose_name='Логотип / герб министерства',
        validators=[validate_file_size],
    )
    website_url = models.URLField(
        blank=True,
        verbose_name='Официальный сайт министерства',
        help_text='Ссылка будет открываться в новой вкладке',
    )

    class Meta:
        verbose_name = 'Страница Министерства'
        verbose_name_plural = 'Страница Министерства'

    def __str__(self):
        return self.title


# ── Academics ─────────────────────────────────────────────────────────────────

class Specialty(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название специальности')
    code = models.CharField(max_length=50, verbose_name='Код специальности')
    duration = models.CharField(max_length=100, verbose_name='Срок обучения')
    qualification = models.CharField(max_length=255, verbose_name='Квалификация')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ['name']

    def __str__(self):
        return self.name


# ── News ──────────────────────────────────────────────────────────────────────

class News(_CompressImageMixin, models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(
        upload_to='news/', blank=True, null=True, verbose_name='Изображение',
        validators=[validate_file_size],
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ── Gallery ───────────────────────────────────────────────────────────────────

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория галереи'
        verbose_name_plural = 'Категории галереи'

    def __str__(self):
        return self.name


class Gallery(_CompressImageMixin, models.Model):
    title = models.CharField(max_length=255, verbose_name='Описание фото')
    image = models.ImageField(
        upload_to='gallery/', verbose_name='Изображение',
        validators=[validate_file_size],
    )
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Категория',
        related_name='photos',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Галерея'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ── Contact ───────────────────────────────────────────────────────────────────

class Contact(models.Model):
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    email = models.EmailField(max_length=255, verbose_name='Email')
    map_url = models.URLField(
        max_length=1000,
        blank=True,
        verbose_name='Ссылка на карту',
        help_text='Вставьте ссылку на карту (Google Maps, 2ГИС и т.д.) — появится кнопка «Открыть» рядом с картой',
    )

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return self.address


# ── About ─────────────────────────────────────────────────────────────────────

class CollegeInfo(_CompressImageMixin, models.Model):
    image_field = 'photo'

    photo = models.ImageField(
        upload_to='about/', blank=True, null=True,
        verbose_name='Фото колледжа (секция «О нас»)',
        help_text='Рекомендуемый размер: 800×600 или шире. Фото отображается в секции «О колледже».',
        validators=[validate_file_size],
    )
    history = models.TextField(verbose_name='История колледжа')
    founded_year = models.IntegerField(verbose_name='Год основания')
    ownership_form = models.CharField(max_length=100, verbose_name='Форма собственности')
    building_info = models.TextField(verbose_name='Информация о здании')
    facilities = models.TextField(verbose_name='Материально-техническая база')

    class Meta:
        verbose_name = 'О колледже'
        verbose_name_plural = 'О колледже'

    def __str__(self):
        return f'Информация о колледже (осн. {self.founded_year})'


class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название документа')
    file = models.FileField(
        upload_to='documents/', blank=True, null=True, verbose_name='Файл',
        help_text='Разрешены только PDF, DOC, DOCX, максимум 10 МБ.',
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
        ],
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Документ / Лицензия'
        verbose_name_plural = 'Документы и лицензии'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


# ── Admissions ────────────────────────────────────────────────────────────────

class Admission(models.Model):
    conditions = models.TextField(verbose_name='Условия приема')
    required_documents = models.TextField(verbose_name='Необходимые документы')
    tuition_cost = models.TextField(verbose_name='Стоимость обучения')
    deadlines = models.TextField(verbose_name='Сроки подачи документов')
    committee_contacts = models.TextField(verbose_name='Контакты приемной комиссии')

    class Meta:
        verbose_name = 'Информация для абитуриентов'
        verbose_name_plural = 'Информация для абитуриентов'

    def __str__(self):
        return 'Информация для абитуриентов'

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from .models import (
    SiteSettings, MinistryPage, Specialty, News,
    Gallery, GalleryCategory, Contact, CollegeInfo, Document, Admission,
    Testimonial, FAQ,
)

TINYMCE_OVERRIDES = {
    models.TextField: {'widget': TinyMCE()},
}


def _thumb(url, size=60):
    return format_html(
        '<img src="{}" style="height:{}px;width:{}px;object-fit:cover;border-radius:6px;border:1px solid #ddd">',
        url, size, size,
    )


# ── Site Settings ──────────────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslationAdmin):
    list_display = ('college_name', 'logo_preview')
    save_on_top = True
    formfield_overrides = TINYMCE_OVERRIDES

    fieldsets = (
        ('Фон главного баннера', {
            'fields': ('hero_background',),
        }),
        ('Логотип и иконка', {
            'fields': ('logo', 'favicon'),
        }),
        ('Статистика на главной странице', {
            'fields': ('graduates_count', 'teachers_count'),
        }),
        ('Русский язык (РУС)', {
            'fields': ('college_name_ru', 'subtitle_ru', 'mission_ru'),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': ('college_name_ky', 'subtitle_ky', 'mission_ky'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Логотип')
    def logo_preview(self, obj):
        if obj.logo:
            return _thumb(obj.logo.url)
        return '—'

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── Ministry Page ──────────────────────────────────────────────────────────────

@admin.register(MinistryPage)
class MinistryPageAdmin(TranslationAdmin):
    list_display = ('title', 'website_url', 'logo_preview')
    save_on_top = True
    formfield_overrides = TINYMCE_OVERRIDES

    fieldsets = (
        ('Общее', {
            'fields': ('logo', 'website_url'),
        }),
        ('Русский язык (РУС)', {
            'fields': ('title_ru', 'description_ru', 'content_ru'),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': ('title_ky', 'description_ky', 'content_ky'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Логотип')
    def logo_preview(self, obj):
        if obj.logo:
            return _thumb(obj.logo.url)
        return '—'

    def has_add_permission(self, request):
        return not MinistryPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── Specialty ──────────────────────────────────────────────────────────────────

@admin.register(Specialty)
class SpecialtyAdmin(TranslationAdmin):
    list_display = ('name', 'code', 'duration', 'qualification')
    search_fields = ('name_ru', 'name_ky', 'code')
    list_per_page = 20
    save_on_top = True
    formfield_overrides = TINYMCE_OVERRIDES

    fieldsets = (
        ('Общее', {
            'fields': ('code', 'duration'),
        }),
        ('Русский язык (РУС)', {
            'fields': ('name_ru', 'qualification_ru', 'description_ru'),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': ('name_ky', 'qualification_ky', 'description_ky'),
            'classes': ('collapse',),
        }),
    )


# ── News ───────────────────────────────────────────────────────────────────────

@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'image_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title_ru', 'title_ky')
    readonly_fields = ('created_at', 'image_preview_large')
    list_per_page = 20
    save_on_top = True
    formfield_overrides = TINYMCE_OVERRIDES

    fieldsets = (
        ('Изображение', {
            'fields': ('image', 'image_preview_large', 'created_at'),
        }),
        ('Русский язык (РУС)', {
            'fields': ('title_ru', 'content_ru'),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': ('title_ky', 'content_ky'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Фото')
    def image_preview(self, obj):
        if obj.image:
            return _thumb(obj.image.url)
        return '—'

    @admin.display(description='Превью')
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:200px;max-width:400px;border-radius:8px;">',
                obj.image.url,
            )
        return '—'


# ── Gallery ────────────────────────────────────────────────────────────────────

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'photo_count')
    list_per_page = 30

    @admin.display(description='Фотографий')
    def photo_count(self, obj):
        return obj.photos.count()


@admin.register(Gallery)
class GalleryAdmin(TranslationAdmin):
    list_display = ('image_preview', 'title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title_ru', 'title_ky')
    readonly_fields = ('created_at', 'image_preview_large')
    list_per_page = 24
    list_select_related = ('category',)
    save_on_top = True

    fieldsets = (
        ('Изображение', {
            'fields': ('image', 'image_preview_large', 'category', 'created_at'),
        }),
        ('Русский язык (РУС)', {
            'fields': ('title_ru',),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': ('title_ky',),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Фото')
    def image_preview(self, obj):
        if obj.image:
            return _thumb(obj.image.url, size=55)
        return '—'

    @admin.display(description='Превью')
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:200px;max-width:400px;border-radius:8px;">',
                obj.image.url,
            )
        return '—'


# ── Contact ────────────────────────────────────────────────────────────────────

@admin.register(Contact)
class ContactAdmin(TranslationAdmin):
    list_display = ('address', 'phone', 'email')
    save_on_top = True

    fieldsets = (
        ('Контактные данные', {
            'fields': ('phone', 'email', 'map_url'),
        }),
        ('Адрес — Русский (РУС)', {
            'fields': ('address_ru',),
        }),
        ('Адрес — Кыргызский (КЫР)', {
            'fields': ('address_ky',),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return not Contact.objects.exists()


# ── College Info ───────────────────────────────────────────────────────────────

@admin.register(CollegeInfo)
class CollegeInfoAdmin(TranslationAdmin):
    list_display = ('founded_year', 'ownership_form', 'photo_preview')
    save_on_top = True
    readonly_fields = ('photo_preview',)
    formfield_overrides = TINYMCE_OVERRIDES

    fieldsets = (
        ('Фото секции «О нас»', {
            'fields': ('photo', 'photo_preview'),
        }),
        ('Общие сведения', {
            'fields': ('founded_year',),
        }),
        ('Русский язык (РУС)', {
            'fields': ('ownership_form_ru', 'history_ru', 'building_info_ru', 'facilities_ru'),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': ('ownership_form_ky', 'history_ky', 'building_info_ky', 'facilities_ky'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Фото')
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:180px;max-width:360px;border-radius:8px;">',
                obj.photo.url,
            )
        return '—'

    def has_add_permission(self, request):
        return not CollegeInfo.objects.exists()


# ── Document ───────────────────────────────────────────────────────────────────

@admin.register(Document)
class DocumentAdmin(TranslationAdmin):
    list_display = ('title', 'file_link', 'uploaded_at')
    search_fields = ('title_ru', 'title_ky')
    readonly_fields = ('uploaded_at',)
    list_per_page = 20
    save_on_top = True

    fieldsets = (
        ('Файл', {
            'fields': ('file', 'uploaded_at'),
        }),
        ('Русский язык (РУС)', {
            'fields': ('title_ru', 'description_ru'),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': ('title_ky', 'description_ky'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Файл')
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">📄 Скачать</a>', obj.file.url)
        return '—'


# ── Admission ──────────────────────────────────────────────────────────────────

@admin.register(Admission)
class AdmissionAdmin(TranslationAdmin):
    list_display = ('__str__',)
    save_on_top = True
    formfield_overrides = TINYMCE_OVERRIDES

    fieldsets = (
        ('Русский язык (РУС)', {
            'fields': (
                'conditions_ru', 'required_documents_ru',
                'tuition_cost_ru', 'deadlines_ru', 'committee_contacts_ru',
            ),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': (
                'conditions_ky', 'required_documents_ky',
                'tuition_cost_ky', 'deadlines_ky', 'committee_contacts_ky',
            ),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return not Admission.objects.exists()


# ── Testimonial ────────────────────────────────────────────────────────────────

@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    list_display = ('name', 'role', 'rating', 'order')
    list_editable = ('order',)
    search_fields = ('name_ru', 'name_ky')
    list_per_page = 20
    save_on_top = True

    fieldsets = (
        ('Общее', {
            'fields': ('icon', 'rating', 'order'),
        }),
        ('Русский язык (РУС)', {
            'fields': ('name_ru', 'role_ru', 'text_ru'),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': ('name_ky', 'role_ky', 'text_ky'),
            'classes': ('collapse',),
        }),
    )


# ── FAQ ────────────────────────────────────────────────────────────────────────

@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)
    search_fields = ('question_ru', 'question_ky')
    list_per_page = 20
    save_on_top = True
    formfield_overrides = TINYMCE_OVERRIDES

    fieldsets = (
        ('Общее', {
            'fields': ('order',),
        }),
        ('Русский язык (РУС)', {
            'fields': ('question_ru', 'answer_ru'),
        }),
        ('Кыргызский язык (КЫР)', {
            'fields': ('question_ky', 'answer_ky'),
            'classes': ('collapse',),
        }),
    )

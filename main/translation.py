from modeltranslation.translator import register, TranslationOptions
from .models import (
    SiteSettings, CollegeInfo, Specialty, News,
    Admission, Contact, Document, GalleryCategory, Gallery, MinistryPage,
    Testimonial, FAQ,
)


@register(SiteSettings)
class SiteSettingsTranslation(TranslationOptions):
    fields = ('college_name', 'subtitle', 'mission')


@register(MinistryPage)
class MinistryPageTranslation(TranslationOptions):
    fields = ('title', 'description', 'content')


@register(Specialty)
class SpecialtyTranslation(TranslationOptions):
    fields = ('name', 'description', 'qualification')


@register(News)
class NewsTranslation(TranslationOptions):
    fields = ('title', 'content')


@register(GalleryCategory)
class GalleryCategoryTranslation(TranslationOptions):
    fields = ('name',)


@register(Gallery)
class GalleryTranslation(TranslationOptions):
    fields = ('title',)


@register(Contact)
class ContactTranslation(TranslationOptions):
    fields = ('address',)


@register(CollegeInfo)
class CollegeInfoTranslation(TranslationOptions):
    fields = ('history', 'ownership_form', 'building_info', 'facilities')


@register(Document)
class DocumentTranslation(TranslationOptions):
    fields = ('title', 'description')


@register(Admission)
class AdmissionTranslation(TranslationOptions):
    fields = ('conditions', 'required_documents', 'tuition_cost', 'deadlines', 'committee_contacts')


@register(Testimonial)
class TestimonialTranslation(TranslationOptions):
    fields = ('name', 'role', 'text')


@register(FAQ)
class FAQTranslation(TranslationOptions):
    fields = ('question', 'answer')

from django.shortcuts import render
from django.views.generic import DetailView
from .models import (
    Specialty, News, Gallery, GalleryCategory,
    Contact, CollegeInfo, Document, Admission, MinistryPage,
    Testimonial, FAQ,
)


def index(request):
    """Single-page view — loads all section data at once."""
    return render(request, 'main/index.html', {
        'specialties':    Specialty.objects.all(),
        'news_items':     News.objects.order_by('-created_at')[:9],
        'gallery_photos': Gallery.objects.select_related('category').order_by('-created_at'),
        'categories':     GalleryCategory.objects.all(),
        'college_info':   CollegeInfo.objects.first(),
        'documents':      Document.objects.all(),
        'contact':        Contact.objects.first(),
        'admission':      Admission.objects.first(),
        'ministry':       MinistryPage.objects.first(),
        'testimonials':   Testimonial.objects.all(),
        'faqs':           FAQ.objects.all(),
    })


class NewsDetailView(DetailView):
    model = News
    template_name = 'main/news_detail.html'
    context_object_name = 'news'

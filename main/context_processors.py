from .models import Contact, SiteSettings


def site_context(request):
    contact = Contact.objects.first()
    site_settings = SiteSettings.objects.first()
    return {
        'site_contact': contact,
        'site_settings': site_settings,
    }

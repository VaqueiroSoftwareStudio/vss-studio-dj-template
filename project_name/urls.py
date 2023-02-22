"""{{ project_name }} URL Configuration"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.views import serve
from django.urls import include, path
from django.views.generic import TemplateView

try:
    from vss.apps.blog.sitemaps import ArticleSitemap
    from vss_studio.apps.catalog.sitemaps import ServiceSitemap

    sitemaps = {
        'articles' : ArticleSitemap,
        'services' : ServiceSitemap,
    }
except ImportError:
    sitemaps = {}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'),
        name='robots'),
    
] + i18n_patterns(
    path('', include('vss.urls')),
    path('', include('vss_studio.apps.website.urls')),
    # NOTE - Si se cambia prefix_default_language a False, hay que actualizar
    # el modo en que se cambia de idioma. Actualmente hacemos un
    # 'slice' de los tres primeros caracteres.
    # <input name="next" type="hidden"
    #     value="{% if LANGUAGE_CODE == 'es' %}
    #         {{ request.get_full_path }}
    #     {% else %}
    #         {{ request.get_full_path|slice:'3:' }}
    #     {% endif %}" />
    prefix_default_language = True,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += tuple(static(settings.STATIC_URL, view=serve, show_indexes=True))
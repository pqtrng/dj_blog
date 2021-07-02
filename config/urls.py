from django.contrib import admin, sitemaps
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSiteMap

sitemaps = {
    'posts': PostSiteMap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path(
        route='sitemap.xml',
        view=sitemap,
        kwargs={
            'sitemaps': sitemaps
        },
        name='django.contrib.sitemaps.view.sitemap'
    )
]

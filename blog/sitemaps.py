from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSiteMap(Sitemap):
    """A custom sitemap

    Args:
        Sitemap (sitemap): base class for PostSiteMap
    """
    changefreq = 'weekly'  # change frequency of post pages
    priority = 0.9  # relevance in the website

    def items(self):
        """Return the QuerySet of objects to include in this sitemap
        """
        return Post.published.all()

    def lastmod(self, obj):
        """Receive each object from the Query set and return the last time it was modified

        Args:
            obj ([type]): [description]

        Returns:
            [type]: [description]
        """
        return obj.updated

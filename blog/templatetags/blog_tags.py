from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    """A customized tag total_posts and register the function as a simple tag

    Returns:
        int: The number of published posts
    """
    return Post.published.count()


@register.inclusion_tag(filename='blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


# filter shall be use as {{ variable|markdown }}
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """A customized tag total_posts and register the function as a simple tag

    Returns:
        [type]: [description]
    """
    return Post.published.count()


@register.inclusion_tag(filename='blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

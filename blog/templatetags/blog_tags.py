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

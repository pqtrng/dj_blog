from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    # Get all posts with the published status using published manager is created.
    posts = Post.published.all()
    return render(request=request, template_name='blog/post/list.html', context={'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,  # There is only one slug for a given day, because of unique_for_date
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request=request, template_name='blog/post/detail.html', context={'post': post})

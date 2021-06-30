from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    # Get all posts with the published status using published manager is created.
    object_list = Post.published.all()
    # Instantiate with the number of objects to display
    paginator = Paginator(object_list, 3)  # posts in each page

    # Get the current page
    page = request.GET.get('page')
    try:
        # obtain the object for desired page
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(
        request=request,
        template_name='blog/post/list.html',
        context={
            'page': page,
            'posts': posts
        }
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,  # There is only one slug for a given day, because of unique_for_date
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request=request, template_name='blog/post/detail.html', context={'post': post})

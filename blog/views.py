from typing import List
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import EmailPostForm
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


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


def post_share(request, post_id):
    # Retrieve post by id, make sure it is published
    post = get_object_or_404(
        Post,
        id=post_id,
        status='published'
    )

    # Use same view for both displaying the initial form and processing the submitted data

    if request.method == 'POST':
        # Form was submitted, create a from with data is contained in request.POST
        form = EmailPostForm(request.POST)
        # Validate the submitted data, True if all fields contain valid data
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
    else:
        # Empty form is requested
        form = EmailPostForm()
    return render(
        request=request,
        template_name='blog/post/share.html',
        context={
            'post': post,
            'form': form
        })

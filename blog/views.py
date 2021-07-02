from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.views.generic import ListView
from taggit.models import Tag
from django.db.models import Count


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    # Get all posts with the published status using published manager is created.
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        # get Tag object with the given slug
        tag = get_object_or_404(Tag, slug=tag_slug)
        # filter list of posts with this given tag
        object_list = object_list.filter(tags__in=[tag])

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
            'posts': posts,
            'tag': tag
        }
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,  # There is only one slug for a given day, because of unique_for_date
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # Get all active comments of this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Retrieve a python list of IDs for tags of the current post.
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)  # exclude the current post

    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]

    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts,
        }
    )


def post_share(request, post_id):
    # Retrieve post by id, make sure it is published
    post = get_object_or_404(
        Post,
        id=post_id,
        status='published'
    )

    sent = False

    # Use same view for both displaying the initial form and processing the submitted data

    if request.method == 'POST':
        # Form was submitted, create a from with data is contained in request.POST
        form = EmailPostForm(request.POST)
        # Validate the submitted data, True if all fields contain valid data
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(
                subject=subject,
                message=message,
                from_email='admin&email.com',
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        # Empty form is requested
        form = EmailPostForm()
    return render(
        request=request,
        template_name='blog/post/share.html',
        context={
            'post': post,
            'form': form,
            'sent': sent
        })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag


def post_list(req, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 5 Posts Per Page
    paginator = Paginator(post_list, 5)
    page_number = req.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number entered is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is not in range, return the last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(req, 'blog/post/list.html', {'posts': posts,
                                               'tag': tag
                                               })

def post_detail(req, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year =year,
                             publish__month=month,
                             publish__day=day
                            )
    # List of Active Comments For This Post
    comments = post.comments.filter(active=True)
    # Form for Users to Comment
    form = CommentForm()
    
    # List of Similar Posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids.exclude(id=post.id))
    similar_posts= similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    

    return render(req, 'blog/post/detail.html', {
        'post': post, 
        'comments': comments, 
        'form': form,
        'similar_posts': similar_posts
        })


# Class-Based View Alternative
from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'
    
# Recommend Posts By Email
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

def post_share(req, post_id):
    #Get Post By Id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    
    if req.method == 'POST':
        # Form Was Submitted
        form = EmailPostForm(req.POST)
        if form.is_valid():
            # Form Fields Passed Validation
            cd = form.cleaned_data
            post_url = req.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title} "
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'aaronkcarpenter@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(req, 'blog/post/share.html', {'post': post,
                                                'form': form,
                                                'sent': sent
                                                })

@require_POST
def post_comment(req, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=req.POST)
    if form.is_valid():
        # Create a comment object w/o saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(req, 'blog/post/comment.html',
                {
                'post': post,
                'form': form,
                'comment': comment
                })



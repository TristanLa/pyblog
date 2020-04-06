from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from blog.models import Post, Comment
from blog import model_helpers
from blog import navigation
from blog.forms import CreateCommentForm

# Create your views here.
def post_list(request, category_name=model_helpers.post_category_all.slug()):
    category, posts = model_helpers.get_posts_category(category_name)
    categories = model_helpers.get_categories()
    context = {
        "category": category,
        "posts": posts,
        "categories": categories,
        "navigation_items": navigation.navigation_items(navigation.NAV_POSTS),
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, post_id, message=''):
    post = get_object_or_404(Post, pk=post_id)
    similar_posts = Post.objects.filter(category=post.category).filter(published=True).exclude(pk=post_id)
    post_comments = post.comments.exclude(status=Comment.STATUS_HIDDEN).order_by("created_at")

    if request.method == "POST":
        comment_form = CreateCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            args = [post.pk, "Your comment has been posted!"]
            return HttpResponseRedirect(reverse('post-detail-message', args=args) + "#comments")
    else:
        comment_form = CreateCommentForm()

    context = {
        "post": post,
        "similar_posts": similar_posts,
        "post_comments": post_comments,
        "navigation_items": navigation.navigation_items(navigation.NAV_POSTS),
        "comment_form": comment_form,
        "message": message,
    }
    return render(request, "blog/post_detail.html", context)


def about(request):
    context = {
        "navigation_items": navigation.navigation_items(navigation.NAV_ABOUT),
    }
    return render(request, "blog/about.html", context)
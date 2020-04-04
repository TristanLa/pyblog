from blog.models import Post, PostCategory

post_category_all = PostCategory(name="All")

def get_posts_category(category_name):
    posts = Post.objects.filter(published=True)

    if category_name == post_category_all.slug():
        category = post_category_all
    else:
        try:
            category = PostCategory.objects.get(name__iexact=category_name)
            posts = posts.filter(category=category)
        except PostCategory.DoesNotExist:
            category = PostCategory(name=category_name)
            posts = Post.objects.none()

    posts = posts.order_by("-create")
    return category, posts

def get_categories():
    categories = list(PostCategory.objects.all().order_by("name"))
    categories.insert(0, post_category_all)
    return categories

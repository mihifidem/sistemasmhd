from django.db.models import Count, Q

from .models import BlogCategory


def blog_nav_categories(request):
    is_distributor = False
    if request.user.is_authenticated:
        profile = getattr(request.user, 'distributor_profile', None)
        is_distributor = bool(profile and profile.is_approved)

    visible_posts_filter = Q(posts__is_published=True)
    if not is_distributor:
        visible_posts_filter &= Q(posts__distributors_only=False)

    categories = (
        BlogCategory.objects.annotate(visible_posts_count=Count('posts', filter=visible_posts_filter))
        .filter(visible_posts_count__gt=0)
        .order_by('name')
    )

    return {'blog_nav_categories': categories}

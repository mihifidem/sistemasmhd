from django.shortcuts import get_object_or_404, render

from .models import BlogCategory, BlogPost


def _is_approved_distributor(user):
    if not user.is_authenticated:
        return False
    profile = getattr(user, 'distributor_profile', None)
    return bool(profile and profile.is_approved)


def post_list(request):
    is_distributor = _is_approved_distributor(request.user)
    category_slug = request.GET.get('category', '').strip()
    qs = BlogPost.objects.filter(is_published=True).select_related('category')
    if not is_distributor:
        qs = qs.filter(distributors_only=False)

    selected_category = None
    if category_slug:
        selected_category = BlogCategory.objects.filter(slug=category_slug).first()
        if selected_category:
            qs = qs.filter(category=selected_category)

    return render(
        request,
        'blog/list.html',
        {
            'posts': qs,
            'is_distributor': is_distributor,
            'selected_category': selected_category,
        },
    )


def post_detail(request, slug):
    post = get_object_or_404(BlogPost.objects.select_related('category'), slug=slug, is_published=True)
    if post.distributors_only and not _is_approved_distributor(request.user):
        from django.http import Http404
        raise Http404
    return render(request, 'blog/detail.html', {'post': post})

from django.shortcuts import get_object_or_404, render

from .models import BlogPost


def _is_approved_distributor(user):
    if not user.is_authenticated:
        return False
    profile = getattr(user, 'distributor_profile', None)
    return bool(profile and profile.is_approved)


def post_list(request):
    is_distributor = _is_approved_distributor(request.user)
    qs = BlogPost.objects.filter(is_published=True)
    if not is_distributor:
        qs = qs.filter(distributors_only=False)
    return render(request, 'blog/list.html', {'posts': qs, 'is_distributor': is_distributor})


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    if post.distributors_only and not _is_approved_distributor(request.user):
        from django.http import Http404
        raise Http404
    return render(request, 'blog/detail.html', {'post': post})

def distributor_context(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user, 'distributor_profile', None)
    return {'distributor_profile': profile}
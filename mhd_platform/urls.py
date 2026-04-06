from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.templatetags.static import static as static_url
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=static_url('img/favicon.svg'), permanent=False)),
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('distributors/', include('distributors.urls')),
    path('orders/', include('orders.urls')),
    path('invoices/', include('invoices.urls')),
    path('blog/', include('blog.urls')),
    path('support/', include('support.urls')),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

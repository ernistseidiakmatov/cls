from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView 
from django.conf import settings
from django.conf.urls.static import static
from core.views import signup
from core.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls'), name="core"),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("", home, name="home"),
    # path('files/', files, name='files'),
    path('files/<path:folder_path>/', files_detail, name='files_detail'),
    path('signup/', signup, name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # 这里会包含 core 应用的所有路由
    path('accounts/', include('django.contrib.auth.urls')),  # 确保这里的路径存在
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
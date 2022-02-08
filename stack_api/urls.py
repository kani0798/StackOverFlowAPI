"""stack_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import ProblemViewSet

router = DefaultRouter()
router.register('problems', ProblemViewSet)

# problems/ - GET - Problem.objects.all()
# problems/2/ - GET - Problem.objects.get(2)
# problems/ - POST - Problem.objects.create
# problems/2/ - PUT - update
# problems/2/ - PATCH - partial_update
# problems/2/ - DELETE Problem.objects.get(2).delete()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

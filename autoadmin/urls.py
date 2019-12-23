"""autoadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from users.router import user_router
from groups.router import group_router
from servicetree.router import servicetree_router
from pms.router import pms_router
from clouds.router import clouds_router

schema_view = get_schema_view(title='API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

router = DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(group_router.registry)
router.registry.extend(servicetree_router.registry)
router.registry.extend(pms_router.registry)
router.registry.extend(clouds_router.registry)


urlpatterns = [
    url(r'^salt/', include('salt.urls')),
    url(r'^docs/$', schema_view, name='docs'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
]
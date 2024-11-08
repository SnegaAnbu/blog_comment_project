from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostListCreateView, PostDetailView
from django.urls import path
from .views import RegisterView, login_view
from . import views
router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),  # All your API routes will be prefixed with /api/
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail')
]



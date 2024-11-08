from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.forms import UserCreationForm

# Registration API: Create a new user
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create a token for the new user
            token = Token.objects.create(user=user)
            return Response({
                "user": serializer.data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login API: Authenticate a user and return a token
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user using the credentials provided
    user = authenticate(username=username, password=password)
    if user is not None:
        # Generate or get the token for the authenticated user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })
    else:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Assign the post author as the currently authenticated user
        serializer.save(author=self.request.user)

# Retrieve, Update, and Delete a Post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({"detail": "You do not have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({"detail": "You do not have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)
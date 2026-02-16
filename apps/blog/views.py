from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse


from apps.blog.models import Post, CustomUser, Category, Tag

class PostAPIView(APIView):
    def get(self, request: DRFRequest) -> DRFResponse:
        """Create response for GET requests"""

        post_list = Post.objects.all().values()

        return DRFResponse({"posts" : list(post_list)})
    
    def post(self, request: DRFRequest) -> DRFResponse:
        """Function that processes POST requets"""
        author=request.data['author'] 
        category_name=request.data['category']
        tag_names=request.data['tags']

        tags = list(Tag.objects.filter(name__in=tag_names))
        
        user = CustomUser.objects.filter(email=author).first()
        category = Category.objects .filter(name=category_name).first() 
        post_new = Post.objects.create(
            author=user,
            title=request.data['title'],
            body=request.data['body'],
            category=category,
            status=request.data['status'],
        )
        
        post_new.tags.set(tags)

         
        return DRFResponse({"post": model_to_dict(post_new)})


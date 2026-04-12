import json

from asgiref.sync import async_to_sync 
from channels.generic.websocket import WebsocketConsumer

from apps.blog.models import Post

class CommentsConsumer(WebsocketConsumer):
    def connect(self):
        self.post_slug = self.scope["url_route"]["kwargs"]["slug"]        
        self.post_group_name = f"post_{self.post_slug}"

        exists = Post.objects.filter(slug=self.post_slug, deleted_at__isnull=True).exists()

        self.accept()
        
        if not exists:
            self.close(code=4004)
            return

        async_to_sync(self.channel_layer.group_add)(
            self.post_group_name, self.channel_name
        )

 

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.post_group_name, self.channel_name
        )
    
    def post_comment(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"message": message}))
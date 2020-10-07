
from django.conf.urls import url
#it is same as in chat/urls.py --can use url or re_path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    # dont write other than websocket it may not work
     
    #ALLOWED_HOSTS = ['*'] I use * for this--for all validation in setting .py
    # I want user to be inside websocket AuthMiddlewareStack allows this
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
            
                [
                    url(r"^messages/(?P<username>[\w.@+-]+)", ChatConsumer),#this url must match with chat/urls.py
                    # url('messages/username/',ChatConsumer) ---->This might give error sometimes
                ]
            )
            
        )
         
    )
    
    # ws://domain/<username> is our websocket connection
    
    
    
    # Empty for now (http->django views is added by default)
})
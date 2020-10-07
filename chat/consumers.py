
#consumers is like views
import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer

from channels.db import database_sync_to_async

from .models import Thread, ChatMessage



class ChatConsumer(AsyncConsumer):
  
    #request handlers funations blc multiple request can come
    async def websocket_connect(self, event):
     
        print("connected", event)
        # await is used for async i.e means execute that code and wait for the finished
        await self.send({
            "type":"websocket.accept",
            
        })
        
        other_user = self.scope['url_route']['kwargs']['username']#kwargs come from the path routing.py==>It gives other user name--other user i.e from login i.enirmal123
        me = self.scope['user']#this is the admin i.e me--i.e.admin is chatting with user other_user i.e nirmal123
        # print(other_user,me)
        thread_obj = await self.get_thread(me,other_user)
        print(thread_obj)#thread object according to other_user--each_other_user has thread object
        #below making chat room based on object id
        
        self.thread_obj = thread_obj #after this then write 
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
      
        await self.channel_layer.group_add(
              #group_add is itself a chat room
              #for this there should be channels layer in settings.py
              
            chat_room,#this does not have to be unique though it functions like unique =>you can have your multiple user in that chatroom
            self.channel_name#channel_room is the default attribute of channels
            
        )
        
        
        # print(other_user,me)
        #here event is conneted if want to disconnected after connected then use sleep below
        # await asyncio.sleep(5)#5 sec
        # await self.send({
        #     # "type":"websocket.close",#in 10 sec event is disconnected--if i dont disconnect or .close then i dont need sleep
            
            
        #     "type":"websocket.send",
        #     "text":"Hello world"#sending msg to the browser
            
        # })
            
        
        
    async def websocket_receive(self, event):
        print("received from browser", event)
        #websocket_receive map to websocket.receive <==> if websocket_receive2 then dont map
        # received from browser {'type': 'websocket.receive', 'text': '{"message":"How can i help you?"}'}
        #the received text is python dictionary send from browser
        
        front_text = event.get('text',None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            # print(msg)
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username#its output is admin--user bhitra ko username
                # username = user.password then it gives secrete key
            
            
            myResponse = {
                #Dont require this when create a chat room using redis and also remove  chatHolder.append("<li>" + msgText + " via " + me + "</li>") in thread.html
                # 'message': "This is instant message(It is sent from websocket_receive in consumers.py)",
               'message':msg,
                 'username':username
            }
            
            """
            -----------------------------------------------
            I use this before i use chatroom and redis
            -------------------------------------------------
            await self.send({
                 "type":"websocket.send",
                #  "text":msg
                "text":json.dumps(myResponse)#convert to json from python and send to browser
             })
            """
            
            await self.create_chat_message(user, msg)
            #sent via layer in a group--I write this after i create chat_room in websocket_connect
            #this broadcast the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"chat_message",
                    # "message":"Hey nirmall"    check whether chat_mesasge is working or not  
                    "text":json.dumps(myResponse)
                
                 }
            )
            
            
            
     #send the actual message
     #this funciton supports for all the member of the group
    async def chat_message(self,event):
       
        # print('message', event) 
        await self.send({
            "type":"websocket.send",
            "text":event['text']#it call the above event    "text":json.dumps(myResponse)  above in chat_room
        }) 
            
            
            
    async def websocket_disconnect(self,event):
        print("disconnected", event)
        
        
    @database_sync_to_async#grab data from Thread model or method 
    def get_thread(self,user,other_username):
        return Thread.objects.get_or_new(user, other_username)[0]#first value
    
    
    #saves data written at last of the project
    @database_sync_to_async
    def create_chat_message(self, me, msg):
        thread_obj = self.thread_obj#write this only after  self.thread_obj = thread_obj in line 33
        # me         = self.scope['user']#instead of this 
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)#create object
    
    
    
    
        
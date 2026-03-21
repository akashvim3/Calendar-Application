"""
Chat WebSocket consumer for real-time communication.
Handles incoming messages and broadcasts AI responses.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatSession, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    """Consumer for real-time chat with AI."""
    
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'chat_{self.session_id}'
        self.user = self.scope['user']

        # Check if user is authenticated
        if not self.user.is_authenticated:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '').strip()
            
            if not message:
                return

            # Save user message to database
            user_message = await self.save_message(message, is_user_message=True)
            
            # Send user message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': 'user',
                    'message_id': str(user_message.id),
                }
            )
            
            # Simulate thinking and send AI response (placeholder)
            # In a real implementation, this would call an AI service
            ai_response = f"I received your message: '{message}'. This is a simulated AI response."
            
            # Save AI message to database
            ai_message = await self.save_message(ai_response, is_user_message=False)
            
            # Send AI response to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': ai_response,
                    'sender': 'assistant',
                    'message_id': str(ai_message.id),
                }
            )
                
        except json.JSONDecodeError:
            pass
        except Exception as e:
            # Send error message
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': 'Sorry, I encountered an error processing your message.',
                    'sender': 'assistant',
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        message_id = event.get('message_id', '')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'message_id': message_id,
        }))

    @database_sync_to_async
    def save_message(self, content, is_user_message):
        """Save message to database."""
        # Get or create chat session
        session, created = ChatSession.objects.get_or_create(
            session_id=self.session_id,
            defaults={
                'user': self.user,
                'title': content[:50] + '...' if len(content) > 50 else content,
                'is_archived': False
            }
        )
        
        # Determine role based on is_user_message flag
        role = 'user' if is_user_message else 'assistant'
        
        # Create message
        message = ChatMessage.objects.create(
            session=session,
            role=role,
            content=content
        )
        
        # Update session timestamp
        session.save()
        
        return message

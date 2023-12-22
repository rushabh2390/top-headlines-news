# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from news.models import News
from .serializers import NewsSerializer
from asgiref.sync import sync_to_async
from dateutil import parser

class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room or accept the connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room or close the connection
        pass

    def get_news_datas(self, check_date=None):
        if check_date:
            return News.objects.filter(publisher_date__date=check_date.date()).select_related('country').all()
        else:
            return News.objects.select_related('country').all().order_by("-publisher_date")

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = {}
        news_datas = None
        if text_data:
            text_data_json = json.loads(text_data)
        check_date = text_data_json.get("date", None)
        if not check_date:
            is_all_headlines = text_data_json.get("all_headlines", False)
        else:
            check_date = parser.parse(check_date)
            print("check date",check_date.date())
        if check_date or is_all_headlines:
            news_datas = await sync_to_async(self.get_news_datas)(check_date)
        is_data = await self.check_empty(news_datas)
        if is_data:
            for news_data in news_datas:
                response = {
                "success": True,
                "messege": NewsSerializer(news_data).data
                }
                await self.send(text_data=json.dumps(response))

        else:
            response = {
                "success": False,
                "messege": f"No  data found for that date {check_date}"
            }
            await self.send(text_data=json.dumps(response))

    @sync_to_async
    def check_empty(self, result):
        return bool(result)

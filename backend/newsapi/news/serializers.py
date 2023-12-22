from rest_framework import serializers
from .models import News
from country.serializers import CountrySerializer
class NewsSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = News
        fields = ['id','title', 'description', 'publisher_date', 'author', 'news_url','image_url','country','content']

class MultipleNewsSerializer(serializers.ListSerializer):
    child = NewsSerializer()

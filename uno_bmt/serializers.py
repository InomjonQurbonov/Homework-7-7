from rest_framework import serializers
from .models import WorldNews, Members


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id', 'member_name', 'member_added_date']


class MembersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id', 'member_name', 'member_added_date']


class CreateMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id', 'member_name', 'member_added_date']


class UpdateMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id', 'member_name', 'member_added_date']


class DeleteMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id',]


class WorldNewsSerializer(serializers.ModelSerializer):
    news_details_url = serializers.SerializerMethodField('get_details')
    news_info = serializers.SerializerMethodField('get_news_info')

    def get_news_info(self, object):
        return object.news_areas.member_name

    def get_details(self, instance):
        return f"http://127.0.0.1:8000/api/v1/worldnews/{instance.pk}"

    class Meta:
        model = WorldNews
        fields = ['id', 'news_title', 'news_author', 'news_image', 'news_areas', 'news_details_url', 'news_info']


class NewsDetailsSerializer(serializers.ModelSerializer):
    models = WorldNewsSerializer(many=True, read_only=True, source='worldnews')

    class Meta:
        model = WorldNews
        fields = '__all__'


class UpdateNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldNews
        fields = ['id', 'news_title', 'news_author', 'news_image', 'news_areas']


class DeleteNewsSerializer(serializers.Serializer):
    def delete(self, instance):
        instance.delete()

    class Meta:
        model = WorldNews
        fields = ['id']


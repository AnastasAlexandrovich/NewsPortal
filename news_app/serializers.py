from rest_framework import serializers
from news_app.models import User, Item, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ItemForViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class CommentForViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'body')

    def create(self, validated_data):
        return Item.objects.create(
            title=validated_data['title'],
            body=validated_data['body'],
            user=validated_data['user']
        )

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.body = validated_data['body']
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body',)

    def create(self, validated_data):
        return Comment.objects.create(
            item=validated_data['item'],
            user=validated_data['user'],
            body=validated_data['body']
        )

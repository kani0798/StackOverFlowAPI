from rest_framework import serializers

from main.models import Problema, CodeImage, Reply, Comment


class CodeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image',)

    def _get_image_url(self, instance):
        if instance.image:
            url = instance.image.url
            return 'localhost:8000' + url

    def to_representation(self, instance):
        representation = super(CodeImageSerializer, self).to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class ProblemaSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Problema
        fields = "__all__"
        # exclude = ('author',)

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES
        author = request.user
        problem = Problema.objects.create(author=author,
                                          **validated_data)
        for image in images.getlist('images'):
            CodeImage.objects.create(image=image,
                                     problema=problem)
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        images = request.FILES
        for key,value in validated_data.items():
            setattr(instance, key, value)
        if images.getlist('new_images'):
            instance.images.all().delete()
            for image in images.getlist('new_images'):
                CodeImage.objects.create(image=image,
                                         problema=instance)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = CodeImageSerializer(instance.images.all(),
                                                       many=True).data
        action = self.context.get('action')
        if action == 'list':
            representation['replies'] = instance.replies.count()
        else:
            representation['replies'] = ReplySerializer(instance.replies.all(),
                                                    many=True).data
        return representation


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Reply
        fields = "__all__"

    def create(self, validated_data):
        author = self.context.get('request').user
        reply = Reply.objects.create(author=author,
                                     **validated_data)
        return reply

    def to_representation(self, instance):
        representation = super(ReplySerializer, self).to_representation(instance)
        representation['likes'] = instance.likes.count()
        action = self.context.get('action')
        if action == 'list':
            representation['comments'] = instance.commenty.count()
        else:
            representation['comments'] = CommentSerializer(instance.commenty.all(),
                                                           many=True).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        author = self.context.get('request').user
        comment = Comment.objects.create(author=author,
                                     **validated_data)
        return comment

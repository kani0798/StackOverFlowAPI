from rest_framework import serializers

from main.models import Problema, CodeImage


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
        return representation


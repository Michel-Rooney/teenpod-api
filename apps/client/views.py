import os

from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers
from . import utils


class UserViewSets(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def perform_destroy(self, instance):
        if instance.avatar:
            os.remove(instance.avatar.path)
        return super().perform_destroy(instance)

    @action(['get'], False)
    def me(self, request, *args, **kwargs):
        obj = get_object_or_404(models.User, id=request.user.id)
        serializers = self.get_serializer(
            instance=obj
        )
        return Response(serializers.data)


class CommentViewSets(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save()

        params = self.request.query_params
        is_comment = params.get('comment', 'False')
        id_entity = self.request.POST.get('entity', '')

        if is_comment not in ['True', 'False']:
            raise ValidationError({
                'detail': 'Digite apenas True ou False'
            })

        entity = utils.get_podcast(id=id_entity)

        if is_comment == 'True':
            entity = utils.get_comment(id=id_entity)

        entity.comments.add(serializer.instance)
        return serializer

    @action(['get'], detail=True)
    def like(self, request, pk=None):
        obj = get_object_or_404(models.Podcast, pk=pk)

        if request.user in obj.users_liked.all():
            raise ValidationError({
                'detail': 'Usuário já deu like.'
            })

        obj.likes += 1
        obj.users_liked.add(request.user.id)
        obj.users_disliked.remove(request.user.id)

        return Response(status=status.HTTP_200_OK)

    @action(['get'], detail=True)
    def deslike(self, request, pk=None):
        obj = get_object_or_404(models.Podcast, pk=pk)

        if request.user in obj.users_disliked.all():
            raise ValidationError({
                'detail': 'Usuário já deu like.'
            })

        if not obj.likes <= 0:
            obj.likes -= 1
        obj.users_disliked.add(request.user.id)
        obj.users_liked.remove(request.user.id)

        return Response(status=status.HTTP_200_OK)


class PodcastViewSets(ModelViewSet):
    queryset = models.Podcast.objects.all()
    serializer_class = serializers.PodcastSerializer

    def perform_destroy(self, instance):
        if instance.cover:
            os.remove(instance.cover.path)

        if instance.audio:
            os.remove(instance.audio.path)
        return super().perform_destroy(instance)

    @action(['get'], detail=True)
    def like(self, request, pk=None):
        obj = get_object_or_404(models.Podcast, pk=pk)

        if request.user in obj.users_liked.all():
            raise ValidationError({
                'detail': 'Usuário já deu like.'
            })

        obj.likes += 1
        obj.users_liked.add(request.user.id)

        return Response(status=status.HTTP_200_OK)

    @action(['get'], detail=True)
    def dislike(self, request, pk=None):
        obj = get_object_or_404(models.Podcast, pk=pk)

        if request.user in obj.users_disliked.all():
            raise ValidationError({
                'detail': 'Usuário já deu like.'
            })

        if not obj.likes <= 0:
            obj.likes -= 1
        obj.users_disliked.add(request.user.id)

        return Response(status=status.HTTP_200_OK)

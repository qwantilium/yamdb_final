from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta():
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta():
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'category',
        )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True,
    )

    class Meta():
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'category', 'genre'
        )

    def validate(self, data, *args, **kwargs):
        if not self.partial and not data['genre']:
            raise serializers.ValidationError({
                'error': 'Вы не указали ни одного жанра!',
            })
        return data


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')


class UserViewSetSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta():
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            id_title = self.context[
                'request'].parser_context['kwargs']['title_id']
            title = get_object_or_404(Title, pk=id_title)
            if title.reviews.filter(
                    author=self.context['request'].user
            ).exists():
                raise serializers.ValidationError(
                    {
                        'error':
                            'Вы уже оставили отзыв на это произведение!'
                    }
                )
            return data
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta():
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment

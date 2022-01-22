from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMINISTRATOR = 'admin'
    # django 2.2.16
    # Согласно документации так, можем переделать по теории практикума,
    # но там при изменении строк будем менять код везде

    AccessGroup = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMINISTRATOR, 'admin'),
    ]

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=9, choices=AccessGroup,
                            default=USER)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        validators=[
            username_validator,
            RegexValidator(
                '^me$',
                inverse_match=True,
                message='me не может быть использованно в качестве username'
            )
        ],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )

    @property
    def is_administrator(self):
        if self.role:
            return self.role == self.ADMINISTRATOR
        return False

    @property
    def is_moderator(self):
        if self.role:
            return self.role == self.MODERATOR
        return False

    class Meta():
        ordering = ('username',)

    def __str__(self):
        return (
            f'Пользователь: {self.username}. Электронная почта: {self.email}.'
            f'({self.role})'
        )


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50, unique=True,
        validators=[
            RegexValidator(
                '^[-a-zA-Z0-9_]+$',
                message='Slug name must contain only letters, numbers and "_"'
            )
        ]
    )

    class Meta():
        ordering = ('-name',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50, unique=True,
        validators=[
            RegexValidator(
                '^[-a-zA-Z0-9_]+$',
                message='Slag name must contain only letters, numbers and "_"'
            )
        ]
    )

    class Meta():
        ordering = ('-name',)

    def __str__(self):
        return self.slug


class GenreTitle(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='genres_of_title',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles_by_genre',
    )

    class Meta():
        ordering = ('title',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre'
            )
        ]

    def __str__(self):
        return self.title.name + ' - ' + self.genre.slug


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.SmallIntegerField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles')
    genre = models.ManyToManyField(Genre, through=GenreTitle)

    class Meta():
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=datetime.today().year + 10),
                name='A year is valid this year plus 10',
            )
        ]
        ordering = ('id',)

    def __str__(self):
        return (
            f'{self.name} ({self.year}) - {self.category.name} - {self.genre}'
        )

    @property
    def rating(self):
        output = self.reviews.aggregate(models.Avg('score')).get('score__avg')
        if output:
            return round(output, 1)
        return None


def no_future_date(value):
    today = datetime.today()
    if value > today:
        raise ValidationError('Добавили дату из будущего,'
                              ' прости Марти, но не сегодня')


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews', null=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews', null=True)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'review_pub_date', auto_now_add=True, db_index=True,
        validators=[no_future_date]
    )
    score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__gte=0) & models.Q(score__lte=10),
                name='A score value is valid between 0 and 10',
            ),
            models.UniqueConstraint(
                fields=['author', 'title_id'],
                name='unique_title_author'
            ),
        ]
        ordering = ('pub_date',)

    def __str__(self):
        return (
            f'Пользователь - {self.author.username} '
            f'про произведение {self.title.name} ({self.title.year}), '
            f'время публикации {self.pub_date.isoformat(timespec="minutes")}: '
            f'{self.text}'
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'comment_pub_date', auto_now_add=True, db_index=True
    )

    class Meta():
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text

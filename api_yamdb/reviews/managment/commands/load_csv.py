import csv

from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


class Command(BaseCommand):
    help = 'Load data from directory with specific csv files'

    def final_save(self, file, new_files, model):
        try:
            model.objects.bulk_create(new_files)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully load {file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error while importing data form {file}: {e}'
                )
            )

    def get_link(self, file, directory):
        return [directory + '/' + file, file]

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def handle(self, directory: str, *args, **options):

        new_files = []
        link, file = self.get_link('category.csv', directory)
        print(self.get_link('category.csv', directory))
        with open(link, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            new_files = [
                Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                for row in reader
            ]
        self.final_save(file, new_files, Category)

        new_files = []
        link, file = self.get_link('titles.csv', directory)
        with open(link, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            new_files = [
                Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),
                )
                for row in reader
            ]
        self.final_save(file, new_files, Title)

        new_files = []
        link, file = self.get_link('users.csv', directory)
        with open(link, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            new_files = [
                User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
                for row in reader
            ]
        self.final_save(file, new_files, User)

        new_files = []
        link, file = self.get_link('genre.csv', directory)
        with open(link, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            new_files = [
                Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                for row in reader
            ]
        self.final_save(file, new_files, Genre)

        new_files = []
        link, file = self.get_link('genre_title.csv', directory)
        with open(link, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            new_files = [
                GenreTitle(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    genre=Genre.objects.get(id=row['genre_id']),
                )
                for row in reader
            ]
        self.final_save(file, new_files, GenreTitle)

        new_files = []
        link, file = self.get_link('review.csv', directory)
        with open(link, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            new_files = [
                Review(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                for row in reader
            ]
        self.final_save(file, new_files, Review)

        new_files = []
        link, file = self.get_link('comments.csv', directory)
        with open(link, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            new_files = [
                Comment(
                    id=row['id'],
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date'],
                )
                for row in reader
            ]
        self.final_save(file, new_files, Comment)

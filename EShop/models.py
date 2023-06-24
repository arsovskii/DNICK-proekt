import math

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Avg
from star_ratings.models import Rating


# Create your models here.
class SiteUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    importance = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Product(models.Model):
    developer = models.ForeignKey('DeveloperUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    descriptionImage = models.ImageField()
    longDescription = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    price = models.IntegerField()
    discount = models.IntegerField()
    titleImage = models.ImageField()

    windows = models.BooleanField()
    linux = models.BooleanField()
    apple = models.BooleanField()

    popularity = models.IntegerField()
    approved = models.BooleanField()

    files = models.FileField()

    ratings = GenericRelation(Rating, related_query_name='rated')

    releaseDate = models.DateField(auto_now=True)

    def price_with_discount(self):
        return math.floor(self.price - self.price * (self.discount / 100))


    def numOwners(self):
        return self.bought_games.count()

    def __str__(self):
        return f"{self.name} by {self.developer}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()


class BuyerUser(SiteUser):
    games = models.ManyToManyField(Product, related_name="bought_games")
    profilePicture = models.ImageField("/profilePictures", default="default.jpg")


class DeveloperUser(BuyerUser):
    pass

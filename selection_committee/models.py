# from typing import Any, Union

from django.db import models
# from django.db.models.aggregates import Count
# from random import randint


# Create your models here.
# class RandomManager(models.Manager):
#     def random(self):
#         count = self.aggregate(count=Count('id'))['count']
#         random_index = randint(0, count - 1)
#         return self.get(id=random_index)


class Youngling(models.Model):
    name = models.CharField(max_length=200)
    planet_habitat = models.ForeignKey('Planet', on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField()
    teacher = models.ForeignKey('Jedi', on_delete=models.CASCADE, related_name='Younglings', null=True, blank=True)


class Order(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(unique=True, max_length=50)


class Jedi(models.Model):
    name = models.CharField(max_length=200)
    planet_stud = models.ForeignKey('Planet', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Planet(models.Model):
    name = models.CharField(max_length=50)


class Test(models.Model):
    orders_code = models.ForeignKey(Order, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question', through='QAns', through_fields=('test', 'question'))
    youngling = models.OneToOneField(Youngling, on_delete=models.CASCADE, null=True, blank=True)


class Question(models.Model):
    description = models.TextField()


class QAns(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.NullBooleanField()

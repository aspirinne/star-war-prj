from django.db import models


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

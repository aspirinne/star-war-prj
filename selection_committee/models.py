from django.db import models


class Youngling(models.Model):
    """
    Model of Youngling.
    Prospective jedi. He could get the teacher from among the Jedies.
    It include foreign key (teacher) to Jedi model and foreign key (planet_habitat) for Planet model.
    """
    name = models.CharField(max_length=200)
    planet_habitat = models.ForeignKey('Planet', on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField()
    teacher = models.ForeignKey('Jedi', on_delete=models.CASCADE, related_name='Younglings', null=True, blank=True)


class Order(models.Model):
    """
    Model of Jedi Orders.
    It's like Masonic Order, but with spaceships and Samuel L Jackson.
    """
    name = models.CharField(max_length=50)
    code = models.CharField(unique=True, max_length=50)


class Jedi(models.Model):
    """
    Model of Jedi.
    It include foreign keys (planet_stud) to Planet model and (order) to Order model
    """
    name = models.CharField(max_length=200)
    planet_stud = models.ForeignKey('Planet', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Planet(models.Model):
    """
    Model of Planet
    """
    name = models.CharField(max_length=50)


class Test(models.Model):
    """
    Model of Personal Test for Youngling.
    It is connected with One-to-One relationship with the youngling for which it was generated.
    It include the questions as Many-to-Many relationship with Question model.
    """
    orders_code = models.ForeignKey(Order, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question', through='QAns', through_fields=('test', 'question'))
    youngling = models.OneToOneField(Youngling, on_delete=models.CASCADE, null=True, blank=True)


class Question(models.Model):
    """
    Model of Question
    """
    description = models.TextField()


class QAns(models.Model):
    """
    Intermediate model, which links the Test and Question models.
    It was necessary to hold the answers for questions in Test
    """
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.NullBooleanField()

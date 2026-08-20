from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )

class Profile(models.Model):
        customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name="profile"
    )

        bio = models.TextField()
        address = models.CharField(max_length=200)

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)

    courses = models.ManyToManyField(
        Course,
        related_name="students"
    )

    def __str__(self):
        return self.name
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=2000, null=True, blank=True)
    is_published = models.BooleanField(default=False, blank=True)
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name


# class Selection(models.Model):
#     name = models.CharField(max_length=25)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     items = models.ManyToManyField(Ad)
#
#     class Meta:
#         verbose_name = 'Подборка'
#         verbose_name_plural = 'Подборки'
#
#     def __str__(self):
#         return self.name

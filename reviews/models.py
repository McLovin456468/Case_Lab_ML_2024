from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=200)  # Заголовок отзыва
    content = models.TextField()               # Содержание отзыва
    rating = models.IntegerField()              # Рейтинг (от 1 до 10)
    status = models.CharField(max_length=20)   # Статус отзыва (положительный/отрицательный)

    def __str__(self):
        return self.title

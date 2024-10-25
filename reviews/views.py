from .models import Review
import joblib
from django.conf import settings
import os

def decode_labels(combined_labels):
    statuses = []
    ratings = []
    for label in combined_labels:
        if label > 10:  # Отрицательные отзывы
            statuses.append('Negative')  # 0 - отрицательный
            ratings.append(label - 10)  # Рейтинг от 1 до 4
        else:  # Положительные отзывы
            statuses.append('Positive')  # 1 - положительный
            ratings.append(label)  # Рейтинг от 5 до 10
    return statuses, ratings

def predict_review(review):
    model_path = os.path.join(settings.BASE_DIR, 'reviews', 'sentiment_model.pkl')
    model = joblib.load(model_path)
    predicted_label = model.predict([review])[0]
    predicted_statuses, predicted_ratings = decode_labels([predicted_label])
    return predicted_statuses[0], predicted_ratings[0]



def submit_review(request):
    if request.method == 'POST':
        # Получение данных формы
        title = request.POST.get('title')
        content = request.POST.get('content')

        status, rating = predict_review(content)


        # Создание и сохранение нового отзыва
        review = Review(title=title, content=content, rating=rating, status=status)
        review.save()

        # Передача данных в шаблон 'review_success'
        return render(request, 'reviews/review_success.html', {'review': review})
    return render(request, 'reviews/submit_review.html')

from django.shortcuts import render

def review_success(request):
    return render(request, 'reviews/review_success.html')
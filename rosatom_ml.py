import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score
import joblib

def load_data(folder_path):
    texts = []
    combined_labels = []

    for sentiment in ['pos', 'neg']:
        sentiment_path = os.path.join(folder_path, sentiment)
        for filename in os.listdir(sentiment_path):
            if filename.endswith('.txt'):
                with open(os.path.join(sentiment_path, filename), 'r', encoding='utf-8') as file:
                    text = file.read().strip()
                    rating = int(filename.split('_')[1].split('.')[0])

                    # Объединяем статус и рейтинг
                    if sentiment == 'pos':
                        label = rating  # Для положительных отзывов
                    else:
                        label = rating + 10  # Для отрицательных отзывов (11-14)

                    texts.append(text)
                    combined_labels.append(label)

    return texts, combined_labels

train_texts, train_labels = load_data('train')
test_texts, test_labels = load_data('test')

model = make_pipeline(
    TfidfVectorizer(max_features=50000, max_df=0.95, min_df=2),
    LinearSVC()
)
model.fit(train_texts, train_labels)

# Сохраняем модель и векторизатор
joblib.dump(model, 'sentiment_model.pkl')

def decode_labels(combined_labels):
    statuses = []
    ratings = []
    for label in combined_labels:
        if label > 10:  # Отрицательные отзывы
            statuses.append(0)  # 0 - отрицательный
            ratings.append(label - 10)  # Рейтинг от 1 до 4
        else:  # Положительные отзывы
            statuses.append(1)  # 1 - положительный
            ratings.append(label)  # Рейтинг от 5 до 10
    return statuses, ratings

def predict_review(review):
    predicted_label = model.predict([review])[0]
    predicted_statuses, predicted_ratings = decode_labels([predicted_label])
    return predicted_statuses[0], predicted_ratings[0]

# Основной цикл для пользовательского ввода
while True:
    user_input = input("Введите отзыв о фильме (или 'exit' для выхода): ")
    if user_input.lower() == 'exit':
        break

    status, rating = predict_review(user_input)
    print(f"Predicted Sentiment: {'Positive' if status == 1 else 'Negative'}, Predicted Rating: {rating}")

# Для загрузки модели позже можно использовать:
# model = joblib.load('sentiment_model.pkl')



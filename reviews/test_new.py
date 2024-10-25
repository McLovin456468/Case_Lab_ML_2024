import joblib
model = joblib.load('sentiment_model.pkl')
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
    predicted_label = model.predict([review])[0]
    predicted_statuses, predicted_ratings = decode_labels([predicted_label])
    return predicted_statuses[0], predicted_ratings[0]

# Основной цикл для пользовательского ввода
while True:
    user_input = input("Введите отзыв о фильме (или 'exit' для выхода): ")
    if user_input.lower() == 'exit':
        break

    status, rating = predict_review(user_input)
    print(f"Predicted Sentiment: {status}, Predicted Rating: {rating}")
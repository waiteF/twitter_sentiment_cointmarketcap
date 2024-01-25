# Імпорт необхідних модулів та класів
from fastapi import FastAPI
from api_class import CoinmarketcapHandler, CryptoReport

# Інстанціювання класу CryptoReport
report = CryptoReport()

# Створення FastAPI додатку
app = FastAPI()

# Імпорт TensorFlow та необхідних компонентів для аналізу настрою
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle

# Активація спрощеного виконання для TensorFlow
tf.config.run_functions_eagerly(True)

# Завантаження моделі аналізу настрою та токенізатора
model = load_model("C:\\Users\\Waite\\Desktop\\project\\Sentiment_CNN_model.h5")
MAX_SEQUENCE_LENGTH = 300

with open("C:\\Users\\Waite\\Desktop\\project\\tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)

# Функція для передбачення настрою на основі текстового вводу
def predict(text):

    x_test = pad_sequences(
        tokenizer.texts_to_sequences([text]), maxlen=MAX_SEQUENCE_LENGTH
    )
# Передбачення настрою та визначення мітки настрою на основі результату
    score = model.predict(x_test)[0][0]  
    if 0.4 <= score <= 0.6:
        label = "Neutral"
    elif score < 0.4:
        label = "Negative"
    else:
        label = "Positive"

    return {"label": label, "score": float(score)}

# Кореневий шлях
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Передбачення настрою для заданого тексту
@app.get("/test_predict/{text}")
def predict_sentiment(text: str):
    result = predict(text)
    return result

# Основна функція передбачення настрою для заданого тексту та показника gain_top_twenty
@app.get("/predict/{text}")
def main_predict(text: str):
    try:
        # Отримання даних звіту та результату передбачення
        gain_top_twenty = report.gain_top_twenty_currencies()
        result = predict(text)
        print("gain_top_twenty - " + str(gain_top_twenty))
        print("score" + str(result["score"]))
        if gain_top_twenty > 0 and float(result["score"]) > 0.45:
            return "Positive"
        else:
            return "Negative"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Отримання найбільш торгованої валюти
@app.get("/crypto_reports/most_traded")
def get_most_traded_currency():
    try:
        return str(report.reports['most traded']['symbol'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Отримання найкращих десяти валют
@app.get("/crypto_reports/best_ten")
def get_best_ten_currencies():
    try:
        list_temp = []
        for currency in report.reports['best 10']:
            list_temp.append(str(currency['symbol']))
        return list_temp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Отримання найгірших десяти валют
@app.get("/crypto_reports/worst_ten")
def get_worst_ten_currencies():
    try:
        list_temp = []
        for currency in report.reports['worst 10']:
            list_temp.append(str(currency['symbol']))
        return list_temp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Отримання обсягів для перших двадцяти валют
@app.get("/crypto_reports/amount_top_twenty")
def get_amount_top_twenty():
    try:
        amount_top_twenty = report.amount_top_twenty_currencies()
        return {"amount_top_twenty": amount_top_twenty}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Отримання обсягів за торговими обсягами
@app.get("/crypto_reports/amount_by_volumes")
def get_amount_by_volumes():
    try:
        amount_by_volumes = report.amount_by_volumes_currencies()
        return {"amount_by_volumes": amount_by_volumes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Отримання прибутку для перших двадцяти валют
@app.get("/crypto_reports/gain_top_twenty")
def get_gain_top_twenty():
    try:
        gain_top_twenty = report.gain_top_twenty_currencies()
        return {"gain_top_twenty": gain_top_twenty}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
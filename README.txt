Перед тим , як використовувати додаток потрібно встановити залежності файл (requirements.txt) 
pip install -r requirements.txt

запустити uvicore 
uvicorn main:app --reload 


структура:

main.py - опис всіх головних API методів FastAPI, та інтеграція ШІ
api_class.py - підключення до Coinmarketcap.

Sentiment_CNN_model.h5 - ваги моделі (Saved)
tokenizer.pickle Токенізатор використовується для розбиття
тексту на окремі елементи, такі як слова або фрази, і може бути корисним при обробці текстових даних.

requirements.txt - залежності
![](frontend%2Fpublic%2Ffavicon.ico)


## Проект Лояльность 2.0


#### 1. Описание проекта

Сервис прогнозирования оттока банковских клиентов


#### 2. Стек технологий проекта

- backend: FastAPI, SQLAlchemy, Pandas, Numpy, Sklearn

- frontend: Next.js, React, Node.js, Chart.js

- db: SQLite

#### 3. Организация проекта 

- `backend`: Серверная часть - FastAPI

    - `api/`: Реализует роуты FastAPI, обрабатывающие запросы от фронта
        - `analytics.py`:  Эндпоинт /analytics/{file_uid}, возвращает агрегированную аналитику по клиентам
        - `clients.py`:  Эндпоинт /clients-group/{file_uid}?group=N, возвращает клиентов, разделённых по риску оттока
        - `upload.py`: Эндпоинт /fine-tune/, принимает CSV-файл, делает предсказания и сохраняет их в базу данных

    - `data/`: Содержит исходные или тестовые датасеты
        - `row_dataset.csv`:  исходные данные для обучения train и выделения test 

    - `model/`: Содержит код и артефакты, связанные с обучением модели.
        - `train_model.py`:  запускает обучение модели, сохраняет файлы препроцессора и модели
        - `preprocessing.py`:  класс Preprocessor, реализует очистку и трансформацию входных данных
        - `artifacts/`:  — сохранённые модели preprocessor.pkl и random_forest_model.pkl

    - `services/`: Слой бизнес-логики и работы с базой
        - `db_models.py`:   модели SQLAlchemy (Upload, Client).
        - `db_service.py`:  функции для сохранения и извлечения данных из БД

    - `utils/`: Вспомогательные модули
        - `db.py`:  инициализация SQLAlchemy и создание сессии 


    - `churn.db`: Файл SQLite с сохранёнными результатами загрузки и обработки клиентов
    - `main.py`: Точка входа в приложение. Запускает FastAPI, подключает роутеры и middleware
    - `requirements.txt`: Список зависимостей Python проекта. Используется для установки
  
- `frontend`: Клиентская часть - Next.js

    - `.next/`: Директория Next.js для временных файлов, используемых в процессе сборки и рендеринга серверной части
  
    - `components/`: React-компоненты, предназначенные для различных частей интерфейса
        - `header.js`: Компонент шапки страницы
        - `AnalyticsCharts.js`: Компонент диаграмм аналитики
      
    - `node_modules/`: Зависимости, установленные с помощью npm
  
    - `pages/`: Страницы Next.js для роутинга
        - `analytics.js`: Страница аналитики
        - `index.js`: Станица загрузки файла
        - Специальные файлы _app.js и _document.js для настройки общего поведения приложения

    - `public/`: Static ресурсы: логотипы, favicon.ico

    - `styles/`: CSS-модули для стилизации компонентов

    -  `utils/`: Утилиты
        - `api.js`: Методы подключения к api и получения данных

    - `jsonconfig.json` и `next.config.mjs`: Конфигурационные файлы проекта

    - `package.json` / `package-lock.json`: Метаданные проекта и зависимости


#### 4. Запуск проекта

Для сборки проекта локально, необходимо:

- Собрать Frontend (Next.js):

```
cd frontend
npm install        # установка зависимостей
npm run dev        # запуск в режиме разработки
```

- Собрать Backend (FastAPI):

```
cd backend
pip install -r requirements.txt   # установка зависимостей

python model/train_model.py       # обучение модели и сохранение артефактов

uvicorn main:app --reload --host 127.0.0.1 --port 8000 # Запуск FastAPI
```
⚠️ Убедитесь, что после обучения в папке model/artifacts/ появились файлы preprocessor.pkl и random_forest_model.pkl. Без них предсказание невозможно.


#### 5. Интерфейс проекта
![](frontend%2Fpublic%2Fui.png)

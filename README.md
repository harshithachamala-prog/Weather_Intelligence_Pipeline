![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)


# 🌦️ Weather Intelligence Pipeline

An end-to-end weather prediction pipeline built using Python that automatically collects weather data, performs feature engineering, predicts rainfall using an XGBoost machine learning model, and exposes results through a FastAPI REST API.

The project demonstrates the integration of data engineering, machine learning, backend development, automation, and software engineering practices into a single production-style pipeline.

---

## Features

- 🌐 Collects hourly weather data from the WeatherAPI service
- 💾 Stores raw weather observations in SQLite
- 📊 Performs daily feature engineering using Pandas
- 🤖 Predicts rainfall using a pre-trained XGBoost classifier
- ⚡ Exposes predictions and weather data through FastAPI
- ⏰ Automates the entire pipeline using APScheduler
- ❤️ Provides system health monitoring endpoints
- 📖 Automatic API documentation with Swagger UI (`/docs`)

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Backend | FastAPI, Uvicorn |
| Machine Learning | XGBoost, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Database | SQLite |
| Scheduling | APScheduler |
| API | WeatherAPI |
| Version Control | Git & GitHub |
| Containerization | Docker *(Coming Soon)* |

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/Weather-Intelligence-Pipeline.git
```

Navigate into the project

```bash
cd Weather-Intelligence-Pipeline
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the API

```bash
uvicorn api:app --reload
```


## Project Architecture

```

WeatherAPI
│
▼
Hourly Data Collection Layer
(store_hourly_data)
│
▼
hourly_data.db
│
▼
Feature Engineering
(save_daily)
│
▼
daily_data.db
│
▼
Prediction Layer
(predict)
│
▼
prediction.db
│
▼
FastAPI REST API
│
├── GET /
├── GET /daily
├── GET /prediction
└── GET /health

```

---

## Project Structure

```

weather\_api/
│
├── api.py                      # FastAPI application
├── main.py                     # Main pipeline execution
├── scheduler.py                # APScheduler automation
│
├── weatherapi.py               # WeatherAPI communication
├── database.py                 # Hourly database management
├── feature\_eng.py              # Feature engineering pipeline
├── predict.py                  # XGBoost inference
├── prediction.py               # Prediction database functions
│
├── pydantic\_schema.py          # API response models
├── log\_config.py               # Logging configuration
│
├── model/
│   └── rain\_classifier.json    # Trained XGBoost model
│
├── data/
│   ├── hourly\_data.db
│   ├── daily\_data.db
│   └── prediction.db
│
├── logs/
│   ├── api.log
│   ├── pipeline.log
│   └── scheduler.log
│
├── requirements.txt
├── README.md
└── .gitignore

```

---

## Machine Learning Pipeline

The machine learning model expects engineered daily weather features instead of raw hourly observations.

### Raw Hourly Features

- Temperature
- Humidity
- Pressure
- Dew Point
- Wind Speed
- Wind Gust
- Precipitation

### Engineered Daily Features

The hourly observations are aggregated into:

- Minimum temperature
- Maximum temperature
- Mean temperature
- Minimum humidity
- Maximum humidity
- Mean humidity
- Minimum dew point
- Maximum dew point
- Mean dew point
- Minimum pressure
- Maximum pressure
- Mean pressure
- Mean wind speed
- Maximum wind gust
- Daily rainfall
- Temperature change (dT)
- Humidity change (dH)
- Pressure change (dP)
- Day of year
- Month
- Rain yesterday
- Rain in previous three days
- Three-day pressure trend
- Three-day humidity average

These engineered features are then supplied to the trained XGBoost classifier to generate rainfall predictions.

---

## Machine Learning Model

The prediction system uses a pre-trained XGBoost Classifier to determine whether rainfall is expected based on engineered daily weather features.

Prediction Output

- Rain Expected
- No Rain Expected
- Prediction Probability

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API status |
| GET | `/daily` | Latest engineered weather features |
| GET | `/prediction` | Latest rainfall prediction |
| GET | `/health` | System health status |

Interactive API documentation is automatically available at:

```
/docs

```
![FastAPI Swagger UI documentation page showing interactive API documentation. The page displays a left sidebar listing endpoints including GET /, GET /daily, GET /prediction, and GET /health, and a main panel with endpoint details, parameters, and Try it out and Execute buttons. The header shows Swagger UI and API title. Browser window with light theme and typical Swagger layout. Text visible in the image includes Swagger UI, Try it out, Execute, Parameters, and Responses. The tone is informational and neutral.](images/swagger_docs.png)

## Automation

The pipeline is automated using APScheduler with a Cron Trigger that executes at the beginning of every hour.

Pipeline execution flow:

1. Fetch latest weather data
2. Store hourly observations
3. Recover any missed hours if necessary
4. Generate daily engineered features
5. Store daily feature dataset
6. Run XGBoost prediction
7. Store latest prediction
8. Expose results through FastAPI

Scheduler configuration:

- Cron Trigger
- `max_instances = 1`
- `coalesce = True`
- `misfire_grace_time = 180`



## Future Improvements

- Docker containerization
- Cloud deployment
- Automated testing using Pytest
- CI/CD with GitHub Actions
- Authentication for API endpoints
- Historical analytics dashboard

---

## Author

Developed as a software engineering and machine learning portfolio project to demonstrate backend development, data engineering, automation, and deployment concepts.
# Sentiment Analysis on Customer Reviews

A Streamlit-based machine learning app that classifies customer review text into sentiment categories. The current app is tailored for airline/flight reviews and predicts whether a review is positive, neutral, or negative using a trained Logistic Regression model with TF-IDF vectorization.

## Project Overview

This project demonstrates an end-to-end sentiment analysis workflow:

- Cleaning and preprocessing review text
- Training a sentiment classification model
- Saving the trained model and vectorizer
- Building an interactive Streamlit web app for real-time predictions
- Displaying confidence scores and actionable recommendations

## Features

- Interactive Streamlit user interface
- Real-time sentiment prediction
- Positive, neutral, and negative sentiment classes
- TF-IDF text vectorization
- Logistic Regression classifier
- Prediction confidence display
- Probability breakdown for each sentiment class
- Recent prediction history inside the app

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- scikit-learn
- NLTK
- Pickle

## Project Structure

```text
.
├── app/
│   └── app.py
├── Data/
│   └── Tweets.csv
├── models/
│   ├── sentiment_model.pkl
│   └── tfidf_vectorizer.pkl
├── notebooks/
│   └── sentiment_analysis.ipynb
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/AryanBharti5080/Sentiment-Analysis-on-Customer-Reviews-CodTech.git
cd Sentiment-Analysis-on-Customer-Reviews-CodTech
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run app/app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

Enter a customer review or select a sample review in the app to view the predicted sentiment, model confidence, probability breakdown, and suggested actions.

## Model Details

- Vectorizer: TF-IDF
- Classifier: Logistic Regression
- Dataset: US airline tweets/customer review sentiment data
- Sentiment labels: Positive, Neutral, Negative
- Reported app accuracy: 77.87%

## Files

- `app/app.py`: Streamlit application for sentiment prediction
- `notebooks/sentiment_analysis.ipynb`: Notebook used for analysis/model development
- `models/sentiment_model.pkl`: Trained sentiment classification model
- `models/tfidf_vectorizer.pkl`: Saved TF-IDF vectorizer
- `Data/Tweets.csv`: Dataset used for sentiment analysis
- `requirements.txt`: Python dependencies

## Author

Aryan Bharti

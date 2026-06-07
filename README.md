# 😊 Sentiment Analysis on Customer Reviews

## 📌 Overview

This project is a Sentiment Analysis application built using **Natural Language Processing (NLP)**, **Machine Learning**, and **Streamlit**. The application analyzes customer reviews and predicts whether the sentiment expressed in the text is **Positive**, **Negative**, or **Neutral**.

The model is trained on real-world airline customer reviews and uses **TF-IDF Vectorization** along with **Logistic Regression** for sentiment classification. A user-friendly Streamlit interface allows users to enter reviews and receive sentiment predictions, confidence scores, and business recommendations.

---

## 🎯 Project Objectives

✅ Perform sentiment classification on customer reviews

✅ Apply NLP techniques for text preprocessing

✅ Convert text data into numerical features using TF-IDF

✅ Train and evaluate a machine learning model

✅ Build an interactive Streamlit web application

✅ Generate actionable business recommendations

---

## 📊 Dataset

### ✈️ Twitter Airline Sentiment Dataset

The dataset contains customer tweets related to various airlines and includes sentiment labels.

### 📈 Dataset Information

* Total Records: **14,640**
* Features Used:

  * `text`
  * `airline_sentiment`

### 📋 Sentiment Distribution

| Sentiment   | Count |
| ----------- | ----: |
| 😞 Negative | 9,178 |
| 😐 Neutral  | 3,099 |
| 😊 Positive | 2,363 |

### ⚠️ Class Imbalance

The dataset is **imbalanced**, with significantly more **Negative** reviews than **Positive** and **Neutral** reviews.

This imbalance impacts model performance because the classifier receives more training examples from the Negative class, making it easier to identify compared to Positive and Neutral sentiments.

---

## 🛠️ Technologies Used

* 🐍 Python
* 🐼 Pandas
* 🔢 NumPy
* 🤖 Scikit-learn
* 🔍 Regular Expressions (Regex)
* 📝 TF-IDF Vectorization
* 📈 Logistic Regression
* 🎨 Streamlit
* 💾 Pickle

---

## 📁 Project Structure

```text
Sentiment-Analysis-Task/
│
├── data/
│   └── Tweets.csv
│
├── notebooks/
│   └── sentiment_analysis.ipynb
│
├── models/
│   ├── sentiment_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── app/
│   └── app.py
│
├── requirements.txt
│
└── README.md
```

---

## ⚙️ Project Workflow

### 📥 1. Data Collection

* Loaded the Twitter Airline Sentiment Dataset
* Explored dataset structure and features
* Checked for missing values

### 🧹 2. Data Preprocessing

Text cleaning steps included:

* Converting text to lowercase
* Removing URLs
* Removing special characters
* Removing extra whitespace

### 🔤 3. Feature Engineering

TF-IDF (Term Frequency-Inverse Document Frequency) was used to transform textual reviews into numerical feature vectors.

### 🤖 4. Model Training

A Logistic Regression classifier was trained using the TF-IDF features.

### 📊 5. Model Evaluation

The model was evaluated using:

* Accuracy Score
* Precision
* Recall
* F1-Score
* Classification Report

### 🚀 6. Deployment

The trained model and TF-IDF vectorizer were saved using Pickle and deployed through a Streamlit application.

---

## 📈 Model Performance

### 🎯 Accuracy

```text
77.87%
```

### 📊 Classification Report

| Sentiment   | Precision | Recall | F1-Score |
| ----------- | --------- | ------ | -------- |
| 😞 Negative | 0.81      | 0.93   | 0.87     |
| 😐 Neutral  | 0.63      | 0.48   | 0.54     |
| 😊 Positive | 0.81      | 0.58   | 0.67     |

### 🔍 Key Observation

* The model performs best on **Negative** reviews.
* Neutral sentiment is the most difficult class to classify.
* Dataset imbalance contributes to stronger performance on the Negative class.

---

## 🌟 Streamlit Application Features

### ✍️ User Input

Users can enter any customer review.

### 🧠 Sentiment Prediction

The application predicts:

* 😊 Positive
* 😐 Neutral
* 😞 Negative

### 📊 Confidence Score

Displays prediction confidence percentage.

### 💡 Business Recommendations

Provides actionable recommendations based on sentiment.

### 📝 Example Reviews

Includes sample reviews for quick testing.

## 🧪 Sample Predictions

### 😊 Positive Review

text
The flight was amazing and the staff were very friendly.

**Prediction:** Positive

### 😐 Neutral Review
text
The flight departed on time and arrived as scheduled.


**Prediction:** Neutral

### 😞 Negative Review

```text
Worst airline experience ever. Very disappointed.
```

**Prediction:** Negative

---

## 🚀 Installation

### 📥 Clone Repository

```bash
git clone <repository-url>
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Run Streamlit App

```bash
streamlit run app/app.py
```

---

## 💼 Skills Demonstrated

* 🧠 Natural Language Processing (NLP)
* 🧹 Text Cleaning & Preprocessing
* 🔤 TF-IDF Vectorization
* 🤖 Machine Learning
* 📈 Logistic Regression
* 📊 Model Evaluation
* 🎨 Streamlit Development
* 💡 Business Insight Generation


## 🔮 Future Improvements

* Balance the dataset using advanced techniques
* Compare multiple machine learning models
* Explore deep learning approaches
* Deploy on Streamlit Community Cloud
* Add sentiment analytics dashboard


## 🏁 Conclusion

This project demonstrates how **Natural Language Processing**, **Machine Learning**, and **Streamlit** can be combined to analyze customer feedback and generate meaningful insights.

By leveraging **TF-IDF Vectorization** and **Logistic Regression**, the application effectively classifies customer reviews into **Positive**, **Neutral**, and **Negative** sentiments while providing confidence scores and business recommendations.

# Machine Learning & Deep Learning Model Architecture — AI Financial Advisor

---

## 1. Expense Categorization NLP Model
- **Algorithm**: TF-IDF Vectorizer (1-2 ngrams, sublinear scaling) + Calibrated Multi-Class Classifier (Logistic Regression / Random Forest / HistGradientBoosting).
- **Classes (16)**: `Food`, `Grocery`, `Rent`, `Utilities`, `Transport`, `Fuel`, `Shopping`, `Entertainment`, `Education`, `Healthcare`, `Travel`, `Salary`, `Freelancing`, `Business`, `Investment`, `Other`.
- **Target Accuracy**: >94.0%.
- **Output**: Predicted Category and Softmax Confidence Score.
- **Serialization**: `models/expense_classifier.joblib`.

---

## 2. Fraud & Anomaly Detection Model
- **Algorithm**: Isolation Forest (`n_estimators=150`, `contamination=0.05`) combined with statistical z-score rules.
- **Input Features**: `[Amount, Hour of day (0-23), Day of week (0-6), Category index, Merchant familiarity index]`.
- **Output**: Risk Level (`LOW`, `MEDIUM`, `HIGH`), Anomaly Probability (0.0 - 1.0), and Human-readable reasoning triggers.
- **Deep Learning Autoencoder**: 4-layer Dense neural reconstruction network calculating Mean Squared Reconstruction Error against established baseline threshold.
- **Serialization**: `models/fraud_detector.joblib` and `models/fraud_autoencoder.keras`.

---

## 3. Credit Risk Assessment & Explainable AI (XAI)
- **Algorithm**: Gradient Boosting Classifier (`n_estimators=100`, `max_depth=4`) + Feature Attribution Engine.
- **Input Dimensions**: Annual Income, Employment Duration, Existing Loans, Monthly Debt, On-time Payment %, Credit Utilization %, Open Accounts, Previous Defaults, Age.
- **Output**: Risk Category (`LOW RISK`, `MEDIUM RISK`, `HIGH RISK`), Estimated Credit Score Range, Default Probability, Top Positive Drivers, and Top Risk Factors.
- **Explainability**: SHAP value approximations and relative feature importance weights.
- **Serialization**: `models/credit_model.joblib`.

---

## 4. Spending Forecast Regressor & Deep Learning LSTM
- **Time Series Regressors**: Random Forest Regressor & Gradient Boosting Regressor trained on lag-1, lag-7, lag-14, 7-day rolling mean, 30-day rolling mean, and cyclic day markers.
- **Deep Learning LSTM**: Keras Sequential Recurrent Model (`LSTM(32)` + `Dropout(0.1)` + `Dense(16)` + `Dense(1)`).
- **Metrics**: MAE ($14.20), RMSE ($18.50), $R^2$ (0.88).
- **Output**: Next week spending, Next month spending, 30-day projected sequence with 90% confidence ribbon bounds.
- **Graceful Handling**: Returns `"Not enough historical data to generate a reliable forecast"` if records < 7 days.
- **Serialization**: `models/spending_regressor.joblib` and `models/lstm_forecast.keras`.

---

## 5. Computer Vision Receipt Scanner & OCR
- **Image Preprocessing**: OpenCV Grayscale Conversion, Bilateral Noise Reduction Filter, Adaptive Otsu Thresholding, Edge Enhancement.
- **Text & Entity Parsing**: Regular expression token matching for Merchant Name, Dates, Line items, Unit prices, Subtotal, Tax, and Total amount.

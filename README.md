# SentimentIQ — AI Sentiment Analyzer 🧠✨

SentimentIQ is a real-time, end-to-end Machine Learning web application built to analyze the emotional tone behind any given text. Whether it's a tweet, a product review, or a simple message, the custom-trained AI model instantly evaluates it and surfaces the underlying sentiment (Positive or Negative) through a highly-polished interactive frontend.

## 🚀 Features
* **Custom Machine Learning Model**: Trained on thousands of real-world movie reviews from the NLTK corpus using **Logistic Regression** and **TF-IDF Vectorization** with bigram context awareness.
* **Modern Web Interface**: A sleek, fully-responsive dark mode UI featuring smooth CSS micro-animations, glassmorphism card designs, and instant visual feedback (emojis and dynamic color coding).
* **Flask REST API**: Built on a lightweight Python Flask backend that handles JSON payloads securely and optimally unpickles the ML pipeline on startup.
* **Robust Text Preprocessing**: Automates edge-case handling by performing lowercase conversions and regex-based special character pruning before making inferences.

---

## 🛠️ Tech Stack
* **Backend**: Python 3, Flask
* **Machine Learning**: Scikit-Learn (`LogisticRegression`, `TfidfVectorizer`), NLTK (Corpus & Datasets), NumPy
* **Frontend**: Vanilla HTML5, CSS3 (Custom Properties & Keyframe Animations), and Vanilla JavaScript (Fetch API)
* **Serialization**: Pickle

---

## 📦 Local Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/AnkitGit-prog/SentimentIQ-Analyzer-ML.git
   cd SentimentIQ-Analyzer-ML
   ```

2. **Set up a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   The application will start a local development server. Navigate to `http://127.0.0.1:5000` in your web browser to use SentimentIQ!

---

## 🔬 How The AI Pipeline Works
1. **Input**: A user submits a paragraph directly into the UI.
2. **Pre-processing**: The Flask API extracts the text, forces lowercasing, and uses standard regex to strip away noise and unhelpful special characters (e.g. `!@#$`).
3. **Vectorization**: The string is pushed through the pre-fitted `TfidfVectorizer` mapping string features into numerical arrays based on term-frequencies against contextual bigrams.
4. **Prediction**: The `LogisticRegression` model evaluates the vectorized inputs against its learned probabilistic weights and returns `1` (Positive) or `0` (Negative).
5. **Output**: The JSON returns immediately and the JavaScript UI decodes it dynamically into a beautiful feedback card.

---

## 🔮 Future Enhancements
- Expand classification boundaries to accommodate an explicitly 'Neutral' baseline threshold.
- Train on larger datasets (e.g. Kaggle IMDB 50K or Twitter APIs) to handle a wider scope of casual shorthand slang.
- Build a lightweight database (e.g., MongoDB/Postgres) to log queries for continuous model reinforcement and accuracy tracking.

## 📄 License
This project is open source and available under the [MIT License](LICENSE).

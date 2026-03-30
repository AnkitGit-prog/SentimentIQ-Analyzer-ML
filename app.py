# App loaded
import pickle
import os
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# Load the pre-trained model and vectorizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

# ─── HTML Template ────────────────────────────────────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SentimentIQ — AI Sentiment Analyzer</title>
    <meta name="description" content="SentimentIQ uses machine learning to analyze the sentiment of any text in real-time.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --bg-primary: #0a0a0f;
            --bg-card: rgba(255,255,255,0.04);
            --border: rgba(255,255,255,0.08);
            --text-primary: #f0f0f5;
            --text-secondary: #8a8a9a;
            --accent: #6c5ce7;
            --accent-glow: rgba(108,92,231,0.35);
            --positive: #00cec9;
            --negative: #ff6b6b;
            --neutral: #fdcb6e;
            --radius: 16px;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
        }

        /* animated background blobs */
        body::before, body::after {
            content: '';
            position: fixed;
            border-radius: 50%;
            filter: blur(120px);
            opacity: .35;
            z-index: 0;
            pointer-events: none;
        }
        body::before {
            width: 500px; height: 500px;
            background: var(--accent);
            top: -120px; left: -100px;
            animation: float 12s ease-in-out infinite alternate;
        }
        body::after {
            width: 400px; height: 400px;
            background: var(--positive);
            bottom: -80px; right: -80px;
            animation: float 10s ease-in-out infinite alternate-reverse;
        }
        @keyframes float {
            0%   { transform: translate(0, 0) scale(1); }
            100% { transform: translate(60px, 40px) scale(1.15); }
        }

        .container {
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 640px;
            padding: 24px;
        }

        /* ── Header ── */
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .logo {
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 12px;
        }
        .header h1 {
            font-size: 42px;
            font-weight: 800;
            line-height: 1.15;
            background: linear-gradient(135deg, #f0f0f5, var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p {
            margin-top: 10px;
            color: var(--text-secondary);
            font-size: 15px;
            line-height: 1.6;
        }

        /* ── Card ── */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 32px;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            transition: border-color .3s;
        }
        .card:hover { border-color: rgba(108,92,231,.25); }

        /* ── Form ── */
        label {
            display: block;
            font-weight: 500;
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 8px;
            letter-spacing: .5px;
            text-transform: uppercase;
        }
        textarea {
            width: 100%;
            min-height: 140px;
            padding: 16px;
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            color: var(--text-primary);
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            border-radius: 12px;
            resize: vertical;
            outline: none;
            transition: border-color .3s, box-shadow .3s;
        }
        textarea::placeholder { color: rgba(255,255,255,.2); }
        textarea:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            width: 100%;
            margin-top: 20px;
            padding: 14px 28px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 15px;
            color: #fff;
            background: linear-gradient(135deg, var(--accent), #a29bfe);
            box-shadow: 0 4px 24px var(--accent-glow);
            transition: transform .2s, box-shadow .2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 32px var(--accent-glow);
        }
        .btn:active { transform: scale(.97); }
        .btn.loading { pointer-events: none; opacity: .7; }

        /* spinner */
        .spinner {
            width: 18px; height: 18px;
            border: 2px solid rgba(255,255,255,.3);
            border-top-color: #fff;
            border-radius: 50%;
            animation: spin .6s linear infinite;
            display: none;
        }
        .btn.loading .spinner { display: block; }
        .btn.loading .btn-label { display: none; }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* ── Result ── */
        .result {
            margin-top: 28px;
            padding: 24px;
            border-radius: 14px;
            text-align: center;
            animation: fadeUp .4s ease;
            display: none;
        }
        .result.show { display: block; }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(12px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .result.positive { background: rgba(0,206,201,.1); border: 1px solid rgba(0,206,201,.25); }
        .result.negative { background: rgba(255,107,107,.1); border: 1px solid rgba(255,107,107,.25); }
        .result.neutral  { background: rgba(253,203,110,.1); border: 1px solid rgba(253,203,110,.25); }

        .result-emoji { font-size: 40px; margin-bottom: 8px; }
        .result-label {
            font-size: 22px;
            font-weight: 700;
        }
        .result.positive .result-label { color: var(--positive); }
        .result.negative .result-label { color: var(--negative); }
        .result.neutral  .result-label { color: var(--neutral); }
        .result-sub {
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 6px;
        }

        /* footer */
        .footer {
            text-align: center;
            margin-top: 48px;
            font-size: 12px;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="logo">SentimentIQ</div>
            <h1>Understand the Emotion Behind Words</h1>
            <p>Paste any review, tweet, or message and let our AI reveal its sentiment instantly.</p>
        </header>

        <div class="card" id="analyzerCard">
            <label for="textInput">Enter your text</label>
            <textarea id="textInput" placeholder="e.g. I absolutely loved the new update — it's faster and more intuitive!"></textarea>
            <button class="btn" id="analyzeBtn" onclick="analyze()">
                <span class="btn-label">Analyze Sentiment ✦</span>
                <span class="spinner"></span>
            </button>

            <div class="result" id="resultBox">
                <div class="result-emoji" id="resultEmoji"></div>
                <div class="result-label" id="resultLabel"></div>
                <div class="result-sub" id="resultSub"></div>
            </div>
        </div>

        <div class="footer">Built with ML &amp; Flask &nbsp;·&nbsp; SentimentIQ &copy; 2026</div>
    </div>

    <script>
        async function analyze() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) { alert('Please enter some text.'); return; }

            const btn = document.getElementById('analyzeBtn');
            const result = document.getElementById('resultBox');
            btn.classList.add('loading');
            result.classList.remove('show', 'positive', 'negative', 'neutral');

            try {
                const res = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });
                const data = await res.json();

                const emoji = document.getElementById('resultEmoji');
                const label = document.getElementById('resultLabel');
                const sub   = document.getElementById('resultSub');

                const sentiment = data.sentiment.toLowerCase();
                let cls = 'neutral', icon = '😐', nice = 'Neutral';

                if (sentiment.includes('pos')) {
                    cls = 'positive'; icon = '😊'; nice = 'Positive';
                } else if (sentiment.includes('neg')) {
                    cls = 'negative'; icon = '😞'; nice = 'Negative';
                }

                result.className = 'result show ' + cls;
                emoji.textContent = icon;
                label.textContent = nice + ' Sentiment';
                sub.textContent = 'Detected sentiment for your input text.';
            } catch (err) {
                alert('Something went wrong. Please try again.');
                console.error(err);
            } finally {
                btn.classList.remove('loading');
            }
        }

        // allow Ctrl+Enter to submit
        document.getElementById('textInput').addEventListener('keydown', e => {
            if (e.ctrlKey && e.key === 'Enter') analyze();
        });
    </script>
</body>
</html>
"""


# ─── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/predict", methods=["POST"])
def predict():
    import re
    data = request.get_json(force=True)
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    # 1. & 2. & 3. Preprocess text: lowercase and remove special characters
    processed_text = text.lower()
    processed_text = re.sub(r'[^a-z0-9\s]', '', processed_text)

    # 4. Transform input with the saved vectorizer (no refitting)
    text_vectorized = vectorizer.transform([processed_text])
    prediction = model.predict(text_vectorized)[0]

    # 5. Ensure correct label mapping (0 = negative, 1 = positive)
    label_map = {"0": "Negative", "1": "Positive"}
    pred_str = str(prediction).strip()
    
    if pred_str in label_map:
        sentiment = label_map[pred_str]
    else:
        sentiment = pred_str

    return jsonify({"sentiment": sentiment, "input": text})


# ─── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n  ✦  SentimentIQ is running → http://127.0.0.1:5000\n")
    app.run(debug=True)
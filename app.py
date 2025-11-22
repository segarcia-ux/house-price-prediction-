# app.py → LUXE with Historical Price Chart (Past 20 Years Fluctuations)
from flask import Flask, request
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)
model = joblib.load('model.pkl')

# Load and analyze data
df = pd.read_csv('../data/House Price Prediction Dataset.csv')

# Historical chart data: Average prices by year (past 20 years)
df_sorted = df.sort_values('YearBuilt')
yearly_avg = df_sorted.groupby('YearBuilt')['Price'].mean().reset_index()
recent_years_df = yearly_avg[yearly_avg['YearBuilt'] >= 2005]  # Past ~20 years
chart_years = recent_years_df['YearBuilt'].tolist()
chart_prices = recent_years_df['Price'].tolist()

# Yearly growth (CAGR)
if len(chart_prices) > 1:
    cagr = (chart_prices[-1] / chart_prices[0]) ** (1 / (chart_years[-1] - chart_years[0])) - 1
    avg_yearly_increase = round(cagr * 100, 1)
else:
    avg_yearly_increase = 5.5

# Market averages
market_avg_price = df['Price'].mean()
market_avg_rent = round(market_avg_price * 0.0055)

# Chart JSON for Plotly (embedded)
CHART_JSON = {
    "data": [
        {
            "x": chart_years,
            "y": chart_prices,
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Avg Price",
            "line": {"color": "#fbbf24", "width": 4},
            "marker": {"size": 8, "color": "#fbbf24"}
        }
    ],
    "layout": {
        "title": {"text": "Price Fluctuations (Past 20 Years)", "font": {"color": "#f1f5f9", "size": 18}},
        "xaxis": {"title": {"text": "Year"}, "color": "#f1f5f9"},
        "yaxis": {"title": {"text": "Avg Price ($)"}, "color": "#f1f5f9"},
        "template": "plotly_dark",
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(30,41,59,0.8)",
        "font": {"color": "#f1f5f9"},
        "hovermode": "x unified",
        "height": 400,
        "margin": {"l": 50, "r": 20, "t": 60, "b": 50},
        "legend": {"bgcolor": "rgba(30,41,59,0.9)"}
    }
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LUXE House AI</title>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <style>
        :root{--gold:#fbbf24;--dark:#0f172a;--card:#1e293b;--text:#f1f5f9;--green:#10b981}
        body{margin:0;font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#0f172a,#1e1b4b);color:var(--text);min-height:100vh;padding:20px}
        .header{text-align:center;padding:40px 20px;background:linear-gradient(to right,#1e293b,#312e81);border-bottom:4px solid var(--gold);margin-bottom:30px;border-radius:20px 20px 0 0}
        h1{font-size:3.5rem;margin:0;background:linear-gradient(to right,#fbbf24,#fcd34d);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
        .container{max-width:1400px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:40px}
        @media(max-width:1100px){.container{grid-template-columns:1fr}}
        .card{background:var(--card);border-radius:24px;padding:40px;box-shadow:0 30px 70px rgba(0,0,0,0.8);border:2px solid rgba(251,191,36,0.4)}
        label{display:block;font-weight:bold;color:var(--gold);margin:25px 0 10px 5px;font-size:1.2rem}
        input,select{width:100%;padding:18px;border-radius:16px;border:2px solid #334155;background:#1e293b;color:white;font-size:18px;box-sizing:border-box}
        input:focus,select:focus{outline:none;border-color:var(--gold);box-shadow:0 0 0 6px rgba(251,191,36,0.3)}
        button{width:100%;padding:22px;margin-top:40px;background:linear-gradient(to right,var(--gold),#f59e0b);border:none;border-radius:18px;color:black;font-size:1.7rem;font-weight:bold;cursor:pointer;transition:.4s}
        button:hover{transform:translateY(-8px);box-shadow:0 30px 60px rgba(251,191,36,0.7)}
        .result{margin-top:45px;padding:40px;background:linear-gradient(135deg,#166534,var(--green));border-radius:24px;text-align:center;font-size:3.3rem;color:white;border:6px solid var(--gold);font-weight:bold}
        .rent{font-size:1.8rem;margin-top:16px}
        .range{font-size:1.35rem;margin-top:18px;opacity:0.9}
        .stats{margin-top:45px;display:grid;grid-template-columns:1fr 1fr;gap:25px}
        .stat-card{background:rgba(251,191,36,0.2);padding:25px;border-radius:20px;text-align:center;border:3px solid var(--gold)}
        .stat-value{font-size:2.1rem;font-weight:bold;color:var(--gold)}
        .stat-label{font-size:1rem;color:#cbd5e1;margin-top:8px}
        #chart{border-radius:20px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,0.6);background:#1e293b}
        footer{text-align:center;padding:40px;color:#64748b;font-size:1rem}
    </style>
</head>
<body>
    <div class="header">
        <h1>LUXE House AI</h1>
        <p style="color:#94a3b8;font-size:1.5rem;margin-top:10px">Instant Professional Valuation & Market Trends</p>
    </div>

    <div class="container">
        <!-- Left: Valuation Form -->
        <div class="card">
            <form method="post">
                <label>Square Footage (sq ft)</label>
                <input type="number" name="area" value="3200" required min="500">

                <label>Bedrooms</label>
                <select name="bedrooms"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option><option>6+</option></select>

                <label>Bathrooms</label>
                <select name="bathrooms"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5+</option></select>

                <label>Floors</label>
                <select name="floors"><option>1</option><option selected>2</option><option>3</option><option>4</option></select>

                <label>Year Built</label>
                <input type="number" name="yearbuilt" value="2005" required min="1900" max="2025">

                <label>Location</label>
                <select name="location"><option>Downtown</option><option selected>Suburban</option><option>Urban</option><option>Rural</option></select>

                <label>Condition</label>
                <select name="condition"><option>Poor</option><option>Fair</option><option selected>Good</option><option>Excellent</option></select>

                <label>Garage</label>
                <select name="garage"><option>No</option><option selected>Yes</option></select>

                <button type="submit">Get Instant Valuation</button>
            </form>

            {% if result %}
            <div class="result">
                ${{ prediction }}
                <div class="rent">Estimated Monthly Rent ≈ ${{ rent }}/mo</div>
                <div class="range">Range: ${{ lower }} – ${{ upper }} (±12%)</div>
            </div>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">+{{ growth }}%</div>
                    <div class="stat-label">Avg Yearly Price Growth</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{ avg_rent }}</div>
                    <div class="stat-label">Market Avg Monthly Rent</div>
                </div>
            </div>
            {% endif %}
        </div>

        <!-- Right: Historical Chart -->
        <div class="card">
            <h2 style="text-align:center;color:var(--gold);font-size:1.8rem;margin-bottom:20px">Price Trends Over Time</h2>
            <div id="chart"></div>
        </div>
    </div>

    <footer>LUXE House AI • {{ year }} • AI-Powered Real Estate Intelligence</footer>

    <script>
        const chartData = {{ chart_json|safe }};
        Plotly.newPlot('chart', chartData.data, chartData.layout, {responsive: true});
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = lower = upper = rent = None
    year = datetime.now().year

    if request.method == "POST":
        try:
            data = {
                'Area': [int(request.form['area'])],
                'Bedrooms': [int(request.form.get('bedrooms', '3').replace('+','').replace('6','6'))],
                'Bathrooms': [int(request.form.get('bathrooms', '2').replace('+',''))],
                'Floors': [int(request.form['floors'])],
                'YearBuilt': [int(request.form['yearbuilt'])],
                'Location': [request.form['location']],
                'Condition': [request.form['condition']],
                'Garage': [request.form['garage']]
            }
            pred = model.predict(pd.DataFrame(data))[0]
            prediction = round(pred)
            lower = round(pred * 0.88)
            upper = round(pred * 1.12)
            rent = round(pred * 0.0055)
        except:
            pass

    html = HTML.replace("{{ year }}", str(year))
    html = html.replace("{{ growth }}", str(avg_yearly_increase))
    html = html.replace("{{ avg_rent }}", f"{market_avg_rent:,.0f}")
    html = html.replace("{{ chart_json|safe }}", str(CHART_JSON).replace("'", '"'))

    if prediction:
        html = html.replace("{% if result %}", "").replace("{% endif %}", "")
        html = html.replace("{{ prediction }}", f"{prediction:,}")
        html = html.replace("{{ lower }}", f"{lower:,}")
        html = html.replace("{{ upper }}", f"{upper:,}")
        html = html.replace("{{ rent }}", f"{rent:,}")
    else:
        html = html.replace("{% if result %}", "<!--").replace("{% endif %}", "-->")

    return html

if __name__ == "__main__":
    print("LUXE House AI is LIVE! → http://127.0.0.1:5000")
    app.run(debug=True)
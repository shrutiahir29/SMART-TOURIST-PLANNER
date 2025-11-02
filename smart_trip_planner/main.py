from flask import Flask, render_template, request
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)

# ---------- Trip Planning Logic ----------
def best_itinerary(places, total_days=2):
    """
    Selects best combination of places maximizing ratings within available time.
    Each day assumed to have 8 hours.
    """
    data = [[row["Place"], row["Time (hrs)"], row["Rating"]] for _, row in places.iterrows()]
    best_score = 0
    best_plan = []

    for r in range(1, len(data)+1):
        for combo in itertools.combinations(data, r):
            total_time = sum(p[1] for p in combo)
            total_score = sum(p[2] for p in combo)
            if total_time <= total_days * 8:
                if total_score > best_score:
                    best_score = total_score
                    best_plan = combo

    itinerary = {}
    day_hours = 8
    current_day = 1
    day_list = []
    used_time = 0

    for p in best_plan:
        if used_time + p[1] <= day_hours:
            day_list.append(p)
            used_time += p[1]
        else:
            itinerary[f"Day {current_day}"] = day_list
            current_day += 1
            day_list = [p]
            used_time = p[1]
    if day_list:
        itinerary[f"Day {current_day}"] = day_list

    return itinerary, best_score


# ---------- Graph Generator ----------
def create_charts(df, itinerary):
    """
    Generates in-memory charts and returns them as base64 strings
    (so they can display directly in the HTML).
    """
    images = {}

    # Pie Chart: Time Distribution
    plt.figure()
    plt.pie(df["Time (hrs)"], labels=df["Place"], autopct="%1.1f%%", startangle=140)
    plt.title("Time Distribution per Place")
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    images["pie"] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # Bar Chart: Ratings
    plt.figure()
    plt.bar(df["Place"], df["Rating"], color="#0077cc")
    plt.xticks(rotation=45, ha="right")
    plt.title("Attraction Ratings")
    plt.ylabel("Rating (1–10)")
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    images["bar"] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # Line Chart: Daily Time
    daily_times = [sum(p[1] for p in itinerary[day]) for day in itinerary]
    plt.figure()
    plt.plot(list(itinerary.keys()), daily_times, marker="o", color="orange")
    plt.title("Daily Time Utilization")
    plt.ylabel("Hours per Day")
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    images["time"] = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return images


# ---------- Flask Routes ----------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    days = int(request.form.get('days', 2))
    trip_name = request.form.get('trip_name', 'My Trip')

    df = pd.read_csv(file)

    # Validate CSV headers
    required = {"Place", "Time (hrs)", "Rating"}
    if not required.issubset(df.columns):
        return f"❌ CSV must contain these headers: {', '.join(required)}"

    itinerary, score = best_itinerary(df, total_days=days)
    charts = create_charts(df, itinerary)

    return render_template(
        'index.html',
        itinerary=itinerary,
        score=score,
        trip_name=trip_name,
        days=days,
        charts=charts
    )


if __name__ == '__main__':
    app.run(debug=True)



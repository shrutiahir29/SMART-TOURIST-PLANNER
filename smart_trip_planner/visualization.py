import matplotlib.pyplot as plt

def visualize_data(selected, route, total_distance):
    destinations = [d["Destination"] for d in selected]
    cost = [d["Cost"] for d in selected]
    popularity = [d["Popularity"] for d in selected]
    time = [d["Time"] for d in selected]

    plt.figure(figsize=(12, 8))

    # Bar chart: Popularity vs Cost
    plt.subplot(1, 3, 1)
    plt.bar(destinations, popularity, color="skyblue")
    plt.xlabel("Destination")
    plt.ylabel("Popularity")
    plt.title("Popularity Comparison")

    # Line chart: Route Distance
    plt.subplot(1, 3, 2)
    plt.plot([d["Destination"] for d in route], [d["DistanceFromPrev"] for d in route], marker="o")
    plt.title(f"Travel Route (Total Distance = {total_distance} km)")
    plt.xlabel("Destinations")
    plt.ylabel("Distance from Previous")

    # Pie chart: Time Distribution
    plt.subplot(1, 3, 3)
    plt.pie(time, labels=destinations, autopct="%1.1f%%", startangle=90)
    plt.title("Time Distribution")

    plt.tight_layout()
    plt.show()

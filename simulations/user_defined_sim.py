import random
import matplotlib.pyplot as plt
import io
import base64
from threading import Lock

# Global lock for thread safety
plot_lock = Lock()

class User:
    def __init__(self, user_type, daily_growth, activity_distribution, goal_social_media):
        self.type = user_type
        self.daily_growth = daily_growth
        self.activity_distribution = activity_distribution
        self.goal_social_media = goal_social_media
        self.total_points = 0
        self.daily_results = []

    def simulate_day(self, day, total_time):
        activities = ["Nothing", "Social Media", "Reading", "Regular"]
        counts = {act: 0 for act in activities}
        
        for _ in range(total_time):
            activity = random.choices(activities, weights=self.activity_distribution)[0]
            counts[activity] += 1
        
        social_media_penalty = -0.5 if self.type == "hard" else -0.25
        day_points = (counts["Nothing"] + counts["Regular"]) * 1 + \
                     counts["Social Media"] * social_media_penalty + \
                     counts["Reading"] * 1.5
        self.total_points += day_points
        
        result = {
            "Day": day,
            "Total Time": total_time,
            "Nothing Time": counts["Nothing"],
            "Social Media Time": counts["Social Media"],
            "Read Time": counts["Reading"],
            "Regular Time": counts["Regular"],
            "Day Points": round(day_points, 2),
            "Total Points": round(self.total_points, 2)
        }
        self.daily_results.append(result)
        
        # Update probabilities
        self.activity_distribution[1] -= self.daily_growth  # Decrease Social Media
        self.activity_distribution[2] += self.daily_growth * 2 * counts["Reading"]  # Increase Reading
        self.activity_distribution[0] += self.daily_growth  # Increase Nothing
        self.activity_distribution[3] += self.daily_growth  # Increase Regular
        
        # Normalize probabilities
        total = sum(self.activity_distribution)
        self.activity_distribution = [p / total for p in self.activity_distribution]

        return counts["Social Media"] <= self.goal_social_media

def plot_results(all_results):
    days = [r["Day"] for r in all_results]
    social_media_time = [r["Social Media Time"] for r in all_results]
    read_time = [r["Read Time"] for r in all_results]
    total_points = [r["Total Points"] for r in all_results]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    
    ax1.plot(days, social_media_time, 'r-', label='Social Media Time')
    ax1.plot(days, read_time, 'g-', label='Reading Time')
    ax2.plot(days, total_points, 'b-', label='Total Points')
    
    ax1.set_xlabel('Day')
    ax1.set_ylabel('Hours')
    ax2.set_ylabel('Total Points')
    
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    plt.title('User-Defined Simulation Results')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img


def run_user_defined_simulation(data):
    difficulty = data['difficulty']
    days = data['days']
    total_time = data['total_time']
    initial_hours = data['initial_hours']
    daily_growth = data['motivation']
    goal_social_media = data['goal_social_media']
    
    # Convert initial hours to probabilities
    total_initial_hours = sum(initial_hours)
    activity_distribution = [h / total_initial_hours for h in initial_hours]
    
    user = User(difficulty, daily_growth, activity_distribution, goal_social_media)
    all_results = []
    
    for day in range(1, days + 1):
        goal_reached = user.simulate_day(day, total_time)
        all_results.append(user.daily_results[-1])
        
        if goal_reached:
            break
    
    # Generate HTML table for results
    table_html = "<table><tr><th>Day</th><th>Total Time</th><th>Social Media Time</th><th>Read Time</th><th>Day Points</th><th>Total Points</th></tr>"
    for result in all_results:
        table_html += f"<tr><td>{result['Day']}</td><td>{result['Total Time']}</td><td>{result['Social Media Time']}</td><td>{result['Read Time']}</td><td>{result['Day Points']}</td><td>{result['Total Points']}</td></tr>"
    table_html += "</table>"
    
    # Generate plot
    plot = plot_results(all_results)
    
    return table_html, plot


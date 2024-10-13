import random
from typing import List, Dict
from tabulate import tabulate
import matplotlib.pyplot as plt
import io
import base64

class User:
    def __init__(self, type: str, motivation: float, initial_probs: List[float]):
        self.type = type
        self.motivation = motivation
        self.probs = initial_probs
        self.daily_results = []
        self.total_points = 0

    def simulate_day(self, day: int):
        activities = ["Nothing", "Social Media", "Reading", "Regular"]
        counts = {act: 0 for act in activities}
        
        for _ in range(16):  # 16 hours of activity
            activity = random.choices(activities, weights=self.probs)[0]
            counts[activity] += 1
        
        total_time = counts["Social Media"] + counts["Reading"] + counts["Regular"]
        
        # Calculate points
        day_points = (counts["Nothing"] + counts["Regular"]) * 1 + \
                     counts["Social Media"] * -0.5 + \
                     counts["Reading"] * 1.5
        self.total_points += day_points
        
        result = {
            "Day": day,
            "Total Time": total_time,
            "Social Media Time": counts["Social Media"],
            "Read Time": counts["Reading"],
            "Day Points": round(day_points, 2),
            "Total Points": round(self.total_points, 2)
        }
        self.daily_results.append(result)
        
        # Update probabilities
        self.probs[1] -= self.motivation  # Decrease Social Media
        self.probs[2] += self.motivation * 2 * counts["Reading"]  # Increase Reading
        self.probs[0] += self.motivation  # Increase Nothing
        self.probs[3] += self.motivation  # Increase Regular
        
        # Normalize probabilities
        total = sum(self.probs)
        self.probs = [p / total for p in self.probs]

def plot_results(all_results):
    user_types = ["High", "Medium", "Low"]
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 18), sharex=True)
    
    for i, user_type in enumerate(user_types):
        user_data = [r for r in all_results if r["User Type"] == user_type]
        days = [r["Day"] for r in user_data]
        social_media_time = [r["Social Media Time"] for r in user_data]
        read_time = [r["Read Time"] for r in user_data]
        total_points = [r["Total Points"] for r in user_data]
        
        ax1 = axes[i]
        ax2 = ax1.twinx()
        
        line1, = ax1.plot(days, social_media_time, 'r-', label='Social Media Time')
        line2, = ax1.plot(days, read_time, 'g-', label='Reading Time')
        line3, = ax2.plot(days, total_points, 'b-', label='Total Points')
        
        ax1.set_ylabel('Hours')
        ax2.set_ylabel('Total Points')
        ax1.set_title(f'{user_type} Usage User')
        
        if i == 2:  # Only set x-label for the bottom subplot
            ax1.set_xlabel('Day')
        
        lines = [line1, line2, line3]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode the bytes buffer to base64
    plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    plt.close(fig)
    return plot_base64

def run_predefined_simulation(days: int = 7):
    user_types = ['High', 'Medium', 'Low']
    all_results = []
    
    for user_type in user_types:
        total_points = 0
        for day in range(1, days + 1):
            total_time = random.randint(2, 10)
            social_media_time = random.randint(0, total_time)
            read_time = random.randint(0, total_time - social_media_time)
            day_points = (total_time - social_media_time) + (read_time * 1.5)
            total_points += day_points
            
            all_results.append({
                'User Type': user_type,
                'Day': day,
                'Total Time': total_time,
                'Social Media Time': social_media_time,
                'Read Time': read_time,
                'Day Points': round(day_points, 2),
                'Total Points': round(total_points, 2)
            })
    
    # Prepare plot data
    plot_data = {
        'High User': {'x': [], 'y': []},
        'Medium User': {'x': [], 'y': []},
        'Low User': {'x': [], 'y': []}
    }
    for result in all_results:
        user_type = f"{result['User Type']} User"
        plot_data[user_type]['x'].append(result['Day'])
        plot_data[user_type]['y'].append(result['Total Points'])
    
    return all_results, plot_data

if __name__ == "__main__":
    run_predefined_simulation()
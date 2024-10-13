from crewai import Agent, Crew, Task
import random
import json

class HocusfocusCrew:
    def __init__(self):
        self.high_usage_agent = self.create_high_usage_agent()
        self.medium_usage_agent = self.create_medium_usage_agent()
        self.low_usage_agent = self.create_low_usage_agent()

    def create_high_usage_agent(self):
        return Agent(
            role="High Usage Smartphone User",
            goal="Gradually reduce social media usage and increase reading time while maintaining a realistic usage pattern.",
            backstory="You're a heavy smartphone user, typically spending about 10 hours a day on your device, with 8 hours dedicated to social media and 2 hours for other activities.",
            verbose=True
        )

    def create_medium_usage_agent(self):
        return Agent(
            role="Medium Usage Smartphone User",
            goal="Balance screen time between social media and other activities, while increasing reading time.",
            backstory="You're a moderate smartphone user, typically spending about 8 hours a day on your device, with 4 hours dedicated to social media and 4 hours for other activities.",
            verbose=True
        )

    def create_low_usage_agent(self):
        return Agent(
            role="Low Usage Smartphone User",
            goal="Maintain low screen time while balancing necessary tasks and occasional leisure.",
            backstory="You're a light smartphone user, typically spending about 4 hours a day on your device, with 1 hour dedicated to social media and 3 hours for other activities.",
            verbose=True
        )

    def create_simulate_day_task(self, agent):
        return Task(
            description=f"Simulate one day of smartphone usage for the {agent.role}. "
                        f"Choose between social media, regular usage, reading, or no usage. "
                        f"Aim to achieve your goal. "
                        f"Calculate total screen time, social media time, and reading time.",
            expected_output="A JSON string with the following format: "
                            "{'total_time': float, 'social_media_time': float, 'read_time': float}. "
                            "All times should be in hours, rounded to one decimal place.",
            agent=agent
        )

    def process_result(self, agent, day, result):
        try:
            if isinstance(result, dict) and all(key in result for key in ['total_time', 'social_media_time', 'read_time']):
                data = result
            else:
                task_output = result.tasks[0].output if hasattr(result, 'tasks') else str(result)
                output_str = task_output.strip().strip('"')
                data = json.loads(output_str)
            
            goal_time = random.randint(2, 9)
            
            return {
                'agent_name': agent.role,
                'day': day,
                'total_time': round(float(data['total_time']), 1),
                'goal_time': goal_time,
                'social_media_time': round(float(data['social_media_time']), 1),
                'read_time': round(float(data['read_time']), 1)
            }
        except Exception as e:
            print(f"Error processing result for {agent.role} on day {day}: {e}")
            return None

    def run_simulation(self, days=7):
        agents = [self.high_usage_agent, self.medium_usage_agent, self.low_usage_agent]
        simulation_results = []
        
        for day in range(1, days + 1):
            for agent in agents:
                task = self.create_simulate_day_task(agent)
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    verbose=True
                )
                
                result = crew.kickoff()
                
                if isinstance(result, list):
                    result = result[0]
                
                processed_result = self.process_result(agent, day, result)
                
                if processed_result:
                    simulation_results.append(processed_result)
        
        return simulation_results
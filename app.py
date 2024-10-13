from flask import Flask, render_template, request, jsonify
from simulations.predefined_sim import run_predefined_simulation
from simulations.user_defined_sim import run_user_defined_simulation
import base64
import io
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

app = Flask(__name__)

def generate_plot(plot_data):
    plt.figure(figsize=(10, 6))
    for label, data in plot_data.items():
        plt.plot(data['x'], data['y'], label=label)
    plt.xlabel('Day')
    plt.ylabel('Total Points')
    plt.title('Simulation Results')
    plt.legend()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()  # Close the figure to free up memory
    return base64.b64encode(img.getvalue()).decode('utf-8')

def generate_table_html(results):
    table_html = "<table><tr><th>User Type</th><th>Day</th><th>Total Time</th><th>Social Media Time</th><th>Read Time</th><th>Day Points</th><th>Total Points</th></tr>"
    for result in results:
        table_html += f"<tr><td>{result['User Type']}</td><td>{result['Day']}</td><td>{result['Total Time']}</td><td>{result['Social Media Time']}</td><td>{result['Read Time']}</td><td>{result['Day Points']}</td><td>{result['Total Points']}</td></tr>"
    table_html += "</table>"
    return table_html

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/predefined_sim')
def predefined_sim():
    return render_template('predefined_sim.html')

@app.route('/user_defined_sim')
def user_defined_sim():
    return render_template('user_defined_sim.html')

@app.route('/run_predefined_sim', methods=['POST'])
def run_predefined_sim():
    try:
        results, plot_data = run_predefined_simulation()
        table_html = generate_table_html(results)
        plot_base64 = generate_plot(plot_data)
        return jsonify({'results': table_html, 'plot': plot_base64})
    except Exception as e:
        print(f"Error in run_predefined_sim: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/run_user_defined_sim', methods=['POST'])
def run_user_defined_sim():
    try:
        data = request.json
        results, plot_data = run_user_defined_simulation(data)
        plot_base64 = generate_plot(plot_data)
        return jsonify({'results': results, 'plot': plot_base64})
    except Exception as e:
        print(f"Error in run_user_defined_sim: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
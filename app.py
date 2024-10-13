from flask import Flask, render_template, request, jsonify
from simulations.predefined_sim import run_predefined_simulation
from simulations.user_defined_sim import run_user_defined_simulation
import base64
import io

app = Flask(__name__)

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
        results, plot = run_predefined_simulation()
        plot_base64 = encode_plot(plot)
        return jsonify({'results': results, 'plot': plot_base64})
    except Exception as e:
        print(f"Error in run_predefined_sim: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/run_user_defined_sim', methods=['POST'])
def run_user_defined_sim():
    try:
        data = request.json
        results, plot = run_user_defined_simulation(data)
        plot_base64 = encode_plot(plot)
        return jsonify({'results': results, 'plot': plot_base64})
    except Exception as e:
        print(f"Error in run_user_defined_sim: {str(e)}")
        return jsonify({'error': str(e)}), 500

def encode_plot(plot):
    if isinstance(plot, io.BytesIO):
        return base64.b64encode(plot.getvalue()).decode('utf-8')
    elif isinstance(plot, str):
        return plot
    else:
        return str(plot)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Paths
MODEL_PATH = os.path.join('models', 'ddos_lstm_model.h5')
SCALER_PATH = os.path.join('models', 'scaler.save')

print("Current working directory:", os.getcwd())
print("Model path exists:", os.path.exists(MODEL_PATH))
print("Scaler path exists:", os.path.exists(SCALER_PATH))

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

if not os.path.exists('attack_log.txt'):
    open('attack_log.txt', 'w').close()

def mitigate_attack(row_id, src_ip="Unknown"):
    log_entry = f"[{datetime.now()}] Attack Detected - Row: {row_id}, Source IP: {src_ip}\n"
    with open("attack_log.txt", "a") as log_file:
        log_file.write(log_entry)
    return log_entry

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        raw_input = request.form.get('raw_input')
        if raw_input:
            raw_values = raw_input.strip().replace(',', '').split()
            if len(raw_values) != 22:
                session['prediction'] = "Error: Expected 22 values."
                session['is_attack'] = False
                session['mitigation'] = None
            else:
                try:
                    src_ip = raw_values[3]
                    indices_to_remove = [2, 3, 5, 21]
                    numeric_values = [float(val) for i, val in enumerate(raw_values) if i not in indices_to_remove]

                    model_input = np.array(numeric_values).reshape(1, -1)
                    model_input_scaled = scaler.transform(model_input)
                    model_input_scaled = model_input_scaled.reshape(1, 1, model_input_scaled.shape[1])

                    prediction = model.predict(model_input_scaled)
                    predicted_class = int(prediction[0][0] > 0.5)

                    if predicted_class == 1:
                        session['is_attack'] = True
                        session['prediction'] = f"🚨 ALERT: Attack Detected from IP: {src_ip}"
                        session['mitigation'] = f"🛡️ Mitigation triggered and logged for IP: {src_ip}"
                        mitigate_attack("WebInput", src_ip)
                    else:
                        session['is_attack'] = False
                        session['prediction'] = "✅ Normal Traffic"
                        session['mitigation'] = None
                except Exception as e:
                    session['prediction'] = f" Error in processing input: {e}"
                    session['is_attack'] = False
                    session['mitigation'] = None

        return redirect(url_for('index'))

    # GET
    prediction_result = session.pop('prediction', None)
    is_attack = session.pop('is_attack', False)
    mitigation_message = session.pop('mitigation', None)

    return render_template('index.html', 
                       prediction=prediction_result, 
                       is_attack=is_attack, 
                       mitigation_message=mitigation_message, 
                       raw_input=raw_input if request.method == 'POST' else '')



if __name__ == '__main__':
    app.run(debug=True)

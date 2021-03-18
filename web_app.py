import numpy as np
from flask import Flask, request, render_template
import pickle

flask_app = Flask(__name__)
model_7 = pickle.load(open('model7.pkl', 'rb'))

@flask_app.route('/')
def home():
    return render_template('web_template.html')

engine_size_min_value = 61
engine_size_max_value = 326

car_price_min = 5118
car_price_max = 41315

@flask_app.route('/predict_model',methods=['POST'])
def predict_model():
    input_values = [int(x) for x in request.form.values()]
    input_values_1 = []
    for x in range(5):
        # Adding 1 for the constant value
        if x == 0:
            input_values_1.append(1)
        # Scaling the engine size value 
        if x == 1:
            input_value = (input_values[x-1] - engine_size_min_value) / (engine_size_max_value - engine_size_min_value)
            input_values_1.append(input_value)
        if x > 1:
            input_values_1.append(input_values[x-1])
    final_input_values = [np.array(input_values_1)]
    prediction = model_7.predict(final_input_values)
    prediction = prediction * (car_price_max - car_price_min) + car_price_min
    prediction_1 = int(prediction[0])
    return render_template('web_template.html', car_price_prediction='Car Price could be: ${}'.format(prediction_1))

if __name__ == "__main__":
    flask_app.run(debug=True)
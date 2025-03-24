from flask import Flask, render_template, request
import ollama

app = Flask(__name__)

def get_response(query):
    prompt = '''
You are a certified Dietician and Healthcare Expert. Answer ONLY health-related questions such as fitness, diseases, nutrition, and well-being.

Rules:
- If asked about non-health topics, reply: "I am a Healthcare Assistant and can answer health-related questions only."
- If asked for medicine names or prescriptions, reply: "Please consult your doctor for medication advice."

User Query:
'''
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are a helpful healthcare expert."},
            {"role": "user", "content": prompt + query}
        ]
    )
    return response['message']['content']

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    bmi_result = ""
    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form.get('query')
            if query.strip():
                result = get_response(query)
        if 'weight' in request.form and 'height' in request.form:
            try:
                weight = float(request.form.get('weight'))
                height = float(request.form.get('height'))
                height_m = height / 100
                bmi = weight / (height_m ** 2)
                bmi_result = f"BMI: {bmi:.2f} - "
                if bmi < 18.5:
                    bmi_result += "Underweight"
                elif 18.5 <= bmi < 24.9:
                    bmi_result += "Normal weight"
                elif 25 <= bmi < 29.9:
                    bmi_result += "Overweight"
                else:
                    bmi_result += "Obese"
            except ValueError:
                bmi_result = "Please enter valid numbers for weight and height."
    
    return render_template('index.html', result=result, bmi_result=bmi_result)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route 1 : Affiche la page HTML
@app.route('/')
def home():
    return render_template('index.html')

# Route 2 : L'API qui reçoit les données du formulaire
@app.route('/api/simulate', methods=['POST'])
def simulate_risk():
    data = request.get_json()
    temp = float(data.get('temp', 0))
    wind = float(data.get('wind', 0))
    humidity = float(data.get('humidity', 0))

    # Règle des 30-30-30
    if temp >= 30 and wind >= 30 and humidity <= 30:
        message = "⚠️ EXTREME RISK! Conditions are optimal for a mega-fire."
        color = "red"
    elif temp >= 25 or wind >= 20 or humidity <= 40:
        message = "⚠️ HIGH RISK. Be careful in the forest."
        color = "darkorange"
    else:
        message = "✅ LOW RISK. Safe conditions."
        color = "green"

    return jsonify({"message": message, "color": color})

if __name__ == '__main__':
    app.run(debug=True)
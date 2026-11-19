from flask import Flask, render_template, jsonify
import csv
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# L'API qui lit ton fichier CSV et fait les calculs
@app.route('/api/bilan')
def get_bilan_data():
    data = []
    # Chemin vers ton fichier dans le dossier 'data'
    filepath = os.path.join('data', 'france_burned_area_bylandcover_2002_2025(in).csv')
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = int(row['Year'])
                
                # Addition de tous les types de surfaces brûlées (en hectares)
                total_hectares = (
                    float(row['Other land']) +
                    float(row['Croplands']) +
                    float(row['Forests']) +
                    float(row['Savannas']) +
                    float(row['Shrublands and grasslands'])
                )
                
                # CITEPA / Calculs d'impact (Estimations : ~15 tonnes CO2 par hectare brûlé)
                co2_tonnes = total_hectares * 15 
                # Une voiture moyenne = ~4.6 tonnes CO2 / an
                cars = co2_tonnes / 4.6
                
                data.append({
                    "year": year,
                    "hectares": round(total_hectares),
                    "co2": round(co2_tonnes),
                    "cars": round(cars)
                })
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
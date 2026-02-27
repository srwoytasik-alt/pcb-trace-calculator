from flask import Flask, render_template, request
from calculator import (
    calculate_trace_width,
    calculate_resistance,
    calculate_voltage_drop,
    COPPER_WEIGHTS
)

app = Flask(__name__)

@app.route("/health")
def health():
    return "OK", 200

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            current = float(request.form.get("current") or 0)
            temp_rise = float(request.form.get("temp_rise") or 0)
            length_mm = float(request.form.get("length_mm") or 0)
            supply_voltage = float(request.form.get("supply_voltage") or 0)
            copper_weight = float(request.form.get("copper_weight") or 1)
            resistance_layer = request.form.get("resistance_layer", "external")

            length = length_mm / 1000

            external_width = calculate_trace_width(
                current, temp_rise, copper_weight, "external"
            )

            internal_width = calculate_trace_width(
                current, temp_rise, copper_weight, "internal"
            )

            if resistance_layer == "internal":
                width_m = internal_width[0] * 0.0000254
            else:
                width_m = external_width[0] * 0.0000254
            thickness_m = COPPER_WEIGHTS[copper_weight]

            resistance = calculate_resistance(length, width_m, thickness_m)
            v_drop = calculate_voltage_drop(current, resistance)

            if supply_voltage > 0:
                v_drop_percent = (v_drop / supply_voltage) * 100
            else:
                v_drop_percent = 0

            result = {
                "external_mil": round(external_width[0], 2),
                "external_mm": round(external_width[1], 3),
                "internal_mil": round(internal_width[0], 2),
                "internal_mm": round(internal_width[1], 3),
                "resistance": round(resistance, 4),
                "voltage_drop": round(v_drop, 4),
                "voltage_drop_percent": round(v_drop_percent, 2),
            }

        except Exception as e:
            print("Error during calculation:", e)
            result = None

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
    
    
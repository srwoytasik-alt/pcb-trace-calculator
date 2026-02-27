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

    # Default empty form values
    form_values = {
        "current": "",
        "temp_rise": "",
        "length_mm": "",
        "supply_voltage": "",
        "copper_weight": "0.5",
        "resistance_layer": "external",
    }

    if request.method == "POST":
        try:
            # Pull raw form values first
            form_values["current"] = request.form.get("current", "")
            form_values["temp_rise"] = request.form.get("temp_rise", "")
            form_values["length_mm"] = request.form.get("length_mm", "")
            form_values["supply_voltage"] = request.form.get("supply_voltage", "")
            form_values["copper_weight"] = request.form.get("copper_weight", "0.5")
            form_values["resistance_layer"] = request.form.get("resistance_layer", "external")

            # Convert to numbers
            current = float(form_values["current"] or 0)
            temp_rise = float(form_values["temp_rise"] or 0)
            length_mm = float(form_values["length_mm"] or 0)
            supply_voltage = float(form_values["supply_voltage"] or 0)
            copper_weight = float(form_values["copper_weight"])
            resistance_layer = form_values["resistance_layer"]

            length = length_mm / 1000

            external_width = calculate_trace_width(
                current, temp_rise, copper_weight, "external"
            )

            internal_width = calculate_trace_width(
                current, temp_rise, copper_weight, "internal"
            )

            if resistance_layer == "internal":
                width_m = internal_width[0] * 0.0000254
                layer_used_label = "Internal Layer"
            else:
                width_m = external_width[0] * 0.0000254
                layer_used_label = "External Layer"

            thickness_m = COPPER_WEIGHTS[copper_weight]

            resistance = calculate_resistance(length, width_m, thickness_m)
            v_drop = calculate_voltage_drop(current, resistance)

            v_drop_percent = (v_drop / supply_voltage) * 100 if supply_voltage > 0 else 0

            result = {
                "external_mil": round(external_width[0], 2),
                "external_mm": round(external_width[1], 3),
                "internal_mil": round(internal_width[0], 2),
                "internal_mm": round(internal_width[1], 3),
                "resistance": round(resistance, 4),
                "voltage_drop": round(v_drop, 4),
                "voltage_drop_percent": round(v_drop_percent, 2),
                "layer_used": layer_used_label,
            }

        except Exception as e:
            return f"Calculation Error: {e}"

    return render_template(
        "index.html",
        result=result,
        form_data=form_values
    )


if __name__ == "__main__":
    app.run(debug=True)
    
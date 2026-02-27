from flask import Flask, render_template, request
from calculator import (
    calculate_trace_width,
    calculate_resistance,
    calculate_voltage_drop,
    COPPER_WEIGHTS
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        current = float(request.form["current"])
        temp_rise = float(request.form["temp_rise"])
        length = float(request.form["length"])
        copper_weight = float(request.form["copper_weight"])

        external_width = calculate_trace_width(
            current, temp_rise, copper_weight, "external"
        )

        internal_width = calculate_trace_width(
            current, temp_rise, copper_weight, "internal"
        )

        width_m = external_width[0] * 0.0000254
        thickness_m = COPPER_WEIGHTS[copper_weight]

        resistance = calculate_resistance(length, width_m, thickness_m)
        v_drop = calculate_voltage_drop(current, resistance)

        result = {
            "external": external_width,
            "internal": internal_width,
            "resistance": resistance,
            "voltage_drop": v_drop,
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
    
    
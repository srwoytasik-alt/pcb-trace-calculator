# calculator.py

COPPER_RESISTIVITY = 1.724e-8  # ohm-meter

COPPER_WEIGHTS = {
    0.5: 17.5e-6,
    1: 35e-6,
    2: 70e-6,
    3: 105e-6
}


def get_ipc_constants(layer_type):
    if layer_type == "external":
        return 0.048, 0.44, 0.725
    elif layer_type == "internal":
        return 0.024, 0.44, 0.725
    else:
        raise ValueError("Invalid layer type")


def calculate_trace_width(current, temp_rise, copper_weight, layer_type):
    k, b, c = get_ipc_constants(layer_type)

    area_mils = (current / (k * (temp_rise ** b))) ** (1 / c)

    thickness_m = COPPER_WEIGHTS[copper_weight]
    thickness_mil = thickness_m / 0.0000254

    width_mil = area_mils / thickness_mil
    width_mm = width_mil * 0.0254

    return width_mil, width_mm


def calculate_resistance(length_m, width_m, thickness_m):
    area = width_m * thickness_m
    return COPPER_RESISTIVITY * (length_m / area)


def calculate_voltage_drop(current, resistance):
    return current * resistance

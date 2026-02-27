import math

COPPER_RESISTIVITY = 1.724e-8  # ohm-meter

COPPER_WEIGHTS = {
    0.5: 17.5e-6,
    1: 35e-6,
    2: 70e-6,
    3: 105e-6
}


def get_ipc_constants(layer_type):
    if layer_type.lower() == "external":
        return 0.048, 0.44, 0.725
    elif layer_type.lower() == "internal":
        return 0.024, 0.44, 0.725
    else:
        raise ValueError("Layer type must be 'external' or 'internal'")


def trace_width(current, temp_rise, copper_weight, layer_type):
    k, b, c = get_ipc_constants(layer_type)

    area_mils = (current / (k * (temp_rise ** b))) ** (1 / c)

    thickness_m = COPPER_WEIGHTS[copper_weight]

    # convert thickness to mils
    thickness_mil = thickness_m / 0.0000254

    width_mil = area_mils / thickness_mil

    return width_mil


def trace_resistance(length_m, width_m, thickness_m):
    area = width_m * thickness_m
    return COPPER_RESISTIVITY * (length_m / area)


def voltage_drop(current, resistance):
    return current * resistance


if __name__ == "__main__":
    current = float(input("Current (A): "))
    temp_rise = float(input("Temperature rise (C): "))
    length = float(input("Trace length (meters): "))
    copper_weight = float(input("Copper weight (0.5, 1, 2, 3 oz): "))
    layer_type = input("Layer type (external/internal): ")

    width_mil = trace_width(current, temp_rise, copper_weight, layer_type)

    print(f"\nRequired trace width: {width_mil:.2f} mil")

    width_m = width_mil * 0.0000254
    thickness_m = COPPER_WEIGHTS[copper_weight]

    resistance = trace_resistance(length, width_m, thickness_m)
    v_drop = voltage_drop(current, resistance)

    print(f"Trace resistance: {resistance:.6f} ohms")
    print(f"Voltage drop: {v_drop:.6f} V")
    
    
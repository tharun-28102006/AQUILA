
from environment import create_environment
from classifier import classify_environment


def encode_state(temperature_state,
                 salinity_state,
                 turbidity_state,
                 range_state):

    """
    Convert four 2-bit states into an 8-bit LUT address.

    Bit arrangement:

    [7:6] = Temperature
    [5:4] = Salinity
    [3:2] = Turbidity
    [1:0] = AUV-Seabed Range
    """

    address = (
        (temperature_state << 6)
        | (salinity_state << 4)
        | (turbidity_state << 2)
        | range_state
    )

    return address


def encode_environment(env):

    states = classify_environment(env)

    address = encode_state(
        states[0],
        states[1],
        states[2],
        states[3]
    )

    return states, address



if __name__ == "__main__":


    env = create_environment(
        temperature=28.0,
        salinity=450.0,
        turbidity=35.0,
        range_m=2.5
    )

    states, address = encode_environment(env)

    print()
    print("==========================================")
    print("        AQUILA STATE ENCODER TEST")
    print("==========================================")

    print()
    print("INPUT")
    print("------------------------------------------")
    print(f"Temperature      : {env.temperature} °C")
    print(f"Salinity         : {env.salinity}")
    print(f"Turbidity        : {env.turbidity}")
    print(f"AUV-Seabed Range : {env.range_m} m")

    print()
    print("CLASSIFICATION")
    print("------------------------------------------")
    print(f"Temperature State : {states[0]}")
    print(f"Salinity State    : {states[1]}")
    print(f"Turbidity State   : {states[2]}")
    print(f"Range State       : {states[3]}")

    print()
    print("8-BIT LUT ADDRESS")
    print("------------------------------------------")

    print(f"Binary : {address:08b}")
    print(f"Hex    : 0x{address:02X}")
    print(f"Decimal: {address}")

    print()
    print("BIT MAPPING")
    print("------------------------------------------")
    print("[7:6] Temperature")
    print("[5:4] Salinity")
    print("[3:2] Turbidity")
    print("[1:0] AUV-Seabed Range")
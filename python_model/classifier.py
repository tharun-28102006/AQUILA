
from environment import Environment
from config import (
    RANGE_FAR_M,
    RANGE_NEAR_M,
    SALINITY_HIGH,
    SALINITY_LOW,
    TEMPERATURE_HIGH_C,
    TEMPERATURE_LOW_C,
    TURBIDITY_HIGH,
    TURBIDITY_LOW,
)


RANGE_NEAR = RANGE_NEAR_M
RANGE_FAR = RANGE_FAR_M
TEMPERATURE_LOW = TEMPERATURE_LOW_C
TEMPERATURE_HIGH = TEMPERATURE_HIGH_C


def classify_temperature(value):
    if value < TEMPERATURE_LOW:
        return 0
    elif value <= TEMPERATURE_HIGH:
        return 1
    else:
        return 2


def classify_salinity(value):
    if value < SALINITY_LOW:
        return 0
    elif value <= SALINITY_HIGH:
        return 1
    else:
        return 2


def classify_turbidity(value):
    if value < TURBIDITY_LOW:
        return 0
    elif value <= TURBIDITY_HIGH:
        return 1
    else:
        return 2


def classify_range(value):
    if value < RANGE_NEAR:
        return 0
    elif value <= RANGE_FAR:
        return 1
    else:
        return 2


def classify_environment(env: Environment):

    temperature_state = classify_temperature(env.temperature)
    salinity_state = classify_salinity(env.salinity)
    turbidity_state = classify_turbidity(env.turbidity)
    range_state = classify_range(env.range_m)

    return (
        temperature_state,
        salinity_state,
        turbidity_state,
        range_state
    )


def state_name(state):

    names = {
        0: "LOW",
        1: "MEDIUM",
        2: "HIGH"
    }

    return names[state]



if __name__ == "__main__":

    env = Environment(
        temperature=28.0,
        salinity=450.0,
        turbidity=35.0,
        range_m=2.5
    )

    states = classify_environment(env)

    print("AQUILA Environmental Classification")
    print("-----------------------------------")

    print(f"Temperature : {state_name(states[0])}")
    print(f"Salinity    : {state_name(states[1])}")
    print(f"Turbidity   : {state_name(states[2])}")
    print(f"Range       : {state_name(states[3])}")
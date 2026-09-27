
from dataclasses import dataclass


@dataclass
class Environment:
    """
    Environmental and range inputs for AQUILA.

    These values represent sensor inputs in the simulation.
    """

    temperature: float       # °C
    salinity: float          # Relative salinity/TDS value
    turbidity: float         # Turbidity value
    range_m: float           # AUV-Seabed distance in meters


def create_environment(
    temperature: float,
    salinity: float,
    turbidity: float,
    range_m: float
) -> Environment:

    return Environment(
        temperature=temperature,
        salinity=salinity,
        turbidity=turbidity,
        range_m=range_m
    )



if __name__ == "__main__":

    env = create_environment(
        temperature=28.0,
        salinity=450.0,
        turbidity=35.0,
        range_m=2.5
    )

    print("AQUILA Environmental Input")
    print("---------------------------")
    print(f"Temperature       : {env.temperature} °C")
    print(f"Salinity          : {env.salinity}")
    print(f"Turbidity         : {env.turbidity}")
    print(f"AUV-Seabed Range  : {env.range_m} m")
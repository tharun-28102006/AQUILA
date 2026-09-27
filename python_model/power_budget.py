from dataclasses import dataclass


SUPPLY_V = 3.3
OUTPUT_VPP_V = 2.0
LOAD_OHMS = 50.0


@dataclass(frozen=True)
class ComponentEstimate:
    name: str
    current_ma: float
    supply_v: float
    category: str


COMPONENTS = (
    ComponentEstimate("FPGA", 150.0, 3.3, "quiescent/dynamic estimate"),
    ComponentEstimate("Environmental sensors", 20.0, 3.3, "quiescent estimate"),
    ComponentEstimate("MCP3208", 2.0, 3.3, "quiescent estimate"),
    ComponentEstimate("Level translator", 10.0, 3.3, "quiescent estimate"),
    ComponentEstimate("AD3541R", 25.0, 3.3, "quiescent estimate"),
    ComponentEstimate("OPA2835", 10.0, 5.0, "quiescent estimate"),
    ComponentEstimate("OPA2684", 20.0, 5.0, "quiescent estimate"),
)


def load_power():
    vrms = OUTPUT_VPP_V / (2.0 * (2.0 ** 0.5))
    return vrms ** 2 / LOAD_OHMS


def main():
    electronics_w = sum(item.current_ma * item.supply_v / 1000.0 for item in COMPONENTS)
    quiescent_w = sum(
        item.current_ma * item.supply_v / 1000.0
        for item in COMPONENTS
        if item.category == "quiescent estimate"
    )
    dynamic_w = electronics_w - quiescent_w
    output_w = load_power()

    print("SIMULATION / DESIGN ESTIMATE")
    print("Component values are configurable estimates, not measured consumption.")
    for item in COMPONENTS:
        print(f"{item.name:24s}: {item.current_ma:7.2f} mA, {item.supply_v:4.1f} V, {item.category}")
    print(f"Electronics total estimate : {electronics_w:.4f} W")
    print(f"Quiescent estimate         : {quiescent_w:.4f} W")
    print(f"Dynamic estimate           : {dynamic_w:.4f} W")
    print(f"50 ohm load power estimate : {output_w:.6f} W")
    print(f"Combined estimate          : {electronics_w + output_w:.4f} W")


if __name__ == "__main__":
    main()

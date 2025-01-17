import json


# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


# Calculate total projected loss with additional complexity and errors
def calculate_projected_losses(building_data, num_years=10):
    total_loss = 0

    for building in building_data:
        floor_area = building["floor_area"]
        construction_cost = building["construction_cost"]
        hazard_probability = building["hazard_probability"]
        inflation_rate = building["inflation_rate"]

        # Calculate future cost
        # Correction: include number of years and floor area
        compound_factor = (1 + inflation_rate) ** num_years
        future_cost = (construction_cost * floor_area) * compound_factor

        # Calculate risk-adjusted loss
        ## Correction: removed (1 - hazard probability) as it is the negative probability ##
        ## Note: Risk adjusted loss is a future risk adjusted loss
        risk_adjusted_loss = future_cost * hazard_probability

        # Calculate present value of the risk-adjusted loss
        # Correction: factor by number of years
        discount_rate = 0.05
        discount_factor = (1 + discount_rate) ** num_years
        present_value_loss = risk_adjusted_loss / discount_factor

        # Calculate maintenance and total maintenance cost
        ## Note: maintenence costs is not mentioned in requirements so it is unclear if it should be left here ##
        maintenance_cost = floor_area * 50  # assuming a flat rate per square meter
        total_maintenance_cost = maintenance_cost / discount_rate

        # Total loss calculation
        total_loss += present_value_loss + total_maintenance_cost

    return total_loss


# Main execution function
def main():
    data = load_data("data.json")
    total_projected_loss = calculate_projected_losses(data)
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")


if __name__ == "__main__":
    main()

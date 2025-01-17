import json
import math
import time


# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


# Calculate total projected loss with additional complexity and errors
def calculate_projected_losses(
    building_data, standard_discount_rate=0.05, num_years=10
):
    """
    An implementation of the Complex Loss Calculation Formula written for ease of
    reading and without consideration of optimisation.
    """
    total_loss = 0
    individual_losses = {}

    for building in building_data:
        floor_area = building["floor_area"]
        construction_cost = building["construction_cost"]
        hazard_probability = building["hazard_probability"]
        inflation_rate = building["inflation_rate"]
        building_id = building["buildingId"]

        exponent = math.exp(inflation_rate * floor_area / 1000)
        cost = construction_cost * exponent * hazard_probability
        discount = (1 + standard_discount_rate) ** num_years

        loss_estimate = cost / discount
        individual_losses[building_id] = loss_estimate
        total_loss += loss_estimate

    return total_loss, individual_losses


# Main execution function
def main():
    data = load_data("data.json")
    start = time.time()
    total_projected_loss, individual_losses = calculate_projected_losses(data)
    end = time.time()
    print(f"Individual Losses: {individual_losses}")
    print(f"Duration: {(end - start):.2f}")
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")


if __name__ == "__main__":
    main()

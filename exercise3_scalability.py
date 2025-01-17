from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count
import json
import math
import numpy as np
import time


# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


def calculate_projected_losses_numpy(
    building_data, standard_discount_rate=0.05, num_years=10
):

    inflation_rate = np.array(
        [building["inflation_rate"] for building in building_data]
    )
    floor_area = np.array([building["floor_area"] for building in building_data])
    hazard_probability = np.array(
        [building["hazard_probability"] for building in building_data]
    )
    construction_cost = np.array(
        [building["construction_cost"] for building in building_data]
    )

    exponent = np.exp(inflation_rate * floor_area / 1000)
    cost = construction_cost * exponent * hazard_probability
    discount = (1 + standard_discount_rate) ** num_years
    individual_losses = cost / discount

    return np.sum(individual_losses), individual_losses


def make_chunks(list, size):
    for i in range(0, len(list), size):
        yield list[i : i + size]


def parallel_calculate_losses(data):
    num_workers = max(cpu_count() - 2, 1)

    chunk_size = math.ceil(len(data) / num_workers)
    chunks = make_chunks(data, chunk_size)

    with Pool(processes=num_workers) as pool:
        # Map the function to chunks and get results
        results = pool.map(calculate_projected_losses_numpy, chunks)

        # Unzip the results into separate lists
        chunk_totals, chunk_losses = zip(*results)

        # Calculate total loss and combine all losses
        total_loss = sum(chunk_totals)
        all_losses = np.concatenate(chunk_losses)

    return total_loss, all_losses


# Main execution function
def main():
    data = load_data("data.json")
    data_long = [data[0] for i in range(100_000_000)]

    start = time.time()
    individual_losses = []
    total_projected_loss, individual_losses = parallel_calculate_losses(data_long)

    end = time.time()
    print(f"Individual Losses ({len(individual_losses)}): {individual_losses}")
    print(f"Duration: {(end - start):.2f}")
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")


if __name__ == "__main__":
    main()

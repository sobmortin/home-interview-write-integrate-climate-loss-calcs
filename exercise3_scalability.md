## Exercise 3: Scaling the Loss Calculation Model

A simple script using python for loops is acceptable for a small dataset, though there are a number of improvements that could be made to improve the scalability in both the way the data is read and how it is processed. The script in excercise2, in it's simplest form benchmarks to ~20s for 100 million rows. Implementing some of the following changes made a 75% reduction in time to ~5s, but still further improvements could be made.

### Reading in Data

I would consider whether json is the optmimal method of reading in the data and whether csv would be better. The bloated nature of JSON with its repeated keys means that more memory would be used and processihg slowed. If json is required then using a library like ijson or pandas allows the data to be read in chunks and reduce the memory usage.

### Processing Data


1. Using NumPy to benefit from the increased speed of the library, avoiding native python loops. NumPy vectorization allows for batch calculation which is much faster, and also manages memory more efficiently:

    ```python
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
    ```

2. Reading and processing in batches is also a faster and safer way to manage large datasets. First of all, should a file be very large, trying to reading it all into memory at once could crash the program orresult in bottleneck issues. Furthermore, the nature of this calculation doing lends itself very nicely to parrelisation, and chunks are a good way of distributing calcations across available processes.

3. Implementing threading / multicore processing for parrallel computing. As all of these calulcations are made independently and aggregated, they can very easily be sped up with parrallel processing. The below snippet shows one implementation, taking into consideration the resources available :

    ```python

    def parallel_calculate_losses(data):
        num_workers = max(cpu_count() - 1, 1)
        chunk_size = math.ceil(len(data) / num_workers)
        chunks = make_chunks(data, chunk_size)
        with Pool(processes=num_workers) as pool:
            results = pool.map(calculate_projected_losses_numpy, chunks)
            chunk_totals, chunk_losses = zip(*results)
            total_loss = sum(chunk_totals)
            individual_losses = np.concatenate(chunk_losses)

        return total_loss, individual_losses
    ```

Ultimately a combination of all methods would be ideal, but the exact implementation would depend on priorities and constraints such as speed and cost. A full working version is shown in `exercise3_scalability.py`
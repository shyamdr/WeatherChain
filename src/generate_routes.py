import pandas as pd
import numpy as np

np.random.seed(42)
num_routes = 10
routes = pd.DataFrame({
    "route_id": range(1, num_routes + 1),
    "start_lat": np.random.uniform(8, 37, num_routes),
    "start_lon": np.random.uniform(68, 97, num_routes),
    "end_lat": np.random.uniform(8, 37, num_routes),
    "end_lon": np.random.uniform(68, 97, num_routes),
    "travel_days": np.random.randint(1, 5, num_routes)
})
routes.to_csv("data/routes_small.csv", index=False)
print("Generated data/routes_small.csv with 10 routes.")
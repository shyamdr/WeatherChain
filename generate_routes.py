import pandas as pd
import numpy as np

np.random.seed(42)
num_routes = 10000
routes = pd.DataFrame({
    "route_id": range(1, num_routes + 1),
    "start_lat": np.random.uniform(-90, 90, num_routes),
    "start_lon": np.random.uniform(-180, 180, num_routes),
    "end_lat": np.random.uniform(-90, 90, num_routes),
    "end_lon": np.random.uniform(-180, 180, num_routes),
    "travel_days": np.random.randint(1, 5, num_routes)
})
routes.to_csv("routes_large.csv", index=False)
print("Generated routes_large.csv with 10,000 routes.")
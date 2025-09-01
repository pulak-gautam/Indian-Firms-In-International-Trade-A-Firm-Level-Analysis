import pandas as pd
import numpy as np

# Load the dataset
file_path = 'classfn_4064_final.csv'
data = pd.read_csv(file_path)

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on the earth."""
    R = 6371  # Earth radius in kilometers
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    return R * c

# Step 1: Calculate minimum distance to GQ for each firm
gq_cities = {
    "Delhi": (28.6139, 77.2090), "Mumbai": (19.0760, 72.8777), "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707), "Ahmedabad": (23.0225, 72.5714), "Pune": (18.5204, 73.8567),
    "Surat": (21.1702, 72.8311), "Vadodara": (22.3072, 73.1812), "Jaipur": (26.9124, 75.7873),
    "Udaipur": (24.5854, 73.7125), "Nagpur": (21.1458, 79.0882), "Varanasi": (25.3176, 82.9739),
    "Allahabad": (25.4358, 81.8463), "Kanpur": (26.4499, 80.3319), "Agra": (27.1767, 78.0081),
    "Gwalior": (26.2183, 78.1828), "Ranchi": (23.3441, 85.3096), "Bhubaneswar": (20.2961, 85.8245),
    "Vishakhapatnam": (17.6868, 83.2185)
}

firm_distances_gq = []
nearest_cities_gq = []
for index, row in data.iterrows():
    distances_to_cities = {city: haversine_distance(row['Latitude'], row['Longitude'], lat, lon) for city, (lat, lon) in gq_cities.items()}
    nearest_city = min(distances_to_cities, key=distances_to_cities.get)
    min_dist = distances_to_cities[nearest_city]
    firm_distances_gq.append(min_dist)
    nearest_cities_gq.append(nearest_city)

data['min_distance_to_GQ'] = firm_distances_gq
data['nearest_city_to_GQ'] = nearest_cities_gq

# Step 2: Calculate distance to Delhi-Meerut Expressway
delhi_meerut_points = [(28.6139, 77.2090), (28.6270, 77.2773), (28.7440, 77.4995), (28.9845, 77.7064), (29.0832, 77.7109)]
data['distance_to_Delhi_Meerut'] = data.apply(
    lambda row: min([haversine_distance(row['Latitude'], row['Longitude'], p_lat, p_lon) for p_lat, p_lon in delhi_meerut_points]), axis=1
)

# Step 3: Calculate distance to WDFC
wdfc_points = [(28.7041, 77.1025), (27.0238, 74.2179), (26.9124, 75.7873), (25.4358, 78.5685), (22.7196, 75.8577), (23.2599, 77.4126), (21.1702, 72.8311), (19.0760, 72.8777)]
data['distance_to_WDFC'] = data.apply(
    lambda row: min([haversine_distance(row['Latitude'], row['Longitude'], p_lat, p_lon) for p_lat, p_lon in wdfc_points]), axis=1
)

# Step 4: Calculate distance to EDFC
edfc_points = [(30.9000, 75.8573), # Ludhiana
               (26.4499, 80.3319), # Kanpur
               (24.9807, 84.0374)] # Sonnagar
data['distance_to_EDFC'] = data.apply(
    lambda row: min([haversine_distance(row['Latitude'], row['Longitude'], p_lat, p_lon) for p_lat, p_lon in edfc_points]), axis=1
)

# Save the updated DataFrame to a new CSV file
output_file_path = 'firm_proximity_data.csv'
data.to_csv(output_file_path, index=False)

print(f"Proximity data calculated and saved to {output_file_path}")

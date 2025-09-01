from matplotlib.pyplot import plt
import pandas as pd

# Load the dataset
file_path = 'classfn_4064_final.csv'
data = pd.read_csv(file_path)

# Plotting the latitude and longitude points directly without a base map
plt.figure(figsize=(10, 10))
plt.scatter(data['Longitude'], data['Latitude'], color='red', s=10, label="Locations")

# Setting latitude and longitude boundaries typical for India's geographic area
plt.xlim(68, 98) # India's approximate longitude range
plt.ylim(6, 38) # India's approximate latitude range

# Customizing the plot for plotting the firms on map
plt.title("Geographical Plot of Locations within India")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.grid(True) # Added for better readability
plt.show()

# code to generate data
import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)

# Parameters for dataset generation
num_buildings = 1000  # Number of buildings to simulate

# Generate Building IDs
building_ids = [f"B{str(i).zfill(4)}" for i in range(1, num_buildings + 1)]

# Generate Building Characteristics
building_sizes = np.random.randint(50, 5000, size=num_buildings)  # Size in square meters
building_ages = np.random.randint(1, 100, size=num_buildings)  # Age in years
insulation_types = np.random.choice(['Poor', 'Fair', 'Good', 'Excellent'], size=num_buildings, p=[0.2, 0.3, 0.3, 0.2])

# Generate Weather Data
temperatures = np.random.uniform(-10, 40, size=num_buildings)  # Temperature in Celsius
humidities = np.random.uniform(10, 90, size=num_buildings)  # Humidity in percentage

# Generate Energy Consumption Data
# Energy consumption is influenced by building size, age, insulation, temperature, and humidity
base_energy = building_sizes * np.random.uniform(0.05, 0.15, size=num_buildings)  # Base energy usage
age_factor = building_ages * np.random.uniform(0.1, 0.5, size=num_buildings)  # Older buildings consume more
insulation_factor = [0.8 if i == 'Excellent' else 1.0 if i == 'Good' else 1.2 if i == 'Fair' else 1.5 for i in insulation_types]
weather_factor = (temperatures * 0.5 + humidities * 0.3)  # Weather impact on energy consumption
energy_consumption = base_energy + age_factor + weather_factor * insulation_factor

# Generate Supplier Lead Time
supplier_lead_times = np.random.randint(1, 30, size=num_buildings)  # Lead time in days

# Generate Renewable Energy Source
renewable_energy_sources = np.random.choice(['Solar', 'Wind', 'None'], size=num_buildings, p=[0.4, 0.3, 0.3])

# Create DataFrame
data = pd.DataFrame({
    'BuildingID': building_ids,
    'BuildingSize': building_sizes,
    'BuildingAge': building_ages,
    'InsulationType': insulation_types,
    'Temperature': temperatures,
    'Humidity': humidities,
    'EnergyConsumption': energy_consumption,
    'SupplierLeadTime': supplier_lead_times,
    'RenewableEnergySource': renewable_energy_sources
})

# Save to CSV
data.to_csv('building_energy_data.csv', index=False)

print("Synthetic dataset generated and saved as 'building_energy_data.csv'.")

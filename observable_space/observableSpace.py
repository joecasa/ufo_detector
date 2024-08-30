import numpy as np
import matplotlib.pyplot as plt

# Constants in US customary units
R_earth = 3959  # Earth radius in miles
observer_height = 6 / 5280  # Observer height in miles (6 feet converted to miles)

# Function to calculate the distance from the observer's eyes to a point on the ground
def ground_distance_corrected(angle_deg):
    angle_rad = np.radians(angle_deg)
    d = np.sqrt((R_earth + observer_height)**2 + R_earth**2 - 2 * (R_earth + observer_height) * R_earth * np.cos(angle_rad))
    return d  # Distance in miles

# Calculate the blocking angle
blocked_angle_corrected = np.degrees(np.arccos(R_earth / (R_earth + observer_height)))
blocked_distance_corrected = ground_distance_corrected(blocked_angle_corrected)

# Angle positions
angles_full_range = np.linspace(-180, 180, 1000)
angles_zoomed_corrected = np.linspace(-0.05, 0.05, 500)

# Calculate distances
distances_full_range = ground_distance_corrected(angles_full_range)
distances_zoomed_corrected = ground_distance_corrected(angles_zoomed_corrected)

# Set up the figure with two subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 12))

# First plot: Full range from -180 to 180 degrees
axs[0].plot(angles_full_range, distances_full_range, label="Distance from Observer's Eyes to Point on Ground")
axs[0].axvline(x=-blocked_angle_corrected, color='red', linestyle='--', label=f'Blocked at {blocked_angle_corrected:.2f} degrees')
axs[0].axvline(x=blocked_angle_corrected, color='red', linestyle='--')
axs[0].scatter([-blocked_angle_corrected, blocked_angle_corrected], [blocked_distance_corrected, blocked_distance_corrected], color='red')
axs[0].text(-blocked_angle_corrected, blocked_distance_corrected, f'({-blocked_angle_corrected:.2f} degrees, {blocked_distance_corrected:.2f} miles)', color='red', ha='right')
axs[0].text(blocked_angle_corrected, blocked_distance_corrected, f'({blocked_angle_corrected:.2f} degrees, {blocked_distance_corrected:.2f} miles)', color='red', ha='left')
axs[0].set_xlim(-180, 180)
axs[0].set_ylim(0, max(distances_full_range) + 0.5)
axs[0].set_xlabel("Angular Distance (degrees)")
axs[0].set_ylabel("Distance (miles)")
axs[0].set_title("Full Plot: Distance from Observer's Eyes to Point on Ground (6' AGL)")
axs[0].legend()
axs[0].grid(True)

# Second plot: Zoomed in, ensuring the line reaches the intersections
axs[1].plot(angles_zoomed_corrected, distances_zoomed_corrected, label="Distance from Observer's Eyes to Point on Ground")
axs[1].axvline(x=-blocked_angle_corrected, color='red', linestyle='--', label=f'Blocked at {blocked_angle_corrected:.2f} degrees')
axs[1].axvline(x=blocked_angle_corrected, color='red', linestyle='--')
axs[1].scatter([-blocked_angle_corrected, blocked_angle_corrected], [blocked_distance_corrected, blocked_distance_corrected], color='red')
axs[1].text(-blocked_angle_corrected, blocked_distance_corrected, f'({-blocked_angle_corrected:.2f} degrees, {blocked_distance_corrected:.2f} miles)', color='red', ha='right')
axs[1].text(blocked_angle_corrected, blocked_distance_corrected, f'({blocked_angle_corrected:.2f} degrees, {blocked_distance_corrected:.2f} miles)', color='red', ha='left')
axs[1].set_xlim(-0.05, 0.05)
axs[1].set_ylim(0, 3.5)  # Set y-axis to 0 - 3.5 miles
axs[1].set_xlabel("Angular Distance (degrees)")
axs[1].set_ylabel("Distance (miles)")
axs[1].set_title("Zoomed Plot: Distance from Observer's Eyes to Point on Ground (6' AGL)")
axs[1].legend()
axs[1].grid(True)

# Show both plots
plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Constants
A = 5  # Amplitude in meter
wavelength = np.pi / 10  # Wavelength of light in meters
k = 2 * np.pi / wavelength  # Wave number
screen_position = 5  # Position of the screen

# Sources coordinates
d = 1  # distance between each slit
n = 1  # Number of slits

# Find location of splits
def splits_loc(n, d):
    shift = 0
    splits = []
    r = n % 2
    if r == 1:
        splits.append([0, 0])
        shift = 0
    else:
        shift = d / 2
    h = round((n - r) / 2)
    for k in range(1, h + 1):
        y_s = k * d - shift
        s_1 = [0, y_s]
        s_2 = [0, -y_s]
        splits.append(s_1)
        splits.append(s_2)
    return splits

# Define the observation plane coordinates
x_obs = np.linspace(0, 10, 1000)  # x-coordinates in the observation plane
y_obs = np.linspace(-5, 5, 1000)  # y-coordinates in the observation plane

# Create a meshgrid of the observation plane coordinates
X_obs, Y_obs = np.meshgrid(x_obs, y_obs)

def intensity_interference(n,d,k):
    splits = splits_loc(n, d)  # Splits location
    field_amplitude = np.zeros_like(X_obs)
    intensity = np.zeros_like(X_obs)
    for source in splits:
        # Calculate the distance from each point in the observation plane to the slit
        r = np.sqrt(((X_obs - source[0]) ** 2) + ((Y_obs - source[1]) ** 2))
        # Calculate the electric field amplitude at each point in the observation plane
        field_amplitude += (A + A * np.sin(k * r))
        
    # Calculate the intensity at each point in the observation plane
    intensity = np.abs(field_amplitude) ** 2
    
    # Calculate the diffraction pattern at the screen position
    index =  np.argmin(np.abs(x_obs - screen_position)) # Find closet value of screen_position
    Y_obs_index = np.where(X_obs == x_obs[index])[1]
    intensity_screen = intensity[:,Y_obs_index]
    
    return intensity,intensity_screen,splits
    
def plot_intensity(intensity,intensity_screen,splits):
    # Plot the intensity pattern
    ax1.imshow(intensity, extent=[x_obs.min(), x_obs.max(), y_obs.min(), y_obs.max()], cmap='gray', aspect='1')
    # Plot point source, separated from intensity image
    for source in splits:
        ax1.scatter(source[0], source[1], color='red', marker='o')
    ax1.axvline(x=screen_position, color='r', linestyle='--')
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.set_title('Wave propagation Pattern')
    # Set ylim so that the y axis has the same y limit as image ax1.imshow
    ax1.set_ylim([-5,5])
    # Plot the diffraction pattern  
    ax2.imshow(intensity_screen, cmap='gray', aspect='7')
    ax2.axis('off')
    ax2.set_title('Diffraction Pattern')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 2))
intensity,intensity_screen,splits = intensity_interference(n,d,k)
plot_intensity(intensity,intensity_screen,splits)

# Create sliders
ax_n = plt.axes([0.15, 0.15, 0.7, 0.025])
ax_d = plt.axes([0.15, 0.1, 0.7, 0.025])
ax_k = plt.axes([0.15, 0.05, 0.7, 0.025])

# Define slider parameters
slider_n = Slider(ax_n, 'Slits (n)', 1, 20, valinit=n, valstep=1,)
slider_d = Slider(ax_d, 'Slit distance (d)', 0.1, 5, valinit=d, valstep=0.01)
slider_k = Slider(ax_k, 'Wavenumber (k)', 0.1, 40, valinit=k, valstep=0.01)

def update(val):
    # Get slider values
    n = int(slider_n.val)
    d = slider_d.val
    k = slider_k.val
    ax1.cla()  
    ax2.cla()
    # Update intensity_interference
    intensity,intensity_screen,splits = intensity_interference(n,d,k)
    # Clear the current plot
    plot_intensity(intensity,intensity_screen,splits)
    fig.canvas.draw_idle()

# Connect update function to slider events
slider_n.on_changed(update)
slider_d.on_changed(update)
slider_k.on_changed(update)

plt.tight_layout()
plt.show()

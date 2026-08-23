"""Inline animation helper for ME 418 Lab 2B."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.transforms as transforms
from matplotlib import animation
from IPython.display import HTML
from scipy import ndimage


def _resize_image(image, max_dimension):
    """Resize large images before animation frames are rendered."""
    height, width = image.shape[:2]
    scale = min(1.0, max_dimension / max(height, width))
    if scale == 1.0:
        return image

    zoom = (scale, scale, 1) if image.ndim == 3 else (scale, scale)
    return ndimage.zoom(image, zoom, order=1)


def _make_edge_background_transparent(image, tolerance=18):
    """Make only the border-connected image background transparent."""
    rgba = np.array(image, dtype=float, copy=True)
    if rgba.max() > 1.0:
        rgba /= 255.0

    if rgba.shape[2] == 3:
        alpha = np.ones(rgba.shape[:2] + (1,), dtype=rgba.dtype)
        rgba = np.concatenate([rgba, alpha], axis=2)

    background_color = rgba[0, 0, :3]
    color_distance = np.linalg.norm(rgba[:, :, :3] - background_color, axis=2)
    background_candidate = color_distance <= tolerance / 255.0

    labels, _ = ndimage.label(background_candidate)
    edge_labels = np.unique(np.concatenate([
        labels[0, :],
        labels[-1, :],
        labels[:, 0],
        labels[:, -1],
    ]))
    edge_labels = edge_labels[edge_labels != 0]
    edge_background = np.isin(labels, edge_labels)

    rgba[edge_background, 3] = 0.0
    return rgba


def animateLanding(output, tf, frame_step=200, rocket_path='PolyX.png', landing_pad_path='Landing Pad.png'):
    """Create an inline animation of the booster landing using the lab images.

    Parameters
    ----------
    output : ndarray
        Simulation output with columns [time, angle, angular_rate, controller_output].
    tf : float
        Final simulation time.
    frame_step : int
        Use every frame_step samples from output to keep the animation lightweight.
    rocket_path : str
        Path to the rocket image, relative to the notebook directory.
    landing_pad_path : str
        Path to the landing-pad image, relative to the notebook directory.
    """
    rocket_img = _make_edge_background_transparent(_resize_image(mpimg.imread(rocket_path), 420))
    landing_pad_img = _resize_image(mpimg.imread(landing_pad_path), 900)

    sampled = output[::frame_step]
    if sampled[-1, 0] != output[-1, 0]:
        sampled = np.vstack([sampled, output[-1]])

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(0.0, 6.0)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.imshow(landing_pad_img, extent=(-2.2, 2.2, 0.0, 0.34), aspect='auto', zorder=1)

    image_height, image_width = rocket_img.shape[:2]
    rocket_height = 1.95
    rocket_width = rocket_height * image_width / image_height
    rocket_extent = (-rocket_width/2, rocket_width/2, -rocket_height/2, rocket_height/2)
    rocket_artist = ax.imshow(rocket_img, extent=rocket_extent, zorder=3)

    time_text = ax.text(-2.05, 5.65, '', fontsize=10)

    final_y = 1.22
    initial_y = 5.05
    tau_y = max(tf / 4, 1e-6)

    def update(frame_index):
        time = sampled[frame_index, 0]
        theta = sampled[frame_index, 1]

        # The image is upright when theta = pi. If theta goes to 0, the rocket
        # appears upside down, matching the original animation behavior.
        display_angle = theta - np.pi
        y = final_y + (initial_y - final_y) * np.exp(-time / tau_y)

        transform = transforms.Affine2D().rotate(display_angle).translate(0.0, y) + ax.transData
        rocket_artist.set_transform(transform)
        time_text.set_text(f't = {time:4.1f} s')
        return rocket_artist, time_text

    anim = animation.FuncAnimation(fig, update, frames=len(sampled), interval=50, blit=True)
    plt.close(fig)
    return HTML(anim.to_jshtml())

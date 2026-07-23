"""Pure NumPy + Matplotlib helpers for the glossy, liquid look.

They build the smooth curves, soft glows, gradient "pours" and gel capsules
that the two public plotting functions layer together.
"""

from __future__ import annotations

import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import Polygon
from matplotlib.transforms import offset_copy


def catmull_rom(px, py, samples: int = 24):
    """Smooth points into one flowing curve (pure-NumPy Catmull-Rom spline)."""
    px = np.asarray(px, float)
    py = np.asarray(py, float)
    cx = np.r_[px[0], px, px[-1]]
    cy = np.r_[py[0], py, py[-1]]
    t = np.linspace(0, 1, samples)
    ox, oy = [], []
    for i in range(1, len(cx) - 2):
        for src, out in ((cx, ox), (cy, oy)):
            p0, p1, p2, p3 = src[i - 1], src[i], src[i + 1], src[i + 2]
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return np.concatenate(ox), np.concatenate(oy)


def soft_glow(ax, x, y, color, width, zorder):
    """Stack translucent fat strokes under a line to fake a gooey halo."""
    for scale, alpha in ((2.8, 0.05), (2.1, 0.07), (1.5, 0.11)):
        ax.plot(x, y, color=color, lw=width * scale, alpha=alpha,
                solid_capstyle="round", solid_joinstyle="round", zorder=zorder)


def liquid_fill(ax, x, y, color, base, zorder):
    """Pour a vertical gradient under a curve that fades to transparent."""
    grad = np.empty((256, 1, 4))
    grad[:, :, :3] = to_rgba(color)[:3]
    grad[:, :, 3] = np.linspace(0.55, 0.0, 256)[:, None]
    im = ax.imshow(grad, extent=[x.min(), x.max(), base, y.max()],
                   origin="upper", aspect="auto", zorder=zorder)
    verts = np.vstack([np.column_stack([x, y]), [x[-1], base], [x[0], base]])
    im.set_clip_path(Polygon(verts, closed=True, transform=ax.transData))
    return im


def gooey_capsule(ax, value, center, color, thickness, zorder):
    """A horizontal bar drawn as a round-capped stroke -> a glossy gel capsule."""
    # soft halo beneath, so neighbouring capsules feel like they could merge
    for scale, alpha in ((1.55, 0.10), (1.28, 0.16)):
        ax.plot([0, value], [center, center], color=color, alpha=alpha,
                lw=thickness * scale, solid_capstyle="round", zorder=zorder - 1)
    ax.plot([0, value], [center, center], color=color, lw=thickness,
            solid_capstyle="round", zorder=zorder)  # capsule body
    # a glossy sheen streak riding along the top of the capsule
    sheen = offset_copy(ax.transData, ax.figure, y=thickness * 0.24, units="points")
    ax.plot([value * 0.07, value * 0.9], [center, center], color="white",
            alpha=0.35, lw=thickness * 0.26, solid_capstyle="round",
            transform=sheen, zorder=zorder + 1)

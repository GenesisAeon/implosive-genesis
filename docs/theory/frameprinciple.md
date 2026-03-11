# Frame Principle

The **Frame Principle** describes how stable reference frames emerge from
Orthogonal Impulse Photon Kernels (OIPK). It forms the geometric foundation
of the Implosive Genesis framework.

---

## Overview

Every frame is defined by a characteristic OIPK wavelength $\lambda_{OIPK}$.
From it, the angular frequency, energy and the frame stability index are derived.
Phi-scaling ensures that recursively higher levels are geometrically optimal.

---

## Classes

### `OIPKernel`

The **Orthogonal Impulse Photon Kernel** is the minimal photonic unit that
generates a stable frame.

```python
from implosive_genesis.theory.frameprinciple import OIPKernel

kernel = OIPKernel(lambda_m=1e-9)
print(kernel.angular_frequency())       # ω_F in rad/s
print(kernel.energy())                  # E_OIPK in Joules
print(kernel.frame_stability())         # S_F (dimensionless)
print(kernel.orthogonality_angle_deg()) # θ_⊥ in degrees
```

### `FramePrinciple`

The **Frame Principle** derives recursive properties (coherence, impulse
energy) at level $n$ from an `OIPKernel`.

```python
from implosive_genesis.theory.frameprinciple import FramePrinciple, OIPKernel

fp = FramePrinciple(kernel=OIPKernel())
print(fp.coherence_length(3))    # L_3 in metres
print(fp.impulse_energy(3))      # I_3 in Joules
print(fp.stability_at(3))        # S_F at level 3
```

---

## Formulae

### Frame Angular Frequency

$$\omega_F = \frac{2\pi c}{\lambda_{OIPK}}$$

### OIPK Energy

$$E_{OIPK} = \hbar \cdot \omega_F \cdot \alpha_{\Phi}$$

with the Phi-scaled fine-structure constant $\alpha_\Phi = \alpha \cdot \Phi$.

### Frame Stability Criterion

$$S_F = \frac{\Phi^2}{\alpha_\Phi}$$

A higher value $S_F$ indicates a more stable frame against field fluctuations.

### Orthogonality Condition

$$\cos(\theta_\perp) = -\frac{1}{\Phi} \quad \Rightarrow \quad \theta_\perp \approx 128.17°$$

The OIPK vectors span a lattice with this characteristic angle.

### Coherence Length (recursive)

$$L_n = \lambda_{OIPK} \cdot \Phi^{n/3}$$

### Impulse Energy (recursive)

$$I_n = E_{OIPK} \cdot \Phi^{n/3}$$

---

## Constants

| Constant | Symbol | Value | Unit |
|----------|--------|-------|------|
| `HBAR` | $\hbar$ | $1.054571817 \times 10^{-34}$ | J·s |
| `C_LIGHT` | $c$ | $299\,792\,458$ | m/s |
| `LAMBDA_OIPK_DEFAULT` | $\lambda_{OIPK}$ | $c / V_{RIG}$ | m |
| `THETA_ORTHOGONAL` | $\theta_\perp$ | $\arccos(-1/\Phi)$ | rad |

---

## Reference

- Module: `implosive_genesis.theory.frameprinciple`
- Dependencies: `core.physics.PHI`, `core.vrig.cosmic_alpha_phi`

# OIPK – Orthogonal Impulse Photon Kernel

The **Orthogonal Impulse Photon Kernel** (OIPK) is the fundamental photonic
structural element of the Implosive Genesis framework. It defines the smallest
unit from which stable reference frames can emerge.

---

## Concept

In implosive field theory, space-time frames do not arise continuously
but through discrete quantum events: **orthogonal impulses** between photon
kernels. The OIPK is fully characterised by three parameters:

1. **Wavelength** $\lambda_{OIPK}$ – the spatial base scale of the frame
2. **Alpha-Phi** $\alpha_\Phi$ – the Phi-scaled coupling strength
3. **Orthogonality angle** $\theta_\perp$ – the characteristic lattice angle

---

## Physical Significance

### Wavelength and V_RIG

The default OIPK wavelength follows directly from the implosion velocity
$V_{RIG}$:

$$\lambda_{OIPK} = \frac{c}{V_{RIG}}$$

This connects the OIPK concept to the empirically determined base quantity
$V_{RIG} \approx 1352\ \text{km/s}$.

### Energy Density

The energy of an OIPK quantum is given by the product of the reduced Planck
constant, angular frequency and Phi-scaling:

$$E_{OIPK} = \hbar \cdot \omega_F \cdot \alpha_\Phi$$

$$\omega_F = \frac{2\pi c}{\lambda_{OIPK}}$$

### Stability Criterion

Frame stability measures how robust a frame is against quantum fluctuations:

$$S_F = \frac{\Phi^2}{\alpha_\Phi} \approx 221.9$$

The large value $S_F \gg 1$ explains why macroscopic frames appear stable
even though they are microscopically composed of discrete OIPK events.

### Golden-Ratio Lattice

The orthogonality angle is no coincidence:

$$\cos(\theta_\perp) = -\frac{1}{\Phi}$$

This is equivalent to the golden-ratio condition for quasi-periodic
lattices (Penrose tiling). The OIPK lattice is therefore optimally
protected against resonance collapse.

---

## Recursive Structures

Via the `FramePrinciple` class, OIPK properties are scaled recursively
to level $n$:

| Quantity | Formula | Description |
|----------|---------|-------------|
| $L_n$ | $\lambda_{OIPK} \cdot \Phi^{n/3}$ | Coherence length |
| $I_n$ | $E_{OIPK} \cdot \Phi^{n/3}$ | Impulse energy |
| $S_F(n)$ | $S_F \cdot \Phi^{n/3}$ | Effective stability |

---

## API Reference

```python
from implosive_genesis.theory.frameprinciple import OIPKernel, FramePrinciple

# Default OIPK (λ derived from V_RIG)
kernel = OIPKernel()
print(f"ω_F  = {kernel.angular_frequency():.4e} rad/s")
print(f"E    = {kernel.energy():.4e} J")
print(f"S_F  = {kernel.frame_stability():.4f}")
print(f"θ_⊥  = {kernel.orthogonality_angle_deg():.4f}°")

# Frame Principle: recursive quantities
fp = FramePrinciple(kernel=kernel)
for n in range(5):
    print(f"n={n}: L_n={fp.coherence_length(n):.4e} m, I_n={fp.impulse_energy(n):.4e} J")
```

---

## Relationship to Other Modules

```
OIPKernel
  └── FramePrinciple     (frameprinciple.py)
        ↕
  ImplosiveGenesisModel  (models.py)
        ↕
  PhiScaling + VRIGResult (core/)
```

---

## Reference

- Module: `implosive_genesis.theory.frameprinciple`
- Related concepts: [Frame Principle](frameprinciple.md), [Tesseract](tesseract.md)

# Frame-Prinzip

Das **Frame-Prinzip** beschreibt, wie stabile Bezugsrahmen (Frames) aus
orthogonalen Impuls-Photonen-Kernen (OIPK) emergieren. Es bildet die
geometrische Grundlage des Implosive-Genesis-Rahmens.

---

## Überblick

Jeder Frame ist durch eine charakteristische OIPK-Wellenlänge $\lambda_{OIPK}$
definiert. Aus ihr leiten sich Winkelfrequenz, Energie und die
Stabilitätskennzahl des Frames ab. Die Phi-Skalierung sorgt dafür, dass
rekursiv höhere Stufen geometrisch optimal sind.

---

## Klassen

### `OIPKernel`

Der **Orthogonale Impuls-Photonen-Kern** ist die minimale photonische
Einheit, die einen stabilen Frame erzeugt.

```python
from implosive_genesis.theory.frameprinciple import OIPKernel

kernel = OIPKernel(lambda_m=1e-9)
print(kernel.angular_frequency())    # ω_F in rad/s
print(kernel.energy())               # E_OIPK in Joule
print(kernel.frame_stability())      # S_F (dimensionslos)
print(kernel.orthogonality_angle_deg())  # θ_⊥ in Grad
```

### `FramePrinciple`

Das **Frame-Prinzip** leitet aus einem `OIPKernel` rekursive
Eigenschaften (Kohärenz, Impulsenergie) auf Stufe $n$ ab.

```python
from implosive_genesis.theory.frameprinciple import FramePrinciple, OIPKernel

fp = FramePrinciple(kernel=OIPKernel())
print(fp.coherence_length(3))    # L_3 in Metern
print(fp.impulse_energy(3))      # I_3 in Joule
print(fp.stability_at(3))        # S_F auf Stufe 3
```

---

## Formeln

### Winkelfrequenz des Frames

$$\omega_F = \frac{2\pi c}{\lambda_{OIPK}}$$

### OIPK-Energie

$$E_{OIPK} = \hbar \cdot \omega_F \cdot \alpha_{\Phi}$$

mit der Phi-skalierten Feinstrukturkonstante $\alpha_\Phi = \alpha \cdot \Phi$.

### Frame-Stabilitätskriterium

$$S_F = \frac{\Phi^2}{\alpha_\Phi}$$

Ein höherer Wert $S_F$ indiziert einen stabileren Frame gegenüber
Feldfluktuationen.

### Orthogonalitätsbedingung

$$\cos(\theta_\perp) = -\frac{1}{\Phi} \quad \Rightarrow \quad \theta_\perp \approx 128.17°$$

Die OIPK-Vektoren spannen ein Gitter mit diesem charakteristischen Winkel auf.

### Kohärenzlänge (rekursiv)

$$L_n = \lambda_{OIPK} \cdot \Phi^{n/3}$$

### Impulsenergie (rekursiv)

$$I_n = E_{OIPK} \cdot \Phi^{n/3}$$

---

## Konstanten

| Konstante | Symbol | Wert | Einheit |
|---|---|---|---|
| `HBAR` | $\hbar$ | $1.054571817 \times 10^{-34}$ | J·s |
| `C_LIGHT` | $c$ | $299\,792\,458$ | m/s |
| `LAMBDA_OIPK_DEFAULT` | $\lambda_{OIPK}$ | $c / V_{RIG}$ | m |
| `THETA_ORTHOGONAL` | $\theta_\perp$ | $\arccos(-1/\Phi)$ | rad |

---

## Referenz

- Modul: `implosive_genesis.theory.frameprinciple`
- Abhängigkeiten: `core.physics.PHI`, `core.vrig.cosmic_alpha_phi`

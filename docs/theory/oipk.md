# OIPK – Orthogonaler Impuls-Photonen-Kern

Der **Orthogonale Impuls-Photonen-Kern** (OIPK, engl. *Orthogonal Impulse
Photon Kernel*) ist das fundamentale photonische Strukturelement des
Implosive-Genesis-Rahmens. Er definiert die kleinste Einheit, aus der
stabile Bezugsrahmen (Frames) entstehen können.

---

## Konzept

In der implosiven Feldtheorie entstehen Raum-Zeit-Frames nicht kontinuierlich,
sondern durch diskrete Quanten-Ereignisse: **Orthogonale Impulse** zwischen
Photonen-Kernen. Der OIPK ist durch drei Parameter vollständig charakterisiert:

1. **Wellenlänge** $\lambda_{OIPK}$ – die räumliche Grundskala des Frames
2. **Alpha-Phi** $\alpha_\Phi$ – die Phi-skalierte Kopplungsstärke
3. **Orthogonalitätswinkel** $\theta_\perp$ – der charakteristische Gitterwinkel

---

## Physikalische Bedeutung

### Wellenlänge und V_RIG

Die Standard-OIPK-Wellenlänge ergibt sich direkt aus der
Implosionsgeschwindigkeit $V_{RIG}$:

$$\lambda_{OIPK} = \frac{c}{V_{RIG}}$$

Dies verbindet das OIPK-Konzept mit der empirisch bestimmten
Grundgröße $V_{RIG} \approx 1352\ \text{km/s}$.

### Energie-Dichte

Die Energie eines OIPK-Quants ist durch das Produkt aus Planckscher
Wirkung, Winkelfrequenz und Phi-Skalierung gegeben:

$$E_{OIPK} = \hbar \cdot \omega_F \cdot \alpha_\Phi$$

$$\omega_F = \frac{2\pi c}{\lambda_{OIPK}}$$

### Stabilitätskriterium

Die Frame-Stabilität misst, wie robust ein Frame gegenüber
Quantenfluktuationen ist:

$$S_F = \frac{\Phi^2}{\alpha_\Phi} \approx 221.9$$

Der hohe Wert $S_F \gg 1$ erklärt, warum makroskopische Frames stabil
erscheinen, obwohl sie mikroskopisch aus diskreten OIPK-Ereignissen bestehen.

### Goldener-Schnitt-Gitter

Der Orthogonalitätswinkel ist kein Zufall:

$$\cos(\theta_\perp) = -\frac{1}{\Phi}$$

Dies ist äquivalent zur Goldenen-Schnitt-Bedingung für quasiperiodische
Gitter (Penrose-Tiling). Das OIPK-Gitter ist damit optimal gegen
Resonanzkollaps geschützt.

---

## Rekursive Strukturen

Über die `FramePrinciple`-Klasse werden OIPK-Eigenschaften rekursiv
auf Stufe $n$ skaliert:

| Größe | Formel | Beschreibung |
|---|---|---|
| $L_n$ | $\lambda_{OIPK} \cdot \Phi^{n/3}$ | Kohärenzlänge |
| $I_n$ | $E_{OIPK} \cdot \Phi^{n/3}$ | Impulsenergie |
| $S_F(n)$ | $S_F \cdot \Phi^{n/3}$ | Effektive Stabilität |

---

## API-Referenz

```python
from implosive_genesis.theory.frameprinciple import OIPKernel, FramePrinciple

# Standard-OIPK (λ von V_RIG abgeleitet)
kernel = OIPKernel()
print(f"ω_F  = {kernel.angular_frequency():.4e} rad/s")
print(f"E    = {kernel.energy():.4e} J")
print(f"S_F  = {kernel.frame_stability():.4f}")
print(f"θ_⊥  = {kernel.orthogonality_angle_deg():.4f}°")

# Frame-Prinzip: Rekursive Größen
fp = FramePrinciple(kernel=kernel)
for n in range(5):
    print(f"n={n}: L_n={fp.coherence_length(n):.4e} m, I_n={fp.impulse_energy(n):.4e} J")
```

---

## Zusammenhang mit anderen Modulen

```
OIPKernel
  └── FramePrinciple     (frameprinciple.py)
        ↕
  ImplosiveGenesisModel  (models.py)
        ↕
  PhiScaling + VRIGResult (core/)
```

---

## Referenz

- Modul: `implosive_genesis.theory.frameprinciple`
- Verwandte Konzepte: [Frame-Prinzip](frameprinciple.md), [Tesseract](tesseract.md)

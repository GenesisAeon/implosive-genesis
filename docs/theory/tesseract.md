# Tesseract, CREP and Entropic Price

The **Tesseract model** describes the 4-dimensional time structure of the
Implosive Genesis framework. Time slices $T_n$ scale with the golden ratio
$\Phi$. **CREP** (Collapse-Resonance-Entropy-Price) quantifies the
thermodynamic cost of the implosive collapse.

---

## Tesseract Time Slices

### Concept

Instead of continuous time, implosive field theory models time as a discrete
spectrum of **time slices** $T_n$. Each slice corresponds to a recursion
level $n$ and scales exponentially with $\Phi$:

$$T_n = t_0 \cdot \Phi^n$$

The **4D tesseract volume** is the fourth power of the time slice:

$$V_{4D}(n) = T_n^4 = t_0^4 \cdot \Phi^{4n}$$

### Resonance Frequency

At each level $n$ there is a characteristic resonance frequency that
establishes the dynamic coupling to $V_{RIG}$:

$$f_R(n) = \frac{V_{RIG}}{T_n} = \frac{V_{RIG}}{t_0 \cdot \Phi^n}$$

### API

```python
from implosive_genesis.theory.tesseract import Tesseract

ts = Tesseract(t_0=1.0)

# Individual time slice
print(ts.time_slice(3))          # T_3 = Φ³ ≈ 4.236

# 4D volume
print(ts.volume_4d(3))           # T_3^4 ≈ 80.9

# Series
slices = ts.slice_series(5)      # [T_0, T_1, ..., T_5]
volumes = ts.volume_series(5)    # [V_4D(0), ..., V_4D(5)]

# Resonance frequency (when t_0 is in seconds)
print(ts.resonance_frequency(3)) # f_R(3) in Hz
```

---

## CREP – Collapse-Resonance-Entropy-Price

### Concept

CREP quantifies the **thermodynamic cost** of the implosive collapse:
the energy converted to entropy during the transition to a higher recursion
level.

### CREP Value

$$CREP = \frac{S_{total} \cdot V_{RIG}}{\Phi \cdot c^2}$$

The factor $\Phi \cdot c^2$ normalises to the relativistic energy scale of
the golden ratio.

### Entropic Price

The entropic price at level $n$ and temperature $T$ is:

$$P_E(n, T) = n \cdot k_B \cdot T \cdot \ln(\Phi)$$

This is equivalent to $k_B \cdot T \cdot \ln(\Phi^n)$ – the classical
expression for the free energy of a transition between $\Phi^n$-fold states.

**Cosmic background:** At the CMB temperature $T_{CMB} = 2.725\ \text{K}$
for $n=3$:

$$P_E(3, 2.725\ \text{K}) \approx 1.54 \times 10^{-23}\ \text{J}$$

### API

```python
from implosive_genesis.theory.tesseract import CREP

crep = CREP()

# CREP value for normalised total entropy
print(crep.crep_value(s_total=1.0))

# Entropic price at CMB temperature
print(crep.entropy_price(n=3, temperature=2.725))

# Series over multiple levels
prices = crep.entropy_price_series(n_max=5, temperature=300.0)

# Cumulative CREP
total = crep.cumulative_crep([0.5, 1.0, 1.5, 2.0])
```

---

## Full Model

Tesseract and CREP are integrated into `ImplosiveGenesisModel`:

```python
from implosive_genesis.theory.models import ImplosiveGenesisModel

model = ImplosiveGenesisModel()
summary = model.full_summary(n=3, temperature=2.725)
print(summary)
```

Example output:

```
FullSummary(n=3)
  β_n            = 1.618034
  V_RIG          = 2187.3412 ± 12.0231 km/s
  α_Φ            = 0.01180450
  L_n            = 2.218e-04 m
  I_n            = 1.543e-27 J
  S_F(n)         = 358.9012
  T_n            = 4.236068
  V_4D(n)        = 3.210e+01
  P_E(n,T)       = 1.540e-23 J  (T=2.725 K)
  CREP(S=1)      = 7.598e-12
```

---

## Formula Overview

| Quantity | Formula | Module |
|----------|---------|--------|
| Time slice | $T_n = t_0 \cdot \Phi^n$ | `Tesseract` |
| 4D volume | $V_{4D}(n) = T_n^4$ | `Tesseract` |
| Resonance frequency | $f_R(n) = V_{RIG} / T_n$ | `Tesseract` |
| Entropic price | $P_E = n \cdot k_B \cdot T \cdot \ln\Phi$ | `CREP` |
| CREP value | $CREP = S \cdot V_{RIG} / (\Phi \cdot c^2)$ | `CREP` |

---

## Constants

| Constant | Symbol | Value | Unit |
|----------|--------|-------|------|
| `K_BOLTZMANN` | $k_B$ | $1.380649 \times 10^{-23}$ | J/K |
| `C_LIGHT_MS` | $c$ | $299\,792\,458$ | m/s |
| `T0_DEFAULT` | $t_0$ | $1.0$ | (normalised) |

---

## Reference

- Module: `implosive_genesis.theory.tesseract`
- Related concepts: [OIPK](oipk.md), [Frame Principle](frameprinciple.md)

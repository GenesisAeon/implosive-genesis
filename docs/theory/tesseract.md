# Tesseract, CREP und entropischer Preis

Das **Tesseract-Modell** beschreibt die 4-dimensionale Zeitstruktur des
Implosive-Genesis-Rahmens. Zeitscheiben $T_n$ skalieren mit dem Goldenen
Schnitt $\Phi$. **CREP** (Collapse-Resonance-Entropy-Price) quantifiziert
den thermodynamischen Preis des implosiven Kollapses.

---

## Tesseract-Zeitscheiben

### Konzept

Statt einer kontinuierlichen Zeit wird in der implosiven Feldtheorie die Zeit
als diskretes Spektrum von **Zeitscheiben** $T_n$ modelliert. Jede Scheibe
entspricht einer Rekursionsstufe $n$ und skaliert exponentiell mit $\Phi$:

$$T_n = t_0 \cdot \Phi^n$$

Das **4D-Tesseraktvolumen** ergibt sich aus der vierten Potenz der Zeitscheibe:

$$V_{4D}(n) = T_n^4 = t_0^4 \cdot \Phi^{4n}$$

### Resonanzfrequenz

Auf jeder Stufe $n$ gibt es eine charakteristische Resonanzfrequenz, die
die dynamische Kopplung an $V_{RIG}$ herstellt:

$$f_R(n) = \frac{V_{RIG}}{T_n} = \frac{V_{RIG}}{t_0 \cdot \Phi^n}$$

### API

```python
from implosive_genesis.theory.tesseract import Tesseract

ts = Tesseract(t_0=1.0)

# Einzelne Zeitscheibe
print(ts.time_slice(3))          # T_3 = Φ³ ≈ 4.236

# 4D-Volumen
print(ts.volume_4d(3))           # T_3^4 ≈ 80.9

# Serien
slices = ts.slice_series(5)      # [T_0, T_1, ..., T_5]
volumes = ts.volume_series(5)    # [V_4D(0), ..., V_4D(5)]

# Resonanzfrequenz (wenn t_0 in Sekunden)
print(ts.resonance_frequency(3)) # f_R(3) in Hz
```

---

## CREP – Collapse-Resonance-Entropy-Price

### Konzept

CREP quantifiziert den **thermodynamischen Preis** des implosiven Kollapses:
Die Energie, die beim Übergang auf eine höhere Rekursionsstufe in Entropie
umgewandelt wird.

### CREP-Wert

$$CREP = \frac{S_{total} \cdot V_{RIG}}{\Phi \cdot c^2}$$

Der Faktor $\Phi \cdot c^2$ normiert auf die relativistische Energieskala
des Goldenen Schnitts.

### Entropischer Preis

Der entropische Preis auf Stufe $n$ bei Temperatur $T$ ist:

$$P_E(n, T) = n \cdot k_B \cdot T \cdot \ln(\Phi)$$

Dies ist äquivalent zu $k_B \cdot T \cdot \ln(\Phi^n)$ – dem klassischen
Ausdruck für die freie Energie beim Übergang zwischen $\Phi^n$-fachen
Zuständen.

**Kosmischer Hintergrund:** Bei der CMB-Temperatur $T_{CMB} = 2.725\ \text{K}$
ergibt sich für $n=3$:

$$P_E(3, 2.725\ \text{K}) \approx 1.54 \times 10^{-23}\ \text{J}$$

### API

```python
from implosive_genesis.theory.tesseract import CREP

crep = CREP()

# CREP-Wert für normierte Gesamtentropie
print(crep.crep_value(s_total=1.0))

# Entropischer Preis bei CMB-Temperatur
print(crep.entropy_price(n=3, temperature=2.725))

# Serie über mehrere Stufen
prices = crep.entropy_price_series(n_max=5, temperature=300.0)

# Kumulativer CREP
total = crep.cumulative_crep([0.5, 1.0, 1.5, 2.0])
```

---

## Vollständiges Modell

Tesseract und CREP sind in `ImplosiveGenesisModel` integriert:

```python
from implosive_genesis.theory.models import ImplosiveGenesisModel

model = ImplosiveGenesisModel()
summary = model.full_summary(n=3, temperature=2.725)
print(summary)
```

Ausgabe (Beispiel):

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

## Formeln im Überblick

| Größe | Formel | Modul |
|---|---|---|
| Zeitscheibe | $T_n = t_0 \cdot \Phi^n$ | `Tesseract` |
| 4D-Volumen | $V_{4D}(n) = T_n^4$ | `Tesseract` |
| Resonanzfrequenz | $f_R(n) = V_{RIG} / T_n$ | `Tesseract` |
| Entropischer Preis | $P_E = n \cdot k_B \cdot T \cdot \ln\Phi$ | `CREP` |
| CREP-Wert | $CREP = S \cdot V_{RIG} / (\Phi \cdot c^2)$ | `CREP` |

---

## Konstanten

| Konstante | Symbol | Wert | Einheit |
|---|---|---|---|
| `K_BOLTZMANN` | $k_B$ | $1.380649 \times 10^{-23}$ | J/K |
| `C_LIGHT_MS` | $c$ | $299\,792\,458$ | m/s |
| `T0_DEFAULT` | $t_0$ | $1.0$ | (normiert) |

---

## Referenz

- Modul: `implosive_genesis.theory.tesseract`
- Verwandte Konzepte: [OIPK](oipk.md), [Frame-Prinzip](frameprinciple.md)

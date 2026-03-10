# Anesthesia-Tests – Frame-Buffer-Simulation bei Bewusstseinsverlust

Die **Anesthesia-Simulation** modelliert den schrittweisen Kollaps des
Frame-Buffers während eines Bewusstseinsverlusts (Anesthesia-Zustand) im
Implosive-Genesis-Rahmen. Sie quantifiziert, wann und wie das rekursive
Feld-Medium den Anesthesia-Schwellwert unterschreitet.

---

## Konzept

Im V_RIG-Framework wird Bewusstsein als kohärenter Frame-Buffer modelliert:
Ein Satz von $N$ Frame-Amplituden $F_i$, deren Mittelwert $\Phi_{buf}$ über
dem **Anesthesia-Schwellwert** $\Theta_{anes}$ liegen muss:

$$\Phi_{buf} = \frac{1}{N} \sum_{i=0}^{N-1} F_i$$

$$\text{bewusst} \iff \Phi_{buf} > \Theta_{anes}$$

---

## Physikalische Modellierung

### Medium-Abklingkurve

Das neuronale Medium wird als exponentiell abklingendes System modelliert:

$$M(t) = M_0 \cdot \exp\!\left(-\frac{t}{\tau_M}\right)$$

$$\Delta M(t) = M_0 \cdot \left(1 - \exp\!\left(-\frac{t}{\tau_M}\right)\right)$$

wobei $\tau_M$ die charakteristische Zeitkonstante des Mediums ist.

### Anesthesia-Schwellwert

Der Schwellwert ergibt sich direkt aus den OIPK-Parametern:

$$\Theta_{anes} = \frac{\alpha_\Phi}{\Phi^2} = \frac{1}{S_F} \approx 0.004504$$

Da $S_F = \Phi^2 / \alpha_\Phi \approx 221.9$ ist, liegt der Schwellwert sehr
niedrig – Bewusstsein ist robust gegenüber kleinen Fluktuationen.

### Frame-Kohärenzverlust

Der Gesamtkohärenzverlust nach Dauer $T$:

$$R_{loss} = 1 - \exp\!\left(-\frac{T}{\tau_M}\right)$$

### Wiederherstellungsrate

Die Erholung nach Anesthesia folgt einer Phi-verlängerten Zeitkonstante:

$$R_{rec} = \exp\!\left(-\frac{T}{\tau_M \cdot \Phi}\right)$$

Die Phi-Skalierung spiegelt das geometrisch optimierte Wiederherstellungsprofil
wider: Erholung ist langsamer als Verlust, was physiologisch beobachtete
Aufwachphasen erklärt.

---

## Simulationsablauf

```
t=0: Buffer leer → Φ_buf = 0 (Anesthesia)
t→: M(t) eingefügt → Buffer füllt sich
    Solange Φ_buf ≤ Θ_anes: Anesthesia-Ereignis aktiv
    Sobald Φ_buf > Θ_anes: Erholung, Ereignis geschlossen
```

---

## API-Referenz

```python
from implosive_genesis.medium.modulation import (
    MediumModulator,
    run_anesthesia_test,
    ANESTHESIA_THRESHOLD,
    FRAME_BUFFER_SIZE,
)

# Standard-Test (5 Minuten, τ_M = 120 s)
result = run_anesthesia_test(duration=300.0)
print(result.summary())

# Benutzerdefiniert
mod = MediumModulator(tau_m=60.0)
result = mod.run_anesthesia_simulation(duration=600.0, dt=0.5)
print(f"Ereignisse: {result.n_events()}")
print(f"Bewusst-Anteil: {result.consciousness_fraction():.4f}")

# Frame-Buffer direkt
from implosive_genesis.medium.modulation import FrameBuffer
buf = FrameBuffer(size=64)
buf.push(0.9)
print(buf.is_conscious())  # True
```

### CLI

```bash
# Standard-Test (300 s)
ig anesthesia-test

# Benutzerdefiniert
ig anesthesia-test --duration 600 --tau-m 60

# Mit Zeitreihe
ig anesthesia-test --duration 300 --timeline
```

---

## Parameter-Übersicht

| Parameter | Symbol | Standard | Beschreibung |
|---|---|---|---|
| Dauer | $T$ | 300 s | Testlänge |
| Zeitkonstante | $\tau_M$ | 120 s | Medium-Abkling-τ |
| Zeitschritt | $\Delta t$ | 1 s | Simulationsauflösung |
| Buffer-Größe | $N$ | 64 | Frame-Buffer-Kapazität |
| Schwellwert | $\Theta_{anes}$ | ≈ 0.004504 | Anesthesia-Grenze |

---

## Zusammenhang mit anderen Modulen

```
MediumModulator
  └── FrameBuffer             (Ringpuffer für Frame-Amplituden)
        ↕
  ANESTHESIA_THRESHOLD        (aus OIPK: α_Φ / Φ² = 1/S_F)
        ↕
  OIPKKernel                  (oipk/kernel.py)
        ↕
  FramePrinciple              (theory/frameprinciple.py)
```

---

## Referenz

- Modul: `implosive_genesis.medium.modulation`
- CLI: `ig anesthesia-test`
- Verwandte Konzepte: [OIPK](oipk.md), [Frame-Prinzip](frameprinciple.md)

"""Medium-Modulation und Anesthesia-Tests.

Modelliert die Wechselwirkung zwischen dem rekursiven Implosions-Feld und
physikalischen Medien. Zentral sind die **Frame-Buffer-Simulation** bei
Bewusstseinsverlust (Anesthesia) und die quantitative Medium-Modulation.

Kern-Gleichungen:

    M(t)   = M_0 · exp(−t / τ_M)              (Medium-Abklingkurve)

    ΔM(t)  = M_0 · (1 − exp(−t / τ_M))        (Modulationstiefe)

    Φ_buf  = Σ_{i=0}^{N-1} F_i / N            (Frame-Buffer-Mittelwert)

    Θ_anes = S_F · α_Φ / Φ²                   (Anesthesia-Schwellwert = 1/S_F)

    R_loss = 1 − exp(−duration / τ_M)         (Frame-Kohärenzverlust)

    R_rec  = exp(−duration / (τ_M · Φ))       (Wiederherstellungsrate nach Anesthesia)

„Bewusstsein kollabiert, wenn der Frame-Buffer unter den Anesthesia-Schwellwert fällt."

Verwendung::

    from implosive_genesis.medium.modulation import MediumModulator, run_anesthesia_test

    mod = MediumModulator(tau_m=60.0)
    state = mod.modulate(t=30.0)
    print(state)

    result = run_anesthesia_test(duration=300.0)
    print(result.summary())
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import NamedTuple

__all__ = [
    "ANESTHESIA_THRESHOLD",
    "FRAME_BUFFER_SIZE",
    "MediumState",
    "FrameBuffer",
    "AnesthesiaEvent",
    "AnesthesiaTestResult",
    "MediumModulator",
    "run_anesthesia_test",
]

# ---------------------------------------------------------------------------
# Konstanten
# ---------------------------------------------------------------------------

_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
_ALPHA_EM: float = 7.2973525693e-3
_ALPHA_PHI: float = _ALPHA_EM * _PHI

ANESTHESIA_THRESHOLD: float = _ALPHA_PHI / _PHI**2
"""Anesthesia-Schwellwert Θ_anes = α_Φ / Φ² = 1/S_F ≈ 0.004504.

Wenn der normalisierte Frame-Buffer-Wert unter diesen Schwellwert fällt,
wird Bewusstsein als kollabiert (Anesthesia-Zustand) klassifiziert.
"""

FRAME_BUFFER_SIZE: int = 64
"""Standard-Größe des Frame-Buffers (Anzahl gespeicherter Frames)."""

_TAU_M_DEFAULT: float = 120.0
"""Standard-Medium-Zeitkonstante τ_M = 120 s."""


# ---------------------------------------------------------------------------
# Datenklassen
# ---------------------------------------------------------------------------


class MediumState(NamedTuple):
    """Zustand des Mediums zum Zeitpunkt t.

    Attributes:
        t:            Zeit [s]
        m_t:          Medium-Amplitude M(t) = M_0·exp(−t/τ_M)
        delta_m:      Modulationstiefe ΔM(t) = M_0·(1−exp(−t/τ_M))
        normalized:   Normalisierter Wert M(t) / M_0 ∈ [0, 1]
        conscious:    True wenn normalized > ANESTHESIA_THRESHOLD
    """

    t: float
    m_t: float
    delta_m: float
    normalized: float
    conscious: bool

    def __str__(self) -> str:
        status = "CONSCIOUS" if self.conscious else "ANESTHESIA"
        return (
            f"MediumState(t={self.t:.1f}s, M={self.m_t:.4f}, "
            f"ΔM={self.delta_m:.4f}, norm={self.normalized:.4f}, [{status}])"
        )


@dataclass
class FrameBuffer:
    """Ringpuffer für Frame-Amplituden-Werte.

    Simuliert den neuronalen Frame-Buffer, der Bewusstseinszustände
    als gewichteten Mittelwert der letzten N Frames hält.

    Attributes:
        size:    Maximale Puffergröße (Standard: FRAME_BUFFER_SIZE).
        _data:   Interne Datenliste.
    """

    size: int = FRAME_BUFFER_SIZE
    _data: list[float] = field(default_factory=list, repr=False)

    def push(self, value: float) -> None:
        """Fügt einen neuen Frame-Wert ein.

        Args:
            value: Frame-Amplitude (normalisiert, ∈ [0, 1] empfohlen).
        """
        self._data.append(value)
        if len(self._data) > self.size:
            self._data.pop(0)

    def mean(self) -> float:
        """Mittelwert aller gepufferten Frame-Werte Φ_buf = Σ F_i / N.

        Returns:
            0.0 wenn der Puffer leer ist, sonst Φ_buf.
        """
        if not self._data:
            return 0.0
        return sum(self._data) / len(self._data)

    def is_conscious(self, threshold: float = ANESTHESIA_THRESHOLD) -> bool:
        """Prüft ob der Buffer über dem Anesthesia-Schwellwert liegt.

        Args:
            threshold: Schwellwert (Standard: ANESTHESIA_THRESHOLD).

        Returns:
            True wenn mean() > threshold.
        """
        return self.mean() > threshold

    def fill_level(self) -> float:
        """Füllstand des Buffers als Anteil [0, 1].

        Returns:
            len(data) / size.
        """
        return len(self._data) / self.size

    def reset(self) -> None:
        """Leert den Frame-Buffer."""
        self._data.clear()

    def __len__(self) -> int:
        return len(self._data)


@dataclass(frozen=True)
class AnesthesiaEvent:
    """Einzelnes Anesthesia-Ereignis innerhalb eines Tests.

    Attributes:
        t_start:     Zeitpunkt des Bewusstseinsverlusts [s]
        t_end:       Zeitpunkt der Wiederherstellung [s] (None = noch aktiv)
        depth:       Anesthesia-Tiefe (1 − normalized_at_nadir)
        recovery:    Wiederherstellungsrate R_rec = exp(−duration/(τ_M·Φ))
    """

    t_start: float
    t_end: float | None
    depth: float
    recovery: float

    @property
    def duration(self) -> float | None:
        """Dauer des Ereignisses [s] oder None wenn noch aktiv."""
        if self.t_end is None:
            return None
        return self.t_end - self.t_start


@dataclass
class AnesthesiaTestResult:
    """Ergebnis eines vollständigen Anesthesia-Tests.

    Attributes:
        duration:         Testdauer [s]
        tau_m:            Medium-Zeitkonstante [s]
        dt:               Zeitschritt [s]
        events:           Liste erkannter Anesthesia-Ereignisse
        frame_means:      Zeitreihe der Buffer-Mittelwerte
        times:            Zeitachse [s]
        loss_rate:        Gesamter Kohärenzverlust R_loss = 1−exp(−T/τ_M)
        recovery_rate:    Gesamte Wiederherstellungsrate R_rec
    """

    duration: float
    tau_m: float
    dt: float
    events: list[AnesthesiaEvent]
    frame_means: list[float]
    times: list[float]
    loss_rate: float
    recovery_rate: float

    def n_events(self) -> int:
        """Anzahl erkannter Anesthesia-Ereignisse."""
        return len(self.events)

    def total_anesthesia_time(self) -> float:
        """Gesamte Anesthesia-Dauer über alle Ereignisse [s]."""
        total = 0.0
        for ev in self.events:
            if ev.duration is not None:
                total += ev.duration
        return total

    def consciousness_fraction(self) -> float:
        """Anteil der Testzeit im bewussten Zustand [0, 1]."""
        if self.duration <= 0:
            return 1.0
        return 1.0 - self.total_anesthesia_time() / self.duration

    def summary(self) -> str:
        """Gibt eine menschenlesbare Zusammenfassung zurück."""
        lines = [
            "AnesthesiaTestResult",
            f"  Dauer          : {self.duration:.1f} s",
            f"  τ_M            : {self.tau_m:.1f} s",
            f"  Ereignisse     : {self.n_events()}",
            f"  Anesthesia-Zeit: {self.total_anesthesia_time():.1f} s "
            f"({100 * (1 - self.consciousness_fraction()):.1f}%)",
            f"  Bewusst-Anteil : {self.consciousness_fraction():.4f}",
            f"  R_loss         : {self.loss_rate:.4f}",
            f"  R_rec          : {self.recovery_rate:.4f}",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Hauptklasse
# ---------------------------------------------------------------------------


@dataclass
class MediumModulator:
    """Medium-Modulator: simuliert Feld-Medium-Wechselwirkung.

    Das Medium wird als exponentiell abklingendes System mit Zeitkonstante τ_M
    modelliert. Die Phi-Skalierung der Wiederherstellung stellt sicher, dass
    die Erholung geometrisch optimal (minimal destruktiv) verläuft.

    Attributes:
        m0:    Initial-Amplitude M_0 (normiert, Standard: 1.0).
        tau_m: Medium-Zeitkonstante τ_M [s] (Standard: 120 s).
    """

    m0: float = 1.0
    tau_m: float = _TAU_M_DEFAULT

    def modulate(self, t: float) -> MediumState:
        """Berechnet den Medium-Zustand zum Zeitpunkt t.

        Formeln:
            M(t) = M_0 · exp(−t/τ_M)
            ΔM(t) = M_0 · (1 − exp(−t/τ_M))

        Args:
            t: Zeit [s] (≥ 0).

        Returns:
            MediumState zum Zeitpunkt t.
        """
        if t < 0:
            t = 0.0
        exp_factor = math.exp(-t / self.tau_m) if self.tau_m > 0 else (1.0 if t == 0.0 else 0.0)
        m_t = self.m0 * exp_factor
        delta_m = self.m0 * (1.0 - exp_factor)
        normalized = m_t / self.m0 if self.m0 != 0 else 0.0
        conscious = normalized > ANESTHESIA_THRESHOLD
        return MediumState(
            t=t, m_t=m_t, delta_m=delta_m, normalized=normalized, conscious=conscious
        )

    def modulation_series(self, t_max: float, n_steps: int = 100) -> list[MediumState]:
        """Zeitreihe des Medium-Zustands von t=0 bis t=t_max.

        Args:
            t_max:   Endzeit [s].
            n_steps: Anzahl der Zeitschritte.

        Returns:
            Liste von MediumState-Objekten.
        """
        if n_steps < 1:
            n_steps = 1
        dt = t_max / n_steps
        return [self.modulate(i * dt) for i in range(n_steps + 1)]

    def frame_loss(self, duration: float) -> float:
        """Frame-Kohärenzverlust: R_loss = 1 − exp(−duration/τ_M).

        Args:
            duration: Dauer [s].

        Returns:
            Kohärenzverlust ∈ [0, 1].
        """
        if self.tau_m <= 0:
            return 1.0
        return 1.0 - math.exp(-duration / self.tau_m)

    def recovery_rate(self, duration: float) -> float:
        """Wiederherstellungsrate nach Anesthesia: R_rec = exp(−duration/(τ_M·Φ)).

        Die Phi-Verlängerung der Zeitkonstante bei der Erholung reflektiert
        das geometrisch optimierte Wiederherstellungsprofil.

        Args:
            duration: Dauer der Anesthesia [s].

        Returns:
            Wiederherstellungsrate ∈ (0, 1].
        """
        if self.tau_m <= 0:
            return 0.0
        return math.exp(-duration / (self.tau_m * _PHI))

    def run_anesthesia_simulation(
        self,
        duration: float,
        dt: float = 1.0,
        threshold: float = ANESTHESIA_THRESHOLD,
    ) -> AnesthesiaTestResult:
        """Führt eine vollständige Anesthesia-Frame-Buffer-Simulation durch.

        Simuliert den schrittweisen Bewusstseinsverlust durch:
        1. Berechnung des Medium-Zustands an jedem Zeitschritt
        2. Einfügen des normalisierten Werts in den Frame-Buffer
        3. Erkennung von Anesthesia-Ereignissen (Buffer < threshold)
        4. Aufzeichnung von Wiederherstellungen

        Args:
            duration:  Testdauer [s].
            dt:        Zeitschritt [s] (Standard: 1.0 s).
            threshold: Anesthesia-Schwellwert (Standard: ANESTHESIA_THRESHOLD).

        Returns:
            AnesthesiaTestResult mit vollständiger Zeitreihe.
        """
        buffer = FrameBuffer(size=FRAME_BUFFER_SIZE)
        times: list[float] = []
        frame_means: list[float] = []
        events: list[AnesthesiaEvent] = []

        in_anesthesia = False
        event_start = 0.0
        event_nadir = 1.0

        n_steps = max(1, int(duration / dt))
        for i in range(n_steps + 1):
            t = i * dt
            state = self.modulate(t)
            buffer.push(state.normalized)

            phi_buf = buffer.mean()
            times.append(t)
            frame_means.append(phi_buf)

            conscious = phi_buf > threshold
            if not conscious and not in_anesthesia:
                in_anesthesia = True
                event_start = t
                event_nadir = phi_buf
            elif not conscious and in_anesthesia:
                event_nadir = min(event_nadir, phi_buf)
            elif conscious and in_anesthesia:
                in_anesthesia = False
                depth = 1.0 - event_nadir
                rec = self.recovery_rate(t - event_start)
                events.append(
                    AnesthesiaEvent(
                        t_start=event_start,
                        t_end=t,
                        depth=depth,
                        recovery=rec,
                    )
                )

        # Offenes Ereignis am Ende schließen
        if in_anesthesia:
            depth = 1.0 - event_nadir
            rec = self.recovery_rate(duration - event_start)
            events.append(
                AnesthesiaEvent(
                    t_start=event_start,
                    t_end=duration,
                    depth=depth,
                    recovery=rec,
                )
            )

        return AnesthesiaTestResult(
            duration=duration,
            tau_m=self.tau_m,
            dt=dt,
            events=events,
            frame_means=frame_means,
            times=times,
            loss_rate=self.frame_loss(duration),
            recovery_rate=self.recovery_rate(duration),
        )


# ---------------------------------------------------------------------------
# Hilfsfunktion
# ---------------------------------------------------------------------------


def run_anesthesia_test(
    duration: float = 300.0,
    tau_m: float = _TAU_M_DEFAULT,
    dt: float = 1.0,
) -> AnesthesiaTestResult:
    """Führt einen Anesthesia-Test mit Standardparametern durch.

    Args:
        duration: Testdauer [s] (Standard: 300 s = 5 Minuten).
        tau_m:    Medium-Zeitkonstante [s] (Standard: 120 s).
        dt:       Zeitschritt [s] (Standard: 1 s).

    Returns:
        AnesthesiaTestResult.
    """
    mod = MediumModulator(tau_m=tau_m)
    return mod.run_anesthesia_simulation(duration=duration, dt=dt)

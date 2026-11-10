---
title: "PDN impedances should be simple"
date: 2026-05-14
lastmod: 2026-05-14
url: /drafts/pdn-impedances-should-be-simple.html
---

Calculation of the maximum impedance a PDN should provide is often a complex task, partly because frequency domain representations are used instead of time domain representations which here make calculations much easier.

In the time domain, the constraint reduces to a simple budget: the resistive drop plus the inductive drop of the transient current must stay below the allowable voltage variation, <asciimath>R \cdot I_text(pk) + L \cdot I_text(pk)/t_r \leq \Delta V_text(max)</asciimath>, from which maximum R and L follow directly.

## Comments on PDN maximum impedance calculation method

### Typical approach

The typical approach, well explained by Ott, is as follows:

1/ Approximate the current drawn by the chip by a series of trapezoidal pulses:

![](pdn-impedances-should-be-simple/edges.png)

From Ott, p. 428.

With I the *peak* current, the charge contained in one triangular pulse is <asciimath>Q = I \cdot t_r</asciimath>, hence the average current over a period T is <asciimath>I_(avg) = I \cdot t_r / T</asciimath>. Reversing this relation, <asciimath>I = I_(avg) \cdot T / t_r</asciimath>, gives the peak current from the average consumption — a relation reused below when estimating the current drawn by the chip from its total consumption.

2/ Express the Fourier transform of this current as such (Ott, p. 429):

<latexmath>
I_n = \frac{2 \cdot I \cdot t_r}{T} \cdot \left[ \frac{\sin(\frac{n \cdot \pi \cdot t_r}{T})}{\frac{n \cdot \pi \cdot t_r}{T}} \right]^2
</latexmath>

Use the following envelope as a simpler upper bound (Ott, p. 430):

![](pdn-impedances-should-be-simple/edges-fourier.png)

Calculate the low frequency part as such:

<latexmath>
Z_t = \frac{k \cdot \Delta V}{\Delta I}
</latexmath>

where <asciimath>\Delta V</asciimath> "is the allowable power supply transient voltage variation", <asciimath>\Delta I</asciimath> "is the amplitude of the transient power supply current drawn by the IC", and k a correction factor taking into account the part of the current "contained in the frequencies below the <asciimath>1/(π \\cdot t_r)</asciimath> frequency" (Ott, pp. 446-447).

![](pdn-impedances-should-be-simple/zt-curve.png)

3/ Calculate the maximum allowed impedance from this curve as (Ott, eqn. 11-7, p. 445).

The second part of this curve, corresponding to the inductive part, starts from <asciimath>Z_t</asciimath> at <asciimath>1/(π \\cdot t_r)</asciimath>, which is equivalent to:

<latexmath>
\begin{gathered}
2 \cdot \pi \cdot f \cdot L = Z_t \quad \text{for} \quad f = \frac{1}{\pi \cdot t_r}  \\
\frac{2 \cdot \pi \cdot L}{\pi \cdot t_r} = Z_t  \\
L_\text{max} = \frac{Z_t \cdot t_r}{2}
\end{gathered}
</latexmath>

Rather complex.

### Alternative time-domain approach

We propose here an alternative approach:

1/ Use the same trapezoidal current approximation as above.

2/ Allocate a maximum R and L from the curves such that <asciimath>R \cdot I_(pk) + L \cdot I_(pk)/t_r <= Delta V_text(max)</asciimath>. Note the solution is not necessarily unique. A starting point could be to allocate the same delta to both terms.

3/ (Optional) Calculate a maximum allowed impedance vs. frequency from R and L.

Note that, here, R and L can be seen not only as physical elements, but also as convenient calculation tools, for example when modelling something whose behavior is more complex than a pure R and L.

## Current drawn by capacitive loading

The repetition rate of the charge of the capacitive loads might seem an important point. However, the R+L model shows that the repetition rate has almost no importance and that the dominant parameters are the rise and fall times.

Anyway, while the current needed to charge the *internal* capacitors of a typical chip is drawn at fCLK, the current for the output capacitors *together* is drawn at fCLK/2 since on average half of these charge at each time, and that for a *single* output capacitor at fCLK/4, following this typical scenario:

* CLK ↑, output ↑, capacitor charges from Vcc

* CLK ↓, output =

* CLK ↑, output ↓, capacitor discharges to GND

* CLK ↓, output =

Worst case peak current can be calculated from charge conservation from the curve: <asciimath>I_text(pk) = C_l \cdot V_text(cc) / t_r</asciimath>. This being said, decoupling of simple chips is straightforward, and complex chips are likely to draw more current from their internals than from their outputs.

## Current drawn by chip consumption (cross-conduction of the gates)

This one is trickier. Most circuits are synchronous nowadays so mainly this case will be studied. Circuits having multiple clock domains can also be studied with this method. It will also be assumed that the current spikes will be dominant on rising edges rather than on falling edges, which is a reasonable worst case.

The calculation is best done from the total consumption, which is easier to measure and define, rather than from other parameters like Cpd. From the same charge conservation considerations as above, calculations lead to <asciimath>I_text(TOTAL) = I_text(pk) \cdot t_r \cdot f_text(CLK)</asciimath>, and thus <asciimath>I_text(pk) = I_text(TOTAL) / (f_text(CLK) \cdot t_r)</asciimath>.

## What to do if tr is missing?

When the datasheet gives no rise/fall time — as for instance in the MSP430 datasheet — the current-based budget above cannot be computed; the best available fallback is then a geometry-consistent decoupling rule: one capacitor per Vcc pin, size consistent with the sizes of the pins. Components are designed to work, and their internal rise and fall times will be consistent with the inductance of the pins and so on. Sure this is not perfect, but this is the best you can do in this case.

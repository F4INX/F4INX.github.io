---
title: "On group delay of antennas."
date: 2022-07-10
lastmod: 2022-07-10 16-54
categories: [Antennas, Group Delay]
url: /posts/on-antennas-group-delay.html
---


<p class="note">Many thanks, in the order of appearance in the LinkedIn discussion, to Dr. Pierre-Antoine Garcia, Theunis Beukman, Benoit Derat, Hüseyin Yiğit, Andreas Barchanski for the insightful LinkedIn discussion which led to this post.</p>

Recently on LinkedIn, a fellow colleague asked whether the group delay of an antenna could be calculated by the simulated complex gain. Sure it can, but with the right precautions.

## What is tried to be measured ?

A reasonable asumption when dealing with an antenna is that there will be an other antenna facing it. The transmission coefficient S21 between the two antennas can be written as follows, using the Friis transmission equation [https://en.wikipedia.org/wiki/Friis_transmission_equation](https://en.wikipedia.org/wiki/Friis_transmission_equation) :

<asciimath>
S_{21} = ubrace{G_a \cdot G_b}_{"Gains."} \cdot \lambda / {4 \cdot \pi} \cdot ubrace{1 / d}_{:("Free space"),("attenuation."):} \cdot ubrace{e^{-j \cdot 2 \cdot \pi \cdot d / \lambda}}_{:("Distance"),("phase shift."):}
</asciimath>

Note this form is slightly different from the usual one, since the amplitude is taken instead of the power. Rearranging in function of the frequency gives:

<asciimath>
S_{21} = G_a \cdot G_b \cdot {c} / {4 \cdot \pi \cdot f} \cdot 1 / d \cdot e^{-j \cdot 2 \cdot \pi \cdot d / c \cdot f}
</asciimath>

For the group delay, only phase matters, hence:

<asciimath>
"phase"(S_{21}) = "phase"(G_a) + "phase"(G_b) - 2 \cdot \pi \cdot d / c \cdot f
</asciimath>

Group delay is calculated using the derivative of the phase by <asciimath> \tau_g = - 1 / (2 \cdot \pi) \cdot (d)/(df) "phase"(S_{21}) </asciimath>, which leads to ask which terms are constant with frequency and which terms changes.

## Phase center of antennas

A non-trivial varying term is the distance between the antennas. Antennas are often big enough compared to the wavelength to forbid the use of a random point to calculate the phase shift from the distance. The right point to take is the phase center, which is the center of the spherical wavefronts at infinity. The phase center depends on the direction, but most importantly for group delay calculations, it depends on frequency[^1].

The group delay formula can be rewritten taking this into account:

<asciimath>
"phase"(S_{21}) = "phase"(G_a) + "phase"(G_b) - 2 \cdot \pi \cdot (d_"geom" - \Delta_1 - \Delta_2) / c \cdot f
</asciimath>

were <asciimath>d_"geom"</asciimath> is the geometrical distance between the antennas and <asciimath>\Delta_1</asciimath> and <asciimath>\Delta_2</asciimath> are the positions of the phase centers relative to the geometrical reference point. This reference can be any point. The sign of <asciimath>\Delta_1</asciimath> and <asciimath>\Delta_2</asciimath> is taken positive when the phase center gets closer to the other antenna.

Since the interest in only in the first antenna and not in the second, this formula can be normalized by taken all parameters of the second antenna to reference values: unit gain, phase center coinciding with geometrical center, and zero distance. The meaning of the last hypothesis is important to emphasize: the physical distance cannot be zero, it's just a way to separate the effects depending of the antenna from the rest. So:

<asciimath>
"phase"(S_{21}) = "phase"(G_a) + 2 \cdot \pi \cdot \Delta_1 / c \cdot f
</asciimath>

Knowing which terms are constant and which are not, the derivative can be calculated:

<asciimath>
\tau_g = - 1 / (2 \cdot \pi) \cdot (d)/(df) [ "phase"(G_a) + 2 \cdot \pi \cdot \Delta_1 / c \cdot f ]
</asciimath>

This last equation shows that not only the phase of the gain must be taken into account, but also the move of the phase center.

## Conclusion

The group delay of an antenna can be calculated using simulation results, but the total phase shift change must be taken into account, including the move of the phase center.

[^1]: Even antennas with a symmetry plane like the ideal dipole can have a varying phase center for directions outside of their symmetry plane.

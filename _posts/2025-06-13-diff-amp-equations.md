---
layout: post
title: Equations for terminating a differential amplifier in single-ended input
permalink: /posts/diff-amp-equations.html
last_modified_at: 2025-06-13
---

## Introduction

A few years ago, I had to terminate a differential amplifier in single-ended input. Analog Devices AN-0990[^1] gives equations for that. Unfortunately, there are an inaccuracy in these equations. According to this page, the input impedance for balanced differential input signals is given by <asciimath>R_"IN, dm"=2\cdotR_G</asciimath> and for a single-ended input by <asciimath>R_"IN, cm"=R_G/(1-R_F/(2\cdot(R_G+R_F))).

However, in this use case, the last equation is **uncorrect**. It would have been correct if the -D<sub>IN</sub> input were connected directly to ground. However, this is not the case, and instead this input is connected to ground through a resistor of value <asciimath>R_S////R_T</asciimath> to ensure symmetry.

## Schematic

The schematic is shown below. Note the strange alignment of R<sub>sp</sub> and R<sub>sn</sub>. R<sub>sp</sub> is part of the source while R<sub>sn</sub> is part of the board. Note that in an actual implementation, R<sub>sn</sub> and R<sub>tn</sub> are likely to be merged. Details of the LTSpice simulation will be described at the end.

<img src="{{ '/posts/diff-amp-equations/diff-amp-SE-schematic.svg' | relative_url }}"/>

## Calculation philosophy: solving vs. enforcing

There are two methods to calculate the values of the components in an electrical circuit:

* Determine all the equations of all the wanted parameters (gain, impedance) in function of the components values, and invert all the equation. This is the solving approach.

* Enforce at as soon as possible in the calculation process the wanted parameters by setting early some components values. This is the enforcing approach.

Calculations get much easier with the enforcing approach, in a similar approach than proposed by Middlebrook and its successors, notably Vorperian and Basso.

This case is a great illustration of this principle. I first tried the first approach, without success, thereafter the second approach, and got manageable equations.

## Calculations details

### Calculation of R<sub>G</sub>

It is assumed that R<sub>F</sub> is fixed. For current feedback amplifiers, common for high speed, R<sub>F</sub> contributes to the amplifier gain and have a value recommended by the datasheet which should be respected in most cases. For voltage feedback amplifiers having some speed, R<sub>F</sub> have to be low enough to avoid issues with the various parasitic capacitances which also leads to a recommended value.

#### Normalisation

After a long time working with these equations, I realized it was easier to use normalized values of the resistors, and the easiest value for normalization is the feedback resistor R<sub>F</sub>, as such:

<latexmath class="framed">
\begin{split}
R_F^{'} &= \frac{R_F}{R_F} = 1 \\
R_G^{'} &= \frac{R_G}{R_F} \\
R_S^{'} &= \frac{R_S}{R_F}
\end{split}
</latexmath>

#### Equation of &&V_X^+&&

<latexmath class="framed">
V_X^{+} = V_S \cdot \frac{Z_\text{IN}}{R_S + Z_\text{IN}} \quad \text{with} \quad K = \frac{Z_\text{IN}}{R_S + Z_\text{IN}}
</latexmath>

#### Equation of &&V_X^-&&

Equations of &&V_X^+&& and &&V_X^-&& can be determined from Millman theorem[^2]:

<latexmath>
V_X^{+} = \frac{\frac{V_S}{R_S}+\frac{0}{R_T}-\frac{\frac{G}{2}\cdot{V_S}}{R_F+R_G}}{\frac{1}{R_S}+\frac{1}{R_T}-\frac{1}{R_F+R_G}} = V_S \cdot \frac{\frac{1}{R_S^{'}}+\frac{0}{R_T^{'}}-\frac{\frac{G}{2}}{1+R_G^{'}}}{\frac{1}{R_S^{'}}+\frac{1}{R_T^{'}}-\frac{1}{1+R_G^{'}}}
</latexmath>

<latexmath>
V_X^{-} = \frac{\frac{0}{R_S}+\frac{0}{R_T}+\frac{\frac{G}{2}\cdot{V_S}}{R_F+R_G}}{\frac{1}{R_S}+\frac{1}{R_T}-\frac{1}{R_F+R_G}} = V_S \cdot \frac{\frac{1}{R_S^{'}}+\frac{0}{R_T^{'}}+\frac{\frac{G}{2}}{1+R_G^{'}}}{\frac{1}{R_S^{'}}+\frac{1}{R_T^{'}}-\frac{1}{1+R_G^{'}}}
</latexmath>

And their ratio can be calculated as such:

<latexmath>
\frac{V_X^{+}}{V_X^{-}} = \frac{\frac{1}{R_S^{'}}-\frac{\frac{G}{2}}{1+R_G^{'}}}{\frac{1}{R_S^{'}}+\frac{\frac{G}{2}}{1+R_G^{'}}} = \frac{\frac{1}{R_S^{'}}}{\frac{1}{R_S^{'}}+\frac{\frac{G}{2}}{1+R_G^{'}}} - 1 = \frac{2\cdot\left(1+R_G^{'}\right)}{G\cdot{R_S^{'}}}-1
</latexmath>

Using the previous expression of &&V_X^+&&, the actual value of &&V_X^-&& can be calculated as such:

<latexmath class="framed">
V_X^{-} = \frac{V_X^{+}}{\frac{2\cdot\left(1+R_G^{'}\right)}{G\cdot{R_S^{'}}}-1} = V_S \cdot K \cdot \frac{1}{\frac{2\cdot\left(1+R_G^{'}\right)}{G\cdot{R_S^{'}}}-1}
</latexmath>

#### Balance of &&V_\"IN\"^+&& and &&V_\"IN\"^-&&

In the normal operation of an operational amplifier, &&V_\"IN\"^+ = V_\"IN\"^-&&. Both quantities can be calculated as such, using again Millman theorem[^2]:

<latexmath>
\begin{split}
V_\text{IN}^{+} &= \frac{\frac{V_X^{+}}{R_G}-\frac{\frac{G}{2}\cdot V_S}{R_F}}{\frac{1}{R_G}+\frac{1}{R_F}} = \frac{\frac{V_X^{+}}{R_G^{'}}-\frac{G}{2}\cdot V_S}{\frac{1}{R_G^{'}}+1} \\
V_\text{IN}^{-} &= \frac{\frac{V_X^{-}}{R_G}+\frac{\frac{G}{2}\cdot V_S}{R_F}}{\frac{1}{R_G}+\frac{1}{R_F}} = \frac{\frac{V_X^{-}}{R_G^{'}}+\frac{G}{2}\cdot V_S}{\frac{1}{R_G^{'}}+1}
\end{split}
</latexmath>

And the condition &&V_\"IN\"^+ = V_\"IN\"^-&& can be written as such:

<latexmath>
\begin{split}
\frac{V_X^{+}}{R_G^{'}}-\frac{G}{2}\cdot V_S &= \frac{V_X^{-}}{R_G^{'}}+\frac{G}{2}\cdot V_S \\
\frac{V_X^{+}}{R_G^{'}}-G\cdot V_S &= \frac{V_X^{-}}{R_G^{'}}
\end{split}
</latexmath>

In which the values of &&V_X^+&& and &&V_X^-&& can be substituted:

<latexmath>
\begin{split}
V_S \cdot K \cdot \frac{1}{R_G^{'}}-G\cdot V_S &=  V_S \cdot K \cdot \frac{1}{\frac{2\cdot\left(1+R_G^{'}\right)}{G\cdot{R_S^{'}}}-1} \cdot \frac{1}{R_G^{'}} \\
K - G \cdot R_G^{'} &=  K \cdot \frac{1}{\frac{2\cdot\left(1+R_G^{'}\right)}{G\cdot{R_S^{'}}}-1}
\end{split}
</latexmath>

<latexmath>
\left[ K - G \cdot R_G^{'} \right] \cdot \left[ \frac{2\cdot\left(1+R_G^{'}\right)}{G\cdot{R_S^{'}}}-1 \right] = K
</latexmath>

Which can be put in a second order equation in the following way (note the early optimizations of the equations):

<latexmath>
-G \cdot \left[ R_G^{'} -\frac{K}{G} \right] \cdot \frac{2}{G\cdot R_S^{'}} \cdot \left[ 1 + R_G^{'} - \frac{G\cdot R_S^{'}}{2}\right] = K
</latexmath>

<latexmath>
\left[ R_G^{'} - \frac{K}{G} \right] \cdot \left[ R_G^{'} + 1 - \frac{G\cdot R_S^{'}}{2} \right] = -\frac{K\cdot R_S^{'}}{2}
</latexmath>

<latexmath>
{R_G^{'}}^2 + \left[ 1 - \frac{G\cdot R_S^{'}}{2} - \frac{K}{G} \right] \cdot R_G^{'} - \frac{K}{G} \cdot \left( 1 - \frac{G\cdot R_S^{'}}{2} \right) + \frac{K \cdot R_S}{2} = 0
</latexmath>

<latexmath>
{R_G^{'}}^2 + \left[ 1 - \frac{G\cdot R_S^{'}}{2} - \frac{K}{G} \right] \cdot R_G^{'} + K \cdot \left( -\frac{1}{G} + \frac{R_S^{'}}{2} + \frac{R_S}{2} \right) = 0
</latexmath>

<latexmath class="framed">
{R_G^{'}}^2 + \left[ 1 - \frac{G\cdot R_S^{'}}{2} - \frac{K}{G} \right] \cdot R_G^{'} + K \cdot \left( -\frac{1}{G} + R_S^{'} \right) = 0
</latexmath>

#### Solving the balance equation

This quadratic equation can be solved in the usual way[^3]:

<latexmath>
A = 1
</latexmath>

<p></p>

<latexmath>
B = 1 - \frac{G \cdot R_S^{'} }{2} - \frac{K}{G}
</latexmath>

<p></p>

<latexmath>
C = K \cdot \left( -\frac{1}{G} + R_S^{'} \right)
</latexmath>

<p></p>

<latexmath>
\Delta = B^2 - 4 \cdot A \cdot C = \left[ 1 - \frac{G \cdot R_S^{'} }{2} - \frac{K}{G} \right]^2 + 4 \cdot K \cdot \left( \frac{1}{G} - R_S^{'} \right)
</latexmath>

Usually, we say some things about the sign of &&\Delta&& and the existence of the roots. This will be left for a further release of this page. For now, just find the equations to put in Excel:

<latexmath class="framed">
R_G^{'} = \frac{1}{2} \cdot \left[ -B \pm \sqrt{\Delta} \right]
</latexmath>

Leading to the final equation for &&R_G^'&&:

<latexmath>
R_G^{'} = \frac{1}{2} \cdot \left[ -\left[ 1 - \frac{G}{2} \cdot R_S^{'} - \frac{K}{G} \right] \pm \sqrt{ \left[ 1 - \frac{G}{2} \cdot R_S^{'} - \frac{K}{G} \right]^2 - K \cdot \left( \frac{1}{G} - R_S^{'} \right) } \right]
</latexmath>

### Calculation of &&R_T&&

For the calculation of &&R_T&&, the resistances are not normalized because the resulting expression is more meaningful.

&&R_T&& can be calculated by the usual way, a bit long. However, there is a quicker shortcut:

Impedance of &&R_G&&, &&R_F&&, and the amplifier can be calculated from the Miller formula[^4]:

<latexmath>
R_\text{amp} = \frac{R_F + R_G}{1 - \frac{V_\text{OUT}^{-}}{V_x^+}}
</latexmath>

where the gain &&V_\"OUT\"/V_x^+&& can be calculated as such:

<latexmath>
\frac{V_\text{OUT}^{-}}{V_x^+} = \frac{V_S}{V_x^+} \cdot \frac{V_\text{OUT}^{-}}{V_S} = \frac{1}{K} \cdot \frac{-G}{2}
</latexmath>

giving:

<latexmath>
R_\text{amp} = \frac{R_F + R_G}{1 + \frac{G}{2 \cdot K}}
</latexmath>

From this resistance, &&Z_\"IN\"&& can be calculated using the usual parallel resistor formula[^5]:

<latexmath>
Z_\text{IN} = \frac{1}{\frac{1}{R_T}+\frac{1}{R_\text{amp}}}
</latexmath>

which can be reversed as such:

<latexmath>
\frac{1}{R_T} = \frac{1}{\frac{1}{Z_\text{IN}}-\frac{1}{R_\text{amp}}}
</latexmath>

leading to the final expression of &&R_T&&:

<latexmath class="framed">
\frac{1}{R_T} = \frac{1}{\frac{1}{Z_\text{IN}}-\left(1 + \frac{G}{2 \cdot K}\right)\cdot\frac{1}{R_F + R_G}}
</latexmath>

## LTSpice simulation

LTSpice simulation filed are provided here: [diff-amp-SE-plot.asc]({{ '/posts/diff-amp-equations/diff-amp-SE-plot.asc' | absolute_url }}) and [diff-amp-SE-plot.plt]({{ '/posts/diff-amp-equations/diff-amp-SE-plot.plt' | absolute_url }}). Gain was set to 2 to allow easier check of proper operation by superimposing the curves.

<img src="{{ '/posts/diff-amp-equations/diff-amp-SE-schematic.svg' | relative_url }}"/>

<img src="{{ '/posts/diff-amp-equations/diff-amp-SE-plot.png' | relative_url }}"/>

[^1]: [https://www.analog.com/en/resources/app-notes/an-0990.html](https://www.analog.com/en/resources/app-notes/an-0990.html)

[^2]: [https://en.wikipedia.org/wiki/Millman%27s_theorem](https://en.wikipedia.org/wiki/Millman%27s_theorem)

[^3]: [https://en.wikipedia.org/wiki/Quadratic_equation](https://en.wikipedia.org/wiki/Quadratic_equation)

[^4]: [{{ '/posts/miller-effect-1.html' | absolute_url }}]({{ '/posts/miller-effect-1.html' | absolute_url }}) [https://en.wikipedia.org/wiki/Miller_effect](https://en.wikipedia.org/wiki/Miller_effect)

[^5]: [https://en.wikipedia.org/wiki/Series_and_parallel_circuits#Resistance_units_2](https://en.wikipedia.org/wiki/Series_and_parallel_circuits#Resistance_units_2)

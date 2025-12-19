---
layout: post
title: On stability of capacitive loaded op-amps, detailed equations.
permalink: /posts/op-amp-capacitor-stability-equations.html
last_modified_at: 2025-10-10
---

## Isolation resistor + double feedback without RFx resistor

Before getting to the more complex case of the double feedback with RFx resistor, it is useful to study this case.

### Operational amplifier output to feedback

<asciimath>
V^- = (V_"AOP" \cdot C_F \cdot s + V_"out" / R_F) / (C_F \cdot s + 1 / R_F) = (V_"AOP" \cdot C_F \cdot s + V_"AOP" \cdot 1/(1+R_"iso" \cdot C_L \cdot s) \cdot 1 / R_F) / (C_F \cdot s + 1 / R_F)
</asciimath>

<p></p>

<asciimath>
V^- = V_"AOP" \cdot (C_F \cdot s + 1/(1+R_"iso" \cdot C_L \cdot s) \cdot 1 / R_F) / (C_F \cdot s + 1 / R_F)
</asciimath>

<p></p>

<asciimath>
V^- = V_"AOP" \cdot (R_F \cdot C_F \cdot s + 1/(1+R_"iso" \cdot C_L \cdot s)) / (R_F \cdot C_F \cdot s + 1)
</asciimath>

Here the time constants can be introduced:

<asciimath>
V^- = V_"AOP" \cdot (\tau_F \cdot s + 1/(1 + \tau_L \cdot s)) / (\tau_F \cdot s + 1)
</asciimath>

<p></p>

<asciimath>
V^- = V_"AOP" \cdot (1 + (\tau_F \cdot s) \cdot (1 + \tau_L \cdot s)) / ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s))
</asciimath>

<p></p>

<asciimath>
V^- = V_"AOP" \cdot (1 + \tau_F \cdot s + \tau_F \cdot \tau_L \cdot s^2) / ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s))
</asciimath>

### Closed loop AOP gain

<asciimath>
V_"AOP" = (V_"in" - V^-) \cdot "GBW"/s
</asciimath>

<p></p>

<asciimath>
V_"AOP" = V_"in" \cdot "GBW"/s - V^- \cdot "GBW"/s
</asciimath>

<p></p>

<asciimath>
V_"AOP" = V_"in" \cdot "GBW"/s - V_"AOP" \cdot 
  (1 + \tau_F \cdot s + \tau_F \cdot \tau_L \cdot s^2) / ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s)) \cdot "GBW"/s
</asciimath>

<p></p>

<asciimath>
V_"AOP" \cdot [ 1 + (1 + \tau_F \cdot s + \tau_F \cdot \tau_L \cdot s^2) / ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s)) \cdot "GBW"/s ]
= V_"in" \cdot "GBW" / s
</asciimath>

<p></p>

<asciimath>
V_"AOP" \cdot [ 1 + ("GBW" + "GBW" \cdot \tau_F \cdot s + "GBW" \cdot \tau_F \cdot \tau_L \cdot s^2) / ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s) \cdot s) ]
= V_"in" \cdot "GBW" / s
</asciimath>

<p></p>

<asciimath>
V_"AOP" \cdot ( (s + (\tau_F + \tau_S) \cdot s^2 + \tau_F \cdot \tau_L \cdot s^3) + ("GBW" + "GBW" \cdot \tau_F \cdot s + "GBW" \cdot \tau_F \cdot \tau_L \cdot s^2) ) / ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s) \cdot s)
= V_"in" \cdot "GBW" / s
</asciimath>

<p></p>

<asciimath>
V_"AOP" \cdot ( "GBW" + (1 + "GBW" \cdot \tau_F) \cdot s + (\tau_F + \tau_S + "GBW" \cdot \tau_F \cdot \tau_L) \cdot s^2 + \tau_F \cdot \tau_L \cdot s^3 ) / ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s) \cdot s)
= V_"in" \cdot "GBW" / s
</asciimath>

Factorizing by <asciimath>"GBW"</asciimath> and <asciimath>1/s</asciimath>:

<asciimath>
V_"AOP" \cdot ( 1 + (\tau_F + 1 / "GBW") \cdot s + (\tau_F \cdot \tau_L + (\tau_F + \tau_L) / "GBW") \cdot s^2 + (\tau_F \cdot \tau_L) / "GBW" \cdot s^3 ) / ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s))
= V_"in"
</asciimath>

Inverting:

<asciimath>
V_"AOP" 
= ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s)) / ( 1 + (\tau_F + 1 / "GBW") \cdot s + (\tau_F \cdot \tau_L + (\tau_F + \tau_L) / "GBW") \cdot s^2 + (\tau_F \cdot \tau_L) / "GBW" \cdot s^3 ) \cdot  V_"in"
</asciimath>

<p></p>

<!-- Trying to factor:

<latexmath>
\begin{align}
& \frac{\tau_F \cdot \tau_L}{\text{GBW}} \cdot s^3 + \left( \tau_F \cdot \tau_L + \frac{\tau_F + \tau_L}{\text{GBW}} \right) \cdot s^2 + (\tau_F + \frac{1}{GBW}) \cdot s + 1  \\
& = \frac{\tau_F \cdot \tau_L}{\text{GBW}} \cdot \left[
        s^3 +
        \left( \text{GBW} + \frac{\tau_F + \tau_L}{\tau_F \cdot \tau_L} \right) \cdot s^2
        + \left( \frac{\text{GBW}}{\tau_L} + \frac{1}{\tau_F \cdot \tau_L} \right) \cdot s
        + \frac{\text{GBW}}{\tau_F \cdot \tau_L}
    \right]  \\
&= \frac{\tau_F \cdot \tau_L}{\text{GBW}} \cdot \left[
       \left( s + \frac{1}{\tau_L} \right) \cdot
       (s^2) +
       \left( \text{GBW} + \frac{\tau_F + \tau_L}{\tau_F \cdot \tau_L} - \frac{1}{\tau_L} \right) \cdot s^2
       + \left( \frac{\text{GBW}}{\tau_L} + \frac{1}{\tau_F \cdot \tau_L} \right) \cdot s
       + \frac{\text{GBW}}{\tau_F \cdot \tau_L}
   \right]  \\
&= \frac{\tau_F \cdot \tau_L}{\text{GBW}} \cdot \left[
       \left( s + \frac{1}{\tau_L} \right) \cdot
       (s^2) +
       \left( \text{GBW} + \frac{\tau_L}{\tau_F \cdot \tau_L} \right) \cdot s^2
       + \left( \frac{\text{GBW}}{\tau_L} + \frac{1}{\tau_F \cdot \tau_L} \right) \cdot s
       + \frac{\text{GBW}}{\tau_F \cdot \tau_L}
   \right]  \\
&= \frac{\tau_F \cdot \tau_L}{\text{GBW}} \cdot \left[
       \left( s + \frac{1}{\tau_L} \right) \cdot
       \left( s^2 + \left( \text{GBW} + \frac{\tau_L}{\tau_F \cdot \tau_L} \right) \cdot s \right) +
       \left( -\frac{\text{GBW}}{\tau_L} - \frac{1}{\tau_F \cdot \tau_L} + \frac{\text{GBW}}{\tau_L} + \frac{1}{\tau_F \cdot \tau_L} \right) \cdot s
       + \frac{\text{GBW}}{\tau_F \cdot \tau_L}
   \right]  \\
&= \frac{\tau_F \cdot \tau_L}{\text{GBW}} \cdot \left[
       \left( s + \frac{1}{\tau_L} \right) \cdot
       \left( s^2 + \left( \text{GBW} + \frac{\tau_L}{\tau_F \cdot \tau_L} \right) \cdot s \right)
       + \frac{\text{GBW}}{\tau_F \cdot \tau_L}
   \right]  \\
\end{align}
</latexmath>

Not successful, attempt an approximate factorization. -->

Seek factorization on the form:

<latexmath>
\begin{align}
& D(s)  \\
& = (1 + 2 \cdot \zeta \cdot \tau_{p0} \cdot s + \tau_{p0}^2 \cdot s^2) \cdot (1 + \tau_{p1} \cdot s)  \\
& = 1 + (2 \cdot \zeta \cdot \tau_{p0} + \tau_{p1}) \cdot s + (\tau_{p0}^2 + 2 \cdot \zeta \cdot \tau_{p0} \cdot \tau_{p1}) \cdot s^2 + \tau_{p0}^2 \cdot \tau_{p1} \cdot s^3
\end{align}
</latexmath>

Leading to following equations:

<latexmath>
\begin{align}
2 \cdot \zeta \cdot \tau_{p0} + \tau_{p1} &= \tau_F + \frac{1}{\text{GBW}}  \\
\tau_{p0}^2 + 2 \cdot \zeta \cdot \tau_{p0} \cdot \tau_{p1} &= \tau_F \cdot \tau_L + \frac{\tau_F + \tau_L}{\text{GBW}}  \\
\tau_{p0}^2 \cdot \tau_{p1} &= \frac{\tau_F \cdot \tau_L}{\text{GBW}}
\end{align}
</latexmath>

Approximating using: <latexmath>\tau_{p0}^2 \gg 2 \cdot \zeta \cdot \tau_{p0} \cdot \tau_{p1}</latexmath>:

<latexmath>
\begin{align}
\tau_{p0}^2 &\approx \tau_F \cdot \tau_L + \frac{\tau_F + \tau_L}{\text{GBW}}  \\
\left[ \tau_F \cdot \tau_L + \frac{\tau_F + \tau_L}{\text{GBW}} \right] \cdot \tau_{p1} &\approx \frac{\tau_F \cdot \tau_L}{\text{GBW}}  \\
2 \cdot \zeta \cdot \tau_{p0} + \tau_{p1} &= \tau_F + \frac{1}{\text{GBW}}
\end{align}
</latexmath>

Equation of last pole:

<latexmath>
\begin{align}
\left[ \text{GBW} + \frac{\tau_F + \tau_L}{\tau_F \cdot \tau_L} \right] \cdot \tau_{p1} \approx 1  \\
\left[ \text{GBW} + \frac{1}{\tau_F} + \frac{1}{\tau_L} \right] \cdot \tau_{p1} \approx 1  \\
\tau_{p1} \approx \frac{1}{\text{GBW} + \frac{1}{\tau_F} + \frac{1}{\tau_L}}
\end{align}
</latexmath>

AOP dominant. Equation of damping:

<latexmath>
\begin{align}
2 \cdot \zeta \cdot \tau_{p0} + \tau_{p1} &= \tau_F + \frac{1}{\text{GBW}}  \\
\zeta &\approx \frac
    { \tau_F + \frac{1}{\text{GBW}} - \frac{1}{\text{GBW} + \frac{1}{\tau_F} + \frac{1}{\tau_L}} }
    { 2 \cdot \sqrt{\tau_F \cdot \tau_L + \frac{\tau_F + \tau_L}{\text{GBW}}} }
\end{align}
</latexmath>

The upper term can be simplified as such:

<latexmath>
\begin{align}
& \frac{1}{\text{GBW}} - \frac{1}{\text{GBW} + \frac{1}{\tau_F} + \frac{1}{\tau_L}}  \\
& = \frac
    {\text{GBW} + \frac{1}{\tau_F} + \frac{1}{\tau_L} - \text{GBW}}
    {\text{GBW} \cdot \left( \text{GBW} + \frac{1}{\tau_F} + \frac{1}{\tau_L} \right)}  \\
& = \frac
    { \frac{1}{\tau_F} + \frac{1}{\tau_L} }
    {\text{GBW} \cdot \left( \text{GBW} + \frac{1}{\tau_F} + \frac{1}{\tau_L} \right)}  \\
& = \frac
    { \tau_F + \tau_L }
    {\text{GBW} \cdot \left( \text{GBW} \cdot \tau_F \cdot \tau_L + \tau_F + \tau_L \right)}
\end{align}
</latexmath>

<!---- REFACTOR BEFORE -->

Giving:

<latexmath>
\begin{align}
\zeta &\approx \frac
    {
        \tau_F
        + \frac
            { \tau_F + \tau_L }
            {\text{GBW} \cdot \left( \text{GBW} \cdot \tau_F \cdot \tau_L + \tau_F + \tau_L \right)}
    }
    { 2 \cdot \sqrt{\tau_F \cdot \tau_L + \frac{\tau_F + \tau_L}{\text{GBW}}} }
\end{align}
</latexmath>

The value for <asciimath>"GBW" = \infty</asciimath> can be outlined as such:

<latexmath>
\begin{align}
\zeta &\approx
    \frac
    { \tau_F }
    {
        2 \cdot \sqrt{\tau_F \cdot \tau_L}
    } \cdot
    \frac
    {
    1
    + \frac
        { \tau_F + \tau_L }
        {\text{GBW} \cdot \tau_F \cdot \left( \text{GBW} \cdot \tau_F \cdot \tau_L + \tau_F + \tau_L \right)}
    }
    { \sqrt{ 1 + \frac{\tau_F + \tau_L}{\text{GBW} \cdot \tau_F \cdot \tau_L} } }  \\
&\approx
    \sqrt{
        \frac
            { \tau_F }
            { 4 \cdot \tau_L }
    } \cdot
    \frac
    {
    1
    + \frac
        { \tau_F + \tau_L }
        {\text{GBW} \cdot \tau_F \cdot \left( \text{GBW} \cdot \tau_F \cdot \tau_L + \tau_F + \tau_L \right)}
    }
    { \sqrt{ 1 + \frac{\tau_F + \tau_L}{\text{GBW} \cdot \tau_F \cdot \tau_L} } }
\end{align}
</latexmath>

This last expression shows that to have an aperiodic answer, the time constant of the feedback network must be at least 4 times the time constant of the output RC. In this case, the feedback network ensures DC accuracy and stability, but for higher frequencies, this scheme is equivalent to a simple voltage followed followed by the RC network, without any improvement on its bandwidth, which lead to the desire of feedback schemes who provide actual bandwidth improvement.

<!-- ### Gain to load

<asciimath>
V_"out" = V_"AOP" \cdot 1/(1 + R_"iso" \cdot C_L \cdot s) = V_"AOP" \cdot 1/(1 + \tau_L \cdot s)
</asciimath>

<p></p>

<asciimath>
V_"out" 
= ... * ( 1 + (\tau_F + 1 / "GBW") \cdot s + (\tau_F \cdot \tau_L + (\tau_F + \tau_L) / "GBW") \cdot s^2 + (\tau_F \cdot \tau_L) / "GBW" \cdot s^3 ) / ((1 + \tau_F \cdot s) \cdot (1 + \tau_L \cdot s)^2) \cdot  V_"in"
</asciimath> -->

## Isolation resistor + double feedback with RFx resistor

### Operational amplifier output to feedback

<p></p>

<asciimath>
V^- = (V_"AOP" / (R_(Fx) + 1 / (C_F \cdot s)) + V_"out" / R_F) / (1 / (R_(Fx) + 1 / (C_F \cdot s)) + 1 / R_F) = (V_"AOP" / (R_(Fx) + 1 / (C_F \cdot s)) + V_"AOP" \cdot 1/(1+R_"iso" \cdot C_L \cdot s) \cdot 1 / R_F) / (1 / (R_(Fx) + 1 / (C_F \cdot s)) + 1 / R_F)
</asciimath>

<p></p>

<asciimath>
V^- = V_"AOP" \cdot (1 / (R_(Fx) + 1 / (C_F \cdot s)) + 1/(1+R_"iso" \cdot C_L \cdot s) \cdot 1 / R_F) / (1 / (R_(Fx) + 1 / (C_F \cdot s)) + 1 / R_F)
</asciimath>

<p></p>

<asciimath>
V^- = V_"AOP" \cdot (R_F / (R_(Fx) + 1 / (C_F \cdot s)) + 1/(1+R_"iso" \cdot C_L \cdot s)) / (R_F / (R_(Fx) + 1 / (C_F \cdot s)) + 1)
</asciimath>

<p></p>

<asciimath>
V^- = V_"AOP" \cdot ( R_F / (R_(Fx) + 1 / (C_F \cdot s)) \cdot (1+R_"iso" \cdot C_L \cdot s) + 1 ) / ( (R_F / (R_(Fx) + 1 / (C_F \cdot s)) + 1) \cdot (1+R_"iso" \cdot C_L \cdot s) )
</asciimath>

<p></p>

<asciimath>
V^- = ( V_"AOP" \cdot R_F \cdot (1+R_"iso" \cdot C_L \cdot s) + R_(Fx) + 1 / (C_F \cdot s) ) / ( (R_F + R_(Fx) + 1 / (C_F \cdot s)) \cdot (1+R_"iso" \cdot C_L \cdot s) )
</asciimath>

<p></p>

<asciimath>
V^- = V_"AOP" \cdot ( R_F \cdot (1+R_"iso" \cdot C_L \cdot s) \cdot C_F \cdot s + R_(Fx) \cdot C_F \cdot s + 1 ) / ( [ 1 + (R_F + R_(Fx)) \cdot C_F \cdot s ] \cdot (1+R_"iso" \cdot C_L \cdot s) )
</asciimath>

<asciimath>
V^- = V_"AOP" \cdot ( R_F \cdot C_F \cdot s + R_"iso" \cdot C_L \cdot R_F \cdot C_F \cdot s^2 + R_(Fx) \cdot C_F \cdot s + 1 ) / ( [ 1 + (R_F + R_(Fx)) \cdot C_F \cdot s ] \cdot (1+R_"iso" \cdot C_L \cdot s) )
</asciimath>

<asciimath>
V^- = V_"AOP" \cdot ( R_F \cdot C_F \cdot s + R_"iso" \cdot C_L \cdot R_F \cdot C_F \cdot s^2 + R_(Fx) \cdot C_F \cdot s + 1 ) / ( (1+R_"iso" \cdot C_L \cdot s) \cdot [ 1 + (R_F + R_(Fx)) \cdot C_F \cdot s ] )
</asciimath>

<asciimath>
V^- = V_"AOP" \cdot ( 1 + ( R_F +  R_(Fx) ) \cdot C_F \cdot s + R_"iso" \cdot C_L \cdot R_F \cdot C_F \cdot s^2 ) / ( (1+R_"iso" \cdot C_L \cdot s) \cdot [ 1 + (R_F + R_(Fx)) \cdot C_F \cdot s ] )
</asciimath>

To avoid overshoots in the transfer function, it is seeked that the numerator has real roots, corresponding to time constants named conveniently <asciimath>\tau_3</asciimath> and <asciimath>\tau_4</asciimath>, sorted in such a way that <asciimath>\tau_3 >= \tau_4</asciimath>. The denominator has two real roots, corresponding to the time constant <asciimath>R_"iso"\cdot C_L</asciimath> and to a time constant <asciimath>\tau_2=(R_F+R_(Fx)) \cdot C_F</asciimath>. Viete's relations show that <asciimath>\tau_3+\tau_4=1+(R_F+R_(Fx)) \cdot C_F</asciimath> and hence that <asciimath>\tau_3+\tau_4=\tau_2</asciimath>. Thus, these constants can be ordered and renamed as follows:

<asciimath>\tau_2 >= \tau_3 >= \tau_4</asciimath>

For stability reasons, the phase shift at the unity gain frequency must be low enough because the op-amp has already a 90° phase shift, so <asciimath>\tau_4 >= \tau_"min"</asciimath>, with <asciimath>\tau_"min"</asciimath> sufficiently lower than the time constant of the unity gain frequency.

### Closed loop AOP gain

<asciimath>
V_"AOP" = (V_"in" - V_x) \cdot "GBW"/s
</asciimath>

<p></p>

<asciimath>
V_"AOP" = V_"in" \cdot "GBW"/s - V_x \cdot "GBW"/s
</asciimath>

<p></p>

<asciimath>
V_"AOP" = V_"in" \cdot "GBW"/s - V_"AOP" \cdot
  ( 1 + (R_F + R_(Fx)) \cdot C_F \cdot s + R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2 ) /
  (1 + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^2 ) \cdot "GBW"/s
</asciimath>

<p></p>

<asciimath>
V_"AOP" \cdot [ 1 + ( 1 + (R_F + R_(Fx)) \cdot C_F \cdot s + R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2 ) /
  (1 + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^2 ) \cdot "GBW"/s ]
= V_"in" \cdot "GBW" / s
</asciimath>

<p></p>

<asciimath>
V_"AOP" \cdot [ 1 + ( "GBW" + "GBW" \cdot (R_F + R_(Fx)) \cdot C_F \cdot s + "GBW" \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2 ) /
  (s + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s^2 + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^3 ) ]
= V_"in" \cdot "GBW" / s
</asciimath>

<p></p>

<asciimath>
V_"AOP" \cdot
( "GBW" + [1 + "GBW" \cdot (R_F + R_(Fx)) \cdot C_F] \cdot s + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F + "GBW" \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F) \cdot s^2 + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^3 ) /
( s + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s^2 + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^3 )
= V_"in" \cdot "GBW" / s
</asciimath>

<p></p>

<asciimath>
V_"AOP" = V_"in" \cdot "GBW" / s \cdot
( s + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s^2 + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^3 ) /
( "GBW" + [1 + "GBW" \cdot (R_F + R_(Fx)) \cdot C_F] \cdot s + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F + "GBW" \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F) \cdot s^2 + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^3 )
</asciimath>

<p></p>

<asciimath>
V_"AOP" = V_"in" \cdot
( 1 + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^2 ) /
( 1 + [1 / "GBW" + (R_F + R_(Fx)) \cdot C_F] \cdot s + ((R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) / "GBW" + R_"iso" \cdot R_F \cdot C_L \cdot C_F) \cdot s^2 + (R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F) / "GBW" \cdot s^3 )
</asciimath>

<!--
### Simpification for GBW high enough

Assuming GBW is high enough, and letting aside the question of what is high enough, the previous monster can be simplified as follows:

<asciimath>
V_"AOP" = V_"in" \cdot
( 1 + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^2 ) /
( 1 + [(R_F + R_(Fx)) \cdot C_F] \cdot s + R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2 )
</asciimath>

Note only the denominator is impacted by this simplification.
-->

### Output at the capacitive load

<asciimath>
V_"out" = V_"AOP" \cdot (1/(C_L \cdot s))/(R_"iso"+1/(C_L \cdot s)) = V_"AOP" \cdot 1/(1+R_"iso" \cdot C_L \cdot s)
</asciimath>

<p></p>

<asciimath>
V_"out" = V_"in" \cdot
( 1 + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^2 ) /
( 1 + [1 / "GBW" + (R_F + R_(Fx)) \cdot C_F] \cdot s + ((R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) / "GBW" + R_"iso" \cdot R_F \cdot C_L \cdot C_F) \cdot s^2 + (R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F) / "GBW" \cdot s^3 )
\cdot 1/(1+R_"iso" \cdot C_L \cdot s)
</asciimath>

<!--
Expression with simplification
<asciimath>
V_"AOP" = V_"in" \cdot
( 1 + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^2 ) /
( 1 + [(R_F + R_(Fx)) \cdot C_F] \cdot s + R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2 )
\cdot 1/(1+R_"iso" \cdot C_L \cdot s)
</asciimath>
-->

<!-- The denominator is a monster, however the numerator does not depends on GBW and can be factored in the usual way.

<asciimath>
Delta = [R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F]^2 - 4 \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F
</asciimath>

<asciimath>
Delta = R_"iso"^2 \cdot C_L^2 + 2 \cdot R_"iso" \cdot C_L \cdot (R_F + R_(Fx)) \cdot C_F + (R_F + R_(Fx))^2 \cdot C_F^2 - 4 \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F
</asciimath> -->

The numerator can be factored as such:

<asciimath>
N(s) = [1 + R_"iso" \cdot C_L \cdot s] \cdot [1 + (R_F + R_(Fx)) \cdot C_F \cdot s]
</asciimath>

Leading to a simpler expression:

<asciimath>
V_"out" = V_"in" \cdot
[1 + (R_F + R_(Fx)) \cdot C_F \cdot s] /
( 1 + [1 / "GBW" + (R_F + R_(Fx)) \cdot C_F] \cdot s + ((R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) / "GBW" + R_"iso" \cdot R_F \cdot C_L \cdot C_F) \cdot s^2 + (R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F) / "GBW" \cdot s^3 )
</asciimath>

<!-- TODO: Use the same factorization method as before. -->

The only practical way to handle this is to assume a big enough GBW:

<asciimath>
V_"out" = V_"in" \cdot
[1 + (R_F + R_(Fx)) \cdot C_F \cdot s] /
( 1 + (R_F + R_(Fx)) \cdot C_F \cdot s + R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2 )
</asciimath>

<!-- The error can be expressed as such:

<asciimath>
V_"out" - V_"in" = V_"in" \cdot
[R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2] /
( 1 + (R_F + R_(Fx)) \cdot C_F \cdot s + R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2 )
</asciimath> -->

### Poles and zeros of the closed loop transfer function

This transfer function has the time constants previously found: a zero with time constant <asciimath>\tau_2=(R_F+R_(Fx)) \cdot C_F</asciimath> and two poles with times constants <asciimath>\tau_3</asciimath> and <asciimath>\tau_4</asciimath> such as <asciimath>\tau_3+\tau_4=\tau_2</asciimath>.

For the transfert function to be as close as possible to an ideal single-pole function, the zero time constant <asciimath>\tau_2</asciimath> should be close enough to one of the time constants of the poles, <asciimath>\tau_3</asciimath> or <asciimath>\tau_4</asciimath>.

Since <asciimath>\tau_3+\tau_4=\tau_2</asciimath> and <asciimath>\tau_3>=\tau_4</asciimath>, this lead to <latexmath>\tau_2 \approx \tau_3 \gg \tau_4</latexmath>.

### Loop gain, stability, and omega max

The loop gain is:

<latexmath>
L = \frac{\text{GBW}}{s} \cdot
    \frac{
        1 + \left( R_F +  R_{Fx} \right) \cdot C_F \cdot s + R_\text{iso} \cdot C_L \cdot R_F \cdot C_F \cdot s^2
    }{
        \left( 1 + R_\text{iso} \cdot C_L \cdot s \right) \cdot \left[ 1 + (R_F + R_{Fx}) \cdot C_F \cdot s \right]
    }
</latexmath>

Plugging into this equation the time constants:

<latexmath>
L = \text{GBW} \cdot
    \frac{
        (1 + \tau_3 \cdot s) \cdot (1 + \tau_4 \cdot s)
    }{
        \left( 1 + \tau_L \cdot s \right) \cdot \left( 1 + \tau_2 \cdot s \right) \cdot s
    }
</latexmath>

Using the relations between time constants:

<latexmath>
L = \text{GBW} \cdot
    \frac{
        (1 + \tau_3 \cdot s) \cdot (1 + \tau_4 \cdot s)
    }{
        \left( 1 + \tau_L \cdot s \right) \cdot \left[ 1 + \left( \tau_3 + \tau_4 \right) \cdot s \right] \cdot s
    }
</latexmath>

At the unity gain frequency to be calculated:

<latexmath>
\begin{align*}
\left| L(\omega_0) \right| &= \left| \text{GBW} \cdot
    \frac{
        (1 + j \cdot \tau_3 \cdot \omega_0) \cdot (1 + j \cdot \tau_4 \cdot \omega_0)
    }{
        \left( 1 + j \cdot \tau_L \cdot \omega_0 \right) \cdot \left[ 1 + j \cdot \left( \tau_3 + \tau_4 \right) \cdot \omega_0 \right] \cdot j \cdot \omega_0
    } \right|  \\
&= \text{GBW} \cdot
    \frac{
        \left| 1 + j \cdot \tau_3 \cdot \omega_0 \right| \cdot \left| 1 + j \cdot \tau_4 \cdot \omega_0 \right|
    }{
        \left| 1 + j \cdot \tau_L \cdot \omega_0 \right| \cdot \left| 1 + j \cdot \left( \tau_3 + \tau_4 \right) \cdot \omega_0 \right| \cdot \omega_0
    }
\end{align*}
</latexmath>

Since for stability reasons the unity gain frequency is much greater than the other poles and zeros, it can be simplified as such:

<latexmath>
\begin{align*}
\left| L(\omega_0) \right| &= \text{GBW} \cdot
    \frac{
        \tau_3 \cdot \omega_0 \cdot \tau_4 \cdot \omega_0
    }{
        \tau_L \cdot \omega_0 \cdot \left( \tau_3 + \tau_4 \right) \cdot \omega_0 \cdot \omega_0
    }  \\
&= \text{GBW} \cdot
    \frac{
        \tau_3 \cdot \tau_4
    }{
        \tau_L \cdot \left( \tau_3 + \tau_4 \right)
    } \cdot \frac{1}{\omega_0}  \\
&= \text{GBW} \cdot
    \frac{
        1
    }{
        \tau_L \cdot \left( \frac{1}{\tau_3} + \frac{1}{\tau_4} \right)
    } \cdot \frac{1}{\omega_0}  \\
\end{align*}
</latexmath>

Since <asciimath>\tau_4</asciimath> depends on <asciimath>\omega_0</asciimath> because it must be high enough compared to <asciimath>1/\omega_0</asciimath>, it is useful to introduce a product <asciimath>k_4 = \tau_4 \cdot \omega_0</asciimath>. 5 can be used as a starting point for a convenient phase shift. With this:

<latexmath>
\begin{align*}
\left| L(\omega_0) \right| &= \text{GBW} \cdot
    \frac{
        1
    }{
        \tau_L \cdot \left( \frac{1}{\tau_3} + \frac{\omega_0}{k_4} \right)
    } \cdot \frac{1}{\omega_0}  \\
\end{align*}
</latexmath>

Solving this equation:

<latexmath>
\begin{align*}
& \left| L(\omega_0) \right| = 1  \\
& \text{GBW} \cdot
    \frac{
        1
    }{
        \tau_L \cdot \left( \frac{1}{\tau_3} + \frac{\omega_0}{k_4} \right)
    } \cdot \frac{1}{\omega_0} = 1  \\
& \text{GBW} = \tau_L \cdot \left( \frac{1}{\tau_3} + \frac{\omega_0}{k_4} \right) \cdot \omega_0  \\
\end{align*}
</latexmath>

This equation will be solved in two ways: a zero order approximation to have a tendency, and a first order approximation based on this tendency.

Since <latexmath>\tau_3 \gg \tau_4</latexmath>, the equation can be simplified as such:

<latexmath>
\begin{align*}
& \text{GBW} \approx \tau_L \cdot \frac{\omega_0}{k_4} \cdot \omega_0 = \frac{\tau_L \cdot \omega_0^2}{k_4} \\
& \omega_0 = \sqrt{\frac{\text{GBW} \cdot k_4}{\tau_L}}
\end{align*}
</latexmath>

### Components values for the unit loop gain

Taking again the expression for the loop gain:

<latexmath>
\begin{align*}
\left| L(\omega_0) \right| &= \text{GBW} \cdot
    \frac{
        \tau_3 \cdot \tau_4
    }{
        \tau_L \cdot \left( \tau_3 + \tau_4 \right)
    } \cdot \frac{1}{\omega_0}  \\
\end{align*}
</latexmath>

Plugging inside the relations between <latexmath>\tau_3 \cdot \tau_4</latexmath>, <latexmath>\tau_3+\tau_4</latexmath>, <latexmath>\tau_L</latexmath> and the component values:

<latexmath>
\begin{align*}
\left| L(\omega_0) \right| &= \frac{\text{GBW}}{\omega_0} \cdot
    \frac{
        R_\text{iso} \cdot C_L \cdot R_F \cdot C_F
    }{
        R_\text{iso} \cdot C_L \cdot \left( R_F + R_{Fx} \right) \cdot C_F
    }  \\
&= \frac{\text{GBW}}{\omega_0} \cdot \frac{R_F}{R_F + R_{Fx}}  \\
\end{align*}
</latexmath>

Since <latexmath>\left| L(\omega_0) \right| = 1</latexmath>:

<latexmath>
\begin{align*}
\frac{R_F}{R_F + R_{Fx}} = \frac{\omega_0}{\text{GBW}} = \sqrt{\frac{k_4}{\text{GBW} \cdot \tau_L}}  \\
\end{align*}
</latexmath>

### LTSpice simulation

<img src="{{ '/posts/op-amp-capacitor-stability/op-amp-capacitor-compensated.png' | relative_url }}" >

<img src="{{ '/posts/op-amp-capacitor-stability/op-amp-capacitor-compensated-AC.png' | relative_url }}" >

<img src="{{ '/posts/op-amp-capacitor-stability/op-amp-capacitor-compensated-tran.png' | relative_url }}" >

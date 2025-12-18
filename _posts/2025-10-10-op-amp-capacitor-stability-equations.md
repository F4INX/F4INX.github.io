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

## Other equations to sort

<!-- Two things must be looked at. First, the transfer function, from <asciimath>V_"in"</asciimath> to <asciimath>V_"out"</asciimath>. Second, the closed loop output impedance, particularly important for outputs which should be fixed like DC voltages, and rightly underlined by Chris Basso in his presentations. -->

<!-- TODO: Add the link for Chris Basso. -->

<!-- Transfert function can be written as such: -->

#### Operational amplifier output to feedback

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

This expression has the following poles and zeros:

* a pole of time constant &&\tau_{p1} = R_\"iso\"\cdot C_L&& corresponding to the isolation resistor and the load, which is quite normal to be in the feedback, because the feedback should compensate it to some extent,

* a zero of time constant &&\tau_{z1}&&, which should be placed before the unity gain cross-over, to ensure stability,

* another zero of time constant &&\tau_{z2}&&, which will be analyzed later,

* another pole of time constant &&\tau_{p2} = (R_F + R_(Fx)) \cdot C_F&&, which will be also analyzed later.

#### Values of the zeros

Instead of solving the numerator to get the roots, we will instead choose them. The numerator can be directly written as a product with its roots:

<latexmath>
\begin{split}
\text{num} &= 1 + ( R_F +  R_{Fx} ) \cdot C_F \cdot s + R_\text{iso} \cdot C_L \cdot R_F \cdot C_F \cdot s^2 \\
\text{num} &= (1 + \tau_{z1} \cdot s) \cdot (1 + \tau_{z2} \cdot s)
\end{split}
</latexmath>

Developping and identifying:

<latexmath>
\begin{split}
( R_F +  R_{Fx} ) \cdot C_F &= \tau_{z1} + \tau_{z2} \\
R_\text{iso} \cdot C_L \cdot R_F \cdot C_F &= \tau_{z1} \cdot \tau_{z2}
\end{split}
</latexmath>

Note we have also, from the denominator:

<latexmath>
\begin{split}
( R_F +  R_{Fx} ) \cdot C_F &= \tau_{p2}
\end{split}
</latexmath>

Giving the following equations linking the values of the components and the pole &&\tau_{p2}&& to the zeros:

<latexmath>
\begin{split}
( R_F +  R_{Fx} ) \cdot C_F &= \tau_{z1} + \tau_{z2} \\
R_\text{iso} \cdot C_L \cdot R_F \cdot C_F &= \tau_{z1} \cdot \tau_{z2} \\
\tau_{p2} &= \tau_{z1} + \tau_{z2}
\end{split}
</latexmath>

#### Values of the zeros (old)

Instead of solving the numerator to get the roots, we will instead work it to choose the roots. The first root will be chosen as &&s_\"z1\" = -1/\tau_1&&, where the detailed value of &&\tau_1&& will be calculated later. By Euclidean division, the numerator can be rewriten as such:

<asciimath>
"num" = R_"iso" \cdot C_L \cdot R_F \cdot C_F \cdot s^2 + ( R_F +  R_(Fx) ) \cdot C_F \cdot s + 1
</asciimath>

<p></p>

<asciimath>
"num" - (s + 1/\tau_1)(R_"iso" \cdot C_L \cdot R_F \cdot C_F \cdot s) = ( R_F +  R_(Fx) ) \cdot C_F \cdot s - ( R_"iso" \cdot C_L \cdot R_F \cdot C_F ) / \tau_1 \cdot s + 1
</asciimath>

<p></p>

<asciimath>
"num" - (s + 1/\tau_1)(R_"iso" \cdot C_L \cdot R_F \cdot C_F \cdot s) = [ ( R_F +  R_(Fx) ) \cdot C_F - ( R_"iso" \cdot C_L \cdot R_F \cdot C_F ) / \tau_1 ] \cdot s + 1
</asciimath>

<p></p>

<asciimath>
"num" - (s + 1/\tau_1)[R_"iso" \cdot C_L \cdot R_F \cdot C_F \cdot s + [ ( R_F +  R_(Fx) ) \cdot C_F - ( R_"iso" \cdot C_L \cdot R_F \cdot C_F ) / \tau_1 ] ] = - [ ( R_F +  R_(Fx) ) \cdot C_F - ( R_"iso" \cdot C_L \cdot R_F \cdot C_F ) / \tau_1 ] \cdot 1 / \tau_1 + 1
</asciimath>

The right hand side, which should be equal to 0 for &&-1/(\tau_1)&& to be a root, is equal to &&\"num\"(-1/(\tau_1))&&, which is logical. When this condition is fullfilled, the factorization of the numerator and a little simplification give the following equations:

<latexmath>
\begin{split}
\text{num} &= R_\text{iso} \cdot C_L \cdot R_F \cdot C_F \cdot \left(s + \frac{1}{\tau_1}\right) \cdot \left(s + \frac{1}{\tau_2}\right) \\
\tau_2 &= \frac{ R_\text{iso} \cdot C_L \cdot R_F \cdot C_F  } {\tau_1} \\
& - \left[ ( R_F +  R_{Fx} ) \cdot C_F - \frac{ R_\text{iso} \cdot C_L \cdot R_F \cdot C_F }{ \tau_1 } \right] \cdot \frac{1}{\tau_1} + 1 = 0
\end{split}
</latexmath>

<p></p>

Solving the equation for &&\tau_1&&:

<latexmath>
( R_F +  R_{Fx} ) \cdot C_F - \frac{ R_\text{iso} \cdot C_L \cdot R_F \cdot C_F }{ \tau_1 } = \tau_1
</latexmath>

<p></p>

<latexmath>
( R_F +  R_{Fx} ) \cdot C_F - \frac{ R_\text{iso} \cdot C_L \cdot C_F }{ \tau_1 } \cdot \frac{R_F}{R_F +  R_{Fx}} \cdot ( R_F +  R_{Fx} ) \cdot C_F = \tau_1
</latexmath>

<p></p>

<latexmath>
\left[ 1 - \frac{ R_\text{iso} \cdot C_L }{ \tau_1 } \cdot \frac{R_F}{R_F +  R_{Fx}} \right] \cdot \left[ ( R_F +  R_{Fx} ) \cdot C_F \right] = \tau_1
</latexmath>

<p></p>

<latexmath>
( R_F +  R_{Fx} ) \cdot C_F = \frac{\tau_1}{\left[ 1 - \frac{ R_\text{iso} \cdot C_L }{ \tau_1 } \cdot \frac{R_F}{R_F + R_{Fx}} \right]}
</latexmath>

Solve equation for &&\tau_2&&:

<latexmath>
\begin{split}
\tau_2 &= \frac{ R_\text{iso} \cdot C_L \cdot R_F \cdot C_F  } {\tau_1} = R_\text{iso} \cdot C_L \cdot \frac{R_F}{R_F +  R_{Fx}} \cdot \frac{ (R_F +  R_{Fx}) \cdot C_F  } {\tau_1} \\
&= R_\text{iso} \cdot C_L \cdot \frac{R_F}{R_F +  R_{Fx}} \cdot \frac{1}{\left[ 1 - \frac{ R_\text{iso} \cdot C_L }{ \tau_1 } \cdot \frac{R_F}{R_F + R_{Fx}} \right]} \\
&= \frac{ R_\text{iso} \cdot C_L }{\left[ \frac{R_F + R_{Fx}}{R_F} - \frac{ R_\text{iso} \cdot C_L }{ \tau_1 } \right]}
\end{split}
</latexmath>

Relative position of second zero &&\tau_2&& and pole &&\tau_{p2}&&:

<latexmath>
\begin{split}
\frac{\tau_2}{\tau_{p2}} &= R_\text{iso} \cdot C_L \cdot \frac{R_F}{R_F +  R_{Fx}} \cdot \frac{ (R_F +  R_{Fx}) \cdot C_F  } {\tau_1} \cdot \frac{1}{ (R_F +  R_{Fx}) \cdot C_F } \\
&= \frac{ R_\text{iso} \cdot C_L  } {\tau_1} \cdot \frac{R_F}{R_F +  R_{Fx}}
\end{split}
</latexmath>

#### Merging of the zeros

The numerator has two zeros. In a first approach, it could be attempted to make these two zeros coincide, at least to see what happens. Since the numerator is a quadratic equation, the zeros have the same frequency if:

<asciimath>
Delta_"zeros" = 0
</asciimath>

<p></p>

<asciimath>
[ (R_F + R_(Fx)) \cdot C_F ]^2 - 4 \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F = 0
</asciimath>

<!-- <p></p>

<asciimath>
(R_F^2 + 2 \cdot R_F \cdot R_(Fx) + R_(Fx)^2) \cdot C_F^2 - 4 \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F = 0
</asciimath>

<p></p>

<asciimath>
R_F^2 \cdot C_F^2 + 2 \cdot R_F \cdot R_(Fx) \cdot C_F^2 + R_(Fx)^2 \cdot C_F^2 - 4 \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F = 0
</asciimath> -->

Before solving this equation, it is interesting to perform the following change of variables:

<latexmath>
\begin{split}
R_{FT} &= R_{F} + R_{Fx} \\
k_F &= \frac{R_{F}}{R_{FT}}
\end{split}
</latexmath>

Giving the following equation:

<asciimath>
[ R_(FT) \cdot C_F ]^2 - 4 \cdot R_"iso" \cdot k \cdot R_(FT) \cdot C_L \cdot C_F = 0
</asciimath>

<!-- This expression contains a pole corresponding to the RC constant of the isolation resistor and to the load, which is useful because the feedback should compensate it. However, the second pole is not desirable, and should be compensated by one of the zeros of the numeraros. -->

#### Removal of one pole

It would be tempting to solve the numerator to find the zeros, and then placing the zeros where we want. However, since we know the position we want, it is better to directly enforce it, in the following way.

<asciimath>
1 + ( R_F +  R_(Fx) ) \cdot C_F \cdot s + R_"iso" \cdot C_L \cdot R_F \cdot C_F \cdot s^2 = 0 " when " s = - 1 / ((R_F + R_(Fx)) \cdot C_F)
</asciimath>

<asciimath>
1 - ( ( R_F +  R_(Fx) ) \cdot C_F ) / ((R_F + R_(Fx)) \cdot C_F) + ( R_"iso" \cdot C_L \cdot R_F \cdot C_F ) / [(R_F + R_(Fx)) \cdot C_F]^2 = 0
</asciimath>

#### Poles and zeros of the feedback

Zeros can be obtained by solving the quadratic equations:

<asciimath>
Delta_"zeros" = [ (R_F + R_(Fx)) \cdot C_F ]^2 - 4 \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F
</asciimath>

<p></p>

<asciimath>
Delta_"zeros" = (R_F^2 + 2 \cdot R_F \cdot R_(Fx) + R_(Fx)^2) \cdot C_F^2 - 4 \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F
</asciimath>

<p></p>

<asciimath>
Delta_"zeros" = R_F^2 \cdot C_F^2 + 2 \cdot R_F \cdot R_(Fx) \cdot C_F^2 + R_(Fx)^2 \cdot C_F^2 - 4 \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F
</asciimath>

<p></p>

<asciimath>
s_z = (- ( R_F +  R_(Fx) ) \cdot C_F +- sqrt( R_F^2 \cdot C_F^2 + 2 \cdot R_F \cdot R_(Fx) \cdot C_F^2 + R_(Fx)^2 \cdot C_F^2 - 4 \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F ) ) / (2 \cdot R_"iso" \cdot C_L \cdot R_F \cdot C_F )
</asciimath>

<p></p>

<asciimath>
s_z = - ( R_F +  R_(Fx) ) / (2 \cdot R_"iso" \cdot R_F \cdot C_L ) +- sqrt( R_F^2 \cdot C_F^2 + 2 \cdot R_F \cdot R_(Fx) \cdot C_F^2 + R_(Fx)^2 \cdot C_F^2 - 4 \cdot R_"iso" \cdot R_F \cdot C_L \cdot C_F ) / (2 \cdot R_"iso" \cdot C_L \cdot R_F \cdot C_F )
</asciimath>

#### Closed loop AOP gain

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
#### Simpification for GBW high enough

Assuming GBW is high enough, and letting aside the question of what is high enough, the previous monster can be simplified as follows:

<asciimath>
V_"AOP" = V_"in" \cdot
( 1 + (R_"iso" \cdot C_L + (R_F + R_(Fx)) \cdot C_F) \cdot s + R_"iso" \cdot (R_F + R_(Fx)) \cdot C_L \cdot C_F \cdot s^2 ) /
( 1 + [(R_F + R_(Fx)) \cdot C_F] \cdot s + R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2 )
</asciimath>

Note only the denominator is impacted by this simplification.
-->

#### Output at the capacitive load

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

### Aperiodic answer

For most applications, an aperiodic answer is seeked. A too high damping would cause a slow response, and a too low damping would cause undesirable overshoots.

The critically damped condition can be written as:

<latexmath>
\begin{align*}
& 1 + (R_F + R_{Fx}) \cdot C_F \cdot s + R_\text{iso} \cdot R_F \cdot C_L \cdot C_F \cdot s^2 = 1 + \frac{2 \zeta}{\omega} \cdot s + \frac{1}{\omega^2} \cdot s^2  \\
& \zeta = \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot \sqrt{R_\text{iso} \cdot R_F \cdot C_L \cdot C_F}}  \\
& (R_F + R_{Fx}) \cdot C_F = 2 \cdot \zeta \cdot \sqrt{R_\text{iso} \cdot R_F \cdot C_L \cdot C_F}
\end{align*}
</latexmath>

Introducing the following change of variables:

<latexmath>
\begin{split}
R_{FT} &= R_{F} + R_{Fx} \\
k_F &= \frac{R_{F}}{R_{FT}}
\end{split}
</latexmath>

It gives:

<latexmath>
\begin{align*}
& R_{FT} \cdot C_F = 2 \cdot \zeta \cdot \sqrt{R_\text{iso} \cdot R_{FT} \cdot k_F \cdot C_L \cdot C_F}  \\
\\
& R_{FT}^2 \cdot C_F^2 = 4 \cdot \zeta^2 \cdot R_\text{iso} \cdot R_{FT} \cdot k_F \cdot C_L \cdot C_F   \\
\\
& k_F = \frac{R_{FT} \cdot C_F}{4 \cdot \zeta^2 \cdot R_\text{iso} \cdot C_L}
\end{align*}
</latexmath>

### Step answer

<asciimath>
V_"out" = \frac{1}{s} \cdot
[1 + (R_F + R_(Fx)) \cdot C_F \cdot s] /
( 1 + (R_F + R_(Fx)) \cdot C_F \cdot s + R_"iso" \cdot R_F \cdot C_L \cdot C_F \cdot s^2 )
</asciimath>

<!-- Add a link to table -->

We search to express this in the form

<asciimath>
V_"out" = \frac{A}{s} + B \cdot (s + \alpha) / ( (s + \alpha)^2 + \omega^2 ) + C \cdot (\omega) / ( (s + \alpha)^2 + \omega^2 )
</asciimath>

<p></p>

<asciimath>
V_"out" = \frac{A}{s} + (C \cdot \omega + B \cdot \alpha + B \cdot s) / ( \omega^2 + \alpha^2 + 2 \cdot \alpha \cdot s + s^2)
</asciimath>

<p></p>

<!-- TODO: add steps before -->
<asciimath>
V_"out" = 1 / s \cdot ( A \cdot (\omega^2 + \alpha^2) + [C \cdot \omega + (2 \cdot A + B) \cdot \alpha] \cdot s + (A + B) \cdot s^2 ) / ( \omega^2 + \alpha^2 + 2 \cdot \alpha \cdot s + s^2)
</asciimath>

<p></p>

<asciimath>
V_"out" = 1 / s \cdot ( A + [C \cdot \omega + (2 \cdot A + B) \cdot \alpha] / (\omega^2 + \alpha^2) \cdot s + (A + B) / (\omega^2 + \alpha^2) \cdot s^2 ) / ( 1 + (2 \cdot \alpha) / (\omega^2 + \alpha^2) \cdot s + 1 / (\omega^2 + \alpha^2) \cdot s^2)
</asciimath>

Equating the coefficients:

<latexmath>
\begin{align*}
A &= 1   \\
\frac{C \cdot \omega + (2 \cdot A + B) \cdot \alpha}{\omega^2 + \alpha^2} &= (R_F + R_(Fx)) \cdot C_F  \\
\frac{A + B}{\omega^2 + \alpha^2} &= 0  \\
\frac{2 \cdot \alpha}{\omega^2 + \alpha^2} &= (R_F + R_{Fx}) \cdot C_F  \\
\frac{1}{\omega^2 + \alpha^2} &= R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F
\end{align*}
</latexmath>

Solving:

<latexmath>
\begin{align*}
A &= 1   \\
C \cdot \omega + \alpha &= \frac{(R_F + R_(Fx)) \cdot C_F}{R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}  \\
B &= -1  \\
\frac{2 \cdot \alpha}{\omega^2 + \alpha^2} &= (R_F + R_{Fx}) \cdot C_F  \\
\frac{1}{\omega^2 + \alpha^2} &= R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F
\end{align*}
</latexmath>

Expressions for <asciimath>\alpha</asciimath> and C:

<latexmath>
\begin{align*}
\alpha &= \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}  \\
C \cdot \omega &= \frac{(R_F + R_(Fx)) \cdot C_F}{R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} - \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}  \\
&= \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}
\end{align*}
</latexmath>

Solving for frequency <asciimath>\omega</asciimath>:
<latexmath>
\begin{align}
\frac{2 \cdot \alpha}{\omega^2 + \alpha^2} &= (R_F + R_{Fx}) \cdot C_F \\
\frac{1}{\omega^2 + \alpha^2} &= R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F
\end{align}
</latexmath>

<p></p>
<latexmath>
\begin{align}
\alpha &= \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} \\
\omega^2 + \alpha^2 &= \frac{1}{R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}
\end{align}
</latexmath>

<p></p>
<latexmath>
\begin{align}
\omega^2 &= \frac{1}{R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} - \left[ \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} \right]^2  \\
\omega^2 &= \frac{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}{4 \cdot R_{\text{iso}}^2 \cdot R_F^2 \cdot C_L^2 \cdot C_F^2} - \frac{(R_F + R_{Fx})^2 \cdot C_F^2}{4 \cdot R_{\text{iso}}^2 \cdot R_F^2 \cdot C_L^2 \cdot C_F^2}  \\
\omega^2 &= \frac{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}{4 \cdot R_{\text{iso}}^2 \cdot R_F^2 \cdot C_L^2 \cdot C_F^2}
\end{align}
</latexmath>

### Squared integral of the error

<latexmath>
E = \int_{0}^{+\infty} \left[ e^{-\alpha\cdot t}\,\big[ B\cos(\omega t) + C\sin(\omega t) \big] \right]^2 \, dt
</latexmath>

which can be calculated as follows: <!-- FIXME: details -->

<latexmath>
\begin{align*}
E &= \int_{0}^{+\infty} e^{-2at}\big(B\cos(\omega t)+C\sin(\omega t)\big)^2\,dt  \\
  &= \frac{B^2+C^2}{4a} + \frac{a(B^2-C^2)+2\omega BC}{4\,(a^2+\omega^2)}
\end{align*}
</latexmath>

By substituing the previously calculated coefficients values:

<latexmath>
\begin{align*}
\frac{B^2}{\alpha} &= (-1)^2 \cdot \frac{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}{(R_F + R_{Fx}) \cdot C_F}  \\
  &= \frac{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}{(R_F + R_{Fx}) \cdot C_F}  \\
\frac{C^2}{\alpha} &= \left[ \frac{(R_F + R_{Fx}) \cdot C_F}{\omega \cdot 2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} \right]^2 \cdot \frac{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}{(R_F + R_{Fx}) \cdot C_F} \\
  &= \frac{(R_F + R_{Fx}) \cdot C_F}{\omega^2 \cdot 2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}  \\
\frac{B^2+C^2}{\alpha} &= \frac{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}{(R_F + R_{Fx}) \cdot C_F} + \frac{(R_F + R_{Fx}) \cdot C_F}{\omega^2 \cdot 2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}
\end{align*}
</latexmath>

<latexmath>
\begin{align*}
&\omega^2 \cdot 2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F  \\
&= \frac{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}{4 \cdot R_{\text{iso}}^2 \cdot R_F^2 \cdot C_L^2 \cdot C_F^2} \cdot 2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F  \\
&= \frac{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}
\end{align*}
</latexmath>

<latexmath>
\begin{align*}
\frac{(R_F + R_{Fx}) \cdot C_F}{\omega^2 \cdot 2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} =  \frac{\left(2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F \right) \cdot (R_F + R_{Fx}) \cdot C_F}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}
\end{align*}
</latexmath>

<latexmath>
\begin{align*}
\frac{B^2+C^2}{\alpha} &= \frac{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}{(R_F + R_{Fx}) \cdot C_F} + \frac{\left(2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F \right) \cdot (R_F + R_{Fx}) \cdot C_F}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}
\end{align*}
</latexmath>

<!-- FIXME: copy here for the final version -->
Introducing the usual change of variables:

<latexmath>
\begin{align*}
\frac{B^2+C^2}{\alpha} &= \frac{2 \cdot R_{\text{iso}} \cdot k_F \cdot R_{FT} \cdot C_L \cdot C_F}{R_{FT} \cdot C_F} + \frac{\left(2 \cdot R_{\text{iso}} \cdot k_F \cdot R_{FT} \cdot C_L \cdot C_F \right) \cdot R_{FT} \cdot C_F}{4 \cdot R_{\text{iso}} \cdot k_F \cdot R_{FT} \cdot C_L \cdot C_F - R_{FT}^2 \cdot C_F^2}  \\
&= 2 \cdot R_{\text{iso}} \cdot k_F \cdot C_L + \frac{2 \cdot R_{\text{iso}} \cdot k_F \cdot R_{FT} \cdot C_L \cdot C_F}{4 \cdot R_{\text{iso}} \cdot k_F\cdot C_L - R_{FT} \cdot C_F}
\end{align*}
</latexmath>

Second term:

<latexmath>
\begin{align*}
B^2 - C^2 &= 1 - \left[ \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} \right]^2 \cdot \frac{4 \cdot R_{\text{iso}}^2 \cdot R_F^2 \cdot C_L^2 \cdot C_F^2}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}  \\
&= 1 - \frac{(R_F + R_{Fx})^2 \cdot C_F^2}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}%  \\
% &= \frac{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - 2 \cdot (R_F + R_{Fx})^2 \cdot C_F^2}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}
\end{align*}
</latexmath>

<latexmath>
\begin{align*}
% \alpha \cdot (B^2 - C^2) &= \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} \cdot \frac{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - 2 \cdot (R_F + R_{Fx})^2 \cdot C_F^2}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}
\alpha \cdot (B^2 - C^2) &= \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} \cdot \left[ 1 - \frac{(R_F + R_{Fx})^2 \cdot C_F^2}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2} \right]
\end{align*}
</latexmath>

<p></p>

<latexmath>
\begin{align*}
2 \cdot \omega \cdot B \cdot C &= (2) \cdot (B) \cdot (C \cdot \omega) = 2 \cdot (-1) \cdot \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}  \\
&= -2 \cdot \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}
\end{align*}
</latexmath>

<p></p>

<latexmath>
\begin{align*}
\alpha \cdot (B^2 - C^2) + 2 \cdot \omega \cdot B \cdot C &= \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} \cdot \left[ -1 - \frac{(R_F + R_{Fx})^2 \cdot C_F^2}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2} \right]  \\
&= \frac{(R_F + R_{Fx}) \cdot C_F}{2 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F} \cdot \frac{-4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}  \\
&= \frac{-2 \cdot (R_F + R_{Fx}) \cdot C_F}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2}
\end{align*}
</latexmath>

<p></p>

<latexmath>
\begin{align*}
\frac{\alpha \cdot (B^2 - C^2) + 2 \cdot \omega \cdot B \cdot C}{4 \cdot ( \alpha^2 + \omega^2 )} = \frac{-2 \cdot (R_F + R_{Fx}) \cdot C_F}{4 \cdot R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F - (R_F + R_{Fx})^2 \cdot C_F^2} \cdot \frac{R_{\text{iso}} \cdot R_F \cdot C_L \cdot C_F}{4}
\end{align*}
</latexmath>

Introducing the usual change of variables:

<latexmath>
\begin{align*}
\frac{\alpha \cdot (B^2 - C^2) + 2 \cdot \omega \cdot B \cdot C}{4 \cdot ( \alpha^2 + \omega^2 )} &= \frac{-2 \cdot R_{FT} \cdot C_F}{4 \cdot R_{\text{iso}} \cdot k_F \cdot R_{FT} \cdot C_L \cdot C_F - R_{FT}^2 \cdot C_F^2} \cdot \frac{R_{\text{iso}} \cdot k_F \cdot R_{FT} \cdot C_L \cdot C_F}{4}  \\
&= \frac{- \frac{1}{2} \cdot R_{FT} \cdot C_F \cdot R_{\text{iso}} \cdot k_F \cdot C_L}{4 \cdot R_{\text{iso}} \cdot k_F \cdot C_L - R_{FT} \cdot C_F}
\end{align*}
</latexmath>

Get the error term:

<latexmath>
\begin{align*}
E &= \frac{B^2+C^2}{4a} + \frac{a(B^2-C^2)+2\omega BC}{4\,(a^2+\omega^2)}  \\
&= 2 \cdot R_{\text{iso}} \cdot k_F \cdot C_L + \frac{2 \cdot R_{\text{iso}} \cdot k_F \cdot R_{FT} \cdot C_L \cdot C_F}{4 \cdot R_{\text{iso}} \cdot k_F \cdot C_L - R_{FT} \cdot C_F} + \frac{- \frac{1}{2} \cdot R_{FT} \cdot C_F \cdot R_{\text{iso}} \cdot k_F \cdot C_L}{4 \cdot R_{\text{iso}} \cdot k_F \cdot C_L - R_{FT} \cdot C_F}  \\
&= 2 \cdot R_{\text{iso}} \cdot k_F \cdot C_L + \frac{\frac{3}{2} \cdot R_{\text{iso}} \cdot k_F \cdot R_{FT} \cdot C_L \cdot C_F}{4 \cdot R_{\text{iso}} \cdot k_F \cdot C_L - R_{FT} \cdot C_F}  \\
&= \frac{8 \cdot R_{\text{iso}}^2 \cdot k_F^2 \cdot C_L^2 - 2 \cdot R_{FT} \cdot C_F \cdot R_{\text{iso}} \cdot k_F \cdot C_L + \frac{3}{2} \cdot R_{\text{iso}} \cdot k_F \cdot R_{FT} \cdot C_L \cdot C_F}{4 \cdot R_{\text{iso}} \cdot k_F\cdot C_L - R_{FT} \cdot C_F}  \\
&= \frac{8 \cdot R_{\text{iso}}^2 \cdot k_F^2 \cdot C_L^2 - \frac{1}{2} \cdot R_{FT} \cdot C_F \cdot R_{\text{iso}} \cdot k_F \cdot C_L }{4 \cdot R_{\text{iso}} \cdot k_F\cdot C_L - R_{FT} \cdot C_F}  \\
&= \frac{ R_{\text{iso}} \cdot k_F \cdot C_L \cdot \left[ 8 \cdot R_{\text{iso}} \cdot k_F \cdot C_L - \frac{1}{2} \cdot R_{FT} \cdot C_F  \right] }{4 \cdot R_{\text{iso}} \cdot k_F \cdot C_L - R_{FT} \cdot C_F}
\end{align*}
</latexmath>

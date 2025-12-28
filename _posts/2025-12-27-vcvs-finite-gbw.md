---
layout: post
title: VCVS with finite GBW.
permalink: /posts/vcvs-finite-gbw.html
last_modified_at: 2025-12-27
---

## Transfer function

### Full expression

![](/posts/vcvs-finite-gbw/schematic.svg)

Replace R1 and R3 by equivalent circuit: <latexinline>V_\text{TH} = V_\text{IN} \cdot \frac{...}{...}</latexinline>, <latexinline>R_\text{TH} = ...</latexinline>.

The voltage at point x, <latexinline>V_x</latexinline>, can be calculated using Millman theorem:

<latexmath>
\begin{multline*}
V_x = \frac{
    \frac{V_\text{TH}}{R_\text{TH}}+\frac{V^-}{\frac{1}{C \cdot s}}
    + \frac{V_\text{out}}{\frac{1}{C \cdot s}}
  }{
    \frac{1}{R_\text{TH}}
    + \frac{1}{\frac{1}{C \cdot s}}+\frac{1}{\frac{1}{C \cdot s}}
  }
= \frac{
    \frac{1}{R_\text{TH}} \cdot V_\text{TH}
    + C \cdot s \cdot V^-
    + C \cdot s \cdot V_\text{out}
  }{
    \frac{1}{R_\text{TH}}
    + 2 \cdot C \cdot s
  } 
\end{multline*}
</latexmath>

The V- voltage can be calculated in the same way:

<latexmath>
\begin{multline*}
V^- = \frac{
      \frac{V_x}{\frac{1}{C \cdot s}}
      + \frac{V_\text{out}}{R_2}
    }{
      \frac{1}{\frac{1}{C \cdot s}}
      + \frac{1}{R_2}
    }
= \frac{
    C \cdot s \cdot V_x
    + \frac{1}{R_2} \cdot V_\text{out}
  }{
    C \cdot s
    + \frac{1}{R_2}
  }
= \frac{
    R_2 \cdot C \cdot s \cdot V_x
    + V_\text{out}
  }{
    1 + R_2 \cdot C \cdot s
  } 
\end{multline*}
</latexmath>

Combining both equations:

<latexmath>
V^- = \frac{R_2 \cdot C \cdot s}{1 + R_2 \cdot C \cdot s} \cdot \left[
    \frac{
        \frac{1}{R_\text{TH}} \cdot V_\text{TH}
        + C \cdot s \cdot V^-
        + C \cdot s \cdot V_\text{out}
    }{
        \frac{1}{R_\text{TH}}
        + 2 \cdot C \cdot s
    }
  \right] + \frac{1}{1 + R_2 \cdot C \cdot s} \cdot V_\text{out}
</latexmath>

Multiplying both sides of the equation by <latexinline>\left[ 1 + R_2 \cdot C \cdot s \right] \cdot \left[ \frac{1}{R_\text{TH}} + 2 \cdot C \cdot s \right]</latexinline>:

<latexmath>
\left[ 1 + R_2 \cdot C \cdot s \right] \cdot \left[ \frac{1}{R_\text{TH}} + 2 \cdot C \cdot s \right] \cdot V^-
= R_2 \cdot C \cdot s \cdot \left[
    \frac{1}{R_\text{TH}} \cdot V_\text{TH}
    + C \cdot s \cdot V^-
    + C \cdot s \cdot V_\text{out}
  \right]
  + \left[ \frac{1}{R_\text{TH}} + 2 \cdot C \cdot s \right] \cdot V_\text{out}
</latexmath>

Multiplying by R_TH to outline the time constant units:

<latexmath>
\left[ 1 + R_2 \cdot C \cdot s \right] \cdot \left[ 1 + 2 \cdot R_\text{TH} \cdot C \cdot s \right] \cdot V^-
= R_2 \cdot C \cdot s \cdot \left[
    V_\text{TH}
    + R_\text{TH} \cdot C \cdot s \cdot V^-
    + R_\text{TH} \cdot C \cdot s \cdot V_\text{out}
  \right]
  + \left[ 1 + 2 \cdot R_\text{TH} \cdot C \cdot s \right] \cdot V_\text{out}
</latexmath>

Developping and regrouping terms according to their voltage:

<!-- FIXME: move globally -->
<style>
  .math-reduced .MathJax {
    font-size: 1.0em !important;
  }
</style>
<latexmath class="math-reduced">
    \begin{align*}
        &\left[
        1
        + \left(
            2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
            \right) \cdot s
        + 2 \cdot R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2
        \right] \cdot V^-  \\
        & \quad =
        R_2 \cdot C \cdot s \cdot V_\text{TH}
        + R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2 \cdot V^-  \\
        & \qquad + \left[
            1 + 2 \cdot R_\text{TH} \cdot C \cdot s + R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2
        \right] \cdot V_\text{out}
    \end{align*}
</latexmath>

Regrouping V- on the left side (the change is put in bold for clarity):
<latexmath class="math-reduced">
    \begin{align*}
        &\left[
        1
        + \left(
            2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
            \right) \cdot s
        + \pmb{1} \cdot R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2
        \right] \cdot V^-  \\
        & \quad =
        R_2 \cdot C \cdot s \cdot V_\text{TH}
        + \left[
            1 + 2 \cdot R_\text{TH} \cdot C \cdot s + R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2
        \right] \cdot V_\text{out}
    \end{align*}
</latexmath>

Plugging op-amp gain (don’t forget the sign!):

<latexmath class="math-reduced">
    \begin{align*}
        & - \left[
        1
        + \left(
            2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
            \right) \cdot s
        + R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2
        \right] \cdot \frac{V_\text{out}}{\omega_\text{BW} \cdot s}  \\
        & \quad =
        R_2 \cdot C \cdot s \cdot V_\text{TH}
        + \left[
            1 + 2 \cdot R_\text{TH} \cdot C \cdot s + R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2
        \right] \cdot V_\text{out}
    \end{align*}
</latexmath>

Outlining the polynomial of s:

<latexmath class="math-reduced">
    \begin{align*}
        & - \left[
        \frac{1}{\omega_\text{BW}} \cdot s
        + \frac{
            2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
          }{\omega_\text{BW}} \cdot s^2
        + \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW}} \cdot s^3
        \right] \cdot V_\text{out}  \\
        & \qquad =
        R_2 \cdot C \cdot s \cdot V_\text{TH}
        + \left[
            1 + 2 \cdot R_\text{TH} \cdot C \cdot s + R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2
        \right] \cdot V_\text{out}
    \end{align*}
</latexmath>

Putting all the V_out on the left:

<latexmath class="math-reduced">
    \begin{align*}
        & - \left[
        1
        + \left( \frac{1}{\omega_\text{BW}} + 2 \cdot R_\text{TH} \cdot C \right) \cdot s
        +  \left(
                \frac{
                    2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
                }{\omega_\text{BW}}
                + R_\text{TH} \cdot R_2 \cdot C^2
            \right) \cdot s^2
        + \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW}} \cdot s^3
        \right] \cdot V_\text{out}  \\
        & \qquad =
        R_2 \cdot C \cdot s \cdot V_\text{TH}
    \end{align*}
</latexmath>

From which the transfer function can be calculated:

<latexmath class="math-reduced">
    \begin{align*}
        V_\text{out} = \frac{
            - R_2 \cdot C \cdot s
        }{
            1
            + \left( \frac{1}{\omega_\text{BW}} + 2 \cdot R_\text{TH} \cdot C \right) \cdot s
            +  \left(
                    \frac{
                        2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
                    }{\omega_\text{BW}}
                    + R_\text{TH} \cdot R_2 \cdot C^2
                \right) \cdot s^2
            + \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW}} \cdot s^3
        } \cdot V_\text{TH}
    \end{align*}
</latexmath>

### Test expression with infinite GBW

When GBW infinite, the following expression reduces to:

<latexmath class="math-reduced">
    \begin{align*}
        V_\text{out} = \frac{
            - R_2 \cdot C \cdot s
        }{
            1
            + 2 \cdot R_\text{TH} \cdot C \cdot s
            + R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2
        } \cdot V_\text{TH}
    \end{align*}
</latexmath>

For an ideal VCVS filter with infinite GBW opamps[^1]:

[^1]: https://electronics.stackexchange.com/questions/735869/cannot-find-the-derivation-for-gain-and-q-in-a-mfb-bandpass-filter-with-fixed-ga

<latexmath class="math-reduced">
    \begin{align*}
        V_\text{out} = \frac{
            \frac{A^{'}}{Q \cdot \omega_0} s
        }{
            1
            + \frac{1}{Q \cdot \omega_0} \cdot s
            + \frac{1}{\omega_0^2} \cdot s^2
        } \cdot V_\text{TH}
    \end{align*}
</latexmath>

Note the gain is called A^' and not A because it does not include the V_TH/V_IN.

<latexmath class="math-reduced">
    \begin{align*}
        V_\text{out} = \frac{
            \frac{A^{'}}{Q \cdot \omega_0} s
        }{
            1
            + \frac{1}{Q \cdot \omega_0} \cdot s
            + \frac{1}{\omega_0^2} \cdot s^2
        } \cdot V_\text{TH}
        = \frac{
            - R_2 \cdot C \cdot s
        }{
            1
            + 2 \cdot R_\text{TH} \cdot C \cdot s
            + R_\text{TH} \cdot R_2 \cdot C^2 \cdot s^2
        } \cdot V_\text{TH}
    \end{align*}
</latexmath>

<latexmath class="math-reduced">
    \begin{align*}
        \cases{
            \frac{A^{'}}{Q \cdot \omega_0} = - R_2 \cdot C  \\
            \frac{1}{Q \cdot \omega_0} = 2 \cdot R_\text{TH} \cdot C  \\
            \frac{1}{\omega_0^2} = R_\text{TH} \cdot R_2 \cdot C^2
        }
    \end{align*}
</latexmath>

<latexmath class="math-reduced">
    \begin{align*}
        \cases{
            A^{'} = \frac{- R_2}{2 \cdot R_\text{TH}};  \qquad A = \frac{R_3}{R_1+R_3} \cdot \frac{R_1+R_3}{R_1\cdot R_3} \cdot \frac{R_2}{2} = \frac{-R_2}{R_1}; \qquad \text{OK}  \\
            Q = ... = \pi \cdot f_0 \cdot R_C \cdot C; \qquad \text{OK}  \\
            \omega_0 = ...; \qquad f_0 = ...; \qquad \text{OK}
        }
    \end{align*}
</latexmath>

Consistent with the equations for infinite GBW[^2].

[^2]: https://www.changpuak.ch/electronics/downloads/sloa088.pdf

### Parameters for finite GBW

Since this VCVS has another pole due to the finite GBW of the opamps, the transfer function is as follows:

<latexmath class="math-reduced">
    \begin{align*}
        V_\text{out} = \frac{
            \frac{A^{'}}{Q \cdot \omega_0} s
        }{
            \left[
                1
                + \frac{1}{Q \cdot \omega_0} \cdot s
                + \frac{1}{\omega_0^2} \cdot s^2
            \right] \cdot
            \left[
                1 + \frac{1}{\omega_p} \cdot s
            \right]
        } \cdot V_\text{TH}
    \end{align*}
</latexmath>

Assuming the pole is far enough from the center frequency, its effect can be neglected, and the gain has still the same value:

<latexmath>
\frac{A^{'}}{Q \cdot \omega_0} = - R_2 \cdot C; \qquad A^{'} = \frac{- R_2}{2 \cdot R_\text{TH}}
</latexmath>

However, the denominator needs to be factorized before the other parameters can be expressed.

## Factorisation

### Seeked factorisation

Coefficients of denominator:

<latexmath>
D(s) = 1 + b_1 \cdot s + b_2 \cdot s^2 + b_3 \cdot s^3
</latexmath>

Seek factorisation as such, using time constants instead of angular frequencies to make calculations easier:

<latexmath>
\begin{align*}
D(s) &= \left( 1 + \frac{\tau_0}{Q} \cdot s + \tau_0^2 \cdot s^2  \right) \cdot \left( 1 + \tau_p \cdot s \right)  \\
D(s) &= 1 + \left( \frac{\tau_0}{Q} + \tau_p \right) \cdot s + \left( \tau_0^2 + \frac{\tau_0 \cdot \tau_p}{Q} \right) \cdot s^2 + \tau_0^2 \cdot \tau_p \cdot s^3
\end{align*}
</latexmath>

To allow solving, hypothesis <latexinline>\tau_0^2 \gg \frac{\tau_0 \cdot \tau_p}{Q}</latexinline>:

<latexmath class="math-reduced">
    \cases{
        \tau_0^2 \cdot \tau_p = b_3  \\
        \tau_0^2 = b_2  \\
        \frac{\tau_0}{Q} + \tau_p = b_1
    }
</latexmath>

<latexmath class="math-reduced">
    \cases{
        \tau_p = \frac{b_3}{b_2}  \\
        \tau_0^2 = b_2  \\
        \frac{\tau_0}{Q} = b_1 - \frac{b_3}{b_2}
    }
</latexmath>

Anticipating a simplification to come, these equations can be rewritten as follows:

<latexmath class="math-reduced">
    \cases{
        \tau_p = \frac{b_3}{\tau_0^2}  \\
        \tau_0^2 = b_2  \\
        \frac{\tau_0}{Q} = b_1 - \frac{b_3}{\tau_0^2}
    }
</latexmath>

### Applying to components values

Plugging components values:

<latexmath class="math-reduced">
    D(s) = 1
            + \left( 2 \cdot R_\text{TH} \cdot C + \frac{1}{\omega_\text{BW}} \right) \cdot s
            +  \left(
                    R_\text{TH} \cdot R_2 \cdot C^2
                    + \frac{
                        2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
                    }{\omega_\text{BW}}
                \right) \cdot s^2
            + \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW}} \cdot s^3
</latexmath>

<p></p>

<latexmath class="math-reduced">
    \cases{
        \tau_p = \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW} \cdot \tau_0^2}  \\
        \tau_0^2 = R_\text{TH} \cdot R_2 \cdot C^2
                    + \frac{
                        2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
                    }{\omega_\text{BW}}  \\
        \frac{\tau_0}{Q} = 2 \cdot R_\text{TH} \cdot C + \frac{1}{\omega_\text{BW}} - \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW} \cdot \tau_0^2}
    }
</latexmath>

<p></p>

<latexmath class="math-reduced">
\frac{1}{\omega_\text{BW}} - \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW} \cdot \tau_0^2} =
\frac{\tau_0^2 - R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW} \cdot \tau_0^2} =
\frac{2 \cdot R_\text{TH} \cdot C + R_2 \cdot C}{\omega_\text{BW}^2 \cdot \tau_0^2}
</latexmath>

Leading to:

<latexmath class="math-reduced">
    \cases{
        \tau_p = \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW} \cdot \tau_0^2}  \\
        \tau_0^2 = R_\text{TH} \cdot R_2 \cdot C^2
                    + \frac{
                        2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
                    }{\omega_\text{BW}}  \\
        \frac{\tau_0}{Q} = 2 \cdot R_\text{TH} \cdot C + \frac{2 \cdot R_\text{TH} \cdot C + R_2 \cdot C}{\omega_\text{BW}^2 \cdot \tau_0^2}
    }
</latexmath>

## Synthesis formulas

First-order approximation:

![](/posts/vcvs-finite-gbw/eqn15.png)

Next, second equation becomes:

![](/posts/vcvs-finite-gbw/eqn16.png)

And first equation:

![](/posts/vcvs-finite-gbw/eqn17.png)

First-order approximation:

![](/posts/vcvs-finite-gbw/eqn18.png)

Filtering only the first-order terms:

![](/posts/vcvs-finite-gbw/eqn19.png)

Gathering all pieces:

![](/posts/vcvs-finite-gbw/eqn20.png)

## Conditions for realisability

<!-- TODO: add resistor to equations. -->

![](/posts/vcvs-finite-gbw/eqn21.png)

## Hypothesis verification

Remind the hypothesis:

![](/posts/vcvs-finite-gbw/eqn22.png)

Equivalent to:

![](/posts/vcvs-finite-gbw/eqn23.png)

It is difficult to have an exact expression for τ_p, but a bound allows to check the hypothesis:

![](/posts/vcvs-finite-gbw/eqn24.png)

So, a sufficient condition is:

![](/posts/vcvs-finite-gbw/eqn25.png)

This equation is always satisfied when Q is high enough (the precise value calculation is left as an exercise for the reader) and realisable.

## Conclusion

No time to conclude, please find instead a beautiful cat.

<img src="https://upload.wikimedia.org/wikipedia/commons/4/4c/Blackcat-Lilith.jpg" alt="Lilith black cat."/>


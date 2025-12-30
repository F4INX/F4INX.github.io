---
layout: post
title: VCVS with finite GBW.
permalink: /posts/vcvs-finite-gbw.html
last_modified_at: 2025-12-28
---

<!-- FIXME: move globally -->
<style>
  .vcvs-finite-gbw-fixes .MathJax {
    font-size: 1.0em !important;
  }
</style>
<div class="vcvs-finite-gbw-fixes" markdown="1">

<p class="begin-note">Many thanks to Christophe Basso to have showed me the factorisation technique which is the key of this work.</p>

<p class="begin-note">TODO: add some comparison with the existing stuff: lack of compensation equations for the simple case, compensation scheme from TI efficient but with additionnal components.</p>

## Transfer function

### Full expression

![](/posts/vcvs-finite-gbw/schematic.svg)

Replace R1 and R3 by equivalent circuit: <latexinline>V_\text{TH} = V_\text{IN} \cdot \frac{R_3}{R_1 + R_3}</latexinline>, <latexinline>R_\text{TH} = \frac{R_1 \cdot R_3}{R_1 + R_3}</latexinline>.

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

<latexmath>
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
<latexmath>
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

<latexmath>
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

<latexmath>
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

<latexmath>
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

<latexmath>
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

<latexmath>
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

<latexmath>
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

Note this gain is called <latexinline>A^{'}</latexinline> and not <latexinline>A</latexinline> because it does not include the <latexinline>\frac{V_\text{TH}}{V_\text{in}}</latexinline>.

<latexmath>
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

<latexmath>
    \begin{align*}
        \cases{
            \frac{A^{'}}{Q \cdot \omega_0} = - R_2 \cdot C  \\
            \frac{1}{Q \cdot \omega_0} = 2 \cdot R_\text{TH} \cdot C  \\
            \frac{1}{\omega_0^2} = R_\text{TH} \cdot R_2 \cdot C^2
        }
    \end{align*}
</latexmath>

*The ... are equations that will be filled in a future release of this page.*

<latexmath>
    \left\{
        \begin{align*}
            & A^{'} = \frac{- R_2}{2 \cdot R_\text{TH}} \qquad A = \frac{R_3}{R_1+R_3} \cdot \frac{R_1+R_3}{R_1\cdot R_3} \cdot \frac{R_2}{2} = \frac{-R_2}{R_1} && \text{OK}  \\
            & Q = \frac{1}{2 \cdot R_\text{TH} \cdot C\cdot \omega_0} = ... = \pi \cdot f_0 \cdot R_C \cdot C && \text{OK}  \\
            & \omega_0 = ... \qquad f_0 = ... = \frac{1}{2 \cdot \pi \cdot C} \cdot \sqrt{\frac{R_1 + R_3}{R_1 \cdot R_2 \cdot R_3}} && \text{OK}
        \end{align*}
    \right.
</latexmath>

Consistent with the equations for infinite GBW[^2].

[^2]: https://www.changpuak.ch/electronics/downloads/sloa088.pdf

### Parameters for finite GBW

Since this VCVS has another pole due to the finite GBW of the opamps, the transfer function is as follows:

<latexmath>
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

<latexmath>
    \cases{
        \tau_0^2 \cdot \tau_p = b_3  \\
        \tau_0^2 = b_2  \\
        \frac{\tau_0}{Q} + \tau_p = b_1
    }
</latexmath>

<latexmath>
    \cases{
        \tau_p = \frac{b_3}{b_2}  \\
        \tau_0^2 = b_2  \\
        \frac{\tau_0}{Q} = b_1 - \frac{b_3}{b_2}
    }
</latexmath>

Anticipating a simplification to come, these equations can be rewritten as follows:

<latexmath>
    \cases{
        \tau_p = \frac{b_3}{\tau_0^2}  \\
        \tau_0^2 = b_2  \\
        \frac{\tau_0}{Q} = b_1 - \frac{b_3}{\tau_0^2}
    }
</latexmath>

### Applying to components values

Plugging components values:

<latexmath>
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

<latexmath>
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

<latexmath>
\frac{1}{\omega_\text{BW}} - \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW} \cdot \tau_0^2} =
\frac{\tau_0^2 - R_\text{TH} \cdot R_2 \cdot C^2}{\omega_\text{BW} \cdot \tau_0^2} =
\frac{2 \cdot R_\text{TH} \cdot C + R_2 \cdot C}{\omega_\text{BW}^2 \cdot \tau_0^2}
</latexmath>

Leading to:

<latexmath>
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

<!-- FIXME: test this hypothesis. -->
<latexmath>
    \cases{
        \tau_0^2 = R_\text{TH} \cdot R_2 \cdot C^2
                    + \frac{
                        2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
                    }{\omega_\text{BW}}  \\
        \frac{\tau_0}{Q} \approx 2 \cdot R_\text{TH} \cdot C
    }
</latexmath>

Next, second equation becomes:

<latexmath>
     R_\text{TH} \cdot C \approx \frac{\tau_0}{2 \cdot Q}
</latexmath>

And first equation:

<latexmath>
    \begin{gather*}
        R_\text{TH} \cdot R_2 \cdot C^2
        = \tau_0^2
            - \frac{
                2 \cdot R_\text{TH} \cdot C + R_2 \cdot C
            }{\omega_\text{BW}}
        = \tau_0^2
            - \frac{
                2 \cdot R_\text{TH} \cdot C
            }{\omega_\text{BW}}
            - \frac{
                R_2 \cdot C
            }{\omega_\text{BW}}  \\
        \frac{\tau_0}{2 \cdot Q} \cdot R_2 \cdot C
        = \tau_0^2
            - \frac{2}{\omega_\text{BW}} \cdot \frac{\tau_0}{2 \cdot Q}
            - \frac{
                R_2 \cdot C
            }{\omega_\text{BW}}  \\
        \left[ \frac{\tau_0}{2 \cdot Q} + \frac{1}{\omega_\text{BW}} \right] \cdot R_2 \cdot C = \tau_0 \cdot \left[ 1 - \frac{1}{Q \cdot \omega_0 \cdot \tau_0} \right]
    \end{gather*}
</latexmath>

Rewriting to highlight the infinite GBW value and the correction term:

<latexmath>
    \begin{gather*}
        \frac{\tau_0}{2 \cdot Q} \cdot \left[ 1 + \frac{2 \cdot Q}{\omega_\text{BW} \cdot \tau_0} \right] \cdot R_2 \cdot C = \tau_0 \cdot \left[ 1 - \frac{1}{Q \cdot \omega_0 \cdot \tau_0} \right]  \\
        R_2 \cdot C = \left. 2 \cdot Q \cdot \tau_0 \cdot \left[ 1 - \frac{1}{Q \cdot \omega_0 \cdot \tau_0} \right] \middle/ \left[ 1 + \frac{2 \cdot Q}{\omega_\text{BW} \cdot \tau_0} \right]\right.
    \end{gather*}
</latexmath>

A previous version of this article presented a further first order approximation of this equation using the hypothesis <latexinline>\frac{2 \cdot Q}{\omega_\text{BW} \cdot \tau_0} \ll 1</latexinline>. This hypothesis is **inaccurate** in though cases, like the example to come using an LM324, and bring no additional value. Sorry for the inconvenience.

Gathering all pieces:

<latexmath>
    \cases{
        R_2 \cdot C = \left. 2 \cdot Q \cdot \tau_0 \cdot \left[ 1 - \frac{1}{Q \cdot \omega_0 \cdot \tau_0} \right] \middle/ \left[ 1 + \frac{2 \cdot Q}{\omega_\text{BW} \cdot \tau_0} \right]\right.  \\
        R_\text{TH} \cdot C = \frac{\tau_0}{2 \cdot Q}
    }
</latexmath>

<p></p>

<latexmath>
    \cases{
        R_2 = \left. \frac{2 \cdot Q \cdot \tau_0}{C} \cdot \left[ 1 - \frac{1}{Q \cdot \omega_0 \cdot \tau_0} \right] \middle/ \left[ 1 + \frac{2 \cdot Q}{\omega_\text{BW} \cdot \tau_0} \right]\right.  \\
        R_\text{TH} = \frac{\tau_0}{2 \cdot Q \cdot C}
    }
</latexmath>

## Conditions for realisability

The previously done hypothesis allows to calculate the needed values of the components. However, they are not necessarily realisable, for instance when the equations give negative values. The conditions for realisability are as follows:

<latexmath>
    \cases{
        R_2 = \frac{2 \cdot Q \cdot \tau_0}{C} \cdot \left[ 1 - \frac{1 + 2 \cdot Q^2}{\omega_\text{BW} \cdot \tau_0} \right]\geq 0 \\
        R_\text{TH} = \frac{\tau_0}{2 \cdot Q \cdot C} \geq 0
    }
</latexmath>

Leading to this condition:

<latexmath>
    \begin{gather*}
        1 - \frac{1 + 2 \cdot Q^2}{\omega_\text{BW} \cdot \tau_0} \geq 0  \\
        \Leftrightarrow \frac{1 + 2 \cdot Q^2}{\omega_\text{BW} \cdot \tau_0} \leq 1  \\
        \Leftrightarrow \omega_\text{BW} \geq \frac{1 + 2 \cdot Q^2}{\tau_0}
    \end{gather*}
</latexmath>

Which can be interpreted as the gain-bandwidth of the operational amplifier must be higher than the filter frequency multiplied by a factor depending of the quality factor Q.

## Hypothesis verification

Remind the hypothesis:

<latexmath>
\tau_0^2 \gg \frac{\tau_0 \cdot \tau_p}{Q}
</latexmath>

Equivalent to:

<latexmath>
\frac{\tau_p}{Q \cdot \tau_0} \ll 1
</latexmath>

It is difficult to have an exact expression for τ_p, but a bound allows to check the hypothesis:

<latexmath>
\tau_p
= \frac{R_\text{TH} \cdot R_2 \cdot C^2}{\tau_0^2 \cdot \omega_\text{BW}}
= \frac{\tau_0^2 - \frac{2 \cdot R_\text{TH} \cdot C + R_2 \cdot C}{\omega_\text{BW}}}{\tau_0^2 \cdot \omega_\text{BW}}
< \frac{\tau_0^2}{\tau_0^2 \cdot \omega_\text{BW}}
= \frac{1}{\omega_\text{BW}}
</latexmath>

<p></p>

<latexmath>
\frac{\tau_p}{Q \cdot \tau_0} < \frac{1}{Q \cdot \omega_\text{BW} \cdot \tau_0}
</latexmath>

So, a sufficient condition to satisfy the hypothesis is:

<latexmath>
\frac{1}{Q \cdot \omega_\text{BW} \cdot \tau_0} \ll 1
</latexmath>

A sufficient condition for this is:

* the calculated resistance values are realisable

* AND Q is high enough (the precise value calculation is left as an exercise for the reader).

Note that there are some values where 1/ the filter is still realisable and 2/ the hypothesis made at the beginning is not accurate anymore. The determination of these values is left as an exercie for the reader.

## Conclusion

No time to conclude, please find instead a beautiful cat.

<img src="https://upload.wikimedia.org/wikipedia/commons/4/4c/Blackcat-Lilith.jpg" alt="Lilith black cat."/>

</div>  <!-- End of <div class="vcvs-finite-gbw-fixes"> -->

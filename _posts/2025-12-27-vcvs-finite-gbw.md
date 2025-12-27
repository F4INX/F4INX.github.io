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

The X point voltage can be calculated: ...

The V- voltage can be calculated: ...

...

Plugging op-amp gain (don’t forget the sign!):

...

![](/posts/vcvs-finite-gbw/eqn01.png)

Rational transfer function:

...

Cleanup:

![](/posts/vcvs-finite-gbw/eqn02.png)

### Test expression with GBW infinite

When GBW infinite, the following expression reduces to:

![](/posts/vcvs-finite-gbw/eqn03.png)

...

### Parameters for GBW finite

Since this VCVS has another pole due to the finite GBW of the opamps, the transfer function is as follows:

![](/posts/vcvs-finite-gbw/eqn04.png)

Assuming the pole is far enough from the center frequency, its effect can be neglected, and the gain has still the same value.

![](/posts/vcvs-finite-gbw/eqn05.png)

However, the denominator needs to be factorized before the other parameters can be expressed.

## Factorisation

### Seeked factorisation

Coefficients of denominator:

![](/posts/vcvs-finite-gbw/eqn06.png)

Seek factorisation as such:

![](/posts/vcvs-finite-gbw/eqn07.png)

<!-- FIXME: put this in CSS. -->
To allow solving, hypothesis <img style="display:unset;vertical-align:middle;" src="/posts/vcvs-finite-gbw/eqn08.png"/>:

![](/posts/vcvs-finite-gbw/eqn09.png)

### Applying to components values

Plugging components values:

![](/posts/vcvs-finite-gbw/eqn10.png)

![](/posts/vcvs-finite-gbw/eqn11.png)

![](/posts/vcvs-finite-gbw/eqn12.png)

Leading to:

![](/posts/vcvs-finite-gbw/eqn13.png)

The denominator of first and last equation can be simplified using the expression of tau_0, leading to:

![](/posts/vcvs-finite-gbw/eqn14.png)

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


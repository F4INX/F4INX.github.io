---
layout: post
title: LC ladder impedance matching.
permalink: /posts/LC-ladder-impedance-matching.html
last_modified_at: 2023-06-25 21-17
---

<p class="begin-note">This blog page is an English translation and adaptation of a part of my PhD thesis. Numbers in brackets refers to the original bibliography, they will be replaced in a future revision.</p>

Impedance matching is performed by LC ladder networks. This method allows to synthesize low impedances (around 5&#8239;Ω) on the same PCB than the standard 50&#8239;Ω output (no need for a second PCB with high permittivity). Moreover, this method is more compact than quarter-wave transformer.

Exact value calculation was performed by numerical optimization. Manual calculation would be too difficule because the output impedance of the transistor is not a pure resistance[^1]. However, numerical optimization needs to know the number of components of the ladder, because the ADS optimizer is not able to add components when needed, but is only able to determine their value. Moreover, an initial estimate of the values of the components of the LC ladder is useful for the optimizer to converge quicker towards the solution. Calculation method is the one of [84], adapted for the needs of the PhD thesis.

Inductors and capacitors are assumed ideal and lossless, as well as the microstrip junctions. The effets of the polarization networks of the transistors are also ignored. Such effects are absolutely not negligeable, but will be easily corrected by the numerical optimizer in the final phase of the design.

A simple empirical method is commonly used [32], but it doesn't allows a priori calculation of the order and of the mismatch of the matching network.

In [116] and [29], tables of [84] are used to calculate a low-pass matching network of Chebychev type. Unfortunately these tables does not provide values for very broadband impedance matching network (1:6 ratio for the amplifier module of the PhD thesis).

For these reasons this page describes in detail the calculation of such impedance matching networks. The calculation method is the one of [84], adapted for the needs of the PhD thesis.

As usual,  &&f&& is the usual frequency in &&s^-1&& and &&\omega&& the angular pulsation in &&rad \cdot s^-1&&. Calculations will use mainly &&\omega&&.

In a first time, the matching network is calculated for the center frequency &&\omega_m=1&& and source impedance &&R_S=1&&. This normalization is not mandatory, but allows to compare intermediate results with those of [84] to test the good operation of the Python program which was written during the PhD thesis.

The reflexion coefficient of a LC ladder (output) matching network of type Chebychev, seen from the source, is[^2]:

<asciimath>
|\Gamma|^2 = (\epsilon^2\cdotT_n^2((\omega^2-\omega_0^2)/(\Delta\omega^2)))/(1+\epsilon^2\cdotT_n^2((\omega^2-\omega_0^2)/(\Delta\omega^2)))
</asciimath>

with &&\omega_0=sqrt(\omega_a+\omega_b)&&, &&\omega_a&& the beginning of the passband, and &&\omega_b&& the end of the passband.

Next figure shows the reflection coefficient seen from the source of an example of an (output) LC matching network going from 5&#8239;Ω towards 50&#8239;Ω from 1 to 2,5&#8239;GHz. These values are approximately those of the first wideband amplifier of the PhD thesis.

{% comment %}
FIXME: Translate French titles, add alt text.
{% endcomment %}
<figure>
  <img class="dark-mode-invert" src="{{ '/posts/LC-ladder-impedance-matching/LC-ladder-gamma-2.svg' | relative_url }}">
  <figcaption>Fig.&#8239;1. Example of reflection coefficient seen from the source of an LC matching network. See text for parameters.</figcaption>
</figure>

In previous expression, &&\epsilon&& is chosen such as:

<asciimath>
|\Gamma(f=0)|^2=((Z_2-Z_1)/(Z_2+Z_1))^2
</asciimath>

This last condition is needed because LC ladders have no effect in DC. So, the transfert function is entirely determined by the order and the &&Z_2/Z_1&& ratio.

In the passband, maximum reflection coefficient and maximum insertion losses are respectively:

<asciimath>
|\Gamma_max|^2=(\epsilon^2)/(1+\epsilon^2)
</asciimath>
<asciimath>
|S_(21,min)|^2=1/(1+\epsilon^2)
</asciimath>

{% comment %}
Needs <asciimath></asciimath> tags instead of && &&. Not sure why.
{% endcomment %}
The first step of the calculation is to determine the first n such as <asciimath>|\Gamma_max|^2</asciimath> is less than the requirements. This calcul is done numerically, by testing all the integers n from 1 until this requirement is met.

This n is half the number of elements of the final network [84].

Next, variable change p = j · ω is performed. This variable change enables to simplify greatly the calculations to come. Then, the square of the magnitude of the reflection coefficient is factored as such:

<asciimath>
|\Gamma(p)|^2 = (a(p) \cdot a(-p)) / (b(p) \cdot b(-p))
</asciimath>

with a and b two polynomials whose roots have negative real parts[^3].

With this factorization, reflection coefficient (and not only his squared norm) can be calculted as such:

<asciimath>
\Gamma(p) = (a(p)) / (b(p))
</asciimath>

At the beginning of our work on the subject, factorization was performed numerically. This method was thereafter discarded due to numerical instability problems for high orders. This is why a semi-analytic method was taken, inspired by [47, 84]. Roots of the numerator and of the denominator are calculated analytically. Next, factorized polynomianls are calculated by taken only roots with negative real parts.

The calculation, more long than complex, won't be detailed. The roots of the numerator and of the denominator are given by the following formulas:

{% comment %}
FIXME: Math style
{% endcomment %}
<asciimath>
  {: ( +-j sqrt(Delta omega^2 \cdot cos((pi)/(2 \cdot n) \cdot (1 + 2 \cdot k))) , k in [1, n] ),
     ( +-j sqrt(Delta omega^2 \cdot cos(1/n \cdot arccos(j/epsilon))) ,            k in [1, 2 \cdot n] ) :}
</asciimath>

The first equation give directly the set of needed roots, since the numerator has double imaginary roots. However, negative real part roots need to be selected from all the roots given by second equation. This point is easily done numerically.

{% comment %}
FIXME: Translate French titles, add alt text.
{% endcomment %}
<figure>
  <img class="dark-mode-invert" src="{{ '/posts/LC-ladder-impedance-matching/LC-ladder-num.svg' | relative_url }}">
  <figcaption>Fig.&#8239;2. Roots of the numerator in the example. The roots of the numerator are double and purely imaginary.</figcaption>
</figure>

{% comment %}
FIXME: Translate French titles, add alt text.
{% endcomment %}
<figure>
  <img class="dark-mode-invert" src="{{ '/posts/LC-ladder-impedance-matching/LC-ladder-denum.svg' | relative_url }}">
  <figcaption>Fig.&#8239;3. Roots of the denominator in the example. The roots of interest are marked in blue, while the ones in red are ignored.</figcaption>
</figure>

A polynomial is defined by the set of its roots, but up to a multiplicative factor. The next step is to determine this multiplicative factor. Details of the calculation won't be given here, but only the result:

<asciimath>
{: ( a = a_1/(a_1(0)) \cdot abs(epsilon \cdot cos(n \cdot arccos(-omega_0^2/(Delta omega^2))))        ),
   ( b = b_1/(b_1(0)) \cdot sqrt(1 + (epsilon \cdot cos(n \cdot arccos(-omega_0^2/(Delta omega^2))))) ) :}
</asciimath>

with &&a_1&& and &&b_1&& the polynomials initially determined.

Next, the input impedance, normalized[^4] with respect to Z1, is calculated as follows:

<asciimath>
Z(p) = (b(p) + a(p))/(b(p) - a(p))
</asciimath>

This impedance is then expanded into a continued fraction through successive divisions:

<asciimath>
Z(p) = g_1 \cdot p + 1 / (g_2 \cdot p + 1/ (g_3 \cdot p + ... + 1 / (g_m \cdot p + g_(m+1))))
</asciimath>

This expression immediately leads to an LC network. The odd gm values are the normalized values of the inductances, while the even gm values are the normalized values of the capacitances. This denormalization is performed according to the following equations[^5]:

<asciimath>
{: ( L = g / (2 pi f_0) \cdot Z_1 ),
   ( C = g / (2 pi f_0) \cdot 1 / Z_1 ) :}
</asciimath>

The last &&g_m&& is the load resistance, which is also normalized. Its value has been known for a long time, but it can be interesting to recalculate it to verify that there is no significant error due to numerical inaccuracies.

[^1]: It is not even a pure impedance. See the blog pages to come!

[^2]: In [84], &&\Delta\omega^2&& is named A.

[^3]: Such polynomials are called Hurwitz polynomials. The reasons why a and b must satisfy this condition go beyond the scope of this thesis. The reader is encouraged to refer to a book on network synthesis [12, 56, 73].

[^4]: This point has been forgotten to be mentioned in the PhD thesis pdf. Sorry.

[^5]: There is a typo in these formulas in the PhD thesis pdf. Sorry.

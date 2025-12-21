---
layout: post
title: LC ladder impedance matching.
permalink: /posts/LC-ladder-impedance-matching.html
last_modified_at: 2025-11-09
---

<p class="begin-note">2025-11-09: Fix roots calculation and change of variables.</p>

<p class="begin-note">2025-10-26: Fix some errors in formulas, add some details about calculations.</p>

<p class="begin-note">2023-06-25: First version.</p>

<p class="begin-note">This blog page is an English translation and adaptation of a part of my PhD thesis. Numbers in brackets refers to the original bibliography, they will be replaced in a future revision.</p>

Impedance matching is performed by LC ladder networks. This method allows to synthesize low impedances (around 5&#8239;Ω) on the same PCB than the standard 50&#8239;Ω output (no need for a second PCB with high permittivity). Moreover, this method is more compact than quarter-wave transformer.

Exact value calculation was performed by numerical optimization. Manual calculation would be too difficule because the output impedance of the transistor is not a pure resistance[^1]. However, numerical optimization needs to know the number of components of the ladder, because the ADS optimizer is not able to add components when needed, but is only able to determine their value. Moreover, an initial estimate of the values of the components of the LC ladder is useful for the optimizer to converge quicker towards the solution. Calculation method is the one of [^ref84], adapted for the needs of the PhD thesis.

Inductors and capacitors are assumed ideal and lossless, as well as the microstrip junctions. The effets of the polarization networks of the transistors are also ignored. Such effects are absolutely not negligeable, but will be easily corrected by the numerical optimizer in the final phase of the design.

A simple empirical method is commonly used [^ref32], but it doesn't allows a priori calculation of the order and of the mismatch of the matching network.

In [^ref116] and [^ref29], tables of [^ref84] are used to calculate a low-pass matching network of Chebychev type. Unfortunately these tables does not provide values for very broadband impedance matching network (1:6 ratio for the amplifier module of the PhD thesis).

For these reasons this page describes in detail the calculation of such impedance matching networks. The calculation method is the one of [^ref84], adapted for the needs of the PhD thesis.

As usual, <asciimath>f</asciimath> is the usual frequency in <asciimath>s^-1</asciimath> and <asciimath>\omega</asciimath> the angular pulsation in <asciimath>rad \cdot s^-1</asciimath>. Calculations will use mainly <asciimath>\omega</asciimath>.

In a first time, the matching network is calculated for the center frequency <asciimath>\omega_0=1</asciimath> and source [^ref84] to test the good operation of the Python program which was written during the PhD thesis.

The reflexion coefficient of a LC ladder (output) matching network of type Chebychev, seen from the source, is[^2]:

<asciimath>
|\Gamma|^2 = (\epsilon^2\cdotT_n^2((\omega^2-\omega_0^2)/(\Delta\omega^2)))/(1+\epsilon^2\cdotT_n^2((\omega^2-\omega_0^2)/(\Delta\omega^2)))
</asciimath>

with[^errorsite] <asciimath>\omega_0=sqrt((\omega_a^2+\omega_b^2)/2)</asciimath>, <asciimath>\Delta\omega^2=(\omega_b^2-\omega_a^2)/2</asciimath>, <asciimath>\omega_a</asciimath> the beginning of the passband, and <asciimath>\omega_b</asciimath> the end of the passband.

Next figure shows the reflection coefficient seen from the source of an example of an (output) LC matching network going from 5&#8239;Ω towards 50&#8239;Ω from 1 to 2,5&#8239;GHz. These values are approximately those of the first wideband amplifier of the PhD thesis.

{% comment %}
FIXME: Translate French titles, add alt text.
{% endcomment %}
<figure>
  <div id="LC-ladder-gamma-2"></div>
  <figcaption>Fig.&#8239;1. Example of squared reflection coefficient seen from the source of an LC matching network. See text for parameters.</figcaption>
</figure>

<!-- Thanks to Mistral le Chat. -->
<script>
    /* Chebyshev polynomial of the first kind, Tn, for any x */
    function cheby(x, n) {
        if (x < -1) {
            return Math.pow(-1, n) * Math.cosh(n * Math.acosh(-x));
        }
        else if (x <= 1) {
            return Math.cos(n * Math.acos(x));
        }
        else {
            return Math.cosh(n * Math.acosh(x));
        }
    }

    /* Reg test of cheby */
    for (let n = 0; n <= 10; n++) {
        let min = Infinity, max = -Infinity;
        for (let x = -1; x <= 1; x += 0.1) {
            const val = cheby(x, n);
            min = Math.min(min, val);
            max = Math.max(max, val);
        }
        console.log(`n=${n}: min=${min.toFixed(2)}, max=${max.toFixed(2)}`);
    }

    /* epsilon in function of order and gamma_0 */
    function epsilon_fct(order, gamma_0, w_0_2, delta_omega_2) {
        a = gamma_0 ** 2
        b = a / (1.0 - a)
        X0 = -w_0_2 / delta_omega_2
        Y0 = cheby(X0, order)**2
        var epsilon = Math.sqrt(b / Y0)  // Add real part if needed
        return epsilon
    }

    function gamma_square_in_band(order, gamma_0, w_0_2, delta_omega_2) {
        const epsilon = epsilon_fct(order, gamma_0, w_0_2, delta_omega_2);
        return Math.pow(epsilon, 2) / (1.0 + Math.pow(epsilon, 2));
    }

    /* Chebychev order, not components order */
    function min_order(gamma_0, w_0_2, delta_omega_2, gamma_max) {
        return Math.min(...Array.from({length: 99}, (_, N) => N + 1).filter(N => gamma_square_in_band(N, gamma_0, w_0_2, delta_omega_2) < gamma_max**2));
    }

    // Parameters
    z1 = 5.0
    z2 = 50.0
    f1 = 1.0
    f2 = 2.5

    // Normalised parameters
    f0 = (f1 + f2) / 2.0
    w = (f2 - f1) / f0
    w_a = 1.0 - w/2.0;
    w_b = 1.0 + w/2.0;
    w_0_2 = (w_a**2 + w_b**2) / 2.0;
    delta_omega_2 = (w_b**2 - w_a**2) / 2.0;
    gamma_0 = Math.abs((z1-z2)/(z1+z2));

    const n = min_order(gamma_0, w_0_2, delta_omega_2, 0.1);
    console.log(n);
    const epsilon = epsilon_fct(n, gamma_0, w_0_2, delta_omega_2);

    // Generate omega values
    const omega = [];
    for (let i = -10; i <= 10; i += 0.01) {
        omega.push(i);
    }

    // Calculate the function values
    const y = omega.map(om => {
        const Tn = cheby((om * om - w_0_2) / delta_omega_2, n);
        return (Math.pow(epsilon, 2) * Math.pow(Tn, 2)) /
               (1 + Math.pow(epsilon, 2) * Math.pow(Tn, 2));
    });

    // Create the plot
    const trace = {
        x: omega,
        y: y,
        mode: 'lines',
        type: 'scatter',
        name: 'Function',
        line: {
            width: 1  // Adjust this value to make the line thinner or thicker
        }
    };

    const layout = {
        // title: 'Norm squared Γ^2 of the reflection coefficient in function of the frequency',
        xaxis: {
            title: 'Angular frequency ω [rad/s]'
        },
        yaxis: {
            title: 'Norm squared Γ^2 of the reflection coefficient [unitless]'
        }
    };

    Plotly.newPlot('LC-ladder-gamma-2', [trace], layout);
</script>

In previous expression, <asciimath>\epsilon</asciimath> is chosen such as:

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

This n is half the number of elements of the final network [^ref84].

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

The calculation, more long than complex, won't be detailed. The roots of the numerator and of the denominator are given by the following formulas[^errorphd]:

{% comment %}
FIXME: Math style
{% endcomment %}
<asciimath>
  {: ( +- j \cdot sqrt(\omega_0^2 + Delta omega^2 \cdot cos[(pi)/(2 \cdot n) \cdot (1 + 2 \cdot k)]) , k in [0, 2n - 1] ),
     ( +- j \cdot sqrt( \omega_0^2 + Delta omega^2 \cdot cos[1/n \cdot [arccos(j/epsilon) + k \cdot \pi ]]) , k in [0, 2n - 1] ) :}
</asciimath>

In the implementation of this method, the negative real part roots are sorted numerically.

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

This expression immediately leads to an LC network. The odd gm values are the normalized values of the inductances, while the even gm values are the normalized values of the capacitances. This denormalization is performed according to the following equations[^errorphd]:

<asciimath>
{: ( L = g / (2 pi f_0) \cdot Z_1 ),
   ( C = g / (2 pi f_0) \cdot 1 / Z_1 ) :}
</asciimath>

The last &&g_m&& is the load resistance, which is also normalized. Its value has been known for a long time, but it can be interesting to recalculate it to verify that there is no significant error due to numerical inaccuracies.

## Appendix: equations of the roots

### Numerator

The roots of the numerator, without any attempt to remove duplicates, can be expressed as such:

<latexmath>
\begin{align*}
& \epsilon^2 \cdot T_n^2(x) = 0  \\
\Leftrightarrow \enspace & T_n^2(x) = 0  \\
\Leftrightarrow \enspace & \cos \left[ n \cdot \arccos (x) \right] = 0  \\
\Leftrightarrow \enspace & n \cdot \arccos x) = \frac{\pi}{2} + k \cdot \pi, \enspace k \in \mathbb{Z}  \\
\Leftrightarrow \enspace & x = \cos \left[ \frac{\frac{\pi}{2} + k \cdot \pi}{n} \right], \enspace k \in \mathbb{Z}  \\
\Leftrightarrow \enspace & x = \cos \left[ \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k \right) \right], \enspace k \in \mathbb{Z}  \\
\end{align*}
</latexmath>

Due to the periodicity and invariance by sign change of the cosinus, different values of k can lead to the same root. Two different values of k lead to the same root on the following condition:

<latexmath>
\begin{align*}
& \cos \left[ \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k_1 \right) \right] = \cos \left[ \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k_2 \right) \right]  \\
\Leftrightarrow \enspace & \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k_1 \right) = \pm \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k_2 \right) + l \cdot 2 \cdot \pi, \enspace l \in \mathbb{Z}  \\
\Leftrightarrow \enspace & \frac{\pi}{n} \cdot k_1 = \pm \frac{\pi}{n} \cdot k_2 + l \cdot 2 \cdot \pi, \enspace l \in \mathbb{Z}  \\
\Leftrightarrow \enspace & k_1 = \pm k_2 + l \cdot 2 \cdot n, \enspace l \in \mathbb{Z}  \\
\end{align*}
</latexmath>

Which lead to the set of the roots after removing the duplicates:

<latexmath>
\begin{align*}
x_k = \cos \left[ \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k \right) \right], \enspace k \in [0; 2n-1]  \\
\end{align*}
</latexmath>

Next the corresponding values of <asciimath>\omega</asciimath> can be solved:

<latexmath>
\begin{align*}
&\frac{\omega^2-\omega_0^2}{\Delta\omega^2} = \cos \left[ \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k \right) \right], \enspace k \in [0; 2n-1]  \\
&\omega^2 = \omega_0^2 + \Delta\omega^2 \cdot \cos \left[ \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k \right) \right], \enspace k \in [0; 2n-1]  \\
&\omega = \pm \sqrt{ \omega_0^2 + \Delta\omega^2 \cdot \cos \left[ \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k \right) \right] }, \enspace k \in [0; 2n-1]
\end{align*}
</latexmath>

Next the corresponding value of <asciimath>p</asciimath> can be solved. This point led to a confusion in an intermediate version of this page:

<latexmath>
\begin{align*}
p_k = \pm j \cdot \sqrt{ \omega_0^2 + \Delta\omega^2 \cdot \cos \left[ \frac{\pi}{2 \cdot n} \cdot \left( 1 + 2 \cdot k \right) \right] }, \enspace k \in [0; 2n-1]  \\
\end{align*}
</latexmath>

### Denominator

Same method.

<latexmath>
\begin{align*}
& 1 + \epsilon^2 \cdot T_n^2(x) = 0  \\
\Leftrightarrow \enspace & T_n^2 (x) = - \frac{1}{\epsilon^2}  \\
\Leftrightarrow \enspace & T_n(x) = \pm \frac{j}{\epsilon}  \\
\Leftrightarrow \enspace & \cos \left[ n \cdot \arccos \left( x \right) \right] = \pm \frac{j}{\epsilon}  \\
\Leftrightarrow \enspace & n \cdot \arccos \left( x \right) = \pm \arccos \left( \pm \frac{j}{\epsilon} \right) + k \cdot 2 \cdot \pi, \enspace k \in \mathbb{Z}  \\
\Leftrightarrow \enspace & \arccos \left( x \right) = \pm \frac{1}{n} \arccos \left( \pm \frac{j}{\epsilon} \right) + \frac{k}{n} \cdot 2 \cdot \pi, \enspace k \in \mathbb{Z}  \\
\Leftrightarrow \enspace & x = \cos \left[ \frac{1}{n} \arccos \left( \pm \frac{j}{\epsilon} \right) + \frac{k}{n} \cdot 2 \cdot \pi \right] , \enspace k \in \mathbb{Z}
\end{align*}
</latexmath>

And for the same reason as for the numerator, <latexmath>k</latexmath> can be restricted to the interval <latexmath>[0; 2n-1]</latexmath>.

Next, <asciimath>omega</asciimath> and p can be calculated in a similar way than for the numerator.

[^1]: It is not even a pure impedance. See the blog pages to come!

[^2]: In [^ref84], &&\Delta\omega^2&& is named A.

[^3]: Such polynomials are called Hurwitz polynomials. The reasons why a and b must satisfy this condition go beyond the scope of this thesis. The reader is encouraged to refer to a book on network synthesis [12, 56, 73].

[^4]: This point has been forgotten to be mentioned in the PhD thesis pdf. Sorry.

[^errorphd]: There is a typo in these formulas in the PhD thesis pdf. Sorry.

[^errorsite]: There was a typo in these formulas in a previous version of this article. Sorry.

[^ref32]: Chen CHI, Chen JUN et Wang LEI. «L-band high efficiency GaN HEMT power amplifier for space application ». In : Radar Conference 2013, IET International. Avr. 2013, p. 1-4. DOI : 10.1049/cp.2013.0455.

[^ref84]: G.L. MATTHAEI. « Tables of Chebyshev impedance-transforming networks of low-pass filter form». In : Proceedings of the IEEE 52.8 (august 1964), p. 939-963. ISSN : 0018-9219. DOI : 10 . 1109 / PROC . 1964 . 3185.

[^ref116]: D.A. SUKHANOV et A.A. KISHCHINSKIY. « High efficiency L-, S-, C- band GaN power pulse amplifiers ». In: Microwave and Telecommunication Technology (CriMiCo), 2013 23rd International Crimean Conference. Sept. 2013, p. 94-95.

[^ref29]: Kenle CHEN et D. PEROULIS. « Design of Highly Efficient Broadband Class-E Power Amplifier Using Synthesized Low-Pass Matching Networks ». In: Microwave Theory and Techniques, IEEE Transactions on 59.12 (déc. 2011), p. 3162-3173. ISSN : 0018-9480. DOI : 10.1109/TMTT.2011.2169080.

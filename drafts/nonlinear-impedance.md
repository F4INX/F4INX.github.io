---
layout: post
title: Nonlinear impedance
permalink: /drafts/nonlinear-impedance.html
last_modified_at: 2026-03-08
---

### A few words on the notion of transistor output impedance

In section \ref{section-utilite-transitions-impedance}, we set aside the real behavior of power amplifiers to focus on the behavior of their loads, i.e., the inputs of the power combiner. Power amplifiers operating at high power are nonlinear, which causes particular effects on the behavior of their outputs. We will detail these effects in the following section.

### Behavior of a simplified nonlinear power amplifier

Let us consider a simplified nonlinear amplifier. We will initially assume that it reacts instantaneously to its inputs, i.e., its response is frequency-independent. The model will be extended to incorporate frequency variations in the following section. Suppose its response can be described in the time domain by the equation below:

<latexmath>
\label{eq:b2_t}
b_2(t) = \underbrace{G \cdot a_1(t)}_{\text{Gain in small signals}} - \underbrace{\gamma \cdot a_{1}^{3}(t)}_{\text{Gain compression}} + \underbrace{\Gamma \cdot a_2(t)}_{\text{Output reflection in small signals}}  - \underbrace{\lambda \cdot a_{1}^{2}(t) \cdot a_2(t)}_{\text{Variation of reflection with input, self-biasing}}
</latexmath>

This model is highly simplified but already contains the effects found in real amplifiers: small-signal gain, gain compression for large signals, output reflection, self-biasing, and variation of the output reflection coefficient as a function of input power.

For numerical examples, let us take the following values:

<latexmath>
\begin{flalign}
G &= 4 & \gamma &= 0{,}083 & \Gamma &= 0{,}73 & \lambda &= 0{,}06
\end{flalign}
</latexmath>

Figures \ref{fig-plt-non-lineaire-b2-a1} and \ref{fig-plt-non-lineaire-r2-a1} show respectively the instantaneous value of the output b\textsubscript{2}(t) and the instantaneous reflection coefficient \frac{db_{2}(t)}{da_{2}(t)}, both as a function of the input a\textsubscript{1}(t).

<figure>
  <picture>
      <img src="{{ '/drafts/nonlinear-impedance/non-lineaire-b2-a1.svg' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Output b\textsubscript{2}(t) as a function of input a\textsubscript{1}(t).</figcaption>
</figure>

<figure>
  <picture>
      <img src="{{ '/drafts/nonlinear-impedance/non-lineaire-r2-a1.svg' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Instantaneous reflection coefficient \frac{db_{2}(t)}{da_{2}(t)} of the output as a function of input a\textsubscript{1}(t).</figcaption>
</figure>

This nonlinear equation can be linearized \cite{versprecht2006polyharmonic,root2013x} around an operating point, which we will call "LSOP" for "large signal operating point". This operating point is:

<latexmath>
\begin{align}
a_{1,\text{LSOP}}(t) &= \frac{ \Aone \cdot e^{i \omega t} + \conj{A_{1}} \cdot e^{- i \omega t} }{2} \\
a_{2,\text{LSOP}}(t) &= 0
\end{align}
</latexmath>

and we apply to this operating point a perturbation at the output:

<latexmath>
\begin{align}
a_{1}(t) &= a_{1,\text{LSOP}}(t) \\
a_{2}(t) &= a_{2,\text{LSOP}}(t) + \frac{ \delta \Atwo \cdot e^{i \omega t} + \conj{\delta A_{2}} \cdot e^{- i \omega t} }{2}
\end{align}
</latexmath>

Which gives the following equations:

<latexmath>
\begin{align}
\label{eq:a1_t}
a_{1}(t) &= \frac{ \Aone \cdot e^{i \omega t} + \conj{A_{1}} \cdot e^{- i \omega t} }{2}\\
\label{eq:a2_t}
a_{2}(t) &= \frac{ \delta \Atwo \cdot e^{i \omega t} + \conj{\delta A_{2}} \cdot e^{- i \omega t} }{2}
\end{align}
</latexmath>

By combining equations \ref{eq:b2_t}, \ref{eq:a1_t} and \ref{eq:a2_t} we obtain:

<latexmath>
\begin{split}
b_{2}(t) &= G\cdot\left[\frac{\Aone \cdot e^{i \omega t}+\conj{A_{1}}\cdot e^{- i \omega t}}{2}\right] + \Gamma\cdot\left[\frac{\delta\Atwo \cdot e^{i \omega t}+\delta\conj{A_{2}}\cdot e^{- i \omega t}}{2}\right]\\
&-\gamma\cdot\left[\frac{\delta\Atwo\cdot e^{i \omega t}+\delta\conj{A_{2}}\cdot e^{- i \omega t}}{2}\right]^3\\
&-\lambda\cdot\left[\frac{\Aone\cdot e^{i \omega t}+\conj{A_{1}}\cdot e^{- i \omega t}}{2}\right]^2\cdot\left[\frac{\delta\Atwo\cdot e^{i \omega t}+\conj{A_{2}}\cdot e^{- i \omega t}}{2}\right]
\end{split}
</latexmath>

By expanding the previous expression and grouping the terms, we obtain:

<latexmath>
\begin{split}
b_{2}(t) &= \left[ \frac{G}{2} \cdot \Aone - \frac{3 \gamma}{8} \left|\Aone\right|^2 \cdot \Aone + \frac{\Gamma}{2} \cdot \delta\Atwo - \frac{\Aone \cdot \conj{A_{1}} }{4} \cdot \lambda \cdot \delta\Atwo - \frac{A_{1}^{2} \cdot \lambda}{8} \cdot \delta\conj{A_{2}} \right] \cdot e^{i \omega t} \\
&+ \left[ - \frac{A_{1}^{2}}{8} \cdot \left(\Aone \cdot \gamma + \delta\Atwo \cdot \lambda \right) \right] \cdot e^{3 i \omega t} \\
&+ \text{conjugate terms}
\end{split}
</latexmath>

We ignore the terms in e^{3 i \omega t} and e^{-3 i \omega t} which correspond to the third harmonic of the signal, and we are interested in the amplitude of the terms in e^{i \omega t} and e^{i \omega t}:

<latexmath>
b_{2}(t) = \frac{ \Btwo \cdot e^{i \omega t} + \conj{B_{2}} \cdot e^{- i \omega t} }{2} + \text{terms in } e^{3 i \omega t} \text{ and } e^{-3 i \omega t}
</latexmath>

with

<latexmath>
B_{2} = G \cdot A_{1} - \frac{3 \cdot \gamma}{4} \left|A_1\right|^2 \cdot A_{1} + \Gamma \cdot A_{2} - \frac{\Aone \cdot \conj{A_{1}}}{2} \cdot \lambda \cdot \delta A_{2} - \frac{A_{1}^{2} \cdot \lambda}{4} \cdot \conj{\delta A_{2}}
</latexmath>

which we rewrite in a simpler form:

<latexmath>
B_{2} = \underbrace{S_{21}^{\phantom{*}}(\Aone)\cdot \Aone}_\text{Amplification} + \underbrace{S_{22}^{\phantom{*}}(\Aone)\cdot \delta\Atwo}_\text{Normal reflection} + \underbrace{T_{22}^{\phantom{*}}(\Aone)\cdot \delta\conj{A_2}}_\text{Conjugate reflection}
</latexmath>

with:

<latexmath>
\begin{align}
S_{21}(A_1) &= G - \frac{3 \cdot \gamma}{4} \cdot \left|A_1\right|^2 \\
S_{22}(A_1) &= \Gamma - \frac{\left|A_1\right|^2}{2} \\
T_{22}(A_1) &=  - \frac{A_{1}^{2} \cdot \lambda}{4}
\end{align}
</latexmath>

These coefficients depend on the phase of A\textsubscript{1}, which is not very practical. We will therefore renormalize them. Let P = e^{i\cdot\phi(A_1)}. Thus:

<latexmath>
\begin{split}
S_{21}(A_1) &= S_{21}(\left|A_1\right| \cdot P) \\
            &= G - \frac{3 \cdot \gamma}{4} \cdot \big||A_1| \cdot P\big|^2 \\
            &= G - \frac{3 \cdot \gamma}{4} \cdot \big||A_1|\big|^2 \cdot \underbrace{\big|P\big|^2}_{=1} \\
            &= G - \frac{3 \cdot \gamma}{4} \cdot \big||A_1|\big|^2 \\
            &=  S_{21}(\left|A_1\right|)
\end{split}
</latexmath>

Similarly:

<latexmath>
\begin{align*}
S_{22}(A_1) &= S_{22}(\left|A_1\right|) \\
T_{22}(A_1) &= T_{22}(\left|A_1\right|) \cdot P^2 \\
\end{align*}
</latexmath>

and therefore:

<latexmath>
B_{2} = \underbrace{S_{21}^{\phantom{*}}(|A_1|)\cdot \Aone}_\text{Amplification} + \underbrace{S_{22}^{\phantom{*}}(|A_1|)\cdot \delta\Atwo}_\text{Normal reflection} + \underbrace{T_{22}^{\phantom{*}}(|A_1|) \cdot P^2 \cdot \delta\conj{A_2}}_\text{Conjugate reflection}
</latexmath>

This linearization is a simplified version of the X parameters \cite{versprecht2006polyharmonic,root2013x}.

The amplitude of B\textsubscript{2} in large signal regime for A\textsubscript{2}=0 as a function of A\textsubscript{1} is shown in \cref{fig-plt-non-lineaire-complexe-B2-A1}. This figure is different from \cref{fig-plt-non-lineaire-b2-a1} because the latter is an instantaneous transfer function while the former is a sinusoidal regime transfer function. The nonlinear gain S\textsubscript{21}(|A\textsubscript{1}|) is shown as a function of |A\textsubscript{1}| in \cref{fig-plt-non-lineaire-S21}. We recognize the classic gain compression of nonlinear amplifiers.

<figure>
  <picture>
      <img src="{{ '/drafts/nonlinear-impedance/non-lineaire-complexe-B2-A1.svg' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Output amplitude B\textsubscript{2} as a function of |A\textsubscript{1}| in large signal regime.</figcaption>
</figure>

<figure>
  <picture>
      <img src="{{ '/drafts/nonlinear-impedance/non-lineaire-S21.svg' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Nonlinear gain S\textsubscript{21}(|A\textsubscript{1}|) as a function of |A\textsubscript{1}|.</figcaption>
</figure>

The contribution of δA\textsubscript{2} to B\textsubscript{2} is denoted δ\textsubscript{2}B\textsubscript{2} and is given by

<latexmath>
\delta_{2}^{\phantom{*}}B_{2}^{\phantom{*}} = S_{22}^{\phantom{*}}(|A_1|)\cdot A_{2}^{\phantom{*}} + T_{22}^{\phantom{*}}(|A_1|)\cdot \conj{A_2}
</latexmath>

This allows us to calculate the apparent reflection coefficient of the output Γ\textsubscript{2}:

<latexmath>
\Gamma_2 = \frac{\delta_{2}^{\phantom{*}}B_{2}^{\phantom{*}}}{B_{2}^{\phantom{*}}} = S_{22}^{\phantom{*}}(|A_1|) + T_{22}^{\phantom{*}}(|A_1|) \cdot P^2 \cdot \frac{\conj{A_2}}{\Atwo}
</latexmath>

which can be rewritten by replacing P with its value:

<latexmath>
\Gamma_2 = \frac{\delta_{2}^{\phantom{*}}B_{2}^{\phantom{*}}}{B_{2}^{\phantom{*}}} = S_{22}^{\phantom{*}}(|A_1|) + T_{22}^{\phantom{*}}(|A_1|) \cdot P^2 \cdot e^{i \cdot 2 \cdot [\phi(A_2) - \phi(A_1)]}
</latexmath>

B\textsubscript{2} and δB\textsubscript{2} are shown respectively in \cref{fig-plt-non-lineaire-complexe-b2-b2-a1} and \cref{fig-plt-non-lineaire-complexe-deltab2-b2-a1} when δA\textsubscript{2} describes a circle.

<figure>
  <picture>
      <img src="{{ '/drafts/nonlinear-impedance/non-lineaire-complexe-B2-B2-A1.svg' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>δB\textsubscript{2} when δA\textsubscript{2} describes a unit circle for different values of A\textsubscript{1}.</figcaption>
</figure>

<figure>
  <picture>
      <img src="{{ '/drafts/nonlinear-impedance/non-lineaire-complexe-deltaB2-B2-A1.svg' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>δB\textsubscript{2} when δA\textsubscript{2} describes a unit circle for different values of A\textsubscript{1}.</figcaption>
</figure>

The first term depends only on the amplitude of A\textsubscript{1} and behaves exactly like a classic S\textsubscript{22} (except, of course, for the amplitude dependence) \cite{versprecht2006polyharmonic,root2013x}. On the other hand, the second term is more particular. It depends not only on the amplitude of A\textsubscript{1} but also on the phase difference between A\textsubscript{2} and A\textsubscript{1} \cite{versprecht2006polyharmonic,root2013x}.

The coefficient T\textsubscript{22} is simply neglected in classical large-signal S-parameter approaches \cite{versprecht2006polyharmonic,root2013x}. This term is zero at low power but can exceed S\textsubscript{22} when approaching saturation \cite{versprecht2006polyharmonic,root2013x}, as shown in \cref{fig-plt-non-lineaire-s22-t22}. Therefore, two terms are needed to completely describe the output reflection of the amplifier. Note that it is clearly seen in \cref{fig-plt-non-lineaire-s22-t22} that the output matching of this amplifier is very poor at low power but excellent at full power. This is also a classic effect of real power amplifiers.

<figure>
  <picture>
      <img src="{{ '/drafts/nonlinear-impedance/non-lineaire-S22-T22.svg' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Coefficients S\textsubscript{22} and T\textsubscript{22}. The coefficient T\textsubscript{22} is zero at low power but exceeds S\textsubscript{22} in saturation.</figcaption>
</figure>

<figure>
  <picture>
      <img src="{{ '/drafts/nonlinear-impedance/non-lineaire-Gamma2.svg' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Apparent reflection coefficient of the output Γ\textsubscript{2} for different input amplitudes |A\textsubscript{1}|.</figcaption>
</figure>

The strange behavior of the T\textsubscript{22} term deserves further discussion. Surprisingly, and although it arises from nonlinear phenomena, this term translates a linear behavior. Indeed, if the perturbation δA\textsubscript{2,total} is the superposition of two perturbations:

<latexmath>
\begin{equation*}
\delta A_{2,total} = \delta A_{2,a} + \delta  A_{2,b}
\end{equation*}
</latexmath>

then:

<latexmath>
\begin{equation*}
\delta_{2}B_{2,total} = \delta_{2}B_{2,a} + \delta_{2}B_{2,b}
\end{equation*}
</latexmath>

which is the very definition of linear behavior.

This linearity, surprisingly again, is perfectly normal. Indeed, we spent an entire section linearizing the power amplifier around an operating point. A linearization that would not result in a linear model would be an absurdity.

However, this is not ordinary linear behavior, and ordinary linear systems, which can be described by classical S parameters, do not exhibit it. Why this paradox?

Because the T\textsubscript{22} term translates a time-varying linear behavior. However, classical linear systems are time-invariant.

In summary, the linearization of a time-invariant nonlinear system around a time-varying operating point (it's a cosine!) results in a time-varying linear model. This linear model cannot be described by S parameters because these S parameters are reserved for time-invariant linear systems.

The correct way to describe this linearization is the use of X parameters \cite{versprecht2006polyharmonic,root2013x}. The coefficients of the previous section are almost X parameters.

It is always possible to calculate an apparent output impedance from the apparent reflection coefficient of the previous section, but is it correct to speak of the output impedance of a nonlinear amplifier? \cref{fig-plt-non-lineaire-Gamma2} clearly shows that a power amplifier in saturation has multiple impedances depending on the output perturbation. Which one is correct? Moreover, is the term "impedance" still appropriate, given that this impedance does not have the usual properties of an impedance?

One way to see things is to say that a power amplifier does not have a well-defined impedance. Another is to say that a power amplifier has two output impedances: one for signals in phase with the input signal and another for quadrature signals. But it is wrong to say that a power amplifier has a single output impedance independent of the phase of B\textsubscript{2}.

This poses a problem because we need an output impedance, or something close to it, to perform our matching calculations. We will therefore reverse the problem. Instead of asking what the output impedance of the power amplifier is, we will ask what its optimal load impedance is. In our applications, the load is the input of a power combiner followed by an antenna. This load is linear and time-invariant. The load impedance is therefore well defined.

To simplify the reasoning, and by abuse of language, we will call "output impedance" the conjugate of the optimal load impedance. But it is indeed a fiction, given the previous reservations about the notion of output impedance applied to nonlinear systems.

We have talked about amplifiers but not yet about transistors. The same remarks apply to a transistor, but with an additional reservation: since transistors are not matched, the operating point is more complex to define \cite{root2013x}. The conclusions are however globally similar \cite{root2013x}.

Reasoning with load impedances is a common practice in the field of transistor amplifiers. This is the principle of load-pull, whether performed in reality or on a simulator. Similarly, in its datasheets, an example of which is shown in \cref{fig-CGHV14500-datasheet-impedances}, Wolfspeed (formerly CREE) does not provide the output impedances of its transistors but rather the optimal load impedances. QED.

<figure>
  <picture>
      <img src="{{ '/drafts/nonlinear-impedance/CGHV14500-datasheet-impedances.svg' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Extract from the CGHV14500 datasheet showing optimal source and load impedances. Not those of the transistor.</figcaption>
</figure>

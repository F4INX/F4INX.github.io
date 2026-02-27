---
layout: post
title: A (not so) gentle introduction to operational amplifiers.
permalink: /posts/op-amp-introduction.html
last_modified_at: 2026-02-26
---

<p class="begin-note">After some discussions on grounding and various subjects with Gönül Demir, we thought that it could be a good idea to combine our both approaches to make a join page. Indeed I began my series by writing detailed articles about complex points and not by an introduction. We hope that this gentle (or not so) introduction to the topic would fill the gap.</p>

## What is an op-amp?

An operational amplifier (op-amp) is a high-gain analog amplifier designed to amplify the voltage difference between its two input terminals. Although the ideal op-amp model is considered simple, in practice op-amps have certain limitations and non-ideal behaviors. For this reason, op-amps are evaluated not on their own, but within a specific circuit context.

## What is an op-amp used for?

In practice, op-amps are not used merely as “high-gain amplifiers”; they are mainly used to create controlled and predictable analog building blocks with the help of feedback. In this way, a single op-amp structure can perform many fundamental analog functions such as voltage amplification, buffering, summing–subtraction, active filtering, and providing impedance matching in measurement chains. In analog systems, the op-amp is a fundamental component that determines the amplitude and behavior of the signal. 

## Feedback

### Negative feedback

Negative feedback was invented by Harold S. Black based on earlier works during his research on amplifiers for long distance analog telephony with multiple carriers multiplexing [https://brewer.ece.gatech.edu/ece3043/FBBlack.pdf] <!-- Reformat. -->.

The gain of these tube amplifiers was not stable, which was troublesome because a wrong value of the gain compound with the multiple stages and lead to too low or too high outputs. 

These amplifiers had also non-linearities issues which caused not only distortion of the individual carriers but also intermodulation between carriers.
Applying a negative feedback to an amplifier allow to trade a big gain against a stable gain. In the example given in [ref H&H], an amplifier with a voltage open-loop gain varying from 1000 (60 dB) to 10000 (80 dB) end up with a 0.1 feedback (-10 dB) with a gain varying from 9.90 (19.91 dB) to 9.99 (19,99 dB), that is going from a +- 10 dB flatness to a +- 0.04 dB flatness.

A similar although more complex analysis would show that feedback reduces non-linearities. This is left as an exercise for one my the people I’m currently mentoring. In the meanwhile, please find a beautiful picture of a cat <!-- When I start putting pictures of cats, it’s the sign I got myself tired of equations. 😃 -->.

### Operational amplifiers and negative feedback

Operational amplifiers are explicitly designed to be used with feedback. However, an improperly applied feedback can cause circuits to oscillate, and indeed Harold S. Black had to solve instability issues.

Without diving too much in the theory <!-- I am now tired of equations after the VCVS filter. ☺️ -->, instability occurs when the loop gain is higher than 1 for a phase shift higher than 180°. Internal feedback is used in most op-amps <!-- I won’t mention some exotic amplifiers who are undercompensated and not interesting for an intro article. --> so they behave approximately like integrators with 90° phase shift until their unity-gain bandwidth.

The integrator configuration is also convenient to have high gains at DC, and for most practical purposes the DC gain of an operational amplifier can be considered as infinite, and the operational amplifier as a pure integrator until its unity gain frequency, without the corner due to the finite DC gain.

Even if an integrator is not stable alone, this behavior is considered as much “stability friendly”, and H&H tells that making an integrator oscillate needs a real talent. (Sorry, I don’t remember if it is in the 2nd or 3rd edition.)

An operational amplifier is almost never used without negative feedback, at least because its high DC gain combined with its offset would make it saturate. A word of caution: a common mistake by beginners dealing with AC coupled signals is to forget the DC feedback.

### Operational amplifiers and positive feedback

Although if less often used than negative feedback, the positive feedback is used typically for oscillators. Two configurations are worth mentioning: the Wien bridge oscillators and the RC feedback oscillator.

<!-- TODO: put the LTSpice stuff. -->

### Comparators and positive feedback

With comparators, components used to compare two voltages and give a two state output (high or low), positive feedback is commonly used in the form of hysteresis for two reasons. 1/ Avoid multiple transitions in the case of noisy inputs. 2/ Decrease the output raise and fall times using the gain increase due to positive feedback.

However…… comparators are NOT operational amplifiers, and their use cases should not be mixed.

The following oscillator works in a comparator mode, which can be seen by the output taken discrete levels, and thus a comparator should be used for this schematic.

<figure>
  <img src="{{ '/posts/op-amp-intro/rc-oscillator.png' | relative_url }}" />
  <!-- <figcaption>TODO: put title here.</figcaption> -->
</figure>

Some sources on the internet use a 741 in this schematic. Don’t spread this mistake!

## Applications of op-amps and their important parameters

<!-- TODO. -->

## Op-amps according to input stage (BJT, JFET, MOSFET)

Operational amplifiers differ not only according to which application they are optimized for, but also according to the transistor technology used in the input stage.

This choice directly affects the op-amp’s input impedance, input bias current, and noise behavior. For this reason, it is a critical design parameter, especially in sensor interfaces and precision measurement circuits.

### BJT-input op-amps

Thanks to their low input voltage noise and good matching characteristics, they provide an advantage when working with low-impedance sources.

In active-output sensors or low-impedance analog sources, noise performance is generally better.

On the other hand, since the input bias current is relatively high, they can lead to additional offset errors when used with high-impedance sources.

<figure>
  <img src="{{ '/posts/op-amp-intro/bjt-amp-1.png' | relative_url }}" />
  <figcaption>Figure xx: Schematic diagram of a BJT differential amplifier, from https://en.wikipedia.org/wiki/Differential_amplifier</figcaption>
</figure>

<figure>
  <img src="{{ '/posts/op-amp-intro/bjt-amp-2.png' | relative_url }}" />
  <figcaption>Figure xx: Schematic diagram of a BJT differential amplifier, from https://en.wikipedia.org/wiki/Differential_amplifier</figcaption>
</figure>

<!-- TODO: Explain why two schematics. -->

### JFET-input op-amps

They provide much lower input bias current and high input impedance. With these characteristics, they are suitable for medium- and high-impedance sensors. Noise performance is generally weaker <!-- Voltage noise is indeed generally higher, however current noise is generally lower. --> than that of BJT-input op-amps, but in practice the low bias current may be more important. In this respect, JFET-input op-amps are considered a balanced option between BJT and CMOS.

### MOSFET (CMOS)-input op-amps

With extremely high input impedance and very low bias current, they are ideal for applications that require very high impedance and low power consumption.
Battery-powered systems and long-term DC measurements fall into this category. However, low-frequency noise (1/f noise) and temperature-dependent effects may be more pronounced; therefore, modern CMOS op-amps are often supported with zero-drift architecture.

A simplified schematic of a typical CMOS operational amplifier is shown below:

<figure>
  <img src="{{ '/posts/op-amp-intro/fet-amp.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

From OPA391 data sheet, product information and support | TI.com.

<!-- TODO: reformat. -->

In summary, if the source impedance is low, a BJT input is preferred; for medium-to-high impedance sources, a JFET input; and for very high impedance and low power requirements, a CMOS input is generally the most suitable choice.

This distinction plays a decisive role in measurement accuracy and system stability, regardless of the op-amp type.

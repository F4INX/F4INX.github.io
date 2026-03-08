---
layout: post
title: A (not so) gentle introduction to operational amplifiers.
permalink: /posts/op-amp-introduction.html
last_modified_at: 2026-03-08
---

<style>
  .op-amp-introduction {
    counter-reset: h2-counter h3-counter;
  }

  .op-amp-introduction h2::before {
    counter-increment: h2-counter;
    counter-set: h3-counter;
    content: counter(h2-counter) " ";
  }

  .op-amp-introduction .related h2::before {
    counter-increment: unset;
    counter-set: unset;
    content: unset;
  }

  .op-amp-introduction h3::before {
    counter-increment: h3-counter;
    content: counter(h2-counter) "." counter(h3-counter) " ";
  }

  .op-amp-introduction .related h3::before {
    counter-increment: unset;
    content: unset;
  }
</style>

<div markdown="1" class="op-amp-introduction">

<p class="begin-note">After some discussions on grounding and various subjects with <a href="https://www.linkedin.com/in/gonul-demir-49413433/">Gönül Demir</a>, we thought that it could be a good idea to combine our both approaches to make a join page. Indeed I began my series by writing detailed articles about complex points and not by an introduction. We hope that this gentle (or not so) introduction to the topic would fill the gap.</p>

## What is an op-amp?

An operational amplifier (op-amp) is a high-gain analog amplifier designed to amplify the voltage difference between its two input terminals. Although the ideal op-amp model is considered simple, in practice op-amps have certain limitations and non-ideal behaviors. For this reason, op-amps are evaluated not on their own, but within a specific circuit context.

## What is an op-amp used for?

In practice, op-amps are not used merely as “high-gain amplifiers”; they are mainly used to create controlled and predictable analog building blocks with the help of feedback. In this way, a single op-amp structure can perform many fundamental analog functions such as voltage amplification, buffering, summing–subtraction, active filtering, and providing impedance matching in measurement chains. In analog systems, the op-amp is a fundamental component that determines the amplitude and behavior of the signal. 

## Feedback

### Negative feedback

Negative feedback was invented by Harold S. Black based on earlier works during his research on amplifiers for long distance analog telephony with multiple carriers multiplexing [https://brewer.ece.gatech.edu/ece3043/FBBlack.pdf](https://brewer.ece.gatech.edu/ece3043/FBBlack.pdf).

The gain of these tube amplifiers was not stable, which was troublesome because a wrong value of the gain compound with the multiple stages and lead to too low or too high outputs. 

These amplifiers had also non-linearities issues which caused not only distortion of the individual carriers but also intermodulation between carriers.
Applying a negative feedback to an amplifier allow to trade a big gain against a stable gain. In the example given by Horowitz and Hill [2], an amplifier with a voltage open-loop gain varying from 1000 (60 dB) to 10000 (80 dB) end up with a 0.1 feedback (-10 dB) with a gain varying from 9.90 (19.91 dB) to 9.99 (19,99 dB), that is going from a +- 10 dB flatness to a +- 0.04 dB flatness.

A similar although more complex analysis would show that feedback reduces non-linearities. This is left as an exercise for one my the people I’m currently mentoring. In the meanwhile, please find a beautiful picture of a cat <!-- When I start putting pictures of cats, it’s the sign I got myself tired of equations. 😃 -->.

### Operational amplifiers and negative feedback

Operational amplifiers are explicitly designed to be used with feedback. However, an improperly applied feedback can cause circuits to oscillate, and indeed Harold S. Black had to solve instability issues.

Without diving too much in the theory <!-- I am now tired of equations after the VCVS filter. ☺️ -->, instability occurs when the loop gain is higher than 1 for a phase shift higher than 180°. Internal feedback is used in most op-amps <!-- I won’t mention some exotic amplifiers who are undercompensated and not interesting for an intro article. --> so they behave approximately like integrators with 90° phase shift until their unity-gain bandwidth.

The integrator configuration is also convenient to have high gains at DC, and for most practical purposes the DC gain of an operational amplifier can be considered as infinite, and the operational amplifier as a pure integrator until its unity gain frequency, without the corner due to the finite DC gain.

Even if an integrator is not stable without a feedback look, integrators are very friendly for designers, even from a stability point of view, when used in a feedback loop. In addition, the internal feedback used to provide this integrator behavior pushes other poles further in frequency, due to a phenomena called "pole splitting", so they don't add too much phase before the unity gain frequency.

An operational amplifier is almost never used without negative feedback, at least because its high DC gain combined with its offset would make it saturate. A word of caution: a common mistake by beginners dealing with AC coupled signals is to forget the DC feedback.

### Operational amplifiers and positive feedback

Although if less often used than negative feedback, the positive feedback is used typically for oscillators. Two configurations are worth mentioning: the Wien bridge oscillator and the RC feedback oscillator.

#### Wien bridge oscillator

Simulation and output waveform of wien bridge oscillator without automatic gain control are shown below. Note the clipping of the waveform, which creates distorsion and harmonics. The root cause is that the loop gain must be equal to **exactly** 1 for sustained oscillation. Due to the tolerances of the various passives, the only way to get this condition **exactly** is to set the linear loop gain slightly higher than 1 and to count on the non-linear clipping of the amplifier to lower the actual non-linear loop gain to 1. This process creates distorsion and harmonics.

<figure>
  <picture>
      <source srcset="{{ '/posts/op-amp-introduction/wien-without-agc.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
      <!-- <source srcset="{{ '/posts/op-amp-introduction/wien-without-agc-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/> -->
      <img src="{{ '/posts/op-amp-introduction/wien-without-agc-dark.png' | relative_url }}" style="width:75%;"/>
  </picture>
  <figcaption>Schematic of a wien bridge oscillator without automatic gain control.</figcaption>
</figure>

<figure>
  <picture>
      <source srcset="{{ '/posts/op-amp-introduction/wien-without-agc-plot.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
      <source srcset="{{ '/posts/op-amp-introduction/wien-without-agc-plot-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/>
      <img src="{{ '/posts/op-amp-introduction/wien-without-agc-plot.png' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Output after startup of a wien bridge oscillator without automatic gain control. Note the clipping of the waveforms.</figcaption>
</figure>

To avoid the drawbacks of the clipping method to set the loop gain, automatic gain control (AGC) can be used instead, like in the example below. The time constant of the exponential increase or decrease of the amplitudes of the oscillations is sufficienly high to allow setting the gain to the **exact** value of gain through a feedback look, called an automatic gain control. Note that the variation of the amplitude in function of the gain had a behavior similar to an integrator, so the unity gain can be reached for different amplitudes, and the gain is controlled indirectly through the amplitude. The plot show in blue the start of the oscillator with AGC and in green the output of the detector which, once below the threshold voltage of the JFET Q1, increases his resistance and lowers the gain set by the feedback loop R1 and R2+Q1.

<figure>
  <picture>
      <source srcset="{{ '/posts/op-amp-introduction/wien-with-agc.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
      <source srcset="{{ '/posts/op-amp-introduction/wien-with-agc-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/>
      <img src="{{ '/posts/op-amp-introduction/wien-with-agc.png' | relative_url }}" style="width:75%;"/>
  </picture>
  <figcaption>Schematic of a wien bridge oscillator without automatic gain control.</figcaption>
</figure>

<figure>
  <picture>
      <source srcset="{{ '/posts/op-amp-introduction/wien-with-agc-plot.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
      <source srcset="{{ '/posts/op-amp-introduction/wien-with-agc-plot-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/>
      <img src="{{ '/posts/op-amp-introduction/wien-with-agc-plot.png' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Output of a wien bridge oscillator with automatic gain control. The waveform has no clipping.</figcaption>
</figure>

Details on the oscillations in etablished regime, shown below, show the absence of the clipping effect and the purity of the oscillations. The maximum timestep was reduced for easier plotting of the now beautiful shape of the waveform.

<figure>
  <picture>
      <source srcset="{{ '/posts/op-amp-introduction/wien-with-agc-zoom.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
      <!-- <source srcset="{{ '/posts/op-amp-introduction/wien-with-agc-zoom-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/> -->
      <img src="{{ '/posts/op-amp-introduction/wien-with-agc-zoom-dark.png' | relative_url }}" style="width:75%;"/>
  </picture>
  <figcaption>Simulation setup for etablished regime waveform details.</figcaption>
</figure>

<figure>
  <picture>
      <source srcset="{{ '/posts/op-amp-introduction/wien-with-agc-zoom-plot.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
      <source srcset="{{ '/posts/op-amp-introduction/wien-with-agc-zoom-plot-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/>
      <img src="{{ '/posts/op-amp-introduction/wien-with-agc-zoom-plot.png' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Waveform details of a wien bridge oscillator with automatic gain control. No clipping is present.</figcaption>
</figure>

We have also additional simulations for another article, stay in touch.

### Comparators and positive feedback

With comparators, components used to compare two voltages and give a two state output (high or low), positive feedback is commonly used in the form of hysteresis for two reasons. 1/ Avoid multiple transitions in the case of noisy inputs. 2/ Decrease the output raise and fall times using the gain increase due to positive feedback.

However…… comparators are NOT operational amplifiers, and their use cases should not be mixed.

The following oscillator works in a comparator mode, which can be seen by the output taken discrete levels, and thus a comparator should be used for this schematic.

<figure>
  <picture>
      <source srcset="{{ '/posts/op-amp-introduction/rc-comp-oscillator.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
      <source srcset="{{ '/posts/op-amp-introduction/rc-comp-oscillator-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/>
      <img src="{{ '/posts/op-amp-introduction/rc-comp-oscillator.png' | relative_url }}" style="width:25%;"/>
  </picture>
  <figcaption>Schematic of an RC comparator oscillator circuit using positive feedback.</figcaption>
</figure>

<figure>
  <picture>
      <source srcset="{{ '/posts/op-amp-introduction/rc-comp-oscillator-plot.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
      <source srcset="{{ '/posts/op-amp-introduction/rc-comp-oscillator-plot-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/>
      <img src="{{ '/posts/op-amp-introduction/rc-comp-oscillator-plot.png' | relative_url }}" style="width:100%;"/>
  </picture>
  <figcaption>Output waveform of the RC comparator oscillator showing discrete voltage levels characteristic of comparator operation.</figcaption>
</figure>

Some sources on the internet use a 741 in this schematic. Don’t spread this mistake!

## Op-amps according to input stage (BJT, JFET, MOSFET)

Operational amplifiers differ not only according to which application they are optimized for, but also according to the transistor technology used in the input stage.

This choice directly affects the op-amp’s input impedance, input bias current, and noise behavior. For this reason, it is a critical design parameter, especially in sensor interfaces and precision measurement circuits.

### BJT-input op-amps

Thanks to their low input voltage noise and good matching characteristics, they provide an advantage when working with low-impedance sources.

In active-output sensors or low-impedance analog sources, noise performance is generally better.

On the other hand, since the input bias current is relatively high, they can lead to additional offset errors when used with high-impedance sources.

<figure>
<table class="images-table">
<tr>
<td>
  <picture>
    <source srcset="{{ '/posts/op-amp-introduction/bjt-amp-1.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
    <source srcset="{{ '/posts/op-amp-introduction/bjt-amp-1-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/>
    <img src="{{ '/posts//posts/op-amp-introduction/bjt-amp-1.png' | relative_url }}" style="width:100%;"/>
  </picture>
</td>
<td>
  <picture>
    <source srcset="{{ '/posts/op-amp-introduction/bjt-amp-2.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
    <source srcset="{{ '/posts/op-amp-introduction/bjt-amp-2-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/>
    <img src="{{ '/posts/op-amp-introduction/bjt-amp-2.png' | relative_url }}" style="width:100%;"/>
  </picture>
</td>
</tr>
</table>
<figcaption>Simplified schematics of a typical input of a BJT differential amplifier, from https://en.wikipedia.org/wiki/Differential_amplifier. Left use resistors as loads and right uses a better current mirror.</figcaption>
</figure>

### JFET-input op-amps

They provide much lower input bias current and high input impedance. With these characteristics, they are suitable for medium- and high-impedance sensors. Noise performance is generally weaker <!-- Voltage noise is indeed generally higher, however current noise is generally lower. --> than that of BJT-input op-amps, but in practice the low bias current may be more important. In this respect, JFET-input op-amps are considered a balanced option between BJT and CMOS.

### MOSFET (CMOS)-input op-amps

With extremely high input impedance and very low bias current, they are ideal for applications that require very high impedance and low power consumption.
Battery-powered systems and long-term DC measurements fall into this category. However, low-frequency noise (1/f noise) and temperature-dependent effects may be more pronounced; therefore, modern CMOS op-amps are often supported with zero-drift architecture.

A simplified schematic of a typical CMOS operational amplifier is shown below:

<figure>
  <picture>
    <source srcset="{{ '/posts/op-amp-introduction/fet-amp.png' | relative_url }}" media="(prefers-color-scheme: light)"/>
    <source srcset="{{ '/posts/op-amp-introduction/fet-amp-dark.png' | relative_url }}" media="(prefers-color-scheme: dark)"/>
    <img src="{{ '/posts/op-amp-introduction/fet-amp.png' | relative_url }}" style="width:75%;"/>
  </picture>
  <figcaption>Simplified schematic of a typical CMOS operational amplifier input stage from the OPA391 datasheet (<a href="https://www.ti.com/product/OPA391">https://www.ti.com/product/OPA391</a>).</figcaption>
</figure>

In summary, if the source impedance is low, a BJT input is preferred; for medium-to-high impedance sources, a JFET input; and for very high impedance and low power requirements, a CMOS input is generally the most suitable choice.

This distinction plays a decisive role in measurement accuracy and system stability, regardless of the op-amp type.

## Op-amp types according to application and performance purpose

Operational amplifiers do not consist of a single structure; they are designed by prioritizing specific characteristics in line with different application requirements

For this reason, op-amp types are classified not by how they operate, but by the intended use for which they are optimized.

This classification constitutes the first and most important elimination step when selecting the correct component 

### General-purpose op-amps

They offer balanced performance among bandwidth, noise, offset, and power consumption.

They are widely used in education, prototyping, and non-critical analog circuits. In most designs, the first op-amps tested belong to this group.

### Precision op-amps

They are designed for applications where DC accuracy is important, with low input offset voltage and low temperature drift.

Sensor interfaces, current measurement circuits, and front-end stages of high-resolution ADCs are typical application areas for this class.

High bandwidth is generally not a priority in these op-amps.

### Auto-zero op-amps

Auto-zero op-amps are based on the following principle (https://wiki.analog.com/university/courses/electronics/text/chapter-15):

<figure>
  <img src="{{ '/posts/op-amp-introduction/auto-zero.png' | relative_url }}" />
  <figcaption>Block diagram of an auto-zero operational amplifier showing the two amplifier stages and switching mechanism.</figcaption>
</figure>

They use internally two amplifiers and alternate between two modes:

* The correcting amplifier zeros itself by connecting their inputs together and adjusting its own compensation capacitor to compensate its own offset until it sees a zero at its input

* The correcting amplifier zeros the corrected amplifier by adjusting the compensation capacitor of the corrected amplifier to compensate its offset until it sees a zero at its input.

With this technique, offset and drift is reduced to very low values.

Usually, bipolar amplifiers are preferred when searching for low offsets. However, auto-zero amplifiers are often CMOS amplifiers because switches are much easier to realize in CMOS.

While they provide a maor advantage in measurement systems where DC accurary (offset) and long-term stability (offset drive) are critical, they exhibit switching noise and can also have more subtle issues, like recovery from overload (the correcting amplifiers trying to compensate the input difference even if it is not due to an offset). Pay attention to the datasheet.

### Audio op-amps

They are optimized for low distortion (deviation of the signal from the ideal waveform) and highly linear behavior within the human hearing band.

Total harmonic distortion (THD) (the ratio of harmonic frequency components present in the output signal that are not present at the input), output drive capability, and linearity are prioritized; absolute DC accuracy is often of secondary importance.

They are preferred in audio signal chains.

### High-speed op-amps

They are developed for applications requiring wide bandwidth and high slew rate. Video signals, fast data acquisition systems, and high-frequency analog processing fall into this category.

These op-amps are more sensitive to layout, feedback network design, and stability issues.

### Current-feedback amplifiers (CFA)

<!-- TODO: more pictures. -->

<!-- Belong in theory to input stage, but better here. -->

They use a different architecture from voltage-feedback op-amps.

While voltage-feedback amplifiers have their output depending on the difference between the voltages at their inputs, current feedback amplifier apply on their IN- terminal the voltage they get on their IN+ input and have their output depending on the **current** flowing in the IN- input.

Voltage feedback amplifiers are usually compensated to be stable when used as unity gain followers, a more difficult situation for stability than amplifiers having a gain higher than unity, since the feedback for unity gain is higher. When such amplifiers ar used for higher gains, they are clearly over-compensated, which reduced their performance.

On the contrary, with current feedback amplifiers, compensation is adjusted using the feedback resistor, so it has the right value when using higher gains.

This is one of the reason they are very popular, and also why this feedback resistor must have the value recommended by the manufacturer.

The need of a rather low feedback resistance seems inconvenient, but current feedback amplifiers are almost always used for high-speed design where voltage feedback amplifiers would also need a low feedback resistances to avoid the effects of input capacitances. Indeed, in some circuits, both families are in practice almost interchangeable.

For instance, the differential amplifier which gave me the opportunity to write this note ([{{"/posts/diff-amp-equations.html" | relative_url }}]({{"/posts/diff-amp-equations.html" | relative_url }})), used actually an ADA4927 which is a **current feedback** amplifier, but for some reason the demo circuit used in the webpage uses an ADA4937 which is a **voltage feedback** amplifier. But this works well because:

* both have the same footprints, even if not relevant for an LTSpice simulation,

* the recommended feedback resistor value for the current feedback amplifiers are often in the range of recommanded values of high-speed voltage amplifiers, and

* feedback allows to have a similar circuit work with both types: input current or voltage is low enough for calculations.

The feedback **must** be resistive, at least the resistive part of it must be dominant. **Never** directly a capacitor as a feed back.

Slew rates are also faster than voltage-feedback op-amps. In voltage-feedback amplifiers, the output current of the first stage is limited by the current source which in combination with the compensation capacitor limits the slew rage. On the contrary, in current-feedback ampflifiers, this current is directly fed by the user. More details can be found in [https://www.analog.com/en/resources/analog-dialogue/articles/current-feedback-amplifiers-1.html](https://www.analog.com/en/resources/analog-dialogue/articles/current-feedback-amplifiers-1.html).

## Op-amp input stage headroom according to structure

This one is often overlooked but pay attention to this. With some training, it is possible to see at a first glance on the equivalent schematics an idea of the inputs headrooms.

###	N input stage

https://www.ti.com/lit/ds/symlink/tl081.pdf

<figure>
  <img src="{{ '/posts/op-amp-introduction/tl081.png' | relative_url }}" />
  <figcaption>Simplified schematic of the TL081 operational amplifier showing N-channel JFET input stage.</figcaption>
</figure>

Both transistors are source followers trying to apply to their source their input minus some voltage. Guess something between 1 V and 2 V. The current source needs also some headroom. On the other side, there is not so much constraint between the input and the drain.

So, the input range can be inferred as: V- + headroom to Vcc. And indeed the datasheet:

<figure>
  <img src="{{ '/posts/op-amp-introduction/tl081-datasheet.png' | relative_url }}" />
  <figcaption>TL081 datasheet specification showing input voltage range extending from ground + headroom to slightly above Vcc.</figcaption>
</figure>

Input range: ground + headrom to slightly higher than Vcc.
<!-- TODO: add explanation. -->

### P input stage

<!-- TODO: add explanations. -->

<figure>
  <img src="{{ '/posts/op-amp-introduction/p-input.png' | relative_url }}" />
  <figcaption>Simplified schematic showing P-channel input stage configuration with input range from slightly below ground to Vcc - headroom.</figcaption>
</figure>

Input range: slightly lower than ground to Vcc – headroom.

<!-- TODO: add explanation. -->

### N+P input stage

<!-- TODO: Write stuff. -->

https://e2e.ti.com/blogs_/archives/b/thesignal/posts/rail-to-rail-inputs-what-you-should-know

<figure>
  <img src="{{ '/posts/op-amp-introduction/n-p-input.png' | relative_url }}" />
  <figcaption>Rail-to-rail input stage combining both N-channel and P-channel devices for extended input voltage range.</figcaption>
</figure>

### Input supplied with charge pump

https://e2e.ti.com/blogs_/archives/b/thesignal/posts/rail-to-rail-inputs-what-you-should-know

<figure>
  <img src="{{ '/posts/op-amp-introduction/charge-pump-input.png' | relative_url }}" />
  <figcaption>Charge pump circuit used to extend input voltage range beyond supply rails.</figcaption>
</figure>

https://www.ti.com/product/OPA391

<figure>
  <img src="{{ '/posts/op-amp-introduction/opa391-input.png' | relative_url }}" />
  <figcaption>OPA391 operational amplifier input stage schematic showing charge pump implementation.</figcaption>
</figure>

## Basic op-amp parameters

Op-amp parameters describe the extent to which the amplifier deviates from ideal behavior.

None of these parameters is “good” or “bad” on its own; what matters is which one is decisive for a given application

### Availability

Cost, distributors, delays, MOQ, …

<!-- TODO: continue. -->

###	Convenience stuff

Packages, ...

<!-- TODO: continue. -->

### (Input) offset Voltage

It is the small differential input voltage required for the output to be exactly zero when the op-amp inputs are theoretically at the same voltage.

In other words, it is a DC error arising from the op-amp’s internal imbalance.

<figure>
  <img src="{{ '/posts/op-amp-introduction/offset.png' | relative_url }}" />
  <figcaption>Simulation schematic and output waveform of a LT1010 buffer with input offset voltage.</figcaption>
</figure>

#### Applications for which this parameter is critical

* Low-level DC measurements.

* Sensor interfaces.

* Current sensing.

* Bridge circuits.

#### Applications for which this parameter is secondary

* AC-coupled circuits.

* Audio signal processing.

* High-amplitude signals.

#### Disadvantages of good values

* Very low offset generally implies a more complex internal architecture and higher cost.

### Input (dynamic) resistance

The input (dynamic) resistance of an operational amplifier circuit should be high enough compared to the output impedance of the signal source to avoid loading it.

In inverting or substracting amplifiers, this input resistance is determined mostly by the resistors of the network, which must be carefully selected: not too big to avoid loading the signal source and not too high to avoid noise and issues with parasitic capacitances.

When the signal source is directly connected at the input of an operational amplifier, the impedance it sees it directly determined by the operational amplifier input impedance, so it is an important parameter to check in these cases with an high-impedance source.

According to https://www.ti.com/lit/an/sloa011b/sloa011b.pdf, the input resistances and capacitances of an operational amplifier are as follows:

<figure>
  <img src="{{ '/posts/op-amp-introduction/resistances.png' | relative_url }}" />
  <figcaption>Operational amplifier input resistance model showing differential (Rd) and common-mode (Rn, Rp) components.</figcaption>
</figure>

Datasheets give the elements between the inputs and the elements to ground in different ways.

In the LM324 datasheet (https://www.ti.com/lit/ds/symlink/lm324.pdf), the differential-mode input resistance rid = Rd || (Rn + Rp) and the common-mode ric = Rp || Rn are given:

<figure>
  <img src="{{ '/posts/op-amp-introduction/lm324-datasheet.png' | relative_url }}" />
  <figcaption>LM324 datasheet showing differential-mode input resistance (rid) and common-mode input resistance (ric) specifications.</figcaption>
</figure>

The common mode resistance is 400 times higher than the differential due to the operation of the input stage, which is a common behaviour.

The common-mode is indeed much higher than the differential mode.

In the NE5532 datasheet (https://www.ti.com/lit/ds/symlink/ne5532.pdf), the impedance of one input when the other is tied to ground, called single-ended in the jargon, ri = Rd || Rn is given.

<figure>
  <img src="{{ '/posts/op-amp-introduction/ne5532-datasheet.png' | relative_url }}" />
  <figcaption>NE5532 datasheet specification for single-ended input resistance (ri) measurement configuration.</figcaption>
</figure>

No information is given on the common-mode, but is can be reasonably guessed for most purposes that ri ≈ Rd and that Rp and Rn are much higher than Rd.

Due to feedback, the effective input resistance will be higher, but this is still a low value for an op-amp. This is because this operational amplifier is optimized for low-noise.

Most often this value is a check of being in the right ballpark for the use rather than a precise calculation. Here, this amplified is clearly suited only for low input impedances.

When this parameter is important, for DC or near DC, pay attention also to the bias current, and for higher frequencies, pay attention also to the capacitances. For the values of the LM324, the common-mode capacitance starts to dominate the differential-mode resistance from only 11 kHz.

#### Advantages of high input resistance

* The signal source is not loaded

* The measured voltage is transferred to the op-amp without distortion

* High-impedance sensors (e.g., thermistors, piezo elements, electrodes) can be read correctly

#### Disadvantages of high input resistance

* Higher 1/f noise is generally observed in MOSFET/CMOS inputs

#### Beware of

*	Bias currents

*	Capacitances

* Static electricity (whole circuit, not just the op-amp, often including ESD protection)

*	Leakage currents (rather due to the need for high impedance than due to the op-amp)

* PCB contamination and humidity (idem)

### (Input) offset drift

Input offset drive belong to two main categories: thermal drift, depending on temperature, and time drift, which is a longer term aging.

Thermal drive is typically specified in µV/°C.

Time drift is often specified in µV/month or µV/1000 hours. However, **these units can be misleading**. Since aging is a random walk ("drunkard's walk") phenomenon, it is proportional to the **square root** of the elapsed time (https://www.analog.com/media/en/training-seminars/tutorials/MT-037.pdf)[https://www.analog.com/media/en/training-seminars/tutorials/MT-037.pdf] and 1 µV/1000 hour actually corresponds to 3 µV/year instead of 9 µV/year.

#### Applications for which this parameter is critical

* Long-term measurements.

* Industrial and field systems operating over a wide temperature range.

#### Applications for which this parameter is of secondary importance

* Short-term systems with stable temperature.

#### Disadvantage

* Very low drift often requires zero-drift or chopper architecture, which can generate additional low-frequency noise.

### Input Bias Current

It is the small DC current that flows from the inputs to enable the operation of the op-amp’s input transistors.

#### Applications for which this parameter is critical

* High-impedance sensors.

* Piezoelectric elements.

* Circuits operating with large-value resistors.

#### Applications for which this parameter is of secondary importance

* Low-impedance sources (e.g., <1 kΩ).

#### Disadvantages of good parameter values

* Very low bias current is usually achieved with MOSFET/JFET inputs, which in some cases leads to higher 1/f noise.

### CMRR (common-mode rejection ratio)

The CMRR of an amplifier circuit is the ratio between its differential-mode gain and its common-mode gain, expressing its ability to extract a small differential signal superposed to a big common-mode signal.

Before even looking at the datasheet, it should be emphasized that bit factor in the CMRR (or the lack of) is the topology of the circuit and the mismatch of the resistors. Most operational amplifiers have CMRR higher than 70 dB while common resistors are closer to 1 % tolerance. Solutions exists to overcome this point, like the classical 3 operational amplifier differential amplifier, but must be studied carefully before even having a look on the CMRR number of the datasheet.

#### Applications for which this parameter is critical

* Differential measurements.

* Current sensing.

* Noisy industrial environments.

#### Applications for which this parameter is of secondary importance

* Simple, ground-referenced single-ended amplifiers.

#### Beware of

* In practice, CMRR depends not only on the op-amp but also on the matching of external resistors. The datasheet value cannot always be achieved in the system.

### <span id="power-supply-rejection-ratio">PSRR (power supply rejection ratio)</span>

The power supply rejection ratio (PSRR) is the ratio of the variations of the input/output of an operational amplifier relative to the variation of their power supplies.

According to https://www.analog.com/media/en/training-seminars/tutorials/MT-043.pdf which gives lots of valuable explanations on this topic, this quantity should named PSRR when expressed in linear units, and PSR when expressed in dB, but nobody seems to follows exactly this convention.

This quantity can be referred either to the input or to the output, so the datasheet must be read carefully, as advised in https://www.analog.com/media/en/training-seminars/tutorials/MT-043.pdf. However, this precision of sometimes forgotten from the datasheet itself, like in this one from their own colleagues: https://www.analog.com/media/en/technical-documentation/data-sheets/op1177_2177_4177.pdf .

So, in doubt, assume worst case for your circuit between input and outpout.

PSRR can be measured and specified either for the positive supply, either for the negative supply, or for a symmetrical change in both supply. The latter case is often seen but not realistic, because noise on both supplies is likely to be different. In this last case, since the middle of both supplies is likely to move also, not only the "symmetrical PSRR" but also the CMRR must be taken into account for a detailed calculation. Anyway, both quantities have similar origins and similar values.

#### Applications where this parameter is critical

* Battery-powered switching power supplies, typically used with low voltage batteries or when multiple voltages are needed.

* Noisy supply rails, either due to the supply of due to the loads.

#### Applications where this parameter is of secondary importance

* Well-regulated, low-noise laboratory power supplies.

#### Disadvantage of good parameter values

* High PSRR generally requires a more complex internal circuit structure.

### Gain–bandwidth product (GBW)

It defines the fundamental limit between gain and frequency of the op-amp; as gain increases, the usable bandwidth decreases.

#### Applications where this parameter is critical

* Wideband signals.

* Fast control loops.

* Video and high-speed analog processing.

#### Applications where this parameter is of secondary importance

* Slowly varying DC measurements.

#### Disadvantage of good parameter values

* Unnecessarily high GBW can lead to excess noise <!-- TODO: why ? --> and stability problems<!-- TODO: why ? -->.

### Slew rate

It is the maximum rate at which the output voltage can change over time (V/µs).

#### Applications where this parameter is critical

* High-frequency or high-amplitude signals.

#### Applications where this parameter is of secondary importance

* Low-frequency and slowly varying signals.

#### Disadvantage of good parameter values

* High slew rate often comes with higher power consumption.

<!-- TODO: LTSpice simulation. -->

<figure>
  <img src="{{ '/posts/op-amp-introduction/slew-rate.png' | relative_url }}" />
  <figcaption>Illustration of slew rate limitation showing how finite slew rate causes waveform distortion in high-frequency signals.</figcaption>
</figure>
**Source:** https://toshiba.semicon-storage.com/eu/semiconductor/knowledge/faq/linear_opamp/what-is-the-maximum-frequency-at-which-an-op-amp-can-be-used.html

### Noise

<!-- TODO: Add voltage and current noise. -->

Noise consists of unwanted random signal components generated internally by the op-amp; it includes wideband noise and low-frequency 1/f noise <!-- TODO for Hadrien: improve this. -->.

#### Applications where this parameter is critical

* Low-level signals.

* High-impedance sources.

* Precision measurements.

#### Applications where this parameter is of secondary importance

* High-amplitude or digitally dominated systems.

#### Disadvantage of good parameter values

* Low noise is often achieved at the expense of power consumption or bandwidth.

### Headroom

Headroom expresses how close the op-amp inputs and outputs can approach the supply rails.

#### Applications where this parameter is critical

* Single low-voltage supply with non–rail-to-rail amplifiers; insufficient headroom leads to signal clipping and loss of linear behavior.

#### Applications where this parameter is of seconrady importance

* Wide dual-supply (±12 V, ±15 V) circuits operating far from the rails.

### Summary

Op-amp selection is not about making all parameters "the best".

Correct design means prioritizing the parameters that are critical for the application and keeping the others at a sufficient level.

References: [1], [2], [3], [6]

## Op-amps according to output types

The output stage of an op-amp determines how the amplified signal is presented, with respect to which reference it is defined, and which loads it can drive.

Although often overlooked, the output type directly affects design success, especially at low supply voltages, when driving ADCs, and in digital–analog interfaces.

### Single-ended vs. fully differential output

Most operational amplifies have a single signal output, configuration called "single-ended output". This output is often referred to the ground. While amplifiers used with a single supply are connected to this ground and to the positive supply, amplifiers used with a dual supply are connected to the negative and to the positive supply voltages, but almost never directly to the ground.

So, and particularly in cases where the supply voltages move for whatever reason like noise, which is the reference actually used by the operational amplifier ?

Turns out that this question depends a lot on the internal structure, can even be different between input and output stages, and even depends on the common-mode input voltage and output voltage for rail-to-rail operational amplifiers.

So, for pratical purposesn, the reference can be considered as being the ground, the power supplies must be decoupled to it, and the PSRR (see section <a href="#power-supply-rejection-radio">power supply rejection ratio</a>) must be checked because this ratio will precisely tell to which extents your "ground reference" hypothesis is accurate.

Single-ended output operational amplifiers are obviously sufficient when only a single-ended output is needed, but sometimes a differential output is needed, to drive either a differential wire or some component needing a differential input.

Multiple single-ended ampilfiers can be used in this case, but this solution is not perfect:

* need of multiple components,

* amplitude matching between outputs,

* phase matching, particularly at higher frequencies, and

* output impedane mismatch.

For these cases, fully-differential output operational amplifiers can be used. They have directly a differential output, plus a Vocm input to set up the common-mode range.

An example circuit using a fully differential amplifier is given in ([{{"/posts/diff-amp-equations.html" | relative_url }}]({{"/posts/diff-amp-equations.html" | relative_url }})).

#### Typical applications of single-ended output operational amplifiers

* Single-ended output, even if the input is differential

* Differential outputs with other needs like low cost, availability of the components, and other special characteristics

* Various convenience considerations like circuits having already single-ended amplifiers (BOM) or use of multiple units packages

#### Typical applications of fully differential output operational amplifiers

* Circuits with a differential output needing matching between their outputs

* Drivers for differential ADC inputs

* Drivers for differential RF mixers

* Drivers for differential pair cables

* Interfaces between two differential circuits with different common-mode voltages

### Push-pull output

The push-pull output stage is an active structure capable of driving a load by both sourcing and sinking current. The output voltage is actively controlled by the op-amp in both the upward and downward directions. In most classical op-amps, this structure is implemented as Class AB.

#### Typical applications

* Linear analog amplifiers

* ADC input drivers

* Low-impedance loads

* Analog signal processing chains

#### Advantages

* Suitable for linear signal generation

* No external pull-up or additional components required

* Can both source and sink current

* Low output impedance

#### Disadvantages

* Output swing may be reduced at high currents

#### In summary

Push-pull output is the default and most general solution for analog op-amps.

### Open-drain (open-collector) output

This one is a trap.

Often, operational amplifiers and comparators are confused due to their common points despite important differences in their internal construction and operation.

If some IC you want to use as an operational amplifier has an open-drain or open-collector output, this is the sign it is instead a comparator and that it should not be used in operational amplifier circuits without a true good reason. Details on this point are given in the <a href="#operational-amplifiers-vs-comparators">operational amplifiers vs. comparators</a> section.

### Rail-to-rail output

Rail-to-rail output refers to the ability of the op-amp output voltage to swing very close to the supply rails. This feature becomes especially critical at low supply voltages.

### Conclusion on output types

The output type determines not how many volts an op-amp amplifies, but under which conditions and with which system compatibility those volts are delivered.

Choosing the correct output type is the key to system-level performance and stability.

References: [1], [3], [6], [7].

#### Typical applications

* Battery-powered devices

* Circuits requiring full-scale ADC utilization

#### Advantages

* More efficient use of the supply voltage

* Increased dynamic range

* More flexible design under low supply voltages

#### Disadvantages

* Rail-to-rail behavior depends on load current

* Reaching the exact rails is usually not ideal

* More complex internal architecture (may increase noise <!-- TODO for Hadrien: check a bit this one. Usually noise is more dependent on input, but often rail-to-rail is wanted in both sides. --> or cost)

* Beware of open loop output impedance. Non rail to rail output stages use voltages followers with low impedance but high headroom while rail to rail output stages use corrent sources with low headroom but high impedance. The circuits often used to properly bias both positive and negative sides of the output stage makes also the frequency behavior a bit strange. Feedback makes the closed loop impedance low, but the output impedance can cause stability issues with unconvenient loads like capacitors.

#### In summary

Rail-to-rail output is not a simple "yes/no" feature, but a condition-dependent capability; the datasheet must be examined carefully.

## Common traps

### <span id="operational-amplifiers-vs-comparators">Operational amplifiers vs. comparators</span>

Altough they look like similar, operational amplifiers and comparators are very different components.

Operational amplifiers are designed to work in a linear operation, with the difference between their inputs low, due to the effect of a negative feedback. They sometimes can handle other cases, particularly in transients or during input overload, but such cases are not their intended mode of operation. Negative feedback is used to set the gain and ensure linearity.

Quite the contrary, comparators are designed to work in a nonlinear way, with an high difference between their input, and are designed to produce a constant value, near one of the supply rails, depending on the sign of the difference. Positive feedback is used to help the comparator to transition quicker from one state to another.

These differences in the intended operation lead to the following differences of what is inside:

* Operational amplifiers have an internal compensation capacitor (1/3 of the chip area of the original 741 !) to help stability when used with negative feedback while this would be a strange idea for comparators using positive feedback.

* Slew rate of comparators is much higher than of operational amplifiers.

* Comparators have often what could be called "logic convenience": rail-to-rail outputs, open drain output, ...

Confusing them is a great way to fail your circuit, don't fail in this trap.

### Capacitive load, stability

See article on this subject:  <a href="{{ '/posts/op-amp-capacitor-stability.html' | relative_url }}">{{ '/posts/op-amp-capacitor-stability.html' | relative_url }}</a>.

### Botched current measurement circuits

A typical current measurement circuit uses a current measurement resistor on a 5 V rail accross which the voltage difference is about 10 mV to ensure not too much power is dissipated in the resistor and to ensure the voltage drop stays reasonable. Assuming a 10 % full scale accuracy, which is already a bad accuracy, this would lead to a needed common-mode rejection ratio of at least 5 000. Naive circuit using even 1 % resistors are much likely to not meet this target.

Another way to botch current measurement circuits is to ignore the input range. Input common-mode range include often the supply voltage of the operational amplifier, and can be in some cases even higher, like for instance when measuring the current on a 50 V rail using a 5 V operational amplifier.

Solutions exists to overcome these problems. They are outside the scope of this introduction article. But we give just an advice: study well the applications notes on this topic before even thinking.

### Operational amplifiers without ESD protection

Some people are tempted to use operational amplifiers with ESD protection removed for increased performance. Don’t. Even. Think. Of. It.

## Care and feeding

### Decoupling, dual supply case

Operational amplifiers, particularly higher speed ones, should be decoupled like any other component.

Even if most operational amplifiers don't have a ground pin but just two supply voltages, in most cases, their supply voltages must be both decoupled to ground because the load will be referenced to the ground or to another voltage itself decoupled to ground.

For this reason a mere decoupling between both supplies is insufficient, even more when taking into account the layout issues.

<figure>
  <img src="{{ '/posts/op-amp-introduction/decoupling.png' | relative_url }}" />
  <figcaption>Proper decoupling capacitor placement for dual-supply operational amplifier showing separate capacitors to ground for each supply.</figcaption>
</figure>

The capacitor must have a low enough total inductance, including own ESL and traces, to handle the current spikes caused by high slew rates. And he must be high enough to provide the lower frequency transients while the current ramp up in the power supply inductor, mostly the inductor of the supply distribution.

A long time ago, this would have been made using capacitors of several values. Now, available capacitor values in a given size has increased much.

So, the go-to strategy is always the same: select the capacitor size consistent with the component to decouple (similar to pin sizes) and select the highest convenient available value in this size, maybe with some rounding.

</div>

### Decoupling, single supply case

Same principles as before, but even more simple. One of the supplies, almost always the negative one, is tied to the ground plane. The other is decoupled as usual. From a layout point of view, dont try to decouple "between the supplies": tie the grounded one to the ground plane and decouple the other to the ground plane.

### Filtering of mid-supply reference

This problem is not often explained. Beginners will simply forget it and experts will do it without even thinking about it.

In single-supply operational amplifiers, since there are no convenient negative values, a common practice is to center them around the middle of the supplies. This is often performed with a voltage divider. The problem of a naive voltage divider is that it amplifies any noise on the voltage supplies. It is a shame to use operational amplifiers with power supply rejection ratios (PSRR) much higher than 60 dB and getting eventually only 6 dB due to such mistakes.

Solutions to this problem can be summarized as follows:

* filter the mid-supply voltage divider,

* use a regulator to provide the mid-supply voltage (Zener or linear).

This application note from Analog Devices [https://www.analog.com/en/resources/app-notes/an-581.html](https://www.analog.com/en/resources/app-notes/an-581.html) provides a good summary of the problem, as well as valuable hints to solve it. However, a few points are more questionable:

* star grounding is often a bad practice and need some care to properly perform in the rare cases it is useful;

* the low-pass cut-off frequency of the decoupling of the mid-supply reference is not so much a problem in robust circuits because 1/ supplies are often the output of a regulator who will take care of these low frequencies and 2/ such schemes are often coupled in such ways which limit this issue (AC coupled or kind differential).

The following schematic shows the previous points:

* Mid-voltage reference it not filtered. Since the analog to digital converter of the arduino use the Vcc as a reference voltage, filtering this alone would not bring much improvement. Adding some filtering in this case would have needed a little more work than just filtering the mid-supply.

* Chain of operational amplifiers U1A to U1C are wired in a pseudo-differential configuration, all using the same reference, so the supply gain is only 1/2.

<figure>
  <img src="{{ '/posts/op-amp-introduction/ultrasonic-pcb.svg' | relative_url }}" />
  <figcaption>Ultrasonic sensor circuit showing operational amplifier chain U1A-U1C in pseudo-differential configuration with unfiltered mid-supply reference.</figcaption>
</figure>

## References

[1] R. Mancini (Ed.), Op Amps for Everyone, Texas Instruments, SLOD006B, 2002.

[2] P. Horowitz, W. Hill, The Art of Electronics, 3rd Edition, Cambridge University Press, 2015.

[3] A. S. Sedra, K. C. Smith, Microelectronic Circuits, 7th Edition, Oxford University Press, 2014.

[4] Texas Instruments, Current Feedback vs Voltage Feedback Amplifiers, Application Report.

[5] Analog Devices, Op Amp Input Structures: BJT, JFET, CMOS, Technical Article.

[6] Texas Instruments, Understanding Rail-to-Rail Input and Output Amplifiers, Application Note.

[7] Texas Instruments, Fully Differential Amplifiers, Application Report.

[8] IFE - TU Graz, Differential amplifiers - basics, principle, common and differential mode gains, ideal vs. real, CMRR [https://www.youtube.com/watch?v=4PYjRmtSth8](https://www.youtube.com/watch?v=4PYjRmtSth8)

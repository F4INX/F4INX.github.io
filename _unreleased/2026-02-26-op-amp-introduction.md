---
layout: post
title: A (not so) gentle introduction to operational amplifiers.
permalink: /posts/op-amp-introduction.html
last_modified_at: 2026-02-26
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
  <img src="{{ '/posts/op-amp-intro/auto-zero.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

They use internally two amplifiers and alternate between two modes:

* The correcting amplifier zeros itself by connecting their inputs together and adjusting its own compensation capacitor to compensate its own offset until it sees a zero at its input

* The correcting amplifier zeros the corrected amplifier by adjusting the compensation capacitor of the corrected amplifier to compensate its offset until it sees a zero at its input.

With this technique, offset and drift is reduced to very low values.

Usually, bipolar amplifiers are preferred when searching for low offsets. However, auto-zero amplifiers are often CMOS amplifiers because switches are much easier to realize in CMOS.

While they provide a maor advantage in measurement systems where DC accurary (offset) and long-term stability (offset drive) are critical, they exhibit switching noise and can also have more subtle issues, like recovery from overload (the correcting amplifiers trying to compensate the input difference even if it is not due to an offset). Pay attention to the datasheet.

<!-- TODO: Have a look on the most common pitfalls of auto-zero opamps. -->

### Chopper op-amps

<!-- TODO: write on these, often confused with the auto-zero. -->

### Audio op-amps

They are optimized for low distortion (deviation of the signal from the ideal waveform) and highly linear behavior within the human hearing band.

Total harmonic distortion (THD) (the ratio of harmonic frequency components present in the output signal that are not present at the input), output drive capability, and linearity are prioritized; absolute DC accuracy is often of secondary importance.

They are preferred in audio signal chains.

### High-speed op-amps

They are developed for applications requiring wide bandwidth and high slew rate. Video signals, fast data acquisition systems, and high-frequency analog processing fall into this category.

These op-amps are more sensitive to layout, feedback network design, and stability issues.

### Current-feedback amplifiers (CFA)

<!-- Belong in theory to input stage, but better here. -->

They use a different architecture from classical voltage-feedback op-amps.

Bandwidth is largely independent of gain, and very high slew rates can be achieved. On the other hand, the values of feedback components must be selected in accordance with manufacturer recommendations. <!-- TODO: reformulate this. -->

<!-- From Hadrien: I know them very well, let me this one. :) -->

## Op-amp input stage headroom according to structure

This one is often overlooked but pay attention to this. With some training, it is possible to see at a first glance on the equivalent schematics an idea of the inputs headrooms.

###	N input stage

https://www.ti.com/lit/ds/symlink/tl081.pdf

<figure>
  <img src="{{ '/posts/op-amp-intro/tl081.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

Both transistors are source followers trying to apply to their source their input minus some voltage. Guess something between 1 V and 2 V. The current source needs also some headroom. On the other side, there is not so much constraint between the input and the drain.

So, the input range can be inferred as: V- + headroom to Vcc. And indeed the datasheet:

<figure>
  <img src="{{ '/posts/op-amp-intro/tl081-datasheet.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

Input range: ground + headrom to slightly higher than Vcc.
<!-- TODO: add explanation. -->

### P input stage

<!-- TODO: add explanations. -->

<figure>
  <img src="{{ '/posts/op-amp-intro/p-input.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

Input range: slightly lower than ground to Vcc – headroom.

<!-- TODO: add explanation. -->

### N+P input stage

<!-- TODO: Write stuff. -->

https://e2e.ti.com/blogs_/archives/b/thesignal/posts/rail-to-rail-inputs-what-you-should-know

<figure>
  <img src="{{ '/posts/op-amp-intro/n-p-input.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

### Input supplied with charge pump

https://e2e.ti.com/blogs_/archives/b/thesignal/posts/rail-to-rail-inputs-what-you-should-know

<figure>
  <img src="{{ '/posts/op-amp-intro/charge-pump-input.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

https://www.ti.com/product/OPA391

<figure>
  <img src="{{ '/posts/op-amp-intro/opa391-input.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
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

**Critical applications:** low-level DC measurements, sensor interfaces, current sensing, bridge circuits.

**Of secondary importance:** AC-coupled circuits, audio signal processing, high-amplitude signals.

**Disadvantage:** very low offset generally implies a more complex internal architecture and higher cost.

<figure>
  <img src="{{ '/posts/op-amp-intro/offset.png' | relative_url }}" />
  <figcaption>Output waveform of a noninverting amplifier when there is input offset voltage.</figcaption>
  <!-- TODO: rework caption. -->
</figure>

<!-- TODO: add source. -->

### Input (dynamic) resistance

The input (dynamic) resistance of an operational amplifier circuit should be high enough compared to the output impedance of the signal source to avoid loading it.

In inverting or substracting amplifiers, this input resistance is determined mostly by the resistors of the network, which must be carefully selected: not too big to avoid loading the signal source and not too high to avoid noise and issues with parasitic capacitances.

When the signal source is directly connected at the input of an operational amplifier, the impedance it sees it directly determined by the operational amplifier input impedance, so it is an important parameter to check in these cases with an high-impedance source.

According to https://www.ti.com/lit/an/sloa011b/sloa011b.pdf, the input resistances and capacitances of an operational amplifier are as follows:

<figure>
  <img src="{{ '/posts/op-amp-intro/resistances.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

Datasheets give the elements between the inputs and the elements to ground in different ways.

In the LM324 datasheet (https://www.ti.com/lit/ds/symlink/lm324.pdf), the differential-mode input resistance rid = Rd || (Rn + Rp) and the common-mode ric = Rp || Rn are given:

<figure>
  <img src="{{ '/posts/op-amp-intro/lm324-datasheet.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

The common mode resistance is 400 times higher than the differential due to the operation of the input stage, which is a common behaviour.

The common-mode is indeed much higher than the differential mode.

In the NE5532 datasheet (https://www.ti.com/lit/ds/symlink/ne5532.pdf), the impedance of one input when the other is tied to ground, called single-ended in the jargon, ri = Rd || Rn is given.

<figure>
  <img src="{{ '/posts/op-amp-intro/ne5532-datasheet.png' | relative_url }}" />
  <!-- <figcaption>TODO: title</figcaption> -->
</figure>

No information is given on the common-mode, but is can be reasonably guessed for most purposes that ri ≈ Rd and that Rp and Rn are much higher than Rd.

Due to feedback, the effective input resistance will be higher, but this is still a low value for an op-amp. This is because this operational amplifier is optimized for low-noise.

Most often this value is a check of being in the right ballpark for the use rather than a precise calculation. Here, this amplified is clearly suited only for low input impedances.

When this parameter is important, for DC or near DC, pay attention also to the bias current, and for higher frequencies, pay attention also to the capacitances. For the values of the LM324, the common-mode capacitance starts to dominate the differential-mode resistance from only 11 kHz.

Advantages of high input resistance

* The signal source is not loaded

* The measured voltage is transferred to the op-amp without distortion

* High-impedance sensors (e.g., thermistors, piezo elements, electrodes) can be read correctly

Disadvantages of high input resistance

* Higher 1/f noise is generally observed in MOSFET/CMOS inputs

Beware of

*	Bias currents

*	Capacitances

* Static electricity (whole circuit, not just the op-amp, often including ESD protection)

*	Leakage currents (rather due to the need for high impedance than due to the op-amp)

* PCB contamination and humidity (idem)

### (Input) offset drift

<!-- TODO: Add a comment about thermal drift vs. time drift. -->

It is the rate at which the input offset voltage changes with temperature (typically µV/°C).

**Critical applications:** long-term measurements, industrial and field systems operating over a wide temperature range.

**Of secondary importance:** short-term systems with stable temperature.

**Disadvantage:** very low drift often requires zero-drift or chopper architecture, which can generate additional low-frequency noise.

### Input Bias Current

It is the small DC current that flows from the inputs to enable the operation of the op-amp’s input transistors.

**Critical applications:** high-impedance sensors, piezoelectric elements, circuits operating with large-value resistors.

**Of secondary importance:** low-impedance sources (e.g., <1 kΩ).

**Disadvantage:** very low bias current is usually achieved with MOSFET/JFET inputs, which in some cases leads to higher 1/f noise.

### CMRR (common-mode rejection ratio)

It is a measure of how well the op-amp can suppress signals that are common to both inputs (common-mode signals).

**Critical applications:** differential measurements, current sensing, noisy industrial environments.

**Of secondary importance:** simple, ground-referenced single-ended amplifiers.

**Disadvantage:** in practice, CMRR depends not only on the op-amp but also on the matching of external resistors; <!-- TODO for Hadrien: add details. --> the datasheet value cannot always be achieved in the system.

### PSRR (power supply rejection ratio)

It expresses how much fluctuations in the supply voltage are reflected at the output.

**Critical applications:** battery-powered systems, switching or noisy power supplies.

**Of secondary importance:** well-regulated, low-noise laboratory power supplies.

**Disadvantage:** high PSRR generally requires a more complex internal circuit structure.

### Gain–bandwidth product (GBW)

It defines the fundamental limit between gain and frequency of the op-amp; as gain increases, the usable bandwidth decreases.

**Critical applications:** wideband signals, fast control loops, video and high-speed analog processing.

**Of secondary importance:** slowly varying DC measurements.

**Disadvantage:** unnecessarily high GBW can lead to excess noise <!-- TODO: why ? --> and stability problems <!-- TODO: why ? -->.

### Slew rate

It is the maximum rate at which the output voltage can change over time (V/µs).

**Critical applications:** high-frequency and high-amplitude signals.

**Of secondary importance:** low-frequency and slowly varying signals.

**Disadvantage:** high slew rate often comes with higher power consumption

<!-- TODO: LTSpice simulation. -->

<figure>
  <img src="{{ '/posts/op-amp-intro/slew-rate.png' | relative_url }}" />
  <figcaption>Slew-induced waveform distortion.</figcaption>
  <!-- TODO: Rework figure caption. -->
</figure>
**Source:** https://toshiba.semicon-storage.com/eu/semiconductor/knowledge/faq/linear_opamp/what-is-the-maximum-frequency-at-which-an-op-amp-can-be-used.html

### Noise

<!-- TODO: Add voltage and current noise. -->

Noise consists of unwanted random signal components generated internally by the op-amp; it includes wideband noise and low-frequency 1/f noise <!-- TODO for Hadrien: improve this. -->.

**Critical applications:** low-level signals, high-impedance sources, precision measurements.

**Of secondary importance:** high-amplitude or digitally dominated systems.

**Disadvantage:** low noise is often achieved at the expense of power consumption or bandwidth.

### Headroom

Headroom expresses how close the op-amp inputs and outputs can approach the supply rails.

**Critical applications:** it is a critical parameter in single-supply, low-voltage, and non–rail-to-rail designs; insufficient headroom leads to signal clipping and loss of linear behavior.

In wide dual-supply (±12 V, ±15 V) circuits operating far from the rails <!-- TODO: reformulate. -->, it is generally of secondary importance.

### Summary

Op-amp selection is not about making all parameters "the best".

Correct design means prioritizing the parameters that are critical for the application and keeping the others at a sufficient level.

References: [1], [2], [3], [6]

## Op-amps according to output types

The output stage of an op-amp determines how the amplified signal is presented, with respect to which reference it is defined, and which loads it can drive.

Although often overlooked, the output type directly affects design success, especially at low supply voltages, when driving ADCs, and in digital–analog interfaces.

### Single-Ended Output

In a single-ended output, the signal produced by the op-amp is taken from a single output node and is expressed with respect to a fixed reference (most commonly system ground or a defined reference voltage).

When one says "the output is 1.4 V", it is clear with respect to which reference this value is measured. <!-- Comment from Hadrien: But how the op-amp produces an output referred to ground when it has not even connections to it ? You asked without knowing a very good question and open a can of worms… ☺️ --> The vast majority of general-purpose op-amps produce this type of output.

**Typical applications:**

* General-purpose analog amplifiers
* Sensor interfaces (short distance, low-noise environments)
* Active filters
* Laboratory and bench-top measurement circuits

**Advantages:**

<!-- TODO: rework. -->

* Simple circuit topology

* No additional receiver circuitry required

* Easy measurement and debugging

* Direct compatibility with most ADCs and analog blocks

**Disadvantages:**

* Limited noise immunity

* Not suitable for long cables or noisy environments

* Noise at the reference point (ground) directly couples into the signal

**In summary:**

Single-ended output is sufficient for simple and local analog circuits; however, as the system grows and the environment becomes noisier, it becomes a limiting factor.

### Differential output

In a differential output, the signal is not defined as the absolute voltage of a single node, but as the voltage difference between two output nodes. Information is carried in the difference between these two lines; simultaneous shifts of both lines with respect to ground do not change the signal’s meaning.

**Typical applications:**

* Differential-input ADC drivers <!-- And not only ADCs -->

* Long-cable analog connections

* Noisy industrial environments

* High-resolution data acquisition systems

**Advantages:**

* Common-mode noise is largely suppressed  <!-- TODO: Rework. -->

* Higher signal integrity is achieved

* Higher effective dynamic range can be obtained under the same supply voltage

* Natural compatibility with modern ADC architectures

**Disadvantages:**

* More complex circuitry and routing

* Requires a differential receiver or ADC

**Pay attention to:**

* Output common-mode voltage (VOCM) must be set correctly

**In summary:**
Differential output provides a clear advantage in systems where signal integrity is critical; however, this advantage comes at the cost of increased design complexity.

### Push-pull output

The push-pull output stage is an active structure capable of driving a load by both sourcing and sinking current. The output voltage is actively controlled by the op-amp in both the upward and downward directions. In most classical op-amps, this structure is implemented as Class AB.

**Typical applications:**

* Linear analog amplifiers

* ADC input drivers

* Low-impedance loads

* Analog signal processing chains


**Advantages:**

* Suitable for linear signal generation

* No external pull-up or additional components required

* Can both source and sink current

* Low output impedance

**Disadvantages:**

* Output swing may be reduced at high currents

**In summary:**

Push-pull output is the default and most general solution for analog op-amps.

### Open-drain (open-collector) output

This one is a trap.

Often, operational amplifiers and comparators are confused due to their common points despite important differences in their internal construction and operation.

If some IC you want to use as an operational amplifier has an open-drain or open-collector output, this is the sign it is instead a comparator and that it should not be used in operational amplifier circuits without a true good reason. Details on this point are given in the dedicated section <!-- TODO: add reference. -->.

### Rail-to-rail output

Rail-to-rail output refers to the ability of the op-amp output voltage to swing very close to the supply rails. This feature becomes especially critical at low supply voltages.

**Typical applications**

* Battery-powered devices

* Circuits requiring full-scale ADC utilization

**Advantages**

* More efficient use of the supply voltage

* Increased dynamic range

* More flexible design under low supply voltages

**Disadvantages**

* Rail-to-rail behavior depends on load current

* Reaching the exact rails is usually not ideal

* More complex internal architecture (may increase noise <!-- TODO for Hadrien: check a bit this one. Usually noise is more dependent on input, but often rail-to-rail is wanted in both sides. --> or cost)

* Beware of output impedance <!-- TODO for Hadrien: write more about this one. -->

**In summary**

Rail-to-rail output is not a simple "yes/no" feature, but a condition-dependent capability; the datasheet must be examined carefully.

## Common traps

### Comparators vs. op-amps

This section is still to write. In the meanwhile, please find this picture of a beautiful cat.

<img src="https://upload.wikimedia.org/wikipedia/commons/6/68/Bombay_Katzen_of_Blue_Sinfonie.JPG" alt="Bombay black cats of blue symphonie."/>

<!-- TODO: put contents. -->

### Capacitive load, stability

See article. <!-- TODO: put link. -->

### Botched current measurement circuits

Botched current measurement circuits (various ways to botch them).

<!-- TODO: complete this section. -->

### Operational amplifiers without ESD protection

Some people are tempted to use operational amplifiers with ESD protection removed for increased performance. Don’t. Even. Think. Of. It.

</div>

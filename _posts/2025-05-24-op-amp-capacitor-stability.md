---
layout: post
title: On stability of capacitive loaded op-amps.
permalink: /posts/op-amp-capacitor-stability.html
last_modified_at: 2025-05-24
---

## Introduction

Operational amplifiers are often, and for good reason, the go-to building block of many analog functions. They are often used with capacitive loads, for two main reasons. One, when operational amplifiers are used to produce DC voltage supplies, in which cases the capacitive load is used to ensure DC voltage stays constant. Second, when operational amplifiers are used to drive some capacitive load, typically the gate of the transistor of an RF power amplifier, including the capacitors of the biasing network.

However, a common trap with such circuits is that operational amplifiers tend to be unstable when they are capacitively loaded, even for relatively low values.

Recently, a designer in LinkedIn shared his experience on the topic on this page [^1], leading to a very interesting discussion on the topic.

{% comment %}
## Not a simulation issue

Operational amplifier unstability when capacitively loaded is a phenomenon well described by theory and which simulates rather well. However, it is easy to miss in the simulations for three reasons.

First, the simulated test cases are often not hard enough to check for such issues. When simulating something which produces DC rails, my standard test is not to simulate just a resistor but an abrupt transition from 0 to full load. Such an hard test allows to detect lots of problems before they happen in the lab.

Second, a mistake in the simulated values may transform an oscillatory circuit into a barely stable circuit which poorly works but still works. For instance, in some cases, the load capacitance might be underestimated.

Third, the worst case parameters which should be simulated might not be evident, particularly for the opamp GBW (gain bandwidth product). Often the worst case for proper operation is the minimum value. For stability issues the worst cases is most likely to be the maximum value. For instance, the datasheet of the LM741[^2] specifies a min GBW of 437&nbsp;kHz, a typical GBW of 1500&nbsp;kHz, and no maximum GBW.
{% endcomment %}

## Beware of the "high capacitive load drive capability" op-amps

Some op-amps models like the OPA192[^3] advertise an "high capacitive load drive capability", but the stated value is only 1 nF. Even if this is only a typical value, its conditions are rather fair: only 40% overshoot. The main problem is that it is only 1 nF.

The same graphs suggest that a 25&nbsp;Ω improves greatly the overshoot, with a maximum value of 25&nbsp;%, and allows to use an arbitrarily high capacitive load.

<img src="{{ '/posts/op-amp-capacitor-stability/opa192-ds-fig-33.png' | relative_url }}" width="50%" >

And once the isolation resistor is added, it lacks only two components to make something perfect. Why not read the following and add them ?

In the discussion, the OPA994[^4] was suggested. Indeed, it is advertised as having an "unlimited capacitive load drive capability" with a "phase margin of 50° when driving a load of 10&nbsp;μF and 1&nbsp;MΩ". It is indeed the case. However, on some part of the phase margin plots, the phase margin is as low as 20°, and, again, is works much better with an isolation resistor. It should be noted, however, that the OP994 with a 50&nbsp;Ω isolation resistor has a 45&nbsp;% worst case overshoot while the OPA192 has only a 20&nbsp;% overshoot.

<table>
<tr>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/opa994-ds-fig-5-39.png' | relative_url }}"/>
</td>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/opa994-ds-fig-5-40.png' | relative_url }}"/>
</td>
</tr>
</table>

And once the isolation resistor is added, same comment than before.

## The root cause

A feedback system must have less than 180° phase shift from its output to its - input at the unity gain frequency in order to the negative feedback to stay negative and to avoid it going positive and causing unstability. There are more complicated ways to tell this principle but the core concepts are here.

An ideal operational amplifier has already a -90° phase shift due to its integrator nature (the gain bandwidth product). Due to various unperfections, there is also a little more phae shifting. The open loop output impedance of the operational amplifier combined with the capacitive load easily makes almost -90° phase shift at unity gain if the GBW and the capacitor are high enough. All this combined, this can lead to high overshoots, an high closed-loop output impedance, or a caracterized oscillation.

Note what matter for stability is the open loop operational amplifier output impedance. The closed loop output impedance is much lower due to feedback, at least when the feedback operates properly.

## Some details on the topic

The details of the topic won't be explained here, because the most important is to be aware of the problem and of its solutions. Once the problem is known, details are easy to find on Google. Reference [^5] is a great starter, even if I would suggest an other solution on the "RC filter directly at the input", [^6] gives more informations on threee useful solutions: R<sub>ISO</sub>, R<sub>ISO</sub> + DFB, R<sub>ISO</sub> + DFB + RFx, [^7] give more solutions and details, and [^8] is a rather long presentation on the general subject of operational amplifier stability which beats the topic to death, [^8] gives additional details and equations on the topic. This application note from Microchip[^9], although not complete on compensation networks, give useful equation, useful tips for ADC interfacing and give useful information on large signal effects.

The careful reader will probably notice a mistake in the "in-loop compensation circuit" of [^7]: Vin and GND are inverted, as well as the - and + inputs of the operational amplifiers. Despite this mistake, the remaining of the contents is highly valuable.

<!-- TODO: Fix sup references. -->

## Some comments of the common solutions

### Input filtering

Not directly related to output driving load, this is nevertheless an interesting case to mention. Often it is derisable, particularly to reduce sensitivity to RFI and EMI, to filter the input. A capacitor straight at the op-amp inputs, like in figure below, is likely to make it unstable, for the reasons described above.

<img src="{{ '/posts/op-amp-capacitor-stability/analog-article-fig-16.png' | relative_url }}" width="50%"/>

However, I would suggest an other solution than the one proposed by Analog Devices: splitting the input resistor and to put the filtering capacitor <!-- like in the figure below!--> in the middle.

<!-- TODO: Add figure. -->

### Output snubbing network

A perceived drawback of solutions using an isolation resistor is the voltage drop in the isolation resistor and the inability of using the full output voltage range of the operational amplifier, particularly for RRO (rail-to-rail-output) amplifiers.

Whether an isolation resistor is used or not, voltage margin between the desired voltage and the voltage rails of the operational amplifiers is useful so the retroaction loop can work properly.

In the case this solution must be used, like in the schematic below from Analog Devices, the principle can be explained in the following simple way. R<sub>S</sub> is low enough compared to C<sub>L</sub> to make the output load looks like resistive enough to ensure a good phase margin at the unity gain frequency, while C<sub>S</sub> is high enough compared to R<sub>S</sub> to make R<sub>S</sub>+C<sub>S</sub> close enough to only R<sub>S</sub>.

<img src="{{ '/posts/op-amp-capacitor-stability/analog-devices-snubber.gif' | relative_url }}"/>

This solution stabilizes the circuit, but makes the load harder to drive, making this solution ok for DC or low frequency signals, but not so much for higher frequency cases.

A tricky point of this calculation is that the needed components values depends on the unity gain frequency, but it depends itself on the values of the snubber network which tend to reduce it.

### Isolation resistor

An isolation resistor ensures the opamp sees at the unity gain a convenient load, either a low enough capacitance when the capacitive load is low enough compared to the isolation resistor, or the isolation resistor when the capacitive load is high enough. This ensures stability, but at a price: the opamp produced the wanted voltage with the feedback before the resistor, and the actual voltage at the load is RC filtered.

### Isolation resistor + double feedback

This technique exists in two common variants shown in the 2 figures below from the excellent article[^6] from Texas Instruments. 

<figure class="images-table">
<table>
<tr>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/texas-article-fig-2.png' | relative_url }}" />
</td>
<td width="10%">
<!-- FIXME: Quick and dirty fix. -->
</td>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/texas-article-fig-3.png' | relative_url }}" />
</td>
</tr>
</table>
</figure>

The operating principle is the same in the two cases: provide an high frequency and a low frequency feedback paths. The high frequency path, right at the operational amplifier output, undelayed, provides stability, while the low frequency path, at the load, provided an exact low frequency response.

With some mathematics, it is possible to determine the optimum values which ensure both stability and performance.

Since I had not yet the time to do the mathematics, in waiting, please fine a picture of these beautiful cats from Wikipedia:

<img src="https://upload.wikimedia.org/wikipedia/commons/6/68/Bombay_Katzen_of_Blue_Sinfonie.JPG" alt="Bombay black cats of blue symphonie."/>

## Some words on buffers

Unity gain buffer ICs can help to solve this problem, either as a standalone solution, when their offsets are tolerable, or as an addition to the opamp, kind of replacing the isolation resistors.

Since I had not yet the time to write on the topic, in waiting, please find a picture of this beautiful cat from Wikipedia:

<img src="https://upload.wikimedia.org/wikipedia/commons/4/4c/Blackcat-Lilith.jpg" alt="Lilith black cat."/>

{% comment %}
https://www.ti.com/amplifier-circuit/op-amps/high-speed/products.html#89=Fixed%20Gain%2FBuffer&
https://www.analog.com/en/parametricsearch/11086#/d=5057|s6|s7|s25|s3|s5|2687|5002|4502|300|4095|4108|2839|2840|s16&p5057=Buffer%20Amplifier|Line%20Drivers
ttps://www.analog.com/en/parametricsearch/11087#/d=5057|s6|s7|s25|s3|s5|2687|4502|2606|300|4101|5055|4108|2839|2840|s16&p5057=Buffer Amplifier|Line Drivers
Simple buffers:
  BUF634A
The common LT1010 has xxx drawbacks.
{% endcomment %}

## Case studies

### Sariel Hodisan

From this LinkedIn post[^1] from Sariel Hodisan:

<blockquote>
<p>Lately, I designed a simple biasing circuit for bipolar voltage rails (±13.5V) to bias a very precise low-noise analog circuit. To minimize offset in the analog section, it’s mandatory for the ±13.5V rails to be as closely matched as possible. The load is just a few mA, and it’s mostly a DC circuit. No fast current draws.</p>

<p>[...]</p>

<p>I did need decoupling for the biased circuit and figured 1nF would be enough. According to the OPA192 datasheet, there’s around 40&nbsp;% overshoot when loaded with a {% raw %}[2nF, see below]{% endraw %} cap.</p>

<p>[...]</p>

<p>The ±13.5V rails oscillated terribly.</p>

<p>Luckily, I had provisions to add an isolation resistor (30 ohm), and that solved the problem, though at the cost of a slight voltage drop.</p>

</blockquote>

I edited the message to make the total capacitive load more clear: 2 nF total, including 1&nbsp;nF straight at the opamp output and 1&nbsp;nF at the load.

Although some details are specific to his project, like his need of low noise, generating DC voltages to supply something is a very common need.

This circuit should not have oscillated so hard, according to the datasheet, which predicts less than 45&nbsp;% overshoot for a 2&nbsp;nF load.

<img src="{{ '/posts/op-amp-capacitor-stability/opa994-ds-Hodisan.png' | relative_url }}" />

He solved the problem using a simple isolation resistor, at the cost of a small voltage drop, and I suggested him to add a double feedback to eliminate the drop. Since it is a DC need, the simple double feedback is sufficient.

### Microwaves101 gate pulser

In the excellent microwaves101 website[^10], a page is written on the subject of pulsed RF sources. Although it advises drain pulsing (this page was written long before before GaN was mainstream), it also gives some advice about gate pulsing (bold from myself):

<blockquote>
<p>For a good gate pulsing circuit, we recommend the Analog Device's AD8036 "clamping amp", shown below. It lets you set up on and off gate bias voltages independently; for example, if you are using a PHEMT power amp you can set VG(on) to -0.9 volts, and VG(off) to -1.5 volts. You still need charge storage on the drain bias lines, and stability caps on gate and drain biases, as near as possible to the amp. Like all op-amps, the AD8036 can be configured as an inverting or non-inverting amplifier. <b>Yes, we need to add some resistive feedback to the figure!</b></p>
</blockquote>

<img src="{{ '/posts/op-amp-capacitor-stability/microwaves101-gate-driver.jpg' | relative_url }}" />

The feedback was forgotten in the figure, but not in the text.

However, a point which might need to be added is the stabilisation for capacitive loads. The AD8036 datasheet does not mention performance curves when capacitively loaded, but instead a recommended isolation resistor value:

<img src="{{ '/posts/op-amp-capacitor-stability/ad8036-ds-fig-5.png' | relative_url }}" width="50%" />

Given this curve and the typical gate bias network capacitance values, I would recommend a 20&nbsp;&Omega; isolation resistor. The RC bandwidth is already 31.8&nbsp;MHz. If not sufficient, a R<sub>ISO</sub> + DFB + RFx can be used to both remove the R<sub>ISO</sub> offset and to have speed up.

### Microwaves101 gate pulser, alternative solution

That being said, we would propose here an alternative solution.

A problem with the AD8036[^11] is that it is an input clamping amplifier, with clamping only available on its +V<sub>IN</sub>, making it "works only for noninverting or follower applications". This needs a 0 to -5V input signal to have the requested V<sub>H</sub> and V<sub>L</sub> voltages. Not very convenient since most digital circuits operate on positive voltages.

Switching between two voltages levels would be conveniently done by a switch integrated circuit. Most common switches are slow, either because they are plain slow or because they include some "break before make" circuitry which take some transition times. The switches in the "buffered analog multiplexers" section of Analog Devices[^12] provide faster time, probably because the techniques to deal with switching transitions are easier to implement in unidirectional multiplexed buffer than in unidirectional buffer, like current steering:

<blockquote>
<p markdown="1">The &#91;ADV3129[^13]&#93; multiplexer is organized as two input transconductance stages tied in parallel with a single output transimpedance stage followed by a unity-gain buffer. Internal voltage feedback sets the gain.</p>
</blockquote>

The following chips are interesting, with only single channel devices mentionned:

<figure>
<img src="{{ '/posts/op-amp-capacitor-stability/ad8170-ds-block-diagram.png' | relative_url }}" width="50%" />
<figcaption markdown="1">
AD8170[^14]
</figcaption>
</figure>

<figure>
<img src="{{ '/posts/op-amp-capacitor-stability/ad8180-ds-block-diagram.png' | relative_url }}" width="50%" />
<figcaption markdown="1">
AD8180[^15]
</figcaption>
</figure>

<figure>
<img src="{{ '/posts/op-amp-capacitor-stability/adv3219-ds-block-diagram.png' | relative_url }}" width="50%" />
<figcaption markdown="1">
ADV3219[^16]
</figcaption>
</figure>

The AD8170 is a **current feedback** amplifier with a switchable input. These category of operational amplifiers are sensitive to the impedance seen at the feedback pin, to DFB schemes cannot be used directly with them. The datasheet recommands isolation resistor values and feedback resistance. Simple RC calculations shows that the performance is mainly determined by the RC constant of the isolation resistor and the capacitive load.

The AD8180 is an open loop buffer and can drive capacitive loads without isolation resistors. **However, an input resistor is recommended.** This is often the case for buffer amplifiers, and often forgotten. Performance is again determined by the open loop impedance of approximately 25&nbsp;&Omega;.

The ADV3219 is a feedback amplifier with an internal feedback. Performance curves are given for low capacitive loads without isolation resistor. For higher capacitive loads, the datasheets recommands an isolation resistor of "a few tens of ohms", but does not give more performance details. Nevertheless it can be assumes that it will be dominated by the RC constant of the output.

<figure>
<table>
<tr>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/ad8180-ds-fig-22.png' | relative_url }}" />
</td>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/adv3219-ds-fig-56.png' | relative_url }}" />
</td>
</tr>
</table>
</figure>

<figure>
<table>
<tr>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/ad8170-ds-fig-19.png' | relative_url }}" />
<p style="text-align: center;">AD8170</p>
</td>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/ad8180-ds-fig-19.png' | relative_url }}" />
<p style="text-align: center;">AD8180</p>
</td>
</tr>
<tr>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/ad8180-ds-fig-20.png' | relative_url }}" />
<p style="text-align: center;">AD8180</p>
</td>
<td>
<img src="{{ '/posts/op-amp-capacitor-stability/adv3219-ds-fig-4.png' | relative_url }}" />
<p style="text-align: center;">ADV3219</p>
</td>
</tr>
</table>
</figure>

## Conclusion

Sine life is too short to write conclusions, please find this beautiful picture of a cat, courtesy of Microwaves101 ([https://www.microwaves101.com/unknown-editor-121-cat-wrangler-april-2023](https://www.microwaves101.com/unknown-editor-121-cat-wrangler-april-2023)):

<img src="https://www.microwaves101.com/uploads/CatBed.png" />

[^1]: [https://www.linkedin.com/posts/sariel-hodisan_...](https://www.linkedin.com/posts/sariel-hodisan_%F0%9D%97%A7%F0%9D%97%B5%F0%9D%97%B2-%F0%9D%97%B4%F0%9D%97%AE%F0%9D%97%BD-%F0%9D%97%AF%F0%9D%97%B2%F0%9D%98%81%F0%9D%98%84%F0%9D%97%B2%F0%9D%97%B2%F0%9D%97%BB-%F0%9D%98%80%F0%9D%97%B6%F0%9D%97%BA%F0%9D%98%82%F0%9D%97%B9%F0%9D%97%AE-activity-7316060130964340736-RCjM/)

[^3]: [https://www.ti.com/lit/ds/symlink/opa192.pdf](https://www.ti.com/lit/ds/symlink/opa192.pdf)

[^4]: [https://www.ti.com/lit/ds/symlink/opa994.pdf](https://www.ti.com/lit/ds/symlink/opa994.pdf)

[^5]: [https://www.analog.com/en/resources/analog-dialogue/articles/techniques-to-avoid-instability-capacitive-loading.html](https://www.analog.com/en/resources/analog-dialogue/articles/techniques-to-avoid-instability-capacitive-loading.html)

[^6]: [https://www.ti.com/document-viewer/lit/html/SSZT999](https://www.ti.com/document-viewer/lit/html/SSZT999)

[^7]: [https://www.analog.com/en/resources/analog-dialogue/articles/ask-the-applications-engineer-25.html](https://www.analog.com/en/resources/analog-dialogue/articles/ask-the-applications-engineer-25.html)

[^8]: [https://e2e.ti.com/cfs-file/__key/.../Solving_5F00_Op_2D00_Amp_5F00_Stability_5F00_Wells_5F00_6_2D00_5_2D00_12-_2800_2_2900_.pdf](https://e2e.ti.com/cfs-file/__key/telligent-evolution-components-attachments/01-864-00-00-00-66-32-73/Solving_5F00_Op_2D00_Amp_5F00_Stability_5F00_Wells_5F00_6_2D00_5_2D00_12-_2800_2_2900_.pdf)

[^9]: [https://ww1.microchip.com/downloads/en/Appnotes/00884b.pdf](https://ww1.microchip.com/downloads/en/Appnotes/00884b.pdf)

[^10]: [https://www.microwaves101.com/encyclopedias/pulsed-rf-sources](https://www.microwaves101.com/encyclopedias/pulsed-rf-sources)

[^11]: [https://www.analog.com/media/en/technical-documentation/data-sheets/ad8036_8037.pdf](https://www.analog.com/media/en/technical-documentation/data-sheets/ad8036_8037.pdf)

[^12]: [https://www.analog.com/en/parametricsearch/11267#/sort=s3,asc](https://www.analog.com/en/parametricsearch/11267#/sort=s3,asc)

[^13]: [https://www.analog.com/media/en/technical-documentation/data-sheets/ADV3219_3220.pdf](https://www.analog.com/media/en/technical-documentation/data-sheets/ADV3219_3220.pdf)

[^14]: [https://www.analog.com/media/en/technical-documentation/data-sheets/ad8170_8174.pdf](https://www.analog.com/media/en/technical-documentation/data-sheets/ad8170_8174.pdf)

[^15]: [https://www.analog.com/media/en/technical-documentation/data-sheets/AD8180_8182.pdf](https://www.analog.com/media/en/technical-documentation/data-sheets/AD8180_8182.pdf)

[^16]: [https://www.analog.com/media/en/technical-documentation/data-sheets/ADV3219_3220.pdf](https://www.analog.com/media/en/technical-documentation/data-sheets/ADV3219_3220.pdf)

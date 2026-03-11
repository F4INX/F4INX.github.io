---
layout: post
title: The fine art of (not) doing oscillators
permalink: /posts/how-not-to-do-oscillators.html
last_modified_at: 2026-03-09
---

## A day in life...

Riiiiiiiiiiiing.

* Hello the ACME labs. What can I do for you ?

* We just have two of our enginners injured following a bad fight.

* That's a case for the medical doctor.

* Well, we would like to know who was right in this matter.

* Well, tell me more...

* It involved Andreas "Bullterrier", our senior electronics enginneer, and Cătălina "Tank", our field sensor expert.

* Must have been a great match... I wish I were there to watch...

* Indeed a great match... But they will be off a few days and...

* Got it...

## Digging in the problem...

I start simulating the very first version of this circuit by Cătălina "Tank":

<img src="{{ '/posts/how-not-to-do-oscillators/01-rc-phase-shift-oscillator.png' | relative_url }}"/>

On a first glance, nothing worth a fight. Seems to be a boring oscillator.

Next I found this mail of Andreas "Bullterrier":

*"Weird circuit... First, R3 should not have any effect. Second, why your frequency is shifted from the theoretical 6.5 kHz to 6.0 kHz ?"*

First point seems rather sound...

A few mails later, this mail by Cătălina "Tank":

*"You stubborn! Simulations DOES show it has an effect."*

I was thinking this is typical from Cătălina when she lacks coffee... until I ran a simulation:

<img src="{{ '/posts/how-not-to-do-oscillators/02-rc-phase-shift-oscillator.png' | relative_url }}"/>

Holy damn. The resistor which should have no effect DOES HAVE an effect, and now the frequency is even further away from the theory: 4.5 kHz.

## ...even further

Next I simulate the first version proposed by Andreas "Bullterrier" which uses the input resistor of the inverting operational amplifier as an equivalent of the final shunt resistor:

<img src="{{ '/posts/how-not-to-do-oscillators/03-rc-phase-shift-oscillator.png' | relative_url }}"/>

The frequency is far from the theory, 5.0 kHz instead of 6.5 kHz, and the gain needed for a quick start higher than the theory.

## Digging in the problem

All this stuff semm to have one question in common: what is actually the impedance of the operational amplifier circuit, no matter its variant.

I made a Lissajous diagram to have a first look at the impedance:

<img src="{{ '/posts/how-not-to-do-oscillators/03-rc-phase-shift-oscillator-Lissajous.png' | relative_url }}"/>

We see that for low amplitudes the trajectory (green) is close to a 1 kΩ resistance (blue) but that for higher amplitudes the trajectory becomes much more complex, with a mixture of reactive behavior and of non-linearities for an equivalent impedance around 7 kΩ, much higher than expected at a first glance.

<img src="{{ '/posts/how-not-to-do-oscillators/03-rc-phase-shift-oscillator-voltages.png' | relative_url }}"/>

## Andreas striked back

Andreas seems to have seen that the input impedance of the inverting amplifier what not the expected value since he made this second version I simulate:

<img src="{{ '/posts/how-not-to-do-oscillators/04-rc-phase-shift-oscillator.png' | relative_url }}"/>

Indeed he used a shunt resistor and did not rely anymore on the input impedance of the operational amplifier. The oscillation frequency, 6.2 kHz, is closer to the expected value of 6.5 kHz. Again the needed gain is higher. But seems rather fine except...

## Cătălina stikes back

<em markdown=0>"You ******* cheater. You made a comparison between circuits but changed the operational amplifier. Your damn **** does not work with the original amplifier while my circuit does."</em>

Indeed I missed this change. And when simulating with the original amplifier:

<img src="{{ '/posts/how-not-to-do-oscillators/05-rc-phase-shift-oscillator.png' | relative_url }}"/>

I need feedback amplifier gains **much** higher than the theoretical value, and the oscillation frequency, somewhere around 4.5 kHz <!-- TODO: precise value. --> was very far from the expected 6.5 kHz.

## Digging

I tried first to check for any loading effects by introducing ideal followers before the RC and before the operational amplifier with its feedback:

<img src="{{ '/posts/how-not-to-do-oscillators/06-rc-phase-shift-oscillator.png' | relative_url }}"/>

Same tendencies, and the needed resistances are even worse. So, this problem is not in the impedances but really in the transfert functions. Since this problem depends on the operational amplifier, it is the point to check. And since it concerns also the low amplitude part, it should be seen also in small signal.

So I made a small signal simulation of the amplifying part with both operational amplifier models to compare:

<img src="{{ '/posts/how-not-to-do-oscillators/06-rc-phase-shift-oscillator-amplifier.png' | relative_url }}"/>

The LT1001 has a low gain-bandwidth product, around 400 kHz in simulation, sufficient to provide the gain requested by the feedback, but with a 15.5° phase delay compared to the ideal value. On the contrary, the ADA4077 had only a 3.1° phase delay. Note the gain with both amplifiers is almost identical.

15.5° would not seem enough to wreak a circuit, but maybe RC phase shift oscillators are pricky ?

I begin to realize that this circuit might be monster and that it drove mad Andreas and Cătălina for a reason...

## Straight to a solution

*Details coming soon*

<figure>
<table class="images-table">
<tr>
<td>
  <img src="{{ '/posts/how-not-to-do-oscillators/dds-module.jpg' | relative_url }}" style="width:100%;"/>
</td>
<td>
  <img src="{{ '/posts/how-not-to-do-oscillators/dds-module-use.jpg' | relative_url }}" style="width:100%;"/>
</td>
</tr>
</table>
</figure>

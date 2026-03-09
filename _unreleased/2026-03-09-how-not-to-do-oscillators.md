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

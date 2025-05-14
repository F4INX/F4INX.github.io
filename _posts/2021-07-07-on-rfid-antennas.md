---
layout: post
title:  Why RFID antennas should be called neither RFID nor antennas ?
permalink: /posts/on-rfid-antennas.html
last_modified_at: 2021-07-21 00:22:31 +0200
---

A friend of mine told me that he was looking for an "expert antenna engineer" to design RFID antennas, but he was not sure he searches well, because the last antenna expert he interview told him that he had designed hundreds of antennas, but never an rfid antenna. Never. Nada.

He tried to search on antenna books some information on rfid antenna to orient his search. He was quickly disappointed. He opened the excellent "Electromagnetic Waves and Antennas" ([https://web.archive.org/web/20240528230718/www.ece.rutgers.edu/~orfanidi/ewa/)) from Orfanidis, and search for RFID and NFC. Nothing! Same thing with "Antenna Theory: Analysis and Design" from Balanis. This starts bad.

The *coup de grâce* comes from Antenna Theory ([https://www.antenna-theory.com/definitions/nfc-antenna.php](https://www.antenna-theory.com/definitions/nfc-antenna.php)):

> Therefore, NFC antennas are not really antennas, in that no one cares about typical antenna parameters, such as the radiation pattern or the antenna gain

Here we go! Now, time for more explanations.

## What are antennas ?

That's probably the best question to ask to an antenna expect if you want to be sure that not only he knows his stuff but that he will also be able to explain to you the job you pay him for in terms you are able to understand.

Most science magazines would tell that an antenna is something which "converts a current to a wave". Nothing can be more misleading! First, between the conductors who carry a current, there is already a wave. Second, antennas can also be fed by metallic waveguides, who are not well described by their currents, or by dielectric waveguides, who have NO conduction current at all. Third, it does not explain how the wave emitted or received by an antenna is different from the wave in a cable.

A much better definition would be: "an antenna is a device which converts a guided wave to or from a freely propagating wave".

The wave in the wire which connects a transmitter to an antenna is guided by the wire. Same thing for a metallic or a dielectric waveguide. For the output wave, freely propagating is a very important point: an antenna emits a wave even if there is nothing and just the free space in front of it. In this case, the emitted wave will simply travel during eternity until it meets something. The antenna emits equally well whether there is or not an antenna in front of it.

It's actually a difficulty to measure antenna: to make measurements of an antenna. On the one side, we must put the measured antenna in an enclosure to avoid both disturbance from outside transmitters and to disturb outside receivers. On the other side, the antenna must not see the enclosure walls and only something which look like free space. Metallic enclosures reflect waves and look like a mirror from the antenna point of view. Therefore it must be covered by special materials absorbing electromagnetic waves in order to look like free space.

Something important for the remaining of this article is that the field in the near vicinity of the antenna does not depend whether there is an antenna or nothing far before the antenna.

## What are transformers ?

Transformers are a device made from two coupled coils. In transformers used for power supplies, the coupling is made as strong as possible. The details on the various ways to ensure strong coupling are outside of the scope of this article. When a voltage is applied to the first coil, some current flow in it, just enough to produce a "magnetic field"[^1] which would in turn induce in the coil a voltage equal to the applied voltage, as well as a voltage in the second coil. When nothing is connected to the second coil, no current flows into the second coil. When something is connected to the second coil, it draws a current which changes the magnetic field, which in turn cause more current to flow in the first coil[^2].

For a well designed transformer, when no current in drawn from the second coil, the current in the first coil is low and mainly inductive. This is an important point: the inductive current is out of phase with the voltage so the average power consumed is null: it periodically takes and give back power. And inductive current stores energy but don't consumes it.

Of course, there are always somme losses, but they are low. There is no power which escapes and travels to infinity.

## What is NFC ?

NFC means near field communication. This system allows for a reader device with its power supply to communicate with and to provide enough power to process the requested informations to an electronic chip embedded, for example, in a card. Some modulated high frequency voltage is applied to the coil of the reader devices. This produced in turn a voltage to the coil of the tag which allows it to be powered. The modulation of this high frequency voltages allow to transmit information. The tag transmits information by modulating the current it draws to the coil. Which can be sensed by the reader by monitoring the current in its own coil.

Exactly a transformer action: increase of output current, increase of input current.

There are some differences between such transformers and the typical 50/60 Hz mains electricity transformer: the NFC coils are designed for high frequencies and the coupling is lower because the two coils are separated by a few centimeters.

Coils in a transformer are described by both both self-inductances, quantifying the inductive behavior of the coils if they were separated, and a mutual inductance, quantifying the coupling between the two coils. In the same way, an NFC coil is described by its inductance. Mutual inductance changes a lot depending on the application. Secondary coil inductance belongs to the other system, so it's interesting mainly for the designer of the other system.

When looking for nfc coil formulas, all formulas specifies the inductance of the coil. Resistance is often ignored. And when it is calculated or measured, this resistance is mainly ohmic[^3]: the radiation resistance is negligible. On the contrary, radiation resistance of antennas cannot be neglected because it determines the efficiency[^4].

## Why RFID is not a good term ?

"Radio frequency identification". Radio frequency is a loose term designated almost any alternating thing starting from 100 kHz (old amplitude modulated broadcast radios). Identification is a precise term but applies to lots of situations. For instance, have identifiers for various reasons Bluetooth devices, airplanes transponders and so on.

If RFID is a term applicable for lots of things, its almost a term for nothing.

## What are NFC "antennas" ?

Good question. We have seen that their mechanism is not an antenna mechanism but a transformer mechanism. So, antenna is not the proper term. Transformer would apply to the two coils. Half-transformer would be perfect but a bit strange. Coil is perfect.

The only drawback is that coil focuses too much on *how* it is built than *what* is does. But it's still ok because there is not so much ways to design NFC coils than with coils.

## How should I search NFC coil designers ?

Good question. For the terms, the usual terms are bad, but highly common, so stick to it. But keywords more specific to NFC must be added to find candidates coming from the NFC domain. Searching among antenna designers is not a bad starting point, but most people in this domain will be used to radiating antennas. Microwaves conferences are not the best place to search for this reason. Searching among transformer designers might be interesting because NFC coils are half-transformers.

Don't start searching an "antenna expert" and tell him later than it's antenna will be an RFID/NFC antenna. RFID/NFC should be among the first words. "Antenna" should be here just for Google: "coil" is the right term.

An other answer is "don't search NFC coil designers". NFC coil design is easy, provided one has some minimum knowledge in electromagnetism. Application notes like [https://www.nxp.com/docs/en/application-note/AN11564.pdf](https://www.nxp.com/docs/en/application-note/AN11564.pdf) explains all what is needed to do this job. However, matching it, properly select the capacitors, designing the filter, the components, the rest of the system is not. Search RFID experts, who will know these not so easy topics. Search analog electronics designers who will know how to use the NFC coil. Both will learn quickly how to design an NFC coil.

## Sum up

NFC coils should not be called antennas because they operate in a different ways. Antennas radiate a far field in free space while NFC coils tend to keep energy in their near field. Keep this in mind when searching for NFC coil designer.

[^1]: The proper name would be 'excitation', but the difference between the magnetic excitation and the magnetic field is outside of the topic of the article.

[^2]: More precisely, the total magnetic field is the difference between the magnetic fields created by the coils, proportional to the difference of the currents weighted by the number of turns. This total magnetic field induces a voltage in both coils. For a constant voltage, the difference between the currents is constant, so when the second current increases, the first current decreases.

[^3]: Ohmic means "caused by the finite conductivity of the metal".

[^4]: Non negligible does not mean that it is always high. In some cases, the radiation resistance can be low compared to the ohmic resistance. But in such cases, the efficiency is low.

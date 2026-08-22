---
title: "IQ modulator and quadrature coupler sign issues."
date: 2024-11-05
lastmod: 2024-11-05
categories: [Couplers, IQ Modulators, RF Design]
url: /posts/IQ-quadrature-sign.html
---


<p class="begin-note"><b>Update from 2024-11-05:</b> Steve from Microwaves 101 also tackled this topic (<a href="https://www.microwaves101.com/encyclopedias/branchline-coupler-port-definition">https://www.microwaves101.com/encyclopedias/branchline-coupler-port-definition</a>), proposing a different port-naming convention for the branchline coupler. Steve names the direct and coupled outputs in reverse compared to the approach I use. His convention offers some interesting arguments: the output he names "forward" exhibits a higher bandwidth and flatter phase response.</p>

<p class="begin-note">Upon further analysis, it appears that the operating principles of branchline couplers differ significantly from those of coupled line couplers. Consequently, the terms "direct" and "coupled," commonly used for coupled line couplers, no longer carry the same meaning.</p>

<p class="begin-note">For now, I’ll retain the "geometric" convention I initially used, as it seems more common, although I’m not entirely convinced it’s more "correct." Examples that follow this convention can be found in <a href="https://www.researchgate.net/figure/Conventional-branch-line-coupler_fig1_264335850">this research</a>, <a href="https://www.researchgate.net/figure/The-3dB-branch-line-directional-coupler-structure_fig8_221787600">this diagram</a>, <a href="http://jre.cplire.ru/alt/nov12/12/text.html">this article</a>, and <a href="https://www.semanticscholar.org/paper/Miniaturised-broadband-branch-line-coupler-for-and-Thiyagarajan-Kesavamurthy/0a68c3794644204e7e99a7d4f45eb6ef589456c7">this paper</a>).</p>

<p class="begin-note">Many thanks to Steve for raising this interesting topic. Thanks also ChatGPT for improving my English.</p>

## Introduction

IQ modulators and quadrature couplers are often used together to perform a frequency translation while rejecting the unwanted sideband. However, the documentation often does not clarify whether the quadrature signal has a +90° or -90° phase shift, and whether the IQ modulator expects a quadrature input with a +90° or -90° phase shift.

The purpose of this page is to clarify this sign issue.

## Upconverter side

Here, we assume an upconverter is used. The principle of an IQ upconverter is to perform a complex frequency translation as follows:

<asciimath>
"RF" = Re[(I + j \cdot Q) \cdot e^(j \cdot \omega_("rf") \cdot t)]
</asciimath>

In the case of a complex cosine signal in baseband with frequency &&\omega_b&&:

<asciimath>
I + j \cdot Q = e^(j \cdot \omega_b \cdot t) = cos(\omega_b \cdot t) + j \cdot sin(\omega_b \cdot t)
</asciimath>

By application of the trigonometric identity &&sin(x) = cos(x - pi / 2)&&:

<asciimath>
I + j \cdot Q = cos(\omega_b \cdot t) + j \cdot cos(\omega_b \cdot t - \pi / 2)
</asciimath>

This clearly shows that the Q input has a phase lag compared to the I input, which is a -90° phase.

## Coupler side case 1: coupled line coupler

Let's assume that the coupled line coupler [QCH-451+](https://www.minicircuits.com/WebStore/dashboard.html?model=QCH-451%2B) from Mini-Circuits is used. The datasheet indicates which port is the quadrature output but not whether its phase is +90° or -90°.

Using ChatGPT and Plotly, the following plots were easily generated:

<div id="magnitude-plot-1"></div>
<div id="phase-plot-1"></div>
<div id="phase-difference-plot-1"></div>

<script>
    // Helper function to unwrap phase
    function unwrapPhase(phase) {
        let unwrappedPhase = [phase[0]];
        for (let i = 1; i < phase.length; i++) {
            let delta = phase[i] - phase[i - 1];
            if (delta > 180) {
                unwrappedPhase.push(unwrappedPhase[i - 1] + delta - 360);
            } else if (delta < -180) {
                unwrappedPhase.push(unwrappedPhase[i - 1] + delta + 360);
            } else {
                unwrappedPhase.push(unwrappedPhase[i - 1] + delta);
            }
        }
        return unwrappedPhase;
    }

    // Helper function to load and parse S4P file
    async function loadS4P(url, fmax) {
        const response = await fetch(url);
        const s4pText = await response.text();
        
        const lines = s4pText.split('\n');
        let freq = [];
        let s11 = [], s21 = [], s31 = [], s41 = [];
        let phase11 = [], phase21 = [], phase31 = [], phase41 = [];

        for (let line of lines) {
            line = line.trim();
            if (line.startsWith('!') || line.startsWith('#') || line.length === 0) {
                continue;
            }

            const parts = line.split(/\s+/);
            if (parts.length >= 9) {
                const frequency = parseFloat(parts[0]);
                if (frequency <= fmax) {
                    freq.push(frequency);
                    const re11 = parseFloat(parts[1]);
                    const im11 = parseFloat(parts[2]);
                    const re21 = parseFloat(parts[3]);
                    const im21 = parseFloat(parts[4]);
                    const re31 = parseFloat(parts[5]);
                    const im31 = parseFloat(parts[6]);
                    const re41 = parseFloat(parts[7]);
                    const im41 = parseFloat(parts[8]);
                    
                    s11.push(20 * Math.log10(Math.sqrt(re11 ** 2 + im11 ** 2)));
                    s21.push(20 * Math.log10(Math.sqrt(re21 ** 2 + im21 ** 2)));
                    s31.push(20 * Math.log10(Math.sqrt(re31 ** 2 + im31 ** 2)));
                    s41.push(20 * Math.log10(Math.sqrt(re41 ** 2 + im41 ** 2)));
                    
                    phase11.push(Math.atan2(im11, re11) * (180 / Math.PI));
                    phase21.push(Math.atan2(im21, re21) * (180 / Math.PI));
                    phase31.push(Math.atan2(im31, re31) * (180 / Math.PI));
                    phase41.push(Math.atan2(im41, re41) * (180 / Math.PI));
                }
            }
        }
        return { freq, s11, s21, s31, s41, phase11, phase21, phase31, phase41 };
    }

    async function fetchAndPlot_1() {
        url = "../posts/IQ-quadrature-sign/QCH_451+_UN1_+25DEGC.S4P";  // FIXME: temp fix.
        const data = await loadS4P(url, 500e6);
        
        // Unwrap phase
        data.phase31 = unwrapPhase(data.phase31);
        data.phase41 = unwrapPhase(data.phase41);

        // Calculate phase difference
        let phaseDiff = data.phase41.map((p41, index) => p41 - data.phase31[index]);

        // Plotting magnitude using Plotly
        const magData = [
            { x: data.freq, y: data.s11, mode: 'lines', name: 'S11 Magnitude},
            { x: data.freq, y: data.s21, mode: 'lines', name: 'S21 Magnitude},
            { x: data.freq, y: data.s31, mode: 'lines', name: 'S31 Magnitude},
            { x: data.freq, y: data.s41, mode: 'lines', name: 'S41 Magnitude}
        ];

        const magLayout = {
            title: 'S-Parameters Magnitude Plot (0 to 500 MHz)',
            xaxis: { title: 'Frequency (Hz)', range: [0, 500e6] },
            yaxis: { title: 'Magnitude (dB)', range: [-50, 0] }
        };

        Plotly.newPlot('magnitude-plot-1', magData, magLayout);

        // Plotting phase using Plotly
        const phaseData = [
            { x: data.freq, y: data.phase31, mode: 'lines', name: 'S31 Phase},
            { x: data.freq, y: data.phase41, mode: 'lines', name: 'S41 Phase}
        ];

        const phaseLayout = {
            title: 'S-Parameters Phase Plot (0 to 500 MHz)',
            xaxis: { title: 'Frequency (Hz)', range: [0, 500e6] },
            yaxis: { title: 'Phase (Degrees)}
        };

        Plotly.newPlot('phase-plot-1', phaseData, phaseLayout);

        // Plotting phase difference using Plotly
        const phaseDiffData = [
            { x: data.freq, y: phaseDiff, mode: 'lines', name: 'Phase Difference (S41 - S31)}
        ];

        const phaseDiffLayout = {
            title: 'Phase Difference Plot (S41 - S31)',
            xaxis: { title: 'Frequency (Hz)', range: [0, 500e6] },
            yaxis: { title: 'Phase Difference (Degrees)}
        };

        Plotly.newPlot('phase-difference-plot-1', phaseDiffData, phaseDiffLayout);
    }

    fetchAndPlot_1();
</script>

It's clear from the plots than the quadrature output has a +90° phase (lead) compared to the in-phase output.

Besides clarifying the +/-90° sign issue, it is useful to check to what physical element correspond each port number. The hypothesis is that this coupler is made with an equivalent to coupled lines performed using an LC network, as pure coupled lines are obviously too long to fit in the component.

Analysis of the transmission curves enables to deduce the connexions:

* At low frequencies, total transmission from port 1 to port 3 and no transmission to the other ports. Thus both ports are connected to the same first transmission line and ports 2 and 3 are connected to the second line.

* Port 4 is not connected at low frequencies but is coupled in the band. So port 4 is the coupled port of the other line.

* Port 2 is not connecter at low frequencies and remains approximately isolated in the band. So port 2 is the coupled output of the second line.

This leads to the following schematic, compared to the datasheet information:

<!-- FIXME: Add alt textes and titles. -->
<table>
<tr>
<td>
<img src="/posts/IQ-quadrature-sign/mini-circuits-pins.svg" >
</td>
<td>
<img src="/posts/IQ-quadrature-sign/qch-451+-1.svg" >
</td>
</tr>
</table>

The symmetry of the schematic is coherent with the symmetry of the table given in the Mini-Circuits datasheet:

<img src="/posts/IQ-quadrature-sign/qch-451+-2.svg" >

The +90 phase shift stays even at low frequencies. This is coherent with the similar behaviour of an high-pass CR network, which is part of the equivalent schematic at low frequencies.

## Coupler side case 2: branch-line coupler

In this part, the ports are numbered like in Microwaves101 ([https://www.microwaves101.com/encyclopedias/branchline-couplers](https://www.microwaves101.com/encyclopedias/branchline-couplers)), from which this schematic is taken:

<img src="/posts/IQ-quadrature-sign/quadrature-coupler.jpg">

This part was performed in two steps. First, using scikit-rf with a some help of ChatGPT, a Python script was created to produce preliminary plots and an s4p file.  The second step was to reuse the plotting code from the previous section, with some help from ChatGPT to refactor the duplicate parts, to make the following plots:

<div id="magnitude-plot-2"></div>
<div id="phase-plot-2"></div>
<div id="phase-difference-plot-2"></div>

<script>
    async function fetchAndPlot_2() {
        url = "../posts/IQ-quadrature-sign/branchline_coupler.s4p";  // FIXME: temp fix.
        const data = await loadS4P(url, 2e9);
        
        // Unwrap phase
        data.phase21 = unwrapPhase(data.phase21);
        data.phase31 = unwrapPhase(data.phase31);

        // Calculate phase difference
        let phaseDiff = data.phase31.map((p31, index) => p31 - data.phase21[index]);

        // Plotting magnitude using Plotly
        const magData = [
            { x: data.freq, y: data.s11, mode: 'lines', name: 'S11 Magnitude},
            { x: data.freq, y: data.s21, mode: 'lines', name: 'S21 Magnitude},
            { x: data.freq, y: data.s31, mode: 'lines', name: 'S31 Magnitude},
            { x: data.freq, y: data.s41, mode: 'lines', name: 'S41 Magnitude}
        ];

        const magLayout = {
            title: 'S-Parameters Magnitude Plot (0 to 2 GHz)',
            xaxis: { title: 'Frequency (Hz)', range: [0, 2e9] },
            yaxis: { title: 'Magnitude (dB)', range: [-50, 0] }
        };

        Plotly.newPlot('magnitude-plot-2', magData, magLayout);

        // Plotting phase using Plotly
        const phaseData = [
            { x: data.freq, y: data.phase21, mode: 'lines', name: 'S21 Phase},
            { x: data.freq, y: data.phase31, mode: 'lines', name: 'S31 Phase}
        ];

        const phaseLayout = {
            title: 'S-Parameters Phase Plot (0 to 2 GHz)',
            xaxis: { title: 'Frequency (Hz)', range: [0, 2e9] },
            yaxis: { title: 'Phase (Degrees)}
        };

        Plotly.newPlot('phase-plot-2', phaseData, phaseLayout);

        // Plotting phase difference using Plotly
        const phaseDiffData = [
            { x: data.freq, y: phaseDiff, mode: 'lines', name: 'Phase Difference (S31 - S21)}
        ];

        const phaseDiffLayout = {
            title: 'Phase Difference Plot (S31 - S21)',
            xaxis: { title: 'Frequency (Hz)', range: [0, 2e9] },
            yaxis: { title: 'Phase Difference (Degrees)}
        };

        Plotly.newPlot('phase-difference-plot-2', phaseDiffData, phaseDiffLayout);
    }

    fetchAndPlot_2();
</script>

Contrary to coupled lines, which have a very broadband quadrature effect, the branch-line coupler has a narrowband quadrature effect. This is still useful for narrowband applications.

It's clear from the plots than the coupled output has a -90° phase (lag) compared to the direct output.

## Conclusion

Quadrature couplers are important for making image reject mixers, but the actual phase sign is sometimes not clearly stated. According to the theory, IQ mixers needs a -90° phase (lag) for the Q input. For coupled lines couplers, the coupled output has a +90° (lead) phase compared to the uncoupled output. Conversely, for branchline couplers, the coupled output has a -90° (lag) phase compared to the uncoupled output. These points must be considered when selecting the wanted mixer side.

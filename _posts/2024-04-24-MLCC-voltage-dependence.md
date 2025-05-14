---
layout: post
title: MLCC voltage dependence.
permalink: /posts/mlcc-voltage-dependence.html
last_modified_at: 2025-05-14
---

<p class="begin-note">This content was originally published on Microwaves 101 (<a href="https://www.microwaves101.com/encyclopedias/capacitor-voltage-effects">https://www.microwaves101.com/encyclopedias/capacitor-voltage-effects</a>). Many thanks to Steve for improvements on the original version. Have a look on his website for more interesting content.</p>

> This page was suggested by Hadrien, who has had recent experience in MLC capacitor variations with voltage.  Did you know your capacitor nominal value can drop 80% when you apply a DC voltage to it?  Worse, there does not seem to be any standards for voltage variations like there are for temperature variations.

> This page is primarily discussing MLCCs, or multi-layer cerami capacitors, in Class 2.  Class 2 uses exotic dielectrics such as barium titanate (BaTiO) with some other strange additives in order to get high dielectric constant in the thousande (to increase capaitance density).  Barium titanate is a ferro-electric material, which is the source of voltage/capacitance misery.

> From here down,  thanks to Hadrien!

## Case study

Since this page was originally written for Microwaves101, the case study to illustrate this problem was taken from it. Suppose we want to redesign the good old breadboard RF pulsed (<a href="https://www.microwaves101.com/encyclopedias/breadboard-rf-modulator">https://www.microwaves101.com/encyclopedias/breadboard-rf-modulator</a>) source from 2006 with more recent components (first version of this page written in 2019). Start by the capacitors. Capacitors values which were at this time most often made with electrolytic capacitors are nowadays more often made with MLCC (multiple layers caramic) capacitors.

To replace the 4.7 µF capacitor, a simple search gives this component:

https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouche/8467296/ (4.7 µF)
<img src="{{ '/posts/MLCC-voltage-dependence/radiospares-1.png' | relative_url }}">

Seems rather nice, and smaller than the original. Wrong! Let’s check the detailed characteristics:

<a href="https://www.murata.com/en-global/products/productdetail.aspx?partno=GRM188R61A475KE15%23">https://www.murata.com/en-global/products/productdetail.aspx?partno=GRM188R61A475KE15%23</a>

<div id="plot-1"></div>
<script>
	async function makeplot() {
        url = "{{ '/posts/MLCC-voltage-dependence/GRM188R61A475KE15.csv' | relative_url }}";
		const data = await d3.csv(url);
        var x = [], y = [];
        for (var i=0; i<data.length; i++) {
            row = data[i];
            x.push(row['volt']);
            y.push(row['cap']);
        }
        /* Plot */
        var traces = [
            {x: x, y: y, showlegend: false},
            {x: [5.0], y: [1.93655214281807], mode: 'markers', marker: {symbol: 'x', size: 10}, showlegend: false}
        ];
        var layout = {
            title: "GRM188R61A475KE15 DC bias characteristics",
            xaxis: {title: {text: "DC Voltage [V]"}},
            yaxis: {title: {text: "Capacitance [µF]"}, range: [0, 5]}
        };
        Plotly.newPlot('plot-1', traces, layout);
	};
    makeplot();
</script>

Not good! If we need the 4.7 µF capacitance value, we’ll be soon in trouble.

Let’s search a bigger capacitor. We search the biggest value among MLCC capacitors having 10 V rating.
https://fr.rs-online.com/web/c/passifs/condensateurs/condensateurs-ceramique-multicouche/?applied-dimensions=4294244793,4291386526&pn=1
We find some nice models:

<img src="{{ '/posts/MLCC-voltage-dependence/radiospares-2.png' | relative_url }}">
<img src="{{ '/posts/MLCC-voltage-dependence/radiospares-3.png' | relative_url }}">
<img src="{{ '/posts/MLCC-voltage-dependence/radiospares-4.png' | relative_url }}">

Let's plot together their bias characteristics[^3]<sup>,</sup>[^4]<sup>,</sup>[^5]<sup>,</sup>[^6]<sup>,</sup>[^7]<sup>,</sup>[^8]:

<div id="plot-2"></div>
<script>
	async function makeplot() {
        /* Helper function to get csv graph */
        async function get_trace(url, name) {
            const data = await d3.csv(url);
            var x = [], y = [];
            for (var i=0; i<data.length; i++) {
                row = data[i];
                x.push(row['volt']);
                y.push(row['cap']);
            }
            return {x: x, y:y, name:name, line:{shape: 'spline'}, mode:'lines'}
        }
        /* Plot */
        var traces = [
            await get_trace("{{ '/posts/MLCC-voltage-dependence/GRM32ER61A107ME20.csv' | relative_url }}", name="Murata GRM32ER61A107ME20"),
            {x: [5.0], y: [45.94741861], mode: 'markers', showlegend: false, marker: {symbol: 'x', size: 10}},
            await get_trace("{{ '/posts/MLCC-voltage-dependence/C3216X5R1A107M160AC.csv' | relative_url }}", name="TDK C3216X5R1A107M160AC"),
            {x: [5.0], y: [28.7599], mode: 'markers', showlegend: false, marker: {symbol: 'x', size: 10}},
            await get_trace("{{ '/posts/MLCC-voltage-dependence/C1210C107M8PACTU.csv' | relative_url }}", name="Kemet C1210C107M8PACTU"),
            {x: [5.0], y: [49.60000000], mode: 'markers', showlegend: false, marker: {symbol: 'x', size: 10}},
        ];
        var layout = {
            title: "Selected capacitors DC bias characteristics",
            xaxis: {title: {text: "DC Voltage [V]"}},
            yaxis: {title: {text: "Capacitance [µF]"}, range: [0, 105]}
        };
        Plotly.newPlot('plot-2', traces, layout);
	};
    makeplot();
</script>

The values of the capacitors at 5 V range from 28.7 to 45.9 µF. Still low for 100 µF capacitors but all would be more than sufficient to replace the 4.7 µF capacitor of the original design.

Personnally, to keep some safety margin from the maximum voltage, I don't like using a capacitor at a voltage where its capacitance drops more than 50 % of its nominal value. So, if I had to redesign this board, I would continue searching capacitors, even when the Murata and Kemet capacitors are close matches.

## Conclusion of case study

As a conclusion, the "100 µF" capacitors of our study, when a DC voltage is applied to them, have an actual capacitance value much lower than their nominal value. This capacitance value would be still sufficient for our application because we oversized the capacitor. However, to keep a sufficient margin from voltage breakdown, I find careful to not use a capacitor at a voltage where its capacitance drop is more than 50 %. In designs where the capacitors are undersized, the capacitance drop effect on applied voltage can be a bad surprise and lead to severe troubles. Such problems are pretty hard to debug if not aware because the cap meters instruments most often measure at 0 V.

An other interesting point is what happens when we combine both biasing and temperature effects. Let’s see an other curve provided by TDK:

<img src="{{ '/posts/MLCC-voltage-dependence/temperature.png' | relative_url }}">

The temperature dependence is better when biased. This leads to the conclusion that temperature coefficient is most often less troublesome than voltage coefficient for MLCC capacitors.

[^3]: [https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouches/8851960/](https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouches/8851960/)
[^4]: [https://www.murata.com/en-global/products/productdetail.aspx?partno=GRM32ER61A107ME20%23](https://www.murata.com/en-global/products/productdetail.aspx?partno=GRM32ER61A107ME20%23)
[^5]: [https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouches/1084055](https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouches/1084055)
[^6]: [https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3216X5R1A107M160AC](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3216X5R1A107M160AC)
[^7]: [https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouches/8410809/](https://fr.rs-online.com/web/p/condensateurs-ceramique-multicouches/8410809/)
[^8]: [http://ksim.kemet.com/Plots/SpicePlots.aspx](http://ksim.kemet.com/Plots/SpicePlots.aspx)

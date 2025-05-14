---
layout: post
title: Microstrip formulas comparison.
permalink: /posts/microstrip-formulas-comparison.html
last_modified_at: 2025-05-14
---

## Introduction

The designer has several tools and formulas available to calculate the characteristic impedance of microstrip lines. Some are highly precise but rather complex like the Hammerstad and Jensen formulas[^1a]<sup>,</sup>[^2]<sup>,</sup>[^3], while others are rather simple but with questionable accuracy like the IPC-2141 formulas[^4]<sup>,</sup>[^5]<sup>,</sup>[^6]. While approximations can be useful for the first steps of a design, their accuracy must be evaluated before use. The authors of Qucs[^3] made some comparison, but this comparison don’t include the common IPC formulas[^5]<sup>,</sup>[^6]. A comparison of the most common microstrip calculation formulas is shown here.

While Hammerstad and Jensen formulas[^1a] stay the gold standard, other formulas can be safely used but that IPC-2141 formulas[^4]<sup>,</sup>[^5]<sup>,</sup>[^6] must be used with extreme caution.

## Geometry of the problem

![](/posts/microstrip-formulas-comparison/microstrip.png)

<!-- FIXME: Ugly tweak. -->
<style>
    .style-figcaption-after + p {
      font-style: italic;
      text-align: center;
    }
</style>
<div class="style-figcaption-after"></div>

Fig. 1 – Geometry of a microstrip line[^4].

The geometrical parameters of the microstrip line studied are defined in Fig. 1[^4]: w is the width of the microstrip line, h the height of the substrate, t the thickness of the strip. Non-geometrical parameters are the relative permittivity of the substrate. We’ll note for the characteristic impedance of free space.

To simplify the analysis, the strip conductivity is assumed to be infinite, the substrate losses to be null, the thickness t to be null and the frequency to be null. Note that the infinite conductivity hypothesis implies the absence of low-frequency dispersion[^7]<sup>,</sup>[^8]. These assumptions are often used in RF and microwave design, and are of good accuracy for the impedance calculation.

## Reference formula for Microstrip

Evaluating the accuracy of models needs a reference to compare to. Hammerstad and Jensen formulas are the most accurate closed-form formulas, and their accuracy is higher than manufacturing processes. They are commonly used in CAD software[^3]<sup>,</sup>[^9] in which the accuracy of the models of single microstrip lines without discontinuities is recognized. However, these formulas are so complex than their practical use for a comparison can lead to type errors during implementation, which can lead to inaccuracies. 3D EM simulations can be as accurate as needed, but their setup and calculation time is time consuming when accuracy is needed. Measurements are highly expensive due to the need of accuracy in both manufacturing and characterization of board materials. So, for this setup, a well-known software is used, TXLine from AWR. This software implements probably Hammerstad and Jensen formulas and its wide use almost guarantees that the implementation is bug free.

## Formulas to be compared

The formulas to be compared are the following:

### TXLine

TXLine is a small software, lightweight and free to use, from AWR, which allows to calculate the characteristic impedance of transmission lines like microstrip and striplines. A screenshot is shown Fig. 2.

<figure>
  <img src="/posts/microstrip-formulas-comparison/txline.png" alt="TXLINE 2003 - Microstrip" style="width:100%">
  <figcaption>Fig. 2 – Screenshot of TXLine software.</figcaption>
</figure>

Since TXLine has no direct option to handle the infinite conductivity, the zero thickness or the zero frequency, they were approximated as follows: conductivity <asciimath>10^99\ "S"\cdot"m"^-1</asciimath>, thickness 0.1 µm or 0.001 µm (depending on cases), and frequency 1 Hz. The high conductivity can be considered as infinite for all practical purposes, and is high enough to avoid the impact of low-frequency dispersion on the calculation results [^7]<sup>,</sup>[^8]. The thickness also is low enough to approximate the zero-thickness condition.

### Hammerstad and Jensen

According to Hammerstad and Jensen formulas[^1a]<sup>,</sup>[^2]<sup>,</sup>[^3] the calculation is made in two steps. First, the effective dielectric constant is calculated:

<latexmath>
  \begin{array}{c}
    u(w, h) = \frac{w}{h} \\
    a(u) = 1 + \frac{1}{49} \cdot \ln \left[ \frac{u^4 + \left( \frac{u}{52} \right)^2}{u^4 + 0.432} \right] + \frac{1}{18.7} \cdot \ln \left[ 1 + \left( \frac{u}{18.1} \right) \right] \\
    b(\varepsilon_r) = 0.564 \cdot \left( \frac{\varepsilon_r - 0.9}{\varepsilon_r + 3} \right)^{0.053} \\\
    \varepsilon_{r, \text{eff}}(u, \varepsilon_r) = \frac{\varepsilon_r + 1}{2} + \frac{\varepsilon_r - 1}{2} \cdot \left( 1 + \frac{10}{u} \right)^{-a(u) \cdot b(\varepsilon_r)} \\
  \end{array}
</latexmath>

Thereafter, the following formulas are used to calculate the characteristic impedance of the microstrip line, assuming the line is in an homogeneous medium of dielectric constant :

<latexmath>
  \begin{array}{c}
    f(u) = 6 + (2 \cdot \pi - 6) \cdot \exp \left[ - \left( \frac{30.666}{u} \right)^{0.7528} \right] \\
    Z_L(u) = \frac{Z_{F0}}{2 \cdot \pi \cdot \sqrt{\varepsilon_{r, \text{eff}}}} \cdot \ln \left[ \frac{f(u)}{u} + \sqrt{1 + \left( \frac{2}{u} \right)^2} \right]
  \end{array}
</latexmath>

Note that in reference[^1a], the formulas are not very clear about whether or should be used, but this point was double-checked in the Excel spreadsheet formulas.

These formulas are used in these calculators[^10]<sup>,</sup>[^11].

### Wheeler 1965

Wheeler’s formulas are sometimes encountered in technical literature[^3]<sup>,</sup>[^12]. They are rather accurate for most uses, as will be seen in following sections. Their main problem is the undesirable impedance step. Note that, contrary to Hammerstad and Jensen formulas, the effective dielectric constant is not used in the characteristic impedance formulas.

<!-- FIXME: Ugly tweak, should be put in CSS. -->
<latexmath style='font-size:12px'>
  Z_L(w, h, \varepsilon_r) = 
  \begin{cases}
    \frac{Z_{F0}}{2\sqrt{\varepsilon_r}} \cdot \left( \frac{w}{2h} + \frac{1}{\pi} \cdot \ln 4 + \frac{\varepsilon_r + 1}{2\pi\varepsilon_r} \cdot \ln \left[ \frac{\pi \cdot e}{2} \cdot \left( \frac{w}{2h} + 0.94 \right) \right] + \frac{\varepsilon_r - 1}{2\pi\varepsilon_r^2} \cdot \ln \left( \frac{e \cdot \pi^2}{16} \right) \right) & \text{if} \quad \frac{w}{h} \leq 3.3 \\
    \\
    \frac{Z_{F0}}{\pi \sqrt{2(\varepsilon_r + 1)}} \cdot \left[ \ln \left( \frac{4h}{w} \right) + \sqrt{\left( \frac{4h}{w} \right)^2 + 2} - \frac{1}{2} \cdot \frac{\varepsilon_r - 1}{\varepsilon_r + 1} \cdot \left( \ln \frac{\pi}{2} + \frac{1}{\varepsilon_r} \cdot \ln \frac{4}{\pi} \right) \right] & \text{if} \quad \frac{w}{h} > 3.3
  \end{cases}
</latexmath>

We have not found any calculator using these formulas.

### Wheeler 1977

Wheeler 1977 formulas are seen more often than Wheeler 1965 formulas in literature[^4]<sup>,</sup>[^13]<sup>,</sup>[^14]<sup>,</sup>[^15]. They are attributed sometimes to Wadell because he made a good summary in his book[^13]. Note that these formulas are incorrectly typed a reference[^4], where a <asciimath>pi^2</asciimath> was incorrectly replaced by a <asciimath>sqrt(pi)</asciimath>, and an extra square root is present, as pointed by an other reference[^16].

<latexmath>
  \begin{array}{c}
    A = \frac{14 + \frac{8}{\varepsilon_r} \cdot \frac{4 \cdot h}{w'}}{11} \\
    B = \sqrt{A^2 + \frac{1 + \frac{1}{\varepsilon_r} \cdot \pi^2}{2}} \\
    Z_L = \frac{Z_{0F}}{2 \cdot \sqrt{2} \cdot \pi \cdot \sqrt{\varepsilon_r + 1}} \cdot \ln \left[ 1 + \frac{4 \cdot h}{w} \cdot (A + B) \right]
  \end{array}
</latexmath>

They are used in several microwave calculators[^17]<sup>,</sup>[^18]<sup>,</sup>[^19]<sup>,</sup>[^20]<sup>,</sup>[^21]. Calculator[^21] has a mistake in the handling of <asciimath>epsilon_(r,"eff")</asciimath>, which can be diagnosed by calculating impedances with <asciimath>epsilon_r=1</asciimath>.

No explicit formula is given for <asciimath>epsilon_(r,"eff")</asciimath>. The reason is that it can be calculated with: <asciimath>epsilon_(r,"eff")=[(Z_0(h,w,epsilon_r=1))/(Z_0(h,w,epsilon_r=epsilon_r))]^2</asciimath>. This makes these formulas both simple and complex at the same time. In a programming language, it is easy to define a function and to use it two times to calculate . In an old school Excel sheet this would lead to use twice plus one many columns, which more than Hammerstad & Jansen formulas.

### Hammerstad 1975 formulas

Often seen in websites[^22] or in lectures on microwave techniques[^23]<sup>,</sup>[^24], Hammerstad’s 1975 formulas are the following[^22]<sup>,</sup>[^25]<sup>,</sup>[^26]<sup>,</sup>[^27]<sup>,</sup>[^28]. They are often attributed to Bahl, who made an improvement to their strip thickness correction[^26]<sup>,</sup>[^27], not investigated in this article, but the zero-thickness formulas originates from Hammerstad[^25].

<latexmath>
  \begin{eqnarray}
    \varepsilon_{r, \text{eff}} &=&
    \begin{cases} 
      \frac{\varepsilon_r + 1}{2} + \frac{\varepsilon_r - 1}{2} \cdot \left( \left(1 + \frac{12 \cdot h}{w}\right)^{-1/2} + 0.04 \cdot \left(1 - \frac{w}{h}\right)^2 \right) & \text{if} \quad \frac{w}{h} \leq 1 \\ \\
      \frac{\varepsilon_r + 1}{2} + \frac{\varepsilon_r - 1}{2} \cdot \left( 1 + \frac{12 \cdot h}{w} \right)^{-1/2} & \text{if} \quad \frac{w}{h} > 1
    \end{cases} \\
    Z_L &=&
    \begin{cases} 
      \frac{Z_0}{2 \cdot \pi \cdot \sqrt{\varepsilon_{r, \text{eff}}}} \cdot \ln \left( \frac{8 \cdot h}{w} + \frac{w}{4 \cdot h} \right) & \text{if} \quad \frac{w}{h} \leq 1 \\ \\
      \frac{Z_{F0}}{\sqrt{\varepsilon_{r, \text{eff}}}} \cdot \left[ \frac{w}{h} + 1.393 + 0.667 \cdot \ln \left( \frac{w}{h} + 1.444 \right) \right]^{-1} & \text{if} \quad \frac{w}{h} \geq 1
    \end{cases}
  \end{eqnarray}
</latexmath>

These formulas are used in these calculators[^29]<sup>,</sup>[^30]<sup>,</sup>[^31]. Note that this calculator[^30] also includes frequency thickness correction and dispersion.

### Schneider

Not often seen, Schneider formulas[^3]<sup>,</sup>[^32] are as following:

<latexmath>
  \varepsilon_{r, \text{eff}} = \frac{\varepsilon_r + 1}{2} + \frac{\varepsilon_r - 1}{2} \cdot \frac{1}{\sqrt{1 + 10 \cdot \frac{h}{w}}}
</latexmath>
<latexmath>
  Z_L = \frac{Z_{F0}}{\sqrt{\varepsilon_{r, \text{eff}}}} \cdot 
  \begin{cases} 
    \frac{1}{2 \cdot \pi} \cdot \ln \left( \frac{8 \cdot h}{w} + \frac{w}{4 \cdot h} \right) & \text{if} \quad \frac{w}{h} \leq 1 \\ \\
    \frac{1}{\frac{w}{h} + 2.42 - 0.44 \cdot \frac{h}{w} + \left(1 - \frac{h}{w}\right)^6} & \text{if} \quad \frac{w}{h} > 1
  \end{cases}
</latexmath>

We have not found any calculator using this formula.

### IPC-2141 formulas

The IPC-2141 formulas[^4]<sup>,</sup>[^5]<sup>,</sup>[^6]<sup>,</sup>[^28] are very popular. However, despite their popularity, they should be used with extreme caution, as will be demonstrated during our comparison, because their range of validity is extremely narrow, and they have a bad asymptotic behavior.

Although they are widely quoted, their narrow range of validity is much less often quoted[^28]: <asciimath>0.1<w/h<2.0</asciimath> and <asciimath>1<epsilon_r<15</asciimath>. This range becomes even narrower because it enables to synthesize 50 Ω lines only for <asciimath>3.9<epsilon_r<15</asciimath>.

Contrary to other formulas (Hammerstad and Jensen, Wheeler 1965, Wheeler 1977, Schneider and Hammerstad 1975), IPC-2141 formulas have a totally nonsense asymptotic behavior. All other formulas were found to have an accuracy better than 1.5 % for <asciimath>epsilon_r=4.5</asciimath> and <asciimath>w/h</asciimath> ratios ranging from 0.001 to 1000. On the contrary, IPC-2141 formulas give a nonsense negative impedance result for <asciimath>w/h>7.5</asciimath>. This is a large line for most applications, but it still happens in some designs, and give an idea of the problem.

Fig. 1 compares the asymptotic behavior of IPC-2141 formulas with the good formulas. While IPC-2141 have a very bad asymptotic behavior for large lines, all good formulas have a good asymptotic behavior on the very wide range <asciimath>0.001<w/h<1000</asciimath>, well outside of their guaranteed validity range.

<figure>
  <img src="/posts/microstrip-formulas-comparison/asymptotic-behavior.png" alt="">
  <figcaption>Fig. 3 – Asymptotic behavior of formulas.</figcaption>
</figure>

Despite the problems of IPC-2141 formulas, they are used in several online calculators[^33]<sup>,</sup>[^34]<sup>,</sup>[^35]<sup>,</sup>[^36]<sup>,</sup>[^37]<sup>,</sup>[^38]<sup>,</sup>[^39]<sup>,</sup>[^40]. Some calculators[^33]<sup>,</sup>[^34]<sup>,</sup>[^35] give warnings when using IPC-2141 formulas outside of their validity range like shown in Fig. 3. On the contrary, some other calculators[^36]<sup>,</sup>[^37]<sup>,</sup>[^38]<sup>,</sup>[^39]<sup>,</sup>[^40] give neither a warning nor a validity range, including a calculator on a renowned website[^38]. Worse, some calculators[^38]<sup>,</sup>[^39]<sup>,</sup>[^40] even give nonsense negative impedance when fed with proper values without any warning.

![](/posts/microstrip-formulas-comparison/ipc-warning.png)

<!-- FIXME: Ugly tweak. -->
<style>
    .style-figcaption-after + p {
      font-style: italic;
      text-align: center;
    }
</style>
<div class="style-figcaption-after"></div>
Fig. 4 – Screenshot of a microstrip line impedance calculator[^33] raising a warning when trying to calculate impedances outside IPC-2141 validity range.

It should be mentioned that a calculator[^33] not only gives the validity range of the IPC-2141 formula and warns when trying to enter parameters outside of this range, but it also gives accuracy data.

## Comparison results

<figure>
  <img src="/posts/microstrip-formulas-comparison/error-all-formulas.png">
  <figcaption>Fig. 5 – Error of all formulas.</figcaption>
</figure>

<figure>
  <img src="/posts/microstrip-formulas-comparison/error-without-IPC.png">
  <figcaption>Fig. 6 – Error of formulas without IPC-2141.</figcaption>
</figure>

From the Fig. 5 graph, a clear outsider in inaccuracy is the IPC-2141 formula, reaching up to 44 % inaccuracy! This formula will be commented later. Fig. 6 graph, without the IPC-2141 formula on a reduced scale, shows the relative error of the remaining formulas.

The H&J formulas are probably the formulas used in TXLine software since the calculated difference between them is lesser than 0.06 % ! Note that this calculated error is always positive, because TXLine took a line thickness which is non-zero, although very thin, contrary to our calculation. Since we are comparing the H&J formulas to themselves, this benchmark does not prove that they are the most accurate. However, since they are believed to be the most accurate in all the recent literature, we’ll stick to that conclusion. They still have the inconvenient of their complexity, which can lead to potential typing mistakes.

Hammerstad 1975 formulas are at the second place for accuracy: error less than 0,38 % on tested values. However, they still have the inconvenience of their complexity, potentially leading to typing mistake, and of the different expressions for different subdomains.

Wheeler 1965 formulas are at the third place for accuracy: error less than 0.59 % on tested values. However, the calculation step makes them troublesome to use in some cases. And, for use in Excel spreadsheets, it makes mandatory to duplicate the formulas. The 0,06 % accuracy gained from Wheeler 1977 is not worth it.

Wheeler 1977 formulas, although not very known, are rather simple and rather accurate: the error is lesser than 0.66 % on tested values. The absence of impedance steps in these formulas make them interesting.

Schneider formulas are less complex than Hammerstad 1975 formulas but less accurate. Their error is less than 1.6 %. Their interest is mainly historical.

The real strange point is the accuracy of the IPC-2141 formulas. Their relative error reach 44 % on the tested values! A closer look reveals that most of the error happens when the normalized width u is higher than 2. When plotted on a narrower range, like in Fig. 7, the relative error is much lower: less than 2.1 %. This is precisely the range of values of the 50 Ω lines.

<figure>
  <img src="/posts/microstrip-formulas-comparison/error-narrow-range.png">
  <figcaption>Fig. 7 – Error of all formulas on a narrow w/h range.</figcaption>
</figure>

## Review of calculators

The following table sums up some microstrip calculators and the formulas which they use. Only microstrip calculators for which the formula was told or could be inferred from JavaScript source code were included.

<!-- FIXME: Ugly tweak. -->
<style>
    .style-table-after + table,
    .style-table-after + table th,
    .style-table-after + table td {
      border: 1px solid black;
      border-collapse: collapse;
    }
</style>
<div class="style-table-after"></div>

| Website                       | Formula         | Val. warn | Comments                                                                      |
| ----------------------------- | --------------- | --------- | ----------------------------------------------------------------------------- |
| www.microwaves101.com[^10]    | H&J             |           |                                                                               |
| mcalc.sourceforge.net[^11]    | H&J             |           |                                                                               |
| www.eeweb.com[^17]            | Wheeler 1977    |           |                                                                               |
| cepd.com[^18]                 | Wheeler 1977    |           |                                                                               |
| www.finetune.co.jp[^19]       | Wheeler 1977    |           |                                                                               |
| leleivre.com[^20]             | Wheeler 1977    |           |                                                                               |
| chemandy.com[^21]             | Wheeler 1977    |           | _Confusion between ε<sub>r</sub> and ε<sub>r,eff</sub>._                      |
| www.pasternack.com[^29]       | Hammerstad 1975 |           |                                                                               |
| www.emclab.cei.uec.ac.jp[^30] | Hammerstad 1975 |           |                                                                               |
| chemandy.com[^31]             | Hammerstad 1975 |           |                                                                               |
| emclab.mst.edu[^33]           | IPC-2141        | Yes       |                                                                               |
| referencedesigner.com[^34]    | IPC-2121        | Yes       | _Formulas not told in document, but seen in JavaScript source code._          |
| technick.net[^35]             | IPC-2141        | Yes       |                                                                               |
| a8blog.com[^36]               | IPC-2141        | No        | _No warnings, but at least does not print the calculated negative impedance._ |
| www.everythingrf.com[^38]     | IPC-2141        | No        |                                                                               |
| chemandy.com[^39]             | IPC-2141        | No        |                                                                               |
| ncalculators.com[^40]         | IPC-2121        | No        |                                                                               |

## Conclusion

While H&J formulas are the gold standard for calculations, several other formulas give a good trade-off between accuracy and simplicity which are sufficient for most applications. Wheeler 1977 is the clear winner of this tradeoff with 0.66 % error when <asciimath>epsilon_(r,"eff")</asciimath> is not needed. However, on old school Excel sheets, when <asciimath>epsilon_(r,"eff")</asciimath> is needed, the need to duplicate the calculation makes it not anymore convenient than H&J formulas. In this case, Hammerstad 1975 is the winner of this tradeoff with 0.38 % error.

IPC-2141 formulas have severe issues and must be used with extreme caution.      

<!-- 1a ref instead of 1 needed due to a strange bug. -->

[^1a]: E. Hammerstad and O. Jensen, "Accurate Models for Microstrip Computer-Aided Design," in _Microwave symposium Digest, 1980 IEEE MTT-S International_, 1980.

[^2]: S. J. Orfanidis, "Electromagnetic waves and antennas," 2016. \[Online\]. Available (archive): <https://web.archive.org/web/20240528230718/www.ece.rutgers.edu/~orfanidi/ewa/>. \[Accessed 14 May 2025\].

[^3]: S. Jahn, M. Margraf, V. Habchiand and R. Jacob, "Qucs technical papers," 2007.

[^4]: A. J. Burkhardt, C. S. Gregg and J. A. Staniforth, "Calculation of PCB track impedance," \[Online\]. Available: <https://www.polarinstruments.com/support/cits/IPC1999.pdf>. \[Accessed 03 April 2020\].

[^5]: Analog Devices, "Microstrip and stripline design," 2009                                                                                                                                                                        
[^6]: Institute for Interconnection and Packaging Electronic Circuits, _Standard IPC-2141A, "Controlled Impedance Circuit Boards and High Speed Logic Design",_ 2004.

[^7]: S. Huettner, "Low frequency dispersion in TEM lines," June 2011. \[Online\]. Available: <https://www.microwaves101.com/encyclopedias/low-frequency-dispersion-in-tem-lines>.

[^8]: S. Ellingson, "Dispersion in coaxial cables," 01 June 2008. \[Online\]. Available (archive): <https://leo.phys.unm.edu/~lwa/memos/memo/lwa0136.pdf>. \[Accessed 14 May 2025\].

[^9]: Agilent Technologies, "Advanced Design System 2011.01 - Distributed components".                                                                                                                                                                        
[^10]: D. Campbell and S. Huettner, "Microstrip calculator," Microwaves101, \[Online\]. Available: <https://www.microwaves101.com/calculators/1201-microstrip-calculator>. \[Accessed 13 April 2020\].

[^11]: D. R. McMahill, "Microstrip analysis/synthesis calculator," 16 February 2020. \[Online\]. Available: <http://mcalc.sourceforge.net/>. \[Accessed 13 April 2020\].

[^12]: H. A. Wheeler, "Transmission-line properties of parallel strips separated by a dielectric sheet," _IEEE transactions on microwave theory and techniques,_ vol. 13, no. 2, pp. 172-185, 1965.

[^13]: B. C. Wadell, Transmission line design handbook, 1991.

[^14]: H. A. Wheeler, "Transmission-line properties of a strip on a dielectric sheet on a plane," _IEEE transactions on microwave theory and techniques,_ vol. 25, no. 8, pp. 631-647, August 1977.    

[^15]: Wikipedia contributors, "Microstrip - Wikipedia, the free encyclopedia," \[Online\]. Available: <https://en.wikipedia.org/w/index.php?title=Microstrip&oldid=949478476>. \[Accessed 07 April 2020\].

[^16]: Z. Peterson, "Clearing up trace impedance calculators and formulas," 19 May 2019. \[Online\]. Available: <https://resources.altium.com/p/clearing-up-trace-impedance-calculators-and-formulas>. \[Accessed 07 April 2020\].

[^17]: EEWeb, "Microstrip," \[Online\]. Available: <https://www.eeweb.com/tools/microstrip-impedance>. \[Accessed 07 April 2020\].

[^18]: Colorado Electronic Product Design, "Microstrip impedance calculator," 2013. \[Online\]. Available: <http://cepd.com/calculators/microstrip.htm>. \[Accessed 07 April 2020\].     

[^19]: T. Hosoda, "Online calculator - Synthesize/Analyze microstrip transmission line," Finetune co., ltd., 25 December 2017. \[Online\]. Available: <http://www.finetune.co.jp/~lyuka/technote/ustrip/>. \[Accessed 07 April 2020\].   

[^20]: Le Leivre.com, "Microstrip impedance calculator," \[Online\]. Available: <http://leleivre.com/rf_microstrip.html>. \[Accessed 20 April 2020\].

[^21]: W. J. Highton, "Microstrip transmission line characteristic impedance calculator using an equation by Brian C Wadell," 28 November 2019. \[Online\]. Available: <https://chemandy.com/calculators/microstrip-transmission-line-calculator.htm>. \[Accessed 07 April 2020\].

[^22]: S. Huettner, "Microstrip," \[Online\]. Available: <https://www.microwaves101.com/encyclopedias/microstrip>. \[Accessed 02 April 2020\].

[^23]: P. T.-L. Wu, "Microwave Filter Design," 11 February 2011. \[Online\]. Available: <http://ntuemc.tw/upload/file/2011021716275842131.pdf>. \[Accessed 12 April 2020\].

[^24]: P. G. Kumar, "Microwave theory and technology", lecture 9, 03 Septembre 2018. \[Online\]. Available: <https://archive.nptel.ac.in/courses/108/101/108101112/>. \[Accessed 14 May 2025\].

[^25]: E. O. Hammerstad, "Equations for microstrip circuit design," in _Proc. European Microwave Conf._, 1975.

[^26]: I. J. Bahl and D. K. Trivadi, "A designer's guide to microstrip line," _Microwaves,_ pp. 174-182, May 1977.

[^27]: I. J. Bahl and R. Garg, "Simple and accurate formulas for a microstrip with finite strip thickness," _Proceedings of the IEEE,_ vol. 65, no. 11, pp. 1611-1612, November 1977.

[^28]: S. H. Hall, G. W. Hall and J. A. McCall, High-speed digital system - a handbook of interconnect theory and design practices, Wiley, 2000.

[^29]: Pasternack, "Microstrip calculator," \[Online\]. Available: <https://www.pasternack.com/t-calculator-microstrip.aspx>. \[Accessed 12 April 2020\].

[^30]: F. Xiao, "Microstrip trace impedance calculator," \[Online\]. Available: <http://www.emclab.cei.uec.ac.jp/xiao/MSline/index.html>. \[Accessed 12 April 2020\].

[^31]: W. J. Highton, "Microstrip transmission line characteristic impedance calculator," Chemandy electronics, 2 January 2020. \[Online\]. Available: <https://chemandy.com/calculators/microstrip-transmission-line-calculator-hartley27.htm>. \[Accessed 13 April 2020\].

[^32]: M. V. Schneider, "Microstrip lines for microwave integrated circuits," _The Bell System technical journal,_ vol. 48, pp. 1421-1444, May 1969.

[^33]: Electromagnetic compatibility laboratory, "Microstrip impedance calculator," \[Online\]. Available: <https://emclab.mst.edu/resources/tools/pcb-trace-impedance-calculator/microstrip/>. \[Accessed 12 April 2020\].

[^34]: Reference Designer, "Microstrip Impedance Calculator," \[Online\]. Available: <http://referencedesigner.com/tutorials/si/si_06.php>. \[Accessed 12 April 2020\].

[^35]: N. Asuni, "PCB Impedance and Capacitance of Microstrip," 01 March 1998. \[Online\]. Available: <https://technick.net/tools/impedance-calculator/microstrip/>. \[Accessed 12 April 2020\].

[^36]: A8 blog, "Online microstrip impedance calculator with multiple units," \[Online\]. Available: <https://www.a8blog.com/en_microstrip.htm>. \[Accessed 13 April 2020\].

[^38]: R. Kapur, "Microstrip impedance calculator," everything RF, \[Online\]. Available: <https://www.everythingrf.com/rf-calculators/microstrip-impedance-calculator>. \[Accessed 06 April 2020\].

[^39]: W. J. Highton, "Microstrip transmission line calculator using IPC-2141 equation," Chemandy electronics, 2 January 2020. \[Online\]. Available: <https://chemandy.com/calculators/microstrip-transmission-line-calculator-ipc2141.htm>. \[Accessed 13 April 2020\].

[^40]: ncalculators.com, "Microstrip impedance calculator," \[Online\]. Available: <https://ncalculators.com/electronics/microstrip-impedance-calculator.htm>.

[^41]: I. Sukiswo, "Elektronika telekomunikasi, Microstrip," 08 December 2009. \[Online\]. Available: <http://www.elektro.undip.ac.id/sukiswo/?KULIAH:Elektronika_Telekomunikasi>. \[Accessed 16 April 2020\].

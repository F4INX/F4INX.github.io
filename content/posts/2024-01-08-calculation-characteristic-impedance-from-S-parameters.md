---
title: "Calculation of characteristic impedance from S parameters."
date: 2024-01-08
lastmod: 2024-01-08T05:03:00+01:00
categories: [S-parameters, Transmission Lines]
url: /posts/calculation-characteristic-impedance-from-S-parameters.html
excerpt: "Suppose one wants to measure or simulate the characteristic impedance of something similar to a transmission line. This can be for example a 75 Ω coax cable or a via structure on HFSS. The characteristic impedance can be calculated form its measured or simulated S parameters references to 50 Ω."
related_posts:
  - "Transfer S parameters."
  - "Microstrip formulas comparison."
---


## Introduction

Suppose one wants to measure or simulate the characteristic impedance of something similar to a transmission line. This can be for example a 75&#8239;Ω coax cable or a via structure on HFSS. The characteristic impedance can be calculated form its measured or simulated S parameters references to 50&#8239;Ω.

Suppose also that the structure is "symmetric enough" to have the same characteristic impedance on each side (see <a href="https://en.wikipedia.org/wiki/Image_impedance">https://en.wikipedia.org/wiki/Image_impedance</a>)...

## Recommended method using ABCD parameters

According to <a href="https://en.wikipedia.org/wiki/Image_impedance">https://en.wikipedia.org/wiki/Image_impedance</a>, and assuming the symmetry hypothesis which allows to simply discard the second result, the characteristic impedance can be calculated as:

<asciimath>
Z_0 = sqrt((A B)/(C D))
</asciimath>

The ABCD parameters can be obtained from S parameters with <a href="https://www.microwaves101.com/encyclopedias/network-parameters">https://www.microwaves101.com/encyclopedias/network-parameters</a>:

<asciimath>
  {: ( A = ((1 + S_(11))(1 - S_(22)) + S_(12)S_(21))/(2S_(21)) ,
       B = 50 Omega ((1 + S_(11))(1 + S_(22)) - S_(12)S_(21))/(2S_(21)) ),
     ( C = 1/(50 Omega) ((1 - S_(11))(1 - S_(22)) - S_(12)S_(21))/(2S_(21)) ,
       D = ((1 - S_(11))(1 + S_(22)) + S_(12)S_(21))/(2S_(21)) ) :}
</asciimath>

Calculation is made as follows:

<asciimath>
  Z_0 = 50 Omega sqrt(
    (
      ((1 + S_(11))(1 - S_(22)) + S_(12)S_(21))
      ((1 + S_(11))(1 + S_(22)) - S_(12)S_(21))
    ) / (
      ((1 - S_(11))(1 - S_(22)) - S_(12)S_(21))
      ((1 - S_(11))(1 + S_(22)) + S_(12)S_(21))
    )
</asciimath>

These formulas can be conveniently entered into an Excel spreadsheet.

## Alternative non recommended method using transfer S parameters

Transfer S parameters can also be used for this calculation. However, this method is **NOT** recommended because the calculations are cumbersome.

Expressing the characteristic impedance as a reflection coefficient from 50&#8239;Ω, and recalling that by definition its invariant through the system, the following can be written:

<asciimath>
  [[b_1],[a_1]] = [[T_11,T_12],[T_21,T_12]] \ [[a_2],[b_2]]
</asciimath>

<asciimath>
  Gamma = b_1 / a_1 = (T_11 Gamma b_2 + T_12 b_2)/(T_21 Gamma b_2 + T_12 b_2) = (T_11 Gamma + T_12)/(T_21 Gamma + T_12)
</asciimath>

Rearranging:

<asciimath>
  Gamma (T_21 Gamma + T_12) = (T_11 Gamma + T_12)
</asciimath>

<asciimath>
  T_21 Gamma^2 + (T_12 - T_11) Gamma - T_12 = 0
</asciimath>

Solving by the usual methods:
<asciimath>
  Delta = (T_(12)-T_(11))^2+4*T_(21)*T_(12)
</asciimath>
<asciimath>
  Gamma = (T_(11) - T_(12) +- sqrt((T_(12)-T_(11))^2+4*T_(21)*T_(12)))/(2*T_(21))
</asciimath>

So, the procedure, can be outlined as follows:

1. Convert S parameters to T parameters using the previous formulas or scikit-rf (<a href="https://scikit-rf.readthedocs.io/en/latest/api/generated/skrf.network.s2t.html">https://scikit-rf.readthedocs.io/en/latest/api/generated/skrf.network.s2t.html</a>)

2. Calculate the <asciimath>Gamma</asciimath> of the characteristic impedance references to 5&#8239;Ω.

3. From the <asciimath>Gamma</asciimath>, calculate the characteristic impedance.


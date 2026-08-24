---
title: "Transfer S parameters."
date: 2022-03-23
lastmod: 2022-03-23T13:30:00+01:00
categories: [S-parameters, Network Analysis]
url: /posts/transfer-S-parameters.html
excerpt: "Originally published on Microwaves 101, an explanation of transfer S-parameters and their applications."
related_posts:
  - "Calculation of characteristic impedance from S parameters."
---


<p class="begin-note">This content was originally published on Microwaves 101 (<a href="https://www.microwaves101.com/encyclopedias/transfer-s-parameters">https://www.microwaves101.com/encyclopedias/transfer-s-parameters</a>). Many thanks to Steve for hosting the original version. Have a look on his website for more interesting content.</p>

<!-- Manually included to set size, class and alt. Zoomed for better rendering. -->
<img class="dark-mode-invert" src="/posts/transfer-S-parameters/S-parameters.svg" alt="S-parameters matrix of generalized two-port network with characteristic impedance Z0" style="min-width:50%;">

Transfer S parameters are a convenient way to express S parameters in a way that allows to easily cascade blocks. They have the same principle as ABCD parameters: they express all relevant input quantities in function of all relevant output quantities, contrary to normal S parameters which express all scattered waves in function of all incident waves, and are messy when cascading blocks. They are sometimes more convenient than ABCD parameters, because they work with wave quantities instead of voltages and current, which are very difficult to measure at high frequencies.

It is very counter-intuitive, but expressing input in function of output and not the inverse allows to deal with unilateral blocks, what the other convention doesn’t allow. They are most often defined in the following way:

<asciimath>
  [[b_1],[a_1]] = T \ [[a_2],[b_2]]
</asciimath>

Be careful! Another convention exists, with a and b inverted. Some people even express output in function of the input. So, pay attention  to the used convention when reading calculations from other people!

With the definition used in this page, the transfer parameter matrix of a chain of elements can be calculated as follows:

<asciimath>
  T = T_1 \ T_2 \ cdots \ T_N
</asciimath>

And, be careful, this is the inverse order as one expects. Yes, matrix multiplication is very convenient but sometimes crazy!

The following formulas can be used to pass from regular to transfer S parameter:

<asciimath>
  {: (  T_(11) = S_(12) - (S_(11)S_(22))/(S_(21))  ,  S_(11) = T_(12)/T_(22)                     ),
     (  T_(12) = S_(11)/S_(21)                     ,  S_(21) = 1/T_(22)                          ),
     (  T_(21) = - S_(22)/S_(21)                   ,  S_(12) = T_(11) - (T_(12)T_(21))/(T_(22))  ),
     (  T_(22) = 1/S_(21)                          ,  S_(22) = - T_(21)/T_(22)                   ) :}
</asciimath>

---
layout: post
title: Transfer S parameters.
permalink: /posts/transfer-S-parameters.html
last_modified_at: 2022-03-23 13:30
---
<script>
MathJax = { loader: {load: ['input/asciimath', 'output/chtml', 'ui/menu']} };
</script>
<script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/startup.js">
</script>

<p class="begin-note">This content was originally published on Microwaves 101 (<a href="https://www.microwaves101.com/encyclopedias/transfer-s-parameters">https://www.microwaves101.com/encyclopedias/transfer-s-parameters</a>). Many thanks to Steve for hosting the original version. Have a look on his website for more interesting content.</p>

[PICTURE]

Transfer S parameters are a convenient way to express S parameters in a way that allows to easily cascade blocks. They have the same principle as ABCD parameters: they express all relevant input quantities in function of all relevant output quantities, contrary to normal S parameters which express all scattered waves in function of all incident waves, and are messy when cascading blocks. They are sometimes more convenient than ABCD parameters, because they work with wave quantities instead of voltages and current, which are very difficult to measure at high frequencies.

It is very counter-intuitive, but expressing input in function of output and not the inverse allows to deal with unilateral blocks, what the other convention doesn’t allow. They are most often defined in the following way:

<p markdown="0">
`[[b_1],[a_1]] = T \ [[a_2],[b_2]]`
</p>

Be careful! Another convention exists, with a and b inverted. Some people even express output in function of the input. So, pay attention  to the used convention when reading calculations from other people!

With the definition used in this page, the transfer parameter matrix of a chain of elements can be calculated as follows:

<p markdown="0">
`T = T_1 \ T_2 \ cdots \ T_N`
</p>

And, be careful, this is the inverse order as one expects. Yes, matrix multiplication is very convenient but sometimes crazy!

The following formulas can be used to pass from regular to transfer S parameter:

<div markdown="1" align="center">

| <span markdown="0">`T_(11) = S_(12) - (S_(11)S_(22))/(S_(21))`</span>  | <span markdown="0">`S_(11) = T_(12)/T_(22)`</span>                    |
| <span markdown="0">`T_(12) = S_(11)/S_(21)`</span>                     | <span markdown="0">`S_(21) = 1/T_(22)`</span>                         |
| <span markdown="0">`T_(21) = - S_(22)/S_(21)`</span>                   | <span markdown="0">`S_(12) = T_(11) - (T_(12)T_(21))/(T_(22))`</span> |
| <span markdown="0">`T_(22) = 1/S_(21)`</span>                          | <span markdown="0">`S_(22) = - T_(21)/T_(22)`</span>                  |

</div>

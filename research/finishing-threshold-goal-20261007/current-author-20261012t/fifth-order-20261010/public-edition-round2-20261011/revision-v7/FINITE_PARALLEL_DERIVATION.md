# Parallel-pair necessary rows

Let J denote a positive quarter turn and n a unit separating normal. Put
Delta = d_w + delta_h the centre difference, |d_w| <= D, |delta_h| <= dr, and

    mu = (omega_i + omega_j)/2, eps = (omega_j - omega_i)/2,
    |mu| <= m, |eps| <= q <= 1/10,
    X = n.Delta, tau' = (Jn).d_w, |tau'| <= taumax < 1.

Here d_w includes the reference difference and the unscaled slider displacement.
The two surviving directed separating alternatives have different owners and
the same reference normal n. With n_m = R(mu)n, X_m = n_m.Delta,
tau_m = (Jn_m).Delta and e = |eps|, their disjunction implies

    cos(e) X_m + sin(e) |tau_m| >= cos(e)^2 + sin(e) cos(e).

This is the exact unit-square support formula: the other square's relative
angle is 2 eps, and cos(2 eps) is positive on the declared range. Since cos(e)>0,

    X_m - 1 >= cos(e)-1 + sin(e) - tan(e)|tau_m|
              >= e(1-|tau_m|) - e^2/2 - e^3/6 - e^3|tau_m|.

The last line uses cos(e)>=1-e^2/2, sin(e)>=e-e^3/6, and
tan(e)<=e+e^3. The latter follows already from sin(e)<=e and
cos(e)>=1-e^2/2: 1/(1-e^2/2)<=1+e^2 for 0<=e<=1/10.
These inequalities include e=0 without division by e.

Taylor's integral remainder and |R(mu)n-n|<=|mu| give

    |X_m - X - mu*tau'| <= D*m^2/2 + m*dr,
    |tau_m - tau'| <= D*m + dr.

Consequently, with

    E = D*m^2/2 + m*dr + q^2/2 + q^3/6
        + taumax*q^3 + (D*m+dr)*(q+q^3),

we have X-1+mu*tau'+E >= e(1-|tau'|). Because 1-|tau'|>0,
both necessary rows

    X-1+mu*tau' + s*eps*(1-|tau'|) + E >= 0,  s in {-1,+1},

follow. On a box where tau' has constant sign sigma, replace |tau'| by
sigma*tau'. Expanding mu and eps gives exactly the two rows at [file:FINITE_ROW_KERNEL],
lines 252–261, including coefficients (1+s*sigma)/2 and (1-s*sigma)/2
on slider times omega_i and omega_j. Those products are the physical true
products in the necessity argument; their McCormick relaxation preserves them.
If the constant-sign or taumax<1 guard fails, the code omits this pair.
No contact, stress, common-angle or local-minimality assumption is used.

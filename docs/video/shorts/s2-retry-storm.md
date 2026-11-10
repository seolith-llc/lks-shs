# Short S2 · The retry storm

## Your retry button is a weapon
- a dependency starts failing
- every layer retries
- what could go wrong?

Your service calls a service that calls a service. One of them starts failing. So every layer helpfully retries. Three retries each. What could possibly go wrong?

## 243 times the load
-! 243× | load amplification on the failing dependency
- 5 layers deep × 3 retries each

Five layers deep, three retries per layer. That is two hundred and forty three times the load hammering a service that is already dying. You just DDoSed yourself. AWS documented the math, and it is why backoff, jitter, and retry budgets exist.

## The fix
- capped exponential backoff
- jitter
- retry budgets — stop retrying when errors spike

Capped backoff. Jitter. And a retry budget that stops retrying when everyone else is failing too. Three lines of discipline. Links and sources at the repo on screen.

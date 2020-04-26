# guess-the-weight-gtk
[Z3 solver](https://github.com/Z3Prover/z3) PoC to calculate a weight plate combo to hit the desired weight (with a GTK interface).

## Install
Use [pipenv](https://github.com/pypa/pipenv) to set up the envionment or `pip install -r requirements.txt`.

## Use
* Run the app. 
* Select a bar weight.
* Set a target weight.
* Adjust maximum tries, if desired.
* Click 'Calculate".
* View results.

## Methodology
I have two non-standard bars to go with a pile of non-standard weight plates. The bars weigh 7 and 22 pounds, respectively. I wanted to easily calculate the best bar/plate combo to hit near or at a specified weight. I also wanted to tinker with Z3 Solver. Sounds like a good PoC to me!

The solver starts with the target and then tests incrementally distant weights above and below the target until a maximum number of tries:
```
goal = 100
try = {try #}

Try 0:
Upper = goal + try + 1
Lower = goal + try - 1

Try 1:
Upper = goal - try + 1
Lower = goal - try - 1
```




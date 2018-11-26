## Readme

Hopefully we have managed to write our code such that it remains faithful to the setup in the `makefile`. 

initiate bob first (which will always run.)
```
make bob
```

Then, on a seperate terminal, run alice using the predefined calls in the makefile.
```
make alice
```

I did not include the evaluation of the millionaires problem within the primary call to make it more `diff` friendly but this can be computed with `make alice millions`.

The program should work whichever way the execution is performed (i.e it should work if alice is called first and then bob).

alternatively you can use `local` which will compute the
garbled circuit and the oblivious transfer within the same
thread.

```
make local
```

To evaluate a single circuit json, add a third argument when running `alice`:

```
make alice millions
```

## Comments

The assignment was quite interesting and fun to work on,
although there is some differences between the explanations
on the lecture slides and the cryptography book which created
some confusion.

We're convinced that the coursework structure overall was well
though out however. :)
## MOO Lisp

> My [Own|Outstanding|Odd|Overrated|Offbeat|Obnoxious|Otherworldly]{2,} Lisp

Moo is a simple Lisp implemented in Python.
The implementation is probably not waterproof — the Python is bound to shine throgh occasionally and I might have gotten something wrong. Please let me know, or even better send a pull request, if you find something amiss!

Oh, and please don't do anything silly like using Moo for production code, or anything like that. This is obviously just a toy language.

### Usage

To run the REPL (see an example [here](http://ascii.io/a/5544)):

    ./moo

To interpret a file:

    ./moo example.moo


### Why did I write this thing?

**Short answer**: For fun.

**Longer answer**: Implementing your own programming language is a very educational experience. I wrote Moo Lisp both to better understand how programming languages works, and to test my understanding of some concepts I already knew. Hopefully, the implementation of Moo could also serve as an example to others getting started learning about languages.

### Run the tests

The test suite require `nosetests` to be installed. If you want to run the tests yourself, install dependencies like this:

    pip install -r requirements.txt

Then, run the tests

    nosetests

### License

The REPL cow is blatantly ripped from [cowsay](http://en.wikipedia.org/wiki/Cowsay), which is [GPL](http://en.wikipedia.org/wiki/GNU_General_Public_License).

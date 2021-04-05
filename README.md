# Numerical Methods
A Python library for root finding with various numerical methods.

## How to use
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the library required
```bash
pip install -r requirements.txt
```

## Usage
You can use it by running one of the script.
`For Example:`
```bash
$ python
>>> from .methods.bracketing import bisection
>>> bisection('x^2-8x+11', 1, 2, 0.001)
1.7646484375
```

## Planned features:
* GUI wrapper for the library

## Contributing
Currently I have no plans on fixing any issues or updating this since it is mostly used for
my university needs.

## License
[MIT](https://choosealicense.com/licenses/mit/)

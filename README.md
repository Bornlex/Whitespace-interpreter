# WhiteSpace VM
> A whitespace programming language VM

[![Python Version][python-image]][python-url]
[![Pip Version][pip-image]][pip-url]

The following program executes .ws (WhiteSpace) files.

![](header.png)

## About

Whitespace is an esoteric programming language that makes use of only 3 characters:
    - whitespace (of course)
    - tab
    - line feed

It has been invented by Edwin Brady & Chris Morris and released on 1st April 2003.

This is not that easy to find documentation and resources about writing Whitespace, but here are some good ones:
     - [http://web.archive.org/web/20150426193527/http://compsoc.dur.ac.uk:80/whitespace/tutorial.php](http://web.archive.org/web/20150426193527/http://compsoc.dur.ac.uk:80/whitespace/tutorial.php) (specs)
     - [http://vii5ard.github.io/whitespace/](http://vii5ard.github.io/whitespace/) (IDE)
     - [http://www.whoishostingthis.com/resources/whitespace-programming/](http://www.whoishostingthis.com/resources/whitespace-programming/) (Tutorial)

## Installation

OS X, Linux & Windows:

```sh
git clone https://github.com/Bornlex/WhitespaceCompiler.git
```

## Usage example

To execute a .ws file:
```sh
./main.py file_to_execute.ws
```

## Development setup

To add some functionalities to the program and to check that everything is working properly, just run:

```sh
make test
```

All tests should pass.

## Release History

* 0.0.1
    * First release

## Meta

Do not hesitate to contact me for any information or feedback:

jseveno.piltant@gmail.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[python-url]: https://www.python.org/
[pip-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[pip-url]: https://pypi.python.org/pypi/pip
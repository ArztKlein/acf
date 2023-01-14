<p align="center">
    <a href="https://github.com/ArztKlein/acf/issues" alt="Issues">
            <img src="https://img.shields.io/github/issues/ArztKlein/acf" /></a>
    <a href="https://pypi.org/project/acfile/" alt="PyPi version">
            <img src="https://img.shields.io/pypi/v/acfile" /></a>
    <a href="https://pypi.org/project/acfile/" alt="Downloads per month">
            <img src="https://img.shields.io/pypi/dm/acfile" /></a>
</p>

# ACF Advanced Configuration Format

Merging configuration files and programming languages so you don't have to create an interpreter for every project.

Get ACF syntax hightlighting for VS Code [here](https://github.com/ArztKlein/acf-highlighting).

## Installation

Install with `pip install acfile`

## Usage with Python

### Read an ACF file
```py
from acfile import read_file

config = read_file("<FILE_PATH>.acf")
```

### Read values
To read values, get the [section](#sections)
 name and then the value name from the acf object.

```py
print(config.SECTION_NAME.VALUE_NAME)
```

## ACF documentation
The file extension for an acf file is `.acf`.

### Sections

ACF has a section-based structure where the header is preceded by an `@` symbol. Example: `@header`. Each section contains key-value pairs.

### Values
A value contains a name and a value seperated by an equals symbol. Text values must be enclosed with speech marks. 

Example:

```acf
text = "this is text"
number = 42
```

### Referencing other values
As long as the value is in the same section, you can refernce them to perform math operations on. Order of operations is supported  

#### Examples:

```acf
a = 12
b = 2 + 3 * a
```
The value `b` will have the value of `38`.

```acf
a = "hello"
b = 3 * a
```

The value `b` will be "hellohellohello" as operators on strings have the same behaviour as in Python.

### Comments
Inline comments begin with a semicolon `;`.
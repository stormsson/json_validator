## Available Validators

### Base Rule

The base rule is a common ancestor for every validation rule, and every parameter available to the base rule is therefore available to all derived validators.

New validators should be derived from this Validator.

Parameter | Default Value | Required Parameter | Description
----------|----------|----------|----------
mandatory | False | No |Defines is the field must be present in the data provided
allow_empty | True | No | If the field is present, should an empty value be allowed ?



### Number

TODO

### Object

TODO

### Regexp

Parameter | Default Value | Required Parameter | Description
----------|----------|----------|----------
pattern | - | Yes | Regexp pattern to use for validation
flags | 0 | No | Flags to use in regexp validation

The Regexp Validator in the current implementation is basically a wrapper of `re.match` function.

Check [Python documentation] (https://docs.python.org/3.6/library/re.html#re.match) for further details of the `pattern` and `flags` parameters

### String

Parameter | Default Value | Required Parameter | Description
----------|----------|----------|----------
minlength | None | No | In order to positively validate, the string must be at least `minlength` character long
maxlength | None | No | In order to positively validate, the string must be at maximum `maxlength` character long

#### Length and allow_empty parameters priority on empty string validation

** Example **

allow_empty | minlength | maxlength | result
-------|-------|-------|-------
True | 5 | - | False
True | - | 5 | True

The default value for `allow_empty` is `True`, the following behavior occurs when a length parameter is provided:

If `allow_empty=True` and `minlength` is provided, the validator returns `False` if an empty string is provided

If `allow_empty=True` and `maxlength` is provided, the validator returns `True` if an empty string is provided



## Testing

Run test with

`python3 -m unittest discover`
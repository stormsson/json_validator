## Quickstart

Check the examples folder: it's quite straightforward.


## Schemas

In order to validate a json document, a Schema must be provided.

`s = Schema(json_validation_schema=schema_object)`
or
`s = Schema(schema_object)`

`schema_object` is a dictionary that can be hardcoded, or may be loaded from a json file

The dictionary is composed as follow
```
{
    "field_name": {validator_object}
}
```

**Example**

data_to_validate.json:
```
{
    "name": "john",
    "age": 100
}
```

schema.json:
```
{
    "name": {"validator":"string"},
    "age": {"validator":"number"}
}
```


## Available Validators

### Base Rule

The base rule is a common ancestor for every validation rule, and every parameter available to the base rule is therefore available to all derived validators.

New validators should be derived from this Validator.

Parameter | Default Value | Required Parameter | Description
----------|----------|----------|----------
mandatory | False | No |Defines is the field must be present in the data provided
allow_empty | True | No | If the field is present, should an empty value be allowed ?
parent | None | No | reference to the parent schema, if available. Used to create the validator hierarchy.



### Number

Parameter | Default Value | Required Parameter | Description
----------|----------|----------|----------
force_type | None | No | Only allowed values are `int` or `float` (passed as a string). Returns true only if the number provided is of the same type

**Example**

```
{
    "field_name": {
        "validator": "number", "force_type":"int"
    }
}
```


### Object

The object validator is basically a `Schema` instance

Parameter | Default Value | Required Parameter | Description
----------|----------|----------|----------
json_validation_schema | - | Yes | Schema to use for validation

**Example**

```
{
    "field_name": { "validator": "object", "json_validation_schema":{
           "a": { "validator": "string",  "allow_empty": false },
           ...further validators...
        }
    }
}
```


### Regexp

Parameter | Default Value | Required Parameter | Description
----------|----------|----------|----------
pattern | - | Yes | Regexp pattern to use for validation
flags | 0 | No | Flags to use in regexp validation

The Regexp Validator in the current implementation is basically a wrapper of `re.match` function.

Check [Python documentation](https://docs.python.org/3.6/library/re.html#re.match) for further details of the `pattern` and `flags` parameters

**Example**

Check if a string only contains digits:
```
{
    "field_name": {
        "validator": "regexp", "pattern":"\d+"
    },
}
```

### String

Parameter | Default Value | Required Parameter | Description
----------|----------|----------|----------
minlength | None | No | In order to positively validate, the string must be at least `minlength` character long
maxlength | None | No | In order to positively validate, the string must be at maximum `maxlength` character long

**Example**

Check if a string is at least 5 characters long:
```
{
    "field_name": {
        "validator": "string", "minlength":5
    },
}
```

#### Length and allow_empty parameters priority on empty string validation

The default value for `allow_empty` is `True`, the following behavior occurs when a length parameter is provided:

If `allow_empty=True` and `minlength` is provided, the validator returns `False` if an empty string is provided

If `allow_empty=True` and `maxlength` is provided, the validator returns `True` if an empty string is provided

allow_empty | minlength | maxlength | result
-------|-------|-------|-------
True | 5 | - | False
True | - | 5 | True

## Mixed validation

It is possible to use a combination of validators to approve a field.
This is useful when the field could be approved if just one of many conditions occurs.

When multiple validators are used, just one of them is needed to be satisfied in order to approve the validation.

### Mixed validation parameters

A further `parameters` is mandatory in the validator definition, which contains the parameters for every validator in the multiple check
The `parameters` dictionary must have as key value the validator name used in the `validator` field.

**Example**

Allow a field that is a number or a string with minimum 10 characters

```
{
    "field_name": {
        "validator": "number|string", "parameters":{
            "number": {},
            "string": {"minlength":10}
        }
    },
}
```


## Testing

Run test with

`python3 -m unittest discover`
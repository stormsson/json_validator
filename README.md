## Quickstart

Soon...

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

A validator is basically a dictionary with the `validator` key.

All validators descend from `rules/base_rule`

### Base Rule

The base rule is a common ancestor for every validation rule.
Every parameter available to the base rule is therefore available to all derived validators.

New validators should be derived from this Validator.

Parameter | Default Value | Required Parameter | Description
----------|----------|----------|----------
mandatory | False | No |Defines is the field must be present in the data provided
allow_empty | True | No | If the field is present, should an empty value be allowed ?
name | None | No | Assign a name to the validator. It will be stored in the named_rules dictionary of the top level schema.
parent | None | No | reference to the parent schema, if available. Used to create the validator hierarchy.



### Number Rule

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


### Object Rule

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


### Regexp Rule

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

### String Rule

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


## Named validators

Often there could be the necessity to reuse the same validator.
Adding a `name` parameter to the validator parameters will create a named rule.

When creating a Schema, every validator has a reference to its container Schema. This allows the creation of a hierarchy.

Named rules are stored in the top level schema.
It is possible to fetch a named rule by using `Schema._get_named_rule(name)` ,therefore when creating a validator there is the possibility of reusing a named one.

**It is necessary to define a named rule before using it**


**Correct implementation example**

```
{
    "field_1": { "validator": "regexp", "pattern":"\d{3}\-\d{8}", "name":"my_telephone_number_validator"},
    "field_2": { "validator": "my_telephone_number_validator" }
}
```
In this example, the `field_1` validator defines a regexp rule with a specific pattern.
Since it is given a name, it is usable anywhere in the Schema from its definition downward.

**Wrong implementation example**

```
{
    "field_2": { "validator": "my_telephone_number_validator" },
    "field_1": { "validator": "regexp", "pattern":"\d{3}\-\d{8}", "name":"my_telephone_number_validator"}
}
```


### Named validator and mixed validation

When using mixed validation it is possible to define named rules in the `parameters` dictionary

**Example**

```
    "mixed":{ "validator": "my_number_rule|my_regexp_rule", "parameters":{
        "my_number_rule": { "validator": "number", "name": "my_number_rule" },
        "my_regexp_rule": { "validator": "regexp", "pattern":"pattern_\d+", "name": "my_regexp_rule" },
    }}
```


## Testing

Run test with

`python3 -m unittest discover`
# typed_json_dataclass
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4344420de20b4262a4912d81cb28d175)](https://www.codacy.com/app/abatilo/typed-json-dataclass?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=abatilo/typed-json-dataclass&amp;utm_campaign=Badge_Grade)
[![Actions Status](https://wdp9fww0r9.execute-api.us-west-2.amazonaws.com/production/badge/abatilo/typed-json-dataclass?style=flat)](https://wdp9fww0r9.execute-api.us-west-2.amazonaws.com/production/badge/abatilo/typed-json-dataclass?branch=master)
[![codecov](https://codecov.io/gh/abatilo/typed-json-dataclass/branch/master/graph/badge.svg)](https://codecov.io/gh/abatilo/typed-json-dataclass)
[![PyPI status](https://img.shields.io/pypi/status/typed_json_dataclass.svg)](https://pypi.python.org/pypi/typed_json_dataclass/)
[![PyPI version](https://badge.fury.io/py/typed-json-dataclass.svg)](https://badge.fury.io/py/typed-json-dataclass)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/typed-json-dataclass.svg)](https://pypi.python.org/pypi/typed-json-dataclass/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/typed-json-dataclass.svg)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

`typed_json_dataclass` is a library that augments the Python3.7
[dataclass](https://docs.python.org/3/library/dataclasses.html) feature in two
major ways:
1. Add a way to recursively grab class dictionary definitions, thus making your
   dataclass JSON serializable
2. Add a light amount of type validation to your dataclasses, so that you can
   validate that the JSON you're being given matches the data types that you're
   expecting.

By expressing your data as dataclasses, and by having your incoming data
validated as it is received, you can easily implement the [Data Transfer Object
(DTO)](https://martinfowler.com/eaaCatalog/dataTransferObject.html) pattern in
your Python code.

This library can be thought of as a combination of
[attrs](https://github.com/python-attrs/attrs),
[cattrs](https://github.com/Tinche/cattrs), and
[marshamllow](https://github.com/marshmallow-code/marshmallow)

## Getting Started

Install the library from PyPI:
```
pip install typed_json_dataclass
```

Use the dataclass decorator just like normal, but add the `TypedJsonMixin` from
this library, to your class definition. This will add 4 new methods to all of your dataclasses:
1. from_dict()
```python
@classmethod
def from_dict(cls, raw_dict, *, mapping_mode=MappingMode.NoMap):
    """Given a python dict, create an instance of the implementing class.

    :raw_dict: A dictionary that represents the DTO to create
    :mapping_mode: Format for properties
    :returns: Returns an instance of the DTO, instantiated via the dict
    """
```
2. from_json()
```python
@classmethod
def from_json(cls, raw_json, *, mapping_mode=MappingMode.NoMap):
    """Given a raw json string, create an instance of the implementing class.

    :raw_json: A json string that represents the DTO to create
    :mapping_mode: Format for properties
    :returns: Returns an instance of the DTO, instantiated via the json
    """
```
3. to_dict()
```python
def to_dict(self, *, keep_none=False, mapping_mode=MappingMode.NoMap, warn_on_initvar=True):
    """Express the DTO as a dictionary.

    :keep_none: Filter keys that are None
    :mapping_mode: Format for properties
    :warn_on_initvar: Emit a warning if the instance contains non-default
                      init-only variables.
    :returns: Returns the instantiated DTO as a dictionary
    """
```
4. to_json()
```python
def to_json(self, *, keep_none=False, mapping_mode=MappingMode.NoMap, warn_on_initvar=True):
    """Express the DTO as a json string.

    :keep_none: Filter keys that are None
    :mapping_mode: Format for properties
    :warn_on_initvar: Emit a warning if the instance contains non-default
                      init-only variables.
    :returns: Returns the instantiated DTO as a json string
    """
```

## Examples

### Converting your dataclass to a JSON serializable format
```python
from typing import List
from dataclasses import dataclass
from typed_json_dataclass import TypedJsonMixin

@dataclass
class Person(TypedJsonMixin):
    name: str
    age: int

@dataclass
class Family(TypedJsonMixin):
    people: List[Person]

bob = Person(name='Bob', age=24)
alice = Person(name='Alice', age=32)
family = Family(people=[bob, alice])

print(family.to_json())
# => {"people": [{"name": "Bob", "age": 24}, {"name": "Alice", "age": 32}]}
```


If your data doesn't match the type definitions, you'll get a helpful error:
```python
from dataclasses import dataclass
from typed_json_dataclass import TypedJsonMixin

@dataclass
class Person(TypedJsonMixin):
    name: str
    age: int

request_data = '{"name":"Bob","age":"24"}'

bob = Person.from_json(request_data)
# => TypeError: Person.age is expected to be <class 'int'>, but value 24 with type <class 'str'> was found instead
```

And you can parse data from a Python `dict` as well. Just use the `.from_dict()` function instead:
```python
from dataclasses import dataclass
from typed_json_dataclass import TypedJsonMixin

@dataclass
class Person(TypedJsonMixin):
    name: str
    age: int

request_data_as_dict = {
    'name': 'Alice',
    'age': '32'
}

alice = Person.from_dict(request_data_as_dict)
# => TypeError: Person.age is expected to be <class 'int'>, but value 32 with type <class 'str'> was found instead
```

### Setting a mapping_mode for auto mapping
```python
from dataclasses import dataclass
from typed_json_dataclass import TypedJsonMixin, MappingMode

@dataclass
class Person(TypedJsonMixin):
    person_name: str
    person_age: int

request_data_as_dict = {
    'personName': 'Alice',
    'personAge': 32
}

alice = Person.from_dict(request_data_as_dict, mapping_mode=MappingMode.SnakeCase)
# => Person(person_name='Alice', person_age=32)
```

This mapping mode is useful for when you get requests that have the JSON in a
camel case format, but you want your objects to be snake case and stay PEP8
compliant.

## Limitations and Caveats

### Dataclasses with init-only variables

Support for dataclasses with [init-only variables](https://docs.python.org/3/library/dataclasses.html#init-only-variables)
is limited. Although `to_dict` and `to_json` will convert the dataclass, the
resulting dict or JSON string will not contain the init-only variables, since
their values are not available after initialization. This also means that such
dataclasses cannot later be instantiated from a dict or JSON string, since the
init-only variables are a required parameter in the dataclass' `__init__`
method. `TypedJsonMixin` detects the usage of dataclasses with init-only
variables, emits a warning when it is converted to a dict or JSON string, and
refuses to instantiate a dataclass with init-only variables.

A first workaround consists of providing a default value to the init-only
variables:

```python
@dataclass
class Person(TypedJsonMixin):
    person_name: InitVar[str] = ''
    person_first_name: str = ''
    person_last_name: str = ''

    def __post_init__(self, person_name):
        if person_name:
            # Instantiated directly
            self.person_first_name, self.person_last_name = person_name.split()
        # Call TypedJsonMixin __post_init__ method
        super().__post_init__()
```
**Note**: Instantiations without arguments, such as `Person()`, are now
possible, although the created instance would then be invalid.

The second workaround is to remove init-only variables from the dataclass, and
perform the `__post_init__` instantiation using a class method instead:

```python
@dataclass
class Person(TypedJsonMixin):
    person_first_name: str
    person_last_name: str

    @classmethod
    def create(cls, person_name):
        first_name, last_name = person_name.split()
        cls(first_name, last_name)
```

Finally, if the dataclass is not meant to ever be instantiated from a dict or
JSON string, and only the `to_dict` or `to_json` methods are called, the
warnings can be suppressed by passing `warn_on_initvar=False` as a keyword
argument in the method call.

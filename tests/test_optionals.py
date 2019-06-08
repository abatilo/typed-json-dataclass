from dataclasses import dataclass
from typing import Optional, Union

import pytest
from typed_json_dataclass import TypedJsonMixin


@dataclass
class PersonWithOptionalAge(TypedJsonMixin):
    name: str
    age: Optional[int] = None


def test_optionals_are_handled():
    assert PersonWithOptionalAge('John', 42).to_dict() == {
        'name': 'John',
        'age': 42
    }


def test_optionals_are_handled_with_empty_value():
    assert PersonWithOptionalAge('John').to_dict() == {
        'name': 'John',
    }


def test_optionals_are_handled_with_empty_value_and_keeps_none():
    assert PersonWithOptionalAge('John').to_dict(keep_none=True) == {
        'name': 'John',
        'age': None
    }


def test_optionals_that_dont_match_raise():
    with pytest.raises(TypeError) as e_info:
        print(PersonWithOptionalAge('John', '42').to_dict())
    assert ('PersonWithOptionalAge.age was defined to be any of: (<class '
            "'int'>, <class 'NoneType'>) but was found to be <class "
            "'str'> instead") == str(e_info.value)


@dataclass
class FirstNameLastName(TypedJsonMixin):
    first: str
    last: str


@dataclass
class PersonWithUnionType(TypedJsonMixin):
    name: Union[str, FirstNameLastName]


def test_unions_are_all_respected():
    assert PersonWithUnionType('John').to_dict() == {
        'name': 'John',
    }

    assert PersonWithUnionType(FirstNameLastName('John', 'Doe')).to_dict() == {
        'name': {
            'first': 'John',
            'last': 'Doe'
        },
    }

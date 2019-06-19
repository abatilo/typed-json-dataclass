"""Tests for https://github.com/abatilo/typed-json-dataclass/issues/8"""

from dataclasses import dataclass, InitVar

import pytest

from typed_json_dataclass import TypedJsonMixin

@dataclass
class DataclassWithInitVar(TypedJsonMixin):
    init: InitVar[str]
    a: int = 0
    b: str = ''

    def __post_init__(self, init: str) -> None:
        self.a = len(init)
        self.b = init[0]
        super().__post_init__()


def test_that_instantiation_of_dataclass_with_init_var_typechecks() -> None:
    result = DataclassWithInitVar('foo')

    assert result.a == 3
    assert result.b == 'f'


def test_that_dataclass_with_init_var_to_dict_leads_to_warning() -> None:
    dcls = DataclassWithInitVar('foo')

    with pytest.warns(UserWarning, match='init-only variables'):
        result = dcls.to_dict()

    assert result == {'a': 3, 'b': 'f'}


def test_that_dataclass_with_init_var_from_dict_leads_to_typeerror() -> None:
    raw_dict = {'a': 3, 'b': 'f'}

    with pytest.raises(TypeError, match='init-only variables'):
        DataclassWithInitVar.from_dict(raw_dict)

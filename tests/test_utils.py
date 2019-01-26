import pytest
from typed_json_dataclass.utils import (
    to_snake as to_s,
    to_camel as to_c,
)


@pytest.mark.parametrize('target, expected', [
    ('hereIsSomethingInCamelCase', 'here_is_something_in_camel_case'),
    ('hereIsSomeThingInCamelCase', 'here_is_some_thing_in_camel_case'),
    ('_here_is_something_in_snake_case', '_here_is_something_in_snake_case'),
    ('HereIsSomethingInTitleCase', 'here_is_something_in_title_case')
])
def test_to_snake_case(target, expected):
    actual = to_s(target)
    assert expected == actual


@pytest.mark.parametrize('target, expected', [
    ('here_is_something_in_camel_case', 'hereIsSomethingInCamelCase'),
    ('_here_is_something_in_camel_case', 'hereIsSomethingInCamelCase'),
    ('___here_is_something_in_camel_case', 'hereIsSomethingInCamelCase'),
    ('___here___is_something_in_camel__case', 'hereIsSomethingInCamelCase'),
    ('HereIsSomethingInTitleCase', 'hereIsSomethingInTitleCase')
])
def test_to_camel_case(target, expected):
    actual = to_c(target)
    assert expected == actual

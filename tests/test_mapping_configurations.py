from dataclasses import dataclass

import pytest
from typed_json_dataclass import TypedJsonMixin, MappingMode


@dataclass
class SnakeCaseObjects(TypedJsonMixin):
    object_id: str


@dataclass
class CamelCaseObjects(TypedJsonMixin):
    objectId: str


@dataclass
class ChildObject(TypedJsonMixin):
    objectId: str


@dataclass
class ParentObject(TypedJsonMixin):
    objectId: str
    child: ChildObject


def test_mapping_from_dict_to_snake_case():
    camel_case_object = {
        'objectId': 'asdf'
    }

    expected_object = SnakeCaseObjects('asdf')
    assert SnakeCaseObjects.from_dict(
            camel_case_object,
            mapping_mode=MappingMode.SnakeCase) == expected_object


def test_mapping_from_dict_to_camel_case():

    snake_case_json = {
        'object_id': 'asdf'
    }

    expected_object = CamelCaseObjects('asdf')
    assert CamelCaseObjects.from_dict(
            snake_case_json,
            mapping_mode=MappingMode.CamelCase) == expected_object


def test_mapping_from_json_to_snake_case():
    camel_case_json = """
    {
        "objectId": "asdf"
    }
    """

    expected_object = SnakeCaseObjects('asdf')
    assert SnakeCaseObjects.from_json(
            camel_case_json,
            mapping_mode=MappingMode.SnakeCase) == expected_object


def test_mapping_from_json_to_camel_case():
    snake_case_json = """
    {
        "object_id": "asdf"
    }
    """

    expected_object = CamelCaseObjects('asdf')
    assert CamelCaseObjects.from_json(
            snake_case_json,
            mapping_mode=MappingMode.CamelCase) == expected_object


def test_mapping_to_camel_case_dict_from_snake_case():
    expected = {
        'object_id': 'asdf'
    }

    target = CamelCaseObjects('asdf')
    actual = target.to_dict(mapping_mode=MappingMode.SnakeCase)
    assert expected == actual


def test_mapping_to_snake_case_dict_from_camel_case():

    expected = {
        'objectId': 'asdf'
    }

    target = SnakeCaseObjects('asdf')
    actual = target.to_dict(mapping_mode=MappingMode.CamelCase)
    assert expected == actual


def test_from_json_with_invalid_mapping_mode():
    with pytest.raises(ValueError) as e_info:
        SnakeCaseObjects.from_json('{"object_id": ""}', mapping_mode='Invalid')
    assert str(e_info.value) == 'Invalid mapping mode'


def test_to_json_with_invalid_mapping_mode():
    with pytest.raises(ValueError) as e_info:
        SnakeCaseObjects('asdf').to_json(mapping_mode='Invalid')
    assert str(e_info.value) == 'Invalid mapping mode'


def test_from_dict_with_invalid_mapping_mode():
    with pytest.raises(ValueError) as e_info:
        SnakeCaseObjects.from_dict({'object_id': ''}, mapping_mode='Invalid')
    assert str(e_info.value) == 'Invalid mapping mode'


def test_to_dict_with_invalid_mapping_mode():
    with pytest.raises(ValueError) as e_info:
        SnakeCaseObjects('asdf').to_dict(mapping_mode='Invalid')
    assert str(e_info.value) == 'Invalid mapping mode'


def test_recursive_from_dict_mapping():
    target = {
        'object_id': 'asdf',
        'child': {
            'object_id': 'fdsa'
        }
    }
    expected = ParentObject('asdf', ChildObject('fdsa'))
    actual = ParentObject.from_dict(target, mapping_mode=MappingMode.CamelCase)
    assert expected == actual


def test_recursive_to_dict_mapping():
    expected = {
        'object_id': 'asdf',
        'child': {
            'object_id': 'fdsa'
        }
    }
    target = ParentObject('asdf', ChildObject('fdsa'))
    actual = target.to_dict(mapping_mode=MappingMode.SnakeCase)
    assert expected == actual


def test_recursive_from_json_mapping():
    target = """
    {
        "object_id": "asdf",
        "child": {
            "object_id": "fdsa"
        }
    }
    """
    expected = ParentObject('asdf', ChildObject('fdsa'))
    actual = ParentObject.from_json(target, mapping_mode=MappingMode.CamelCase)
    assert expected == actual


def test_recursive_to_json_mapping():
    expected = """{"object_id": "asdf", "child": {"object_id": "fdsa"}}"""
    target = ParentObject('asdf', ChildObject('fdsa'))
    actual = target.to_json(mapping_mode=MappingMode.SnakeCase)
    assert expected == actual

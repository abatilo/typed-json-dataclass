#!/usr/bin/env python3.7
from dataclasses import dataclass
from typing import List

import pytest
from typed_json_dataclass import TypedJsonMixin


@dataclass
class Label(TypedJsonMixin):
    name: str


@dataclass
class Paragraph(TypedJsonMixin):
    text: str
    labels: List[Label] = None


@dataclass
class Document(TypedJsonMixin):
    name: str
    paragraphs: List[Paragraph] = None
    tags: List[str] = None


@dataclass
class Author(TypedJsonMixin):
    name: str


@dataclass
class Book(TypedJsonMixin):
    title: str
    author: Author


# dict based tests


def test_that_valid_dict_becomes_valid_object():
    raw_dict = {'name': 'msa.doc'}
    expected = Document('msa.doc')
    actual = Document.from_dict(raw_dict)
    assert expected == actual


def test_that_invalid_dict_throws_exception():
    raw_dict = {'nam': 'msa.doc'}
    with pytest.raises(TypeError) as e_info:
        Document.from_dict(raw_dict)
    assert ('__init__() got an unexpected keyword argument \'nam\'' ==
            str(e_info.value))


def test_that_dict_with_wrong_type_throws_exception():
    raw_dict = {'name': True}
    with pytest.raises(TypeError) as e_info:
        Document.from_dict(raw_dict)
    assert ('Document.name is expected to be <class \'str\'>, but value '
            'True with type <class \'bool\'> '
            'was found instead') == str(e_info.value)


def test_that_lists_with_complex_objects_are_handled_correctly():
    raw_dict = {'name': 'msa.doc', 'paragraphs': [{'text': 'first paragraph',
                'labels': [{'name': 'msa'}]},
                {'text': 'second paragraph'}], 'tags': ['law', 'important']}
    expected = Document('msa.doc', [
        Paragraph('first paragraph', [Label('msa')]),
        Paragraph('second paragraph')
        ],
                        ['law', 'important'])
    actual = Document.from_dict(raw_dict)
    assert expected == actual


def test_that_nested_objects_in_lists_with_invalid_keys_throws_exception():
    raw_dict = {'name': 'msa.doc', 'paragraphs': [{'tex': 'first paragraph'}]}
    with pytest.raises(TypeError) as e_info:
        Document.from_dict(raw_dict)
    assert (('__init__() got an unexpected keyword argument \'tex\'') ==
            str(e_info.value))


def test_that_objects_with_wrong_type_in_nested_list_throws_exception():
    raw_dict = {'name': 'msa.doc', 'paragraphs': [{'text': 0}]}
    with pytest.raises(TypeError) as e_info:
        Document.from_dict(raw_dict)
    assert ('Paragraph.text is expected to be <class \'str\'>, but value 0 '
            'with type <class \'int\'> '
            'was found instead') == str(e_info.value)


def test_that_nested_object_that_is_not_in_list_is_handled_correctly():
    raw_dict = {'title': 'book', 'author': {'name': 'George'}}
    expected = Book('book', Author('George'))
    actual = Book.from_dict(raw_dict)
    assert expected == actual


def test_that_nested_object_that_is_not_in_list_with_wrong_type_throws():
    raw_dict = {'title': 'book', 'author': {'name': 0}}
    with pytest.raises(TypeError) as e_info:
        Book.from_dict(raw_dict)
    assert (('Book.author is expected to be <class \''
             'test_typed_json_dataclass.Author\'>, '
             'but value {\'name\': 0} is a dict with unexpected keys') ==
            str(e_info.value))


def test_document_to_dict_without_nulls():
    expected = {'name': 'msa.doc'}
    actual = Document('msa.doc').to_dict()
    assert expected == actual


def test_document_to_dict_with_null():
    expected = {'name': 'msa.doc', 'paragraphs': None, 'tags': None}
    actual = Document('msa.doc').to_dict(keep_none=True)
    assert expected == actual


def test_that_dict_with_untyped_list_throws_exception():
    with pytest.raises(TypeError) as e_info:
        MissingListType([])
    assert ('MissingListType.some_list was defined as a <class \'list\'>, '
            'but is missing information about the type of the elements '
            'inside it') == str(e_info.value)

# Json string based tests


def test_that_valid_json_becomes_valid_object():
    raw_json = '{"name": "msa.doc"}'
    expected = Document('msa.doc')
    actual = Document.from_json(raw_json)
    assert expected == actual


def test_that_invalid_json_throws_exception():
    raw_json = '{"nam": "msa.doc"}'
    with pytest.raises(TypeError) as e_info:
        Document.from_json(raw_json)
    assert ('__init__() got an unexpected keyword argument \'nam\'' ==
            str(e_info.value))


def test_that_json_with_wrong_type_throws_exception():
    raw_json = '{"name": true}'
    with pytest.raises(TypeError) as e_info:
        Document.from_json(raw_json)
    assert ('Document.name is expected to be <class \'str\'>, but value True '
            'with type <class \'bool\'> '
            'was found instead') == str(e_info.value)


def test_that_lists_with_complex_json_are_handled_correctly():
    raw_json = ('{"name": "msa.doc", "paragraphs": [{"text": "first '
                'paragraph", "labels": [{"name": "msa"}]},'
                '{"text": "second paragraph"}], "tags": ["law", "important"]}')
    expected = Document('msa.doc', [
        Paragraph('first paragraph', [Label('msa')]),
        Paragraph('second paragraph')
        ],
        ['law', 'important'])
    actual = Document.from_json(raw_json)
    assert expected == actual


def test_that_nested_json_in_lists_with_invalid_keys_throws_exception():
    raw_json = ('{"name": "msa.doc", "paragraphs": '
                '[{"tex": "first paragraph"}]}')
    with pytest.raises(TypeError) as e_info:
        Document.from_json(raw_json)
    assert (('__init__() got an unexpected keyword argument \'tex\'') ==
            str(e_info.value))


def test_that_json_with_wrong_type_in_nested_list_throws_exception():
    raw_json = '{"name": "msa.doc", "paragraphs": [{"text": 0}]}'
    with pytest.raises(TypeError) as e_info:
        Document.from_json(raw_json)
    assert ('Paragraph.text is expected to be <class \'str\'>, but value 0 '
            'with type <class \'int\'> '
            'was found instead') == str(e_info.value)


def test_that_nested_json_that_is_not_in_list_is_handled_correctly():
    raw_json = '{"title": "book", "author": {"name": "George"}}'
    expected = Book('book', Author('George'))
    actual = Book.from_json(raw_json)
    assert expected == actual


def test_that_nested_json_that_is_not_in_list_with_wrong_type_throws():
    raw_json = '{"title": "book", "author": {"name": 0}}'
    with pytest.raises(TypeError) as e_info:
        Book.from_json(raw_json)
    assert (('Book.author is expected to be <class \'test_typed_json_dataclass'
             '.Author\'>, '
             'but value {\'name\': 0} is a dict with unexpected keys') ==
            str(e_info.value))


def test_document_to_json_without_nulls():
    expected = '{"name": "msa.doc"}'
    actual = Document('msa.doc').to_json()
    assert expected == actual


def test_document_to_json_with_null():
    expected = '{"name": "msa.doc", "paragraphs": null, "tags": null}'
    actual = Document('msa.doc').to_json(keep_none=True)
    assert expected == actual


# Edge case tests


@dataclass
class NestedListWithUniformTypes(TypedJsonMixin):
    name: List[List[str]]


def test_that_lists_with_uniform_elements_succeeds():
    name = {'name': [['foo', 'bar'], ['baz', 'bing']]}
    expected = NestedListWithUniformTypes([['foo', 'bar'], ['baz', 'bing']])
    actual = NestedListWithUniformTypes.from_dict(name)
    assert expected == actual


def test_that_lists_with_non_uniform_elements_throws_exception():
    name = {'name': [['str', 0]]}
    with pytest.raises(TypeError) as e_info:
        NestedListWithUniformTypes.from_dict(name)
    assert ('NestedListWithUniformTypes.name is [[\'str\', 0]] which does not '
            'match typing.List[typing.List[str]]. '
            'Unfortunately, we are unable to infer the explicit type of '
            'NestedListWithUniformTypes.name') \
        == str(e_info.value)


@dataclass
class MissingListType(TypedJsonMixin):
    some_list: List = None


def test_that_json_with_untyped_list_throws_exception():
    with pytest.raises(TypeError) as e_info:
        MissingListType.from_json('{"some_list": []}')
    assert ('MissingListType.some_list was defined as a <class \'list\'>, '
            'but is missing information about the type of the elements inside '
            'it') == str(e_info.value)


@dataclass
class UsesNativeList(TypedJsonMixin):
    some_list: list = None


def test_that_dict_with_wrong_list_throws_exception():
    with pytest.raises(TypeError) as e_info:
        UsesNativeList([])
    assert ('UsesNativeList.some_list was defined as a <class \'list\'>, '
            'but you must use typing.List[type] instead') == str(e_info.value)


def test_that_json_with_wrong_list_throws_exception():
    with pytest.raises(TypeError) as e_info:
        UsesNativeList.from_json('{"some_list": []}')
    assert ('UsesNativeList.some_list was defined as a <class \'list\'>, '
            'but you must use typing.List[type] instead') == str(e_info.value)


@dataclass
class UsesNestedNativeList(TypedJsonMixin):
    some_list: List[List[list]]


def test_nested_wrong():
    with pytest.raises(TypeError) as e_info:
        UsesNestedNativeList([])
    assert ('UsesNestedNativeList.some_list was detected to use a native '
            'Python collection in its type definition. '
            'We should only use typing.List[] for these') == str(e_info.value)


@dataclass
class ListOfTuples(TypedJsonMixin):
    name: List[tuple]


def test_for_tuples():
    with pytest.raises(TypeError) as e_info:
        ListOfTuples.from_dict({'name': []})
    assert ('ListOfTuples.name was detected to use a native Python collection '
            'in its type definition. '
            'We should only use typing.List[] for these') == str(e_info.value)


def test_that_if_a_list_of_natives_is_expected_but_dict_is_found_then_throw():
    with pytest.raises(TypeError) as e_info:
        ListOfTuples.from_dict({'name': {}})
    assert ('ListOfTuples.name was detected to use a native Python dict in '
            'its type definition. '
            'We should only use custom objects for these') == str(e_info.value)


@dataclass
class ListOfSet(TypedJsonMixin):
    name: List[set]


def test_for_set():
    with pytest.raises(TypeError) as e_info:
        ListOfSet.from_dict({'name': []})
    assert ('ListOfSet.name was detected to use a native Python collection in '
            'its type definition. '
            'We should only use typing.List[] for these') == str(e_info.value)


@dataclass
class ListOfDict(TypedJsonMixin):
    name: List[dict]


def test_for_dict():
    with pytest.raises(TypeError) as e_info:
        ListOfDict.from_dict({'name': []})
    assert ('ListOfDict.name was detected to use a native Python collection '
            'in its type definition. '
            'We should only use typing.List[] for these') == str(e_info.value)


@dataclass
class ListOfInt(TypedJsonMixin):
    name: List[int]


def test_that_an_empty_dict_does_not_get_cast_to_a_different_type():
    # We test dictionaries for being valid subjects, by attempting to
    # instantiate the expected type with the keys of the dictionary.
    # Unfortunately, calling `int(**{})` evaluates to 0, and similar for other
    # native types like str. Fortunately, an empty dictionary would never
    # instantiate to any subobject, unless the suboject had all default values.
    # If the subobject is trying to be used with all defaults, we're probably
    # using it incorrectly.
    # Thus, just prevent empty dictionaries
    with pytest.raises(TypeError) as e_info:
        ListOfInt([1, 2, {}])
    assert ('ListOfInt.name was found to have an empty dictionary. An empty '
            'dictionary will not '
            'properly instantiate a nested object') == str(e_info.value)


# More complex object tests

@dataclass
class Object3(TypedJsonMixin):
    name: str


@dataclass
class Object2(TypedJsonMixin):
    name: str
    subobjects: List[Object3]


@dataclass
class Object1(TypedJsonMixin):
    name: str
    subobjects: List[Object2]


def test_complex_nested_lists():
    objectThrees: List[Object3] = [Object3('o3_1'), Object3('o3_2')]
    objectTwos: List[Object2] = [Object2('o2_1', objectThrees)]
    objectOne: Object1 = Object1('o1_1', objectTwos)
    object_dict = Object1.from_dict({'name': 'o1_1', 'subobjects':
                                    [
                                        {'name': 'o2_1', 'subobjects': [
                                            {'name': 'o3_1'},
                                            {'name': 'o3_2'}
                                        ]}
                                    ]})
    assert object_dict.to_json() == objectOne.to_json()


# Simulate a LinkedList style scenario
@dataclass
class Node(TypedJsonMixin):
    next_node: 'Node' = None


def test_that_incorrect_recursive_definitions_throws():
    with pytest.raises(TypeError) as e_info:
        Node(next_node='something else')
    assert ('Node.next_node was defined as a <class \'Node\'>, but we '
            'found a <class \'str\'> instead') == str(e_info.value)


def test_that_correct_recursive_definitions_is_handled():
    root = Node(next_node=Node())
    assert root.to_dict() == {'next_node': {'next_node': None}}


# Simulate a Graph
@dataclass
class GraphNode(TypedJsonMixin):
    children: List['GraphNode']


def test_that_recursive_collection_is_handled():
    expected = {
        'children': [
            {
                'children': []
            },
            {
                'children': []
            }
        ]
    }
    assert (GraphNode(children=[GraphNode([]), GraphNode([])]).to_dict() ==
            expected)


def test_that_recursive_collection_with_non_matching_types_throws():
    with pytest.raises(TypeError) as e_info:
        GraphNode(children=[GraphNode([]), 'not a GraphNode'])
    assert ('GraphNode.children is [GraphNode(children=[]), \'not a '
            'GraphNode\'] which does not match typing.List[ForwardRef'
            '(\'GraphNode\')]. Unfortunately, we are unable to infer the '
            'explicit type of GraphNode.children') == str(e_info.value)


def test_deeply_nested_forward_references_are_handled():
    expected = {
        'children': [
            {
                'children': [
                    {
                        'children': []
                    }
                ]
            }
        ]
    }
    assert (GraphNode(
                children=[GraphNode(children=[GraphNode(children=[])])]
            ).to_dict()
            == expected)


def test_deeply_nested_forward_references__with_non_matching_types_throws():
    with pytest.raises(TypeError) as e_info:
        GraphNode(children=[GraphNode(children=[GraphNode(children=['bad'])])])
    assert ('GraphNode.children is [\'bad\'] which does not match '
            'typing.List[ForwardRef(\'GraphNode\')]. Unfortunately, we are '
            'unable to infer the explicit type of GraphNode.'
            'children') == str(e_info.value)

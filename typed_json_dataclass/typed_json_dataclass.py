#!/usr/bin/env python3.7
import json
import typing
from dataclasses import asdict
from enum import Enum

from typed_json_dataclass.utils import to_camel, to_snake, recursive_rename


class MappingMode(Enum):
    SnakeCase = 1
    CamelCase = 2
    NoMap = 3


class TypedJsonMixin:
    """
    A very small Mixin that we can use in conjunction with Python 3.7
    @dataclass in order to get typed DTO validation.
    """

    def __post_init__(self):
        """Validation logic that runs after an object has been instantiated.

        Based heavily on:
        https://stackoverflow.com/questions/50563546/validating-detailed-types-in-python-dataclasses
        """
        for field_name, field_def in self.__dataclass_fields__.items():
            field_value = getattr(self, field_name)
            actual_type = type(field_value)

            if hasattr(field_def.type, '__origin__'):
                # If a type hint uses typing.List, we need to check the origin
                # in order to see that it's a list
                expected_type = field_def.type.__origin__
            else:
                expected_type = field_def.type

            # Lists are a special case, because we have to get the list element
            # type in a different way
            if field_value is not None:
                class_name = self.__class__.__name__

                # A ForwardRef will appear to just be a str
                # Check that the expected type is a str instead of an actual
                # type definition, and check that the name of the current class
                # matches the string in the ForwardRef.
                if (class_name == expected_type and
                        isinstance(expected_type, str)):
                    # Double check that the type itself and the current class
                    # are the same
                    if actual_type != self.__class__:
                        raise TypeError((f'{class_name}.{field_name} was '
                                        'defined as a <class '
                                         f'\'{expected_type}\'>, '
                                         f'but we found a {actual_type} '
                                         'instead'))
                else:
                    if (isinstance(field_value, expected_type) and
                       isinstance(field_value, list)):
                        if not hasattr(field_def.type, '__args__'):
                            raise TypeError((f'{class_name}.{field_name} was '
                                            f'defined as a {actual_type}, '
                                             'but you must use '
                                             'typing.List[type] '
                                             'instead'))

                        expected_element_type = field_def.type.__args__[0]
                        if isinstance(expected_element_type, typing.TypeVar):
                            raise TypeError((f'{class_name}.{field_name} was '
                                            f'defined as a {actual_type}, '
                                             'but is missing information '
                                             'about the'
                                             ' type of the elements inside '
                                             'it'))

                        if not self._ensure_no_native_collections(
                                expected_element_type
                                ):
                            raise TypeError(((f'{class_name}.{field_name} was '
                                              'detected to use a native '
                                              'Python '
                                              'collection in its type '
                                              'definition. '
                                              'We should only use '
                                              'typing.List[] '
                                              'for these')))

                        for i, element in enumerate(field_value):
                            if isinstance(element, dict):
                                if not element:
                                    raise TypeError(((f'{class_name}.'
                                                      f'{field_name} '
                                                      'was found to have an '
                                                      'empty dictionary. An '
                                                      'empty '
                                                      'dictionary will not '
                                                      'properly instantiate a '
                                                      'nested object')))

                                # Set reference of the specific list index.
                                # Kind of a hack, to get around the fact that
                                # __setattr__ can only seem to take field
                                # names, but not indices
                                getattr(
                                    self, field_name
                                )[i] = expected_element_type(**element)

                        if not self._validate_list_types(
                                field_value, field_def.type
                                ):
                            raise TypeError((f'{class_name}.{field_name} is '
                                             f'{field_value} which does not '
                                             'match '
                                             f'{field_def.type}. '
                                             'Unfortunately, '
                                             'we are unable to infer the '
                                             'explicit '
                                             f'type of {class_name}.'
                                             f'{field_name}'))

                    elif not isinstance(field_value, expected_type):
                        if isinstance(field_value, dict):
                            if not self._ensure_no_native_collections(
                                    expected_type
                                  ):
                                raise TypeError((f'{class_name}.{field_name} '
                                                 'was '
                                                 'detected to use a native '
                                                 'Python '
                                                 'dict in its type '
                                                 'definition. '
                                                 'We should only use custom '
                                                 'objects for these'))
                            try:
                                setattr(
                                    self,
                                    field_name,
                                    expected_type(**field_value)
                                )
                            except TypeError:
                                raise TypeError(f'{class_name}.{field_name} '
                                                'is '
                                                'expected to be '
                                                f'{expected_type}, but value '
                                                f'{field_value} is a dict '
                                                'with unexpected keys')
                        else:
                            raise TypeError(f'{class_name}.{field_name} is '
                                            'expected to be '
                                            f'{expected_type}, but value '
                                            f'{field_value} with '
                                            f'type {actual_type} was found '
                                            'instead')

    def _ensure_no_native_collections(self, expected_type):
        """
        Recursively drills down a type hint like List[List[list]] to make
        sure we never use a native collections.
        """
        if hasattr(expected_type, '__origin__'):
            return self._ensure_no_native_collections(
                expected_type.__args__[0]
            )
        else:
            return expected_type not in {dict, list, set, tuple}

    def _validate_list_types(self, actual_value, expected_type):
        """
        Recursively checks nested lists like List[List[str]] and checks that
        all elements in the list are uniform
        """
        # typing.List[type] will have __args__
        if isinstance(actual_value, list) and \
           hasattr(expected_type, '__args__'):
            nested_type = expected_type.__args__[0]
            if isinstance(nested_type, typing.ForwardRef):
                # Strip out ForwardRef(' and ') as a hack for getting the
                # expected class
                type_for_forward_ref = str(nested_type)[12:-2]
                return all(
                    type_for_forward_ref == v.__class__.__name__
                    for v in actual_value
                )

            return all(
                self._validate_list_types(v, nested_type) for v in actual_value
            )
        else:
            return isinstance(actual_value, expected_type)

    @classmethod
    def from_dict(cls, raw_dict, *, mapping_mode=MappingMode.NoMap):
        """Given a python dict, create an instance of the implementing class.

        :raw_dict: A dictionary that represents the DTO to create
        :mapping_mode: Format for properties
        :returns: Returns an instance of the DTO, instantiated via the dict
        """

        if not isinstance(mapping_mode, MappingMode):
            raise ValueError('Invalid mapping mode')

        if mapping_mode == MappingMode.NoMap:
            return cls(**raw_dict)

        format_method = to_snake if mapping_mode == MappingMode.SnakeCase \
            else to_camel
        mapped_dict = recursive_rename(raw_dict, format_method)
        return cls(**mapped_dict)

    @classmethod
    def from_json(cls, raw_json, *, mapping_mode=MappingMode.NoMap):
        """Given a raw json string, create an instance of the implementing class.

        :raw_json: A json string that represents the DTO to create
        :mapping_mode: Format for properties
        :returns: Returns an instance of the DTO, instantiated via the json
        """

        return cls.from_dict(json.loads(raw_json), mapping_mode=mapping_mode)

    def to_dict(self, *, keep_none=False, mapping_mode=MappingMode.NoMap):
        """Express the DTO as a dictionary.

        :keep_none: Filter keys that are None
        :mapping_mode: Format for properties
        :returns: Returns the instantiated DTO as a dictionary
        """
        if not isinstance(mapping_mode, MappingMode):
            raise ValueError('Invalid mapping mode')

        self_dict = None
        mapped_dict = {}

        if keep_none:
            self_dict = asdict(self)
        else:
            self_dict = {k: v for k, v in asdict(self).items()
                         if v is not None}

        if mapping_mode == MappingMode.NoMap:
            return self_dict

        format_method = to_snake if mapping_mode == MappingMode.SnakeCase \
            else to_camel
        mapped_dict = recursive_rename(self_dict, format_method)
        return mapped_dict

    def to_json(self, *, keep_none=False, mapping_mode=MappingMode.NoMap):
        """Express the DTO as a json string.

        :keep_none: Filter keys that are None
        :mapping_mode: Format for properties
        :returns: Returns the instantiated DTO as a json string
        """
        return json.dumps(self.to_dict(
            keep_none=keep_none,
            mapping_mode=mapping_mode))

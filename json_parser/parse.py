import re
from collections import deque

from util import *


def parse(lex_list):
    object_node, lex_list = build_object_node(lex_list)
    assert not lex_list
    return object_node


class ObjectNode:
    @classmethod
    def from_lex_list(cls, lex_list):
        assert len(lex_list) >= 2 and is_type(lex_list[0], LEFT_BRACKET) and is_type(lex_list[-1], RIGHT_BRACKET)

        lex_list.pop()
        lex_list.popleft()
        return cls(list(MemberNode.members_from_lex_list(lex_list)))

    def __init__(self, member_nodes):
        self.member_nodes = member_nodes

    def to_python(self):
        return dict(kv_pair_node.to_python() for kv_pair_node in self.member_nodes)


class MemberNode:
    @classmethod
    def members_from_lex_list(cls, lex_list):
        while lex_list:
            assert len(lex_list) >= 3 and is_type(lex_list[0], STRING) and is_type(lex_list[1], COLON)

            key_node = StringNode.from_lex_item(lex_list.popleft())
            lex_list.popleft()  # throw away colon
            value_node, lex_list = build_node(lex_list)

            assert value_node

            yield cls(key_node, value_node)

            if lex_list:  # has comma next
                assert is_type(lex_list[0], COMMA)
                lex_list.popleft()

    def __init__(self, key_node, value_node):
        self.key_node = key_node
        self.value_node = value_node

    def to_python(self):
        return (self.key_node.to_python(), self.value_node.to_python())


class ArrayNode:
    @classmethod
    def from_lex_list(cls, lex_list):
        assert len(lex_list) >= 2 and is_type(lex_list[0], LEFT_BRACE) and is_type(lex_list[-1], RIGHT_BRACE)

        lex_list.pop()
        lex_list.popleft()

        def _array_items(lex_list):
            while lex_list:
                element_node, lex_list = build_node(lex_list)

                assert element_node

                yield element_node

                if lex_list:  # has comma next
                    assert is_type(lex_list[0], COMMA)
                    lex_list.popleft()

        return cls(list(_array_items(lex_list)))

    def __init__(self, element_nodes):
        self.element_nodes = element_nodes

    def to_python(self):
        return [n.to_python() for n in self.element_nodes]


class StringNode:
    @classmethod
    def from_lex_item(cls, lex_item):
        assert is_type(lex_item, STRING)
        return cls(lex_item.value)

    def __init__(self, value):
        self.value = value

    def to_python(self):
        return self.value


class NumberNode:
    @classmethod
    def from_lex_item(cls, lex_item):
        assert is_type(lex_item, NUMBER)
        return cls(lex_item.value)

    def __init__(self, value):
        self.value = value

    def to_python(self):
        return int(self.value)


class TrueNode:
    @classmethod
    def from_lex_item(cls, lex_item):
        assert is_type(lex_item, TRUE)
        return cls()

    def to_python(self):
        return True


class FalseNode:
    @classmethod
    def from_lex_item(cls, lex_item):
        assert is_type(lex_item, FALSE)
        return cls()

    def to_python(self):
        return False


class NullNode:
    @classmethod
    def from_lex_item(cls, lex_item):
        assert is_type(lex_item, NULL)
        return cls()

    def to_python(self):
        return None


NODE_MAPPING = {
    TRUE: TrueNode,
    FALSE: FalseNode,
    NULL: NullNode,
    STRING: StringNode,
    NUMBER: NumberNode,
}


def build_node(lex_list):
    if not lex_list:
        return None, lex_list
    elif is_type(lex_list[0], LEFT_BRACKET):
        return build_object_node(lex_list)
    elif is_type(lex_list[0], LEFT_BRACE):
        return build_array_node(lex_list)
    else:
        lex_item = lex_list.popleft()
        return build_value_node(lex_item), lex_list


def aggregate_node_builder(opening_item_type, aggregate_node_class):
    assert aggregate_node_class in (ObjectNode, ArrayNode)

    def _build(lex_list):
        assert lex_list and is_type(lex_list[0], opening_item_type)

        right_lex_list = lex_list
        opening_item = right_lex_list.popleft()
        left_lex_list = deque([opening_item])
        stack = [opening_item]

        while stack:
            item = right_lex_list.popleft()
            left_lex_list.append(item)

            if is_type(item, RIGHT_BRACE):
                assert is_type(stack[-1], LEFT_BRACE)
                stack.pop()
            elif is_type(item, RIGHT_BRACKET):
                assert is_type(stack[-1], LEFT_BRACKET)
                stack.pop()
            elif is_type(item, LEFT_BRACE) or is_type(item, LEFT_BRACKET):
                stack.append(item)

        return aggregate_node_class.from_lex_list(left_lex_list), right_lex_list

    return _build


build_object_node = aggregate_node_builder(LEFT_BRACKET, ObjectNode)
build_array_node = aggregate_node_builder(LEFT_BRACE, ArrayNode)


def build_value_node(lex_item):
    node_class = NODE_MAPPING[lex_item.type]
    return node_class.from_lex_item(lex_item)


def is_type(lex_item, type_string):
    return lex_item.type is type_string

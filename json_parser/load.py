from parse import ObjectNode


def load(object_node):
    assert isinstance(object_node, ObjectNode)
    return object_node.to_python()

import functools

@functools.total_ordering
class CompareKeyMixin(object):
    """
    Inherit from this class to automatically add key based comparisons (<, >, <=, etc.) to your
    class. All you have to do is define a __key attribute (or property), which contains a hashable
    collection of attributes to compare against. Based on this answer by Alex Martelli:
    http://stackoverflow.com/a/1061350/1286571
    e.g.:
    >>> class MyClass(CompareKeyMixin):
    ...      def __init__(self, a, b):
    ...         self.a = a
    ...         self.b = b
    ...         self._key = (a, b)
    >>> sorted([MyClass(1, 2), MyClass(0, 100)])[0].a
    0
    """
    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self._key < other._key
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._key == other._key
        return NotImplemented

    def __hash__(self):
        return hash(self._key)

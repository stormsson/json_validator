from abc import abstractmethod

class BaseRule():
    def __init__(self, mandatory=False, allow_empty=True, parent=None, name=None, **kwargs):
        self.allow_empty = allow_empty
        self.mandatory = mandatory
        self.name = name

        self.parent_schema = parent
        self.top_schema = None

        self._set_top_schema()

    def _set_top_schema(self):
        reference = self
        while reference.parent_schema:
            reference = reference.parent_schema

        if reference != self:
            self.top_schema = reference

    def _get_top_schema(self):
        if self.top_schema is None:
            self._set_top_schema()

        return self.top_schema

    def validate(self, value):
        if not self.allow_empty:
            if (value == None) or (value ==""):
                return False

        return True


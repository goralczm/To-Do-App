from enum import Enum


class SortableEnum(Enum): # pragma: no cover
    def __eq__(self, other):
        if isinstance(other, SortableEnum):
            return (
                    self._member_names_.index(self.name) ==
                    self._member_names_.index(other.name)
            )
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, SortableEnum):
            return (
                    self._member_names_.index(self.name) >
                    self._member_names_.index(other.name)
            )
        return NotImplemented
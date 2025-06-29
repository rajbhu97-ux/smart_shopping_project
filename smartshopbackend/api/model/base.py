

import attr

from attr import asdict, fields

@attr.define
class FilteredDictConvertible:

    @classmethod
    def from_dict(cls, parameters: dict):
        filtered = {param.name: parameters[param.name] for param in fields(cls) if param.name in parameters}
        return cls(**filtered)
    
    def to_dict(self):
        return asdict(self)
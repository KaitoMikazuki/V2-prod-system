from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# NONE means that the condition will be omitted in the query statement
@dataclass
class Filters:
    work_type: tuple[str, ...] = () 
    label: tuple[str, ...] = ()
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    datacolumn: str = "*" #Defaults to all columns in sql

    _VALID_WORK_TYPES = set(('tdl', 'deep', 'shallow', None))
    _VALID_LABELS = set((None,)) #TODO: extract the valid labels from SQL table: labels

    # Validates the parameters
    def __post_init__(self):

        # Validates work type
        if not isinstance(self.work_type, tuple):
            raise TypeError("Invalid work_type type")
        invalid = set(self.work_type) - self._VALID_WORK_TYPES
        if invalid: 
            return ValueError("Invalid work_type value")
        
        # Validates labels
        if not isinstance(self.label, tuple):
            raise TypeError("Invalid label type")
        invalid = set(self.label) - self._VALID_LABELS
        if invalid: 
            return ValueError("Invalid label value")

        # validate date related parameters
        if self.start_date is not None:
            try: 
                datetime.fromisoformat(self.start_date)
            except ValueError:
                raise ValueError("Invalid start_date")
            
        if self.end_date is not None:
            try: 
                datetime.fromisoformat(self.end_date)
            except ValueError:
                raise ValueError("Invalid start_date")
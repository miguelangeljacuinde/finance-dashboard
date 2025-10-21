from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    date: str
    category: str
    amount: float
    description: str
    type: str  # 'income' or 'expense'
    id: int = None
    
    def to_dict(self):
        return {
            'date': self.date,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'type': self.type
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
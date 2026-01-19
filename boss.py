"""
Класс врага (босса).
"""
from core import Human


class Boss(Human):
    """Враг для боя."""
    
    def __init__(self, name: str, hp: int = 150, damage: int = 15):
        super().__init__(name, hp, damage)

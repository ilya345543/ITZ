"""
Базовые классы для игры.
"""
import random


class Human:
    """Базовый класс для всех персонажей."""
    
    def __init__(self, name: str, hp: int = 100, damage: int = 10):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
    
    @property
    def is_alive(self) -> bool:
        """Проверяет, жив ли персонаж."""
        return self.hp > 0
    
    def take_damage(self, damage: int):
        """Принимает урон."""
        # max(0, ...) чтобы HP не ушло в минус
        self.hp = max(0, self.hp - damage)
    
    def attack(self, target: 'Human') -> int:
        """Атакует цель. Возвращает нанесенный урон."""
        # Считаем сколько реально нанесли урона (не больше чем HP у цели)
        damage = min(self.damage, target.hp)
        target.take_damage(self.damage)
        return damage
    
    def __str__(self) -> str:
        return f"{self.name} (HP: {self.hp}/{self.max_hp})"


class Warrior(Human):
    """Воин - больше HP и урона."""
    
    def __init__(self, name: str):
        super().__init__(name, hp=120, damage=15)


class Mage(Human):
    """Маг - меньше HP, но больше урона."""
    
    def __init__(self, name: str):
        super().__init__(name, hp=80, damage=20)


class Healer(Human):
    """Лекарь - баланс."""
    
    def __init__(self, name: str):
        super().__init__(name, hp=100, damage=12)

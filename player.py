"""
Класс игрока.
"""
import json
from core import Warrior, Mage, Healer


class Player:
    """Игрок с персонажем."""
    
    def __init__(self, name: str):
        self.name = name
        self.character = None
        self.artifacts = []
        self.story_progress = 0
        self.story_branch = None
    
    def set_character(self, character):
        """Устанавливает персонажа."""
        self.character = character
    
    def add_artifact(self, artifact: str):
        """Добавляет артефакт."""
        self.artifacts.append(artifact)
    
    def to_dict(self) -> dict:
        """Сериализует игрока."""
        # Сохраняем данные персонажа если он есть
        char_data = None
        if self.character:
            char_data = {
                "name": self.character.name,
                "class": self.character.__class__.__name__,  # Название класса нужно чтобы потом восстановить правильный тип
                "hp": self.character.hp,
                "max_hp": self.character.max_hp,
            }
        
        return {
            "name": self.name,
            "story_progress": self.story_progress,
            "story_branch": self.story_branch,
            "artifacts": self.artifacts,
            "character": char_data
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        """Десериализует игрока."""
        player = cls(data["name"])
        player.story_progress = data.get("story_progress", 0)
        player.story_branch = data.get("story_branch")
        player.artifacts = data.get("artifacts", [])
        
        # Словарь чтобы по названию класса найти нужный класс
        class_map = {
            "Warrior": Warrior,
            "Mage": Mage,
            "Healer": Healer,
        }
        
        # Восстанавливаем персонажа из сохраненных данных
        char_data = data.get("character")
        if char_data:
            class_name = char_data["class"]
            if class_name in class_map:
                # Создаем персонажа нужного класса
                char_class = class_map[class_name]
                char = char_class(char_data["name"])
                # Восстанавливаем HP (если нет в сохранении - берем максимум)
                char.hp = char_data.get("hp", char.max_hp)
                player.character = char
        
        return player

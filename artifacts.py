"""
Система артефактов.
"""
import random


class ArtifactStorage:
    """Хранилище артефактов."""
    
    def __init__(self):
        self.all_artifacts = [
            "Меч Дракона",
            "Щит Защитника",
            "Посох Мудрости",
            "Кольцо Силы",
            "Амулет Жизни",
            "Плащ Теней",
            "Броня Титана",
            "Сапоги Скорости"
        ]
    
    def generate_new(self):
        """Генерирует новые артефакты, если все собраны."""
        print("Все артефакты собраны! Генерация новых...")
        new_artifacts = []
        for i in range(8):
            x = random.randint(1, 9999)
            new_artifacts.append(f"АРТЕФАКТ_{x}")
        
        self.all_artifacts = new_artifacts
        print(f"Сгенерировано {len(new_artifacts)} новых артефактов!")
    
    def take_artifact(self) -> str:
        """Берет артефакт из хранилища."""
        # Если артефакты закончились - генерируем новые
        if not self.all_artifacts:
            self.generate_new()
        
        # Берем первый артефакт из списка и удаляем его
        artifact = self.all_artifacts.pop(0)
        return artifact
    
    def return_artifacts(self, artifacts: list):
        """Возвращает артефакты в хранилище."""
        self.all_artifacts.extend(artifacts)
    
    def has_artifacts(self) -> bool:
        """Проверяет, есть ли артефакты в хранилище."""
        return len(self.all_artifacts) > 0
    
    def get_artifacts_count(self) -> int:
        """Возвращает количество артефактов в хранилище."""
        return len(self.all_artifacts)

"""
Простая система боя.
"""


class Battle:
    """Класс для управления боем."""
    
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
    
    def start(self) -> bool:
        """Запускает бой. Возвращает True, если игрок победил."""
        print(f"\nБОЙ: {self.player.name} vs {self.enemy.name}")
        print(f"{self.player.name}: {self.player.hp} HP")
        print(f"{self.enemy.name}: {self.enemy.hp} HP\n")
        
        # Бой идет пока оба живы - сначала ходит игрок, потом враг
        while self.player.is_alive and self.enemy.is_alive:
            # Ход игрока
            if self.player.is_alive:
                damage = self.player.attack(self.enemy)
                print(f"{self.player.name} атакует! Нанесено {damage} урона")
                print(f"{self.enemy.name}: {self.enemy.hp} HP")
                
                if not self.enemy.is_alive:
                    print(f"\n{self.player.name} победил!")
                    return True
            
            # Ход врага
            if self.enemy.is_alive:
                damage = self.enemy.attack(self.player)
                print(f"{self.enemy.name} атакует! Нанесено {damage} урона")
                print(f"{self.player.name}: {self.player.hp} HP")
                
                if not self.player.is_alive:
                    print(f"\n{self.player.name} проиграл...")
                    return False
            
            print()  # Пустая строка между ходами
        
        return False

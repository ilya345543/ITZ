"""
Главный файл игры.
"""
import json
import os
from core import Warrior, Mage, Healer
from boss import Boss
from battle import Battle
from artifacts import ArtifactStorage
from player import Player

SAVE_FILE = "save.txt"


def save_game(player: Player, login: str, password: str):
    """Сохраняет игру."""
    try:
        save_data = {
            "login": login,
            "password": password,
            "player": player.to_dict()
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        print("Игра сохранена!")
    except IOError as e:
        print(f"Ошибка сохранения: {e}")


def load_game(login: str, password: str) -> Player:
    """Загружает игру."""
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            save_data = json.load(f)
        # Проверяем что логин и пароль совпадают
        if save_data.get("login") != login or save_data.get("password") != password:
            return None
        player_data = save_data.get("player")
        if player_data:
            return Player.from_dict(player_data)
    except (json.JSONDecodeError, IOError, KeyError):
        # Если файл поврежден или нет нужных данных - просто возвращаем None
        pass
    return None


def choose_class_menu(player_name: str):
    """Меню выбора класса."""
    print("\nВЫБОР КЛАССА")
    print("1 - Воин (HP: 120, Урон: 15)")
    print("2 - Маг (HP: 80, Урон: 20)")
    print("3 - Лекарь (HP: 100, Урон: 12)")
    
    choice = input("Ваш выбор: ").strip()
    
    if choice == "1":
        character = Warrior(player_name)
        print(f"\nВы выбрали Воина!")
    elif choice == "2":
        character = Mage(player_name)
        print(f"\nВы выбрали Мага!")
    elif choice == "3":
        character = Healer(player_name)
        print(f"\nВы выбрали Лекаря!")
    else:
        character = Warrior(player_name)
        print(f"\nВыбран Воин (по умолчанию)")
    
    print(f"Персонаж: {character}")
    return character


def story_branch_1(player: Player, storage: ArtifactStorage):
    """Сценарий 1: Замок."""
    print("\nЗАМОК")
    print("Вы подходите к замку...")
    
    choice = input("\n1 - Войти в замок\n2 - Обойти замок\nВаш выбор: ").strip()
    
    if choice == "1":
        print("\nВ замке вас встречает страж!")
        enemy = Boss("Страж", hp=100, damage=12)
        battle = Battle(player.character, enemy)
        win = battle.start()
        
        if win:
            artifact = storage.take_artifact()
            player.add_artifact(artifact)
            print(f"\nВы получили артефакт: {artifact}")
            player.story_progress += 1
            return True
        else:
            return False
    
    elif choice == "2":
        print("\nВы обошли замок и нашли артефакт!")
        artifact = storage.take_artifact()
        player.add_artifact(artifact)
        print(f"Вы получили артефакт: {artifact}")
        player.story_progress += 1
        return True
    
    return False


def story_branch_2(player: Player, storage: ArtifactStorage):
    """Сценарий 2: Лес."""
    print("\nЛЕС")
    print("Вы входите в лес...")
    
    choice = input("\n1 - Идти по тропинке\n2 - Идти через чащу\nВаш выбор: ").strip()
    
    if choice == "1":
        print("\nНа тропинке вас атакует волк!")
        enemy = Boss("Волк", hp=80, damage=10)
        battle = Battle(player.character, enemy)
        win = battle.start()
        
        if win:
            artifact = storage.take_artifact()
            player.add_artifact(artifact)
            print(f"\nВы получили артефакт: {artifact}")
            player.story_progress += 1
            return True
        else:
            return False
    
    elif choice == "2":
        print("\nВ чаще вы нашли артефакт!")
        player.character.take_damage(10)
        print("Вы получили немного урона от колючек.")
        artifact = storage.take_artifact()
        player.add_artifact(artifact)
        print(f"Вы получили артефакт: {artifact}")
        player.story_progress += 1
        return True
    
    return False


def story_branch_3(player: Player, storage: ArtifactStorage):
    """Сценарий 3: Пещера."""
    print("\nПЕЩЕРА")
    print("Вы входите в пещеру...")
    
    choice = input("\n1 - Идти вглубь\n2 - Искать сокровища\nВаш выбор: ").strip()
    
    if choice == "1":
        print("\nВ глубине пещеры вас ждет гоблин!")
        enemy = Boss("Гоблин", hp=120, damage=14)
        battle = Battle(player.character, enemy)
        win = battle.start()
        
        if win:
            artifact = storage.take_artifact()
            player.add_artifact(artifact)
            print(f"\nВы получили артефакт: {artifact}")
            player.story_progress += 1
            return True
        else:
            return False
    
    elif choice == "2":
        print("\nВы нашли сокровища!")
        artifact = storage.take_artifact()
        player.add_artifact(artifact)
        print(f"Вы получили артефакт: {artifact}")
        player.story_progress += 1
        return True
    
    return False


def story_branch_heal(player: Player):
    """Локация для восстановления здоровья."""
    print("\nДЕРЕВНЯ")
    print("Вы пришли в деревню, где можно отдохнуть и восстановить здоровье.")
    
    if player.character.hp == player.character.max_hp:
        print("У вас уже полное здоровье!")
        return True
    
    old_hp = player.character.hp
    player.character.hp = player.character.max_hp
    healed = player.character.hp - old_hp
    
    print(f"Вы отдохнули и восстановили {healed} HP!")
    print(f"Текущее здоровье: {player.character.hp}/{player.character.max_hp}")
    return True


def main_menu(player: Player, storage: ArtifactStorage):
    """Главное меню."""
    while True:
        print("\nГЛАВНОЕ МЕНЮ")
        print(f"Игрок: {player.name}")
        print(f"Персонаж: {player.character}")
        print(f"Артефактов: {len(player.artifacts)}")
        if player.artifacts:
            print(f"Артефакты: {', '.join(player.artifacts)}")
        print("\n1 - Замок")
        print("2 - Лес")
        print("3 - Пещера")
        print("4 - Деревня (восстановить здоровье)")
        print("5 - Сохранить игру")
        print("6 - Выход")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            player.story_branch = "branch_1"
            story_branch_1(player, storage)
        elif choice == "2":
            player.story_branch = "branch_2"
            story_branch_2(player, storage)
        elif choice == "3":
            player.story_branch = "branch_3"
            story_branch_3(player, storage)
        elif choice == "4":
            story_branch_heal(player)
        elif choice == "5":
            return "save"
        elif choice == "6":
            return "exit"
        else:
            print("Неверный выбор.")


def main():
    """Главная функция."""
    print("ИГРА")
    
    login = input("Логин: ").strip()
    password = input("Пароль: ").strip()
    
    # Пытаемся загрузить сохранение
    player = None
    if os.path.exists(SAVE_FILE):
        loaded_player = load_game(login, password)
        if loaded_player:
            print("\nНайдено сохранение!")
            load_choice = input("Загрузить? (y/n): ").strip().lower()
            if load_choice == "y":
                player = loaded_player
                print(f"Игра загружена!")
                print(f"Игрок: {player.name}")
                print(f"Артефактов: {len(player.artifacts)}")
    
    # Если не загрузили - создаем нового игрока
    if player is None:
        player_name = input("\nВведите имя: ").strip() or "Герой"
        player = Player(player_name)
        character = choose_class_menu(player_name)
        player.set_character(character)
    
    storage = ArtifactStorage()
    # Если все артефакты собраны - генерируем новые
    if storage.get_artifacts_count() == 0 and len(player.artifacts) > 0:
        storage.generate_new()
    
    while True:
        result = main_menu(player, storage)
        
        if result == "save":
            save_game(player, login, password)
        elif result == "exit":
            print("\nВыход...")
            save_choice = input("Сохранить? (y/n): ").strip().lower()
            if save_choice == "y":
                save_game(player, login, password)
            else:
                print("Игра не сохранена.")
                # Если не сохранили - возвращаем артефакты в хранилище
                if player.artifacts:
                    storage.return_artifacts(player.artifacts)
                    print(f"Артефакты возвращены.")
            break


if __name__ == "__main__":
    main()

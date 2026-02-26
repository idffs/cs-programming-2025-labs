import json
import random
import os
import math
from typing import Dict, List, Any, Optional

DATA_DIR = "data"
CHARACTER_FILE = os.path.join(DATA_DIR, "Character.json")
RACES_FILE = os.path.join(DATA_DIR, "Races.json")
MONSTERS_FILE = os.path.join(DATA_DIR, "Monsters.json")
ARMORS_FILE = os.path.join(DATA_DIR, "Armors.json")
WEAPONS_FILE = os.path.join(DATA_DIR, "Weapons.json")
POTIONS_FILE = os.path.join(DATA_DIR, "Potions.json")
ROOMS_FILE = os.path.join(DATA_DIR, "Rooms.json")
MAIN_FILE = os.path.join(DATA_DIR, "Main.json")
MISC_ITEMS_FILE = os.path.join(DATA_DIR, "miscItems.json")

class Game:
    def __init__(self):
        self.player = self.load_json(CHARACTER_FILE)
        self.races = self.load_json(RACES_FILE)["races"]
        self.monsters = self.load_json(MONSTERS_FILE)["monsters"]
        self.armors = {a["id"]: a for a in self.load_json(ARMORS_FILE)}
        self.weapons = {w["id"]: w for w in self.load_json(WEAPONS_FILE)}
        self.potions = {p["id"]: p for p in self.load_json(POTIONS_FILE)}
        self.misc_items = {m["id"]: m for m in self.load_json(MISC_ITEMS_FILE)["misc_items"]}
        self.rooms = self.load_json(ROOMS_FILE)["rooms"]
        self.settings = self.load_json(MAIN_FILE)["game_settings"]

        self.current_room = None
        self.current_floor = self.settings["start_floor"]
        self.rooms_visited = 0
        self.game_over = False

    def load_json(self, path: str, key: Optional[str] = None) -> Any:
        if not hasattr(self, "_cache"):
            self._cache = {}
        cache_key = f"{path}_{key}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if key is None:
                result = data
            else:
                if key not in data:
                    raise KeyError(f"В JSON-файле {path} отсутствует ключ '{key}'")
                result = data[key]
            self._cache[cache_key] = result
            return result
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Ошибка при загрузке {path}: {e}")
            return {}
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
            raise
    
    def update_armor_from_defense(self):
        defense_bonus = self.player["stats"]["defense"] // 2
        self.player["armor"] = self.player.get("base_armor", 0) + defense_bonus

    def get_dodge_chance(self):
        return 0.05 + (self.player["stats"]["agility"] // 3) * 0.005


    def get_crit_chance(self):
        return 0.05 + (self.player["stats"]["agility"] // 2) * 0.005
        
    def create_character(self):
            print("=== Создание персонажа ===")
            self.player["name"] = input("Имя персонажа: ").strip()

            print("\nВыберите расу:")
            print("1 — Человек")
            print("2 — Эльф")
            print("3 — Дворф")

            race_choice = input("\n> ").strip()

            race_map = {
                "1": "human",
                "2": "elf",
                "3": "dwarf"
            }

            if race_choice not in race_map:
                print("Обнаружен неккоректный ввод. По умолчанию выбран Человек.")
                race_id = "human"
            else:
                race_id = race_map[race_choice]

            selected_race = next((r for r in self.races if r["id"] == race_id), None)
            if not selected_race:
                print("Ошибка: данные о выбранной расе отсутствуют!")
                return

            self.player["race"] = selected_race["name"]
            print(f"\nВы выбрали: {self.player["race"]}")

            if "stats" not in self.player:
                self.player["stats"] = {}

            for stat in ["strength", "agility", "vitality", "Weight", "Height"]:
                min_val, max_val = selected_race["attributes"][stat]
                self.player["stats"][stat] = random.randint(min_val, max_val)

            weight = self.player["stats"]["Weight"]
            height = self.player["stats"]["Height"]
            agility_bonus = max(0, (height - 120) / 10 - weight / 20)
            self.player["stats"]["agility"] += int(agility_bonus)

            self.player["max_health"] = self.player["stats"]["vitality"] * 5
            self.player["health"] = self.player["max_health"]
            self.player["damage"] = self.player["stats"]["strength"] + 1

            self.player["base_armor"] = 0
            self.player["stats"]["defense"] = ( self.player["stats"]["strength"] + self.player["stats"]["vitality"] ) // 3

            self.update_armor_from_defense()

            self.player["stat_points"] = 0


            print(f"\nПерсонаж создан! Здоровье: {self.player["health"]}, Броня: {self.player["armor"]}")


    def enter_room(self):
        self.rooms_visited += 1
        if self.rooms_visited % self.settings["rooms_per_floor"] == 0:
            self.current_floor += 1
            print(f"\nВы перешли на {self.current_floor} этаж!")
            self.increase_monster_difficulty()

        junctions = [r for r in self.rooms if r.get("is_junction", False)]
        if not junctions:
            raise ValueError("Нет комнат с развилками!")

        total_chance = sum(r["chance"] for r in junctions)
        chosen = random.random() * total_chance
        selected_junction = None

        for room in junctions:
            chosen -= room["chance"]
            if chosen <= 0:
                selected_junction = room
                break

        self.current_room = selected_junction
        print(f"\n=== Вы подошли к развилке в: {self.current_room["name"]} ===")
        self.show_branches()
        direction = self.choose_direction()

        if direction == 1:
            next_room = self.current_room["left_branch"]
        elif direction == 2:
            next_room = self.current_room["right_branch"]
        else:
            print("Неверное направление.")
            return

        self.current_room = next_room
        print(f"\n=== Вы вошли в: {self.current_room["name"]} ===")
        self.handle_room_type(self.current_room["type"])


    def show_branches(self):
        left = self.current_room["left_branch"]
        right = self.current_room["right_branch"]

        if self.current_room["visibility"] == "unknown":
            print("Темнота не позволяет определить что находится впереди")
        else:
            print(f"1. Налево: {left["name"]} ({left["type"]})")
            print(f"2. Направо: {right["name"]} ({right["type"]})")


    def choose_direction(self) -> int:
        while True:
            try:
                choice = input("Выберите направление (1 — налево, 2 — направо): ").strip()  
                if choice in ["1", "2"]:
                    return int(choice)
                else:
                    print("Неверный выбор. Введите 1 или 2.")
            except ValueError:
                print("Введите число 1 или 2.")
                    
    def increase_monster_difficulty(self):
        multiplier = self.settings["monster_stat_per_floor"]

        for monster in self.monsters:
            monster["level"] = self.current_floor
        
            monster["health"] = math.ceil(monster["health"] * multiplier)
            monster["maxHealth"] = math.ceil(monster["maxHealth"] * multiplier)
            monster["attack"] = math.ceil(monster["attack"] * multiplier)
            monster["defense"] = math.ceil(monster["defense"] * multiplier)
            monster["health"] = min(monster["health"], monster["maxHealth"])
        
    def handle_room_type(self, room_type: str):
        match room_type:
            case "combat":
                monster = self.encounter_monster()
                if monster:
                    self.fight(monster)
                else:
                    print("В комнате никого нет...")
            case "rest":
                self.rest()
            case "chest":
                self.open_chest()
            case _:
                print(f"Неизвестный тип комнаты: {room_type}")

    def rest(self):
        self.player["health"] = self.player["max_health"]
        print("Вы отдохнули и полностью восстановили здоровье!")
        self.level_up()

    def level_up(self):
        while self.player["experience"] >= self.settings["exp_per_level"]:
            self.player["level"] += 1
            self.player["experience"] -= self.settings["exp_per_level"]
            stat_points = self.settings.get("stat_points_per_level", 2)
            self.player["stat_points"] += stat_points
            print(f"\nУровень повышен! Теперь у вас {self.player["level"]} уровень!")
            print(f"Вы получили {stat_points} очков характеристик для распределения.")
            self.distribute_stats(stat_points)

    def distribute_stats(self, skill_points: int):
        print(f"\n=== Распределение очков навыков (всего {skill_points} очков) ===")
        print("1 — Живучесть")
        print("2 — Ловкость")
        print("3 — Сила")

        while skill_points > 0:
            print(f"\nОсталось распределить: {skill_points} очков.")
            choice = input("Выберите навык (1–3) или 'q' для выхода\n> ").strip()

            if choice == "q":
                print("Распределение прервано.")
                break

            if choice not in ["1", "2", "3"]:
                print("Ошибка: введите 1, 2, 3 или 'q'.")
                continue

            if choice == "1":
                self.player["stats"]["vitality"] += 1
                health_increase = 5
                self.player["max_health"] += health_increase
                self.player["health"] = min(self.player["health"] + health_increase, self.player["max_health"])
                print(f"+1 к Живучести! Максимальное здоровье увеличено на {health_increase}.")

            elif choice == "2":
                self.player["stats"]["agility"] += 1
                print("+1 к Ловкости!")

            elif choice == "3":
                self.player["stats"]["strength"] += 1
                damage_increase = 1
                self.player["damage"] += damage_increase
                print(f"+1   к Силе! Урон увеличен на {damage_increase}.")

            skill_points -= 1

        self.update_armor_from_defense()
        self.player["damage"] = (self.player["stats"]["strength"] +self.get_weapon_damage())
        self.player["max_health"] = self.player["stats"]["vitality"] * 5
        self.player["health"] = min(self.player["health"],self.player["max_health"])

    def open_chest(self):
        loot_types = ["gold", "potion", "weapon", "armor"]
        loot = random.choice(loot_types)
        if loot == "gold":
            gold = random.randint(5, 20)
            self.player["gold"] += gold
            print(f"Вы нашли {gold} золота!")
        elif loot == "potion":
            potion_id = random.choice(list(self.potions.keys()))
            potion_name = self.potions[potion_id]["name"]
            self.add_item(potion_id, potion_name, "potion")
        elif loot == "weapon":
            weapon_id = random.choice(list(self.weapons.keys()))
            weapon_name = self.weapons[weapon_id]["name"]
            self.add_item(weapon_id, weapon_name, "weapon")
        elif loot == "armor":
            armor_id = random.choice(list(self.armors.keys()))
            armor_name = self.armors[armor_id]["name"]
            self.add_item(armor_id, armor_name, "armor")

        if len(self.player["inventory"]) > self.settings["max_inventory_slots"]:
            print(f"Инвентарь переполнен! Максимальное количество слотов: {self.settings["max_inventory_slots"]}")
            self.manage_inventory_overflow()

    def manage_inventory_overflow(self):
        while len(self.player["inventory"]) > self.settings["max_inventory_slots"]: 
            print("\nИнвентарь переполнен. Выберите предмет для удаления:")
            for i, item in enumerate(self.player["inventory"]):
                print(f"{i + 1}. {item["name"]} ({item["id"]})")
            try:
                choice = int(input("Номер предмета для удаления: ")) - 1
                if 0 <= choice < len(self.player["inventory"]):
                    removed_item = self.player["inventory"].pop(choice)
                    print(f"Удален предмет: {removed_item["name"]}")
                else:
                    print("Неверный номер.")
            except ValueError:
                print("Введите число.")

    def encounter_monster(self) -> Optional[Dict[str, Any]]:
        possible = [
            m for m in self.monsters
            if (m.get("location") == self.current_room["id"]) 
        ]
        return random.choice(possible) if possible else None

    def fight(self, monster: Dict[str, Any]):
        player_won = False
        print("\n--- Бой начался! ---")

        while self.player["health"] > 0 and monster["health"] > 0:
            print(f"\nВаше HP: {self.player["health"]} | Монстр HP: {monster["health"]}")
            action = input("1. Атаковать  2. Уклониться  3. Использовать зелье  4. Бежать\n> ").strip()

            crit_chance_monster = 0.05

            if action == "1":
                damage = self.player["damage"]
                is_crit = random.random() < self.get_crit_chance()
                if is_crit:
                    damage *= 2
                    print(f"Критический удар! Урон x2!")

                monster["health"] -= damage
                print(f"Вы нанесли {damage} урона!")

                if monster["health"] > 0:
                    hit_chance = random.random()
                    if hit_chance < self.get_dodge_chance():
                        print(f"Успешное уклонение!")
                    else:
                        m_damage = max(1, monster["attack"] - self.player["armor"])
                        is_crit_monster = random.random() < crit_chance_monster
                        if is_crit_monster:
                            m_damage = int(m_damage * 1.5)
                            print(f"Критический удар монстра! Урон х1.5!")
                        self.player["health"] -= m_damage
                        print(f"Монстр нанес вам {m_damage} урона!")

            elif action == "2":
                if random.random() < self.get_dodge_chance():
                    print("Вы успешно уклонились!")
                else:
                    print("Уклонение не удалось!")
                    m_damage = max(1, monster["attack"] - self.player["armor"])
                    is_crit_monster = random.random() < crit_chance_monster
                    if is_crit_monster:
                        m_damage = int(m_damage * 1.5)
                        print(f"Критический удар монстра при уклонении! Урон х1.5!")
                    self.player["health"] -= m_damage
                    print(f"Монстр нанес вам {m_damage} урона!")

            elif action == "3":
                self.use_potion()
                continue

            elif action == "4":
                if random.random() < 0.5:
                    print("Вы сбежали!")
                    return
                else:
                    print("Не удалось сбежать!")
                    hit_chance = random.random()
                    if hit_chance < self.get_dodge_chance() * 0.5:
                        print(f"Удачливое уклонение! Шанс х0.5")
                        pass
                    m_damage = max(1, monster["attack"] - self.player["armor"])
                    is_crit_monster = random.random() < crit_chance_monster
                    if is_crit_monster:
                        m_damage = int(m_damage * 1.5)
                        print(f"Критический удар при побеге! Урон x1.5!")
                    self.player["health"] -= m_damage
                    print(f"Монстр ударил вас при побеге: {m_damage} урона!")

            else:
                print("Неверное действие.")

        if self.player["health"] <= 0:
            print("Вы погибли... Игра окончена.")
            self.game_over = True
            exit()
        elif monster["health"] <= 0:
            player_won = True
            monster["health"] = monster["maxHealth"]
            print(f"Победа! Вы победили {monster["name"]}!")

        if player_won:
            self.player["experience"] += monster["experience"]
            self.player["gold"] += monster["goldDrop"]
            self.drop_items(monster)
            print(f"Вы получили: {monster["experience"]} опыта, {monster["goldDrop"]} золота.")
        else:
            print("Награда не выдана — бой не завершён победой.")

    def drop_items(self, monster: Dict[str, Any]):
        for item in monster.get("itemsDrop", []):
            if random.random() < item["chance"]:
                item_id = item["item"]
                item_data = None

                if item_id in self.weapons:
                    item_data = self.weapons[item_id]
                    item_type = "weapon"
                elif item_id in self.potions:
                    item_data = self.potions[item_id]
                    item_type = "potion"
                elif item_id in self.misc_items:
                    item_data = self.misc_items[item_id]
                    item_type = "misc"

                if item_data:
                    self.add_item(item_id, item_data["name"], item_type, item_data.get("description", ""))
              
        if len(self.player["inventory"]) > self.settings["max_inventory_slots"]:
            print(f"Инвентарь переполнен! Максимальное количество слотов: {self.settings["max_inventory_slots"]}")
            self.manage_inventory_overflow()


    def use_potion(self):
        potions = [
            item for item in self.player["inventory"]
            if item["id"] in self.potions and item["count"] > 0
        ]
        if not potions:
            print("Нет зелий в инвентаре!")
            return

        print("\n=== Доступные зелья ===")
        for i, item in enumerate(potions):
            potion_data = self.potions[item["id"]]
            heal = potion_data["heal"]
            print(f"{i + 1}. {potion_data["name"]} (+{heal} HP) ×{item["count"]}")


        try:
            choice = int(input("\nВведите номер зелья (0 — отмена): ")) - 1

            if choice == 0:
                print("Действие отменено.")
                return

            if choice < 0 or choice >= len(potions):
                print("Неверный номер! Попробуйте снова.")
                return

            selected_item = potions[choice]
            potion_data = self.potions[selected_item["id"]]
            heal_amount = potion_data["heal"]

            self.player["health"] = min(self.player["max_health"],self.player["health"] + heal_amount)

            print(f"Вы использовали {potion_data["name"]}!")
            print(f"Восстановлено: {heal_amount} HP")
            print(f"Здоровье: {self.player["health"]}/{self.player["max_health"]}")

            selected_item["count"] -= 1
            if selected_item["count"] <= 0:
                self.player["inventory"].remove(selected_item)
                print(" Зелье закончилось и удалено из инвентаря.")

        except ValueError:
            print("Ошибка: введите число!")
        except KeyError as e:
            print(f"Ошибка: не найдено зелье с ID {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

    def get_weapon_damage(self) -> int:
        weapon_id = self.player["equipment"].get("weapon")
        if weapon_id and weapon_id in self.weapons:
            return self.weapons[weapon_id]["damage"]
        return 0

    def show_status(self):
        print("\n=== Статус персонажа ===")
        print(f"Имя: {self.player["name"]}")
        print(f"Раса: {self.player["race"]}")
        print(f"Уровень: {self.player["level"]}")
        print(f"Опыт: {self.player["experience"]} / {self.settings["exp_per_level"]}")

        print(f"\nЗдоровье: {self.player["health"]} / {self.player["max_health"]}")
        print(f"Урон: {self.player["damage"]}")
        print(f"Броня: {self.player["armor"]}")

        dodge_chance = self.get_dodge_chance()
        dodge_percent = dodge_chance * 100
        print(f"Шанс уворота: {dodge_percent:.1f}%")

        crit_chance = self.get_crit_chance()
        crit_percent = crit_chance * 100
        print(f"Шанс критического удара: {crit_percent:.1f}%")

        print(f"\nХарактеристики:")
        print(f"  Сила: {self.player["stats"]["strength"]}")    
        print(f"  Ловкость: {self.player["stats"]["agility"]}")
        print(f"  Живучесть: {self.player["stats"]["vitality"]}")
        print(f"  Вес: {self.player["stats"]["Weight"]}")
        print(f"  Рост: {self.player["stats"]["Height"]}")

    def show_inventory(self):
        if not self.player["inventory"]:
            print("Инвентарь пуст.")
            return

        print("\n=== Инвентарь ===")

        potions = []
        weapons = []
        armors = []
        misc_items = []

        for item in self.player["inventory"]:
            if item["id"] in self.potions:
                potions.append(item)
            elif item["id"] in self.weapons:
                weapons.append(item)
            elif item["id"] in self.armors:
                armors.append(item)
            else:
                misc_items.append(item)

        total_displayed = 0

        if potions:
            print("\nЗелья:")
            for i, item in enumerate(potions, 1):
                potion_data = self.potions[item["id"]]
                count = item["count"]
                heal = potion_data.get("heal", 0)
                print(f"{total_displayed + i}. {potion_data['name']} ×{count} (+{heal} HP)")
            total_displayed += len(potions)

        if weapons:
            print("\nОружие:")
            for i, item in enumerate(weapons, 1):
                weapon_data = self.weapons[item["id"]]
                count = item["count"]
                damage = weapon_data.get("damage", 0)
                print(f"{total_displayed + i}. {weapon_data['name']} ×{count} (урон: {damage})")
            total_displayed += len(weapons)

        if armors:
            print("\nБроня:")
            for i, item in enumerate(armors, 1):
                armor_data = self.armors[item["id"]]
                count = item["count"]
                defense = armor_data.get("defense", 0)
                print(f"{total_displayed + i}. {armor_data['name']} ×{count} (защита: {defense})")
            total_displayed += len(armors)

        if misc_items:
            print("\nПрочие предметы:")
            for i, item in enumerate(misc_items, 1):
                count = item["count"]
                name = item["name"]
                print(f"{total_displayed + i}. {name} ×{count}")
            total_displayed += len(misc_items)

        print("\nВыберите действие:")
        if potions:
            print("1. Использовать зелье")
        if total_displayed > 0:
            print("2. Просмотреть описание предмета")
            print("3. Выбросить предмет")
        print("4. Вернуться в игру")

        choice = input("\nВаш выбор\n> ").strip()

        if choice == "1" and potions:
            try:
                item_index = int(input(f"Введите номер зелья (1–{len(potions)}): ")) - 1
                if 0 <= item_index < len(potions):
                    item = potions[item_index]
                    potion_data = self.potions[item["id"]]
                    heal_amount = potion_data["heal"]
                    self.player["health"] = min(
                        self.player["max_health"],
                self.player["health"] + heal_amount
            )
                    item["count"] -= 1
                    if item["count"] <= 0:
                        self.player["inventory"].remove(item)
                    print(f"Вы использовали {potion_data['name']}! +{heal_amount} HP. Здоровье: {self.player['health']}")
                else:
                    print("Неверный номер зелья!")
            except ValueError:
                print("Введите число!")

        elif choice == "2" and total_displayed > 0:
            try:
                item_num = int(input(f"Введите номер предмета (1–{total_displayed}): ")) - 1
                if item_num < 0 or item_num >= total_displayed:
                    print("Неверный номер предмета!")
                    return

                all_items = potions + weapons + armors + misc_items
                item = all_items[item_num]
                item_id = item["id"]

                item_data = None
                if item_id in self.potions:
                    item_data = self.potions[item_id]
                elif item_id in self.weapons:
                    item_data = self.weapons[item_id]
                elif item_id in self.armors:
                    item_data = self.armors[item_id]
                else:
                    item_data = {"description": f"{item['name']}. Детали неизвестны."}

                desc = item_data.get("description", "Описание отсутствует.")
                print(f"\nОписание: {desc}")

            except ValueError:
                print("Введите число!")

        elif choice == "3" and total_displayed > 0:
            try:
                item_num = int(input(f"Введите номер предмета для выбрасывания (1–{total_displayed}): ")) - 1
                if item_num < 0 or item_num >= total_displayed:
                    print("Неверный номер предмета!")
                    return

                all_items = potions + weapons + armors + misc_items
                item = all_items[item_num]

                if item["count"] > 1:
                    try:
                        quantity = int(input(f"Сколько штук выбросить? (1–{item['count']}): "))
                        if 1 <= quantity <= item["count"]:
                            item["count"] -= quantity
                            print(f"Вы выбросили {quantity} шт. {item['name']}")
                            if item["count"] == 0:
                                self.player["inventory"].remove(item)
                        else:
                            print("Некорректное количество!")
                    except ValueError:
                        print("Введите число!")
                else:
                    self.player["inventory"].remove(item)
                    print(f"Вы выбросили {item['name']}")

            except ValueError:
                print("Введите число!")

        elif choice == "4":
            pass
        else:
            print("Некорректный выбор!")


    def add_item(self, item_id: str, name: str, item_type: str, description: str = ""):
        existing_item = next((i for i in self.player["inventory"] if i["id"] == item_id), None)
        if existing_item:
            existing_item["count"] += 1
        else:
            self.player["inventory"].append({
                "id": item_id,
                "name": name,
                "type": item_type,
                "count": 1,
                "description": description
            })
        print(f"Вы получили: {name}")


    def equip_weapon(self):
        weapons = [
            i for i in self.player["inventory"]
            if i["id"] in self.weapons
        ]
        if not weapons:
            print("Нет оружия в инвентаре.")
            return

        if self.player["equipment"]["weapon"] != "None":
            print("Уже экипировано оружие. Сначала снимите текущее.")
            return

        print("\n=== Доступное оружие ===")
        for i, item in enumerate(weapons):
            weapon_data = self.weapons[item["id"]]
            print(f"{i+1}. {weapon_data['name']} (Урон: {weapon_data['damage']})")

        try:
            choice = int(input("Выберите оружие (номер, 0 — отмена): ")) - 1
            if choice == -1:
                print("Действие отменено.")
                return
            if 0 <= choice < len(weapons):
                selected_item = weapons[choice]
                self.player["inventory"].remove(selected_item)
                self.player["equipment"]["weapon"] = selected_item["id"]
                self.player["damage"] = (self.player["stats"]["strength"] + self.get_weapon_damage())
                print(f"Экипировано оружие: {self.weapons[selected_item['id']]['name']}")
            else:
                print("Неверный номер.")
        except ValueError:
            print("Введите число.")


    def equip_armor(self):
        armors = [
            i for i in self.player["inventory"]
            if i["id"] in self.armors
        ]
        if not armors:
            print("Нет брони в инвентаре.")
            return

        if self.player["equipment"]["armor"] != "None":
            print("Уже экипирована броня. Сначала снимите текущую.")
            return

        print("\n=== Доступная броня ===")
        for i, item in enumerate(armors):
            armor_data = self.armors[item["id"]]
            print(f"{i+1}. {armor_data['name']} (Защита: {armor_data['defense']})")

        try:
            choice = int(input("Выберите броню (номер, 0 — отмена): ")) - 1
            if choice == -1:
                print("Действие отменено.")
                return
            if 0 <= choice < len(armors):
                selected_item = armors[choice]
                self.player["inventory"].remove(selected_item)
                self.player["equipment"]["armor"] = selected_item["id"]
                self.player["armor"] = self.armors[selected_item["id"]]["defense"]
                print(f"Экипирована броня: {self.armors[selected_item['id']]['name']}")
            else:
                print("Неверный номер.")
        except ValueError:
            print("Введите число.")


    def unequip(self):
        print("\n=== Снятие экипировки ===")
        print("1. Снять оружие")
        print("2. Снять броню")
        choice = input("\n> ").strip()

        if choice == "1":
            weapon_id = self.player["equipment"]["weapon"]
            if weapon_id != "None":
                weapon_data = self.weapons[weapon_id]
                self.add_item(weapon_id, weapon_data["name"], "weapon")
                self.player["equipment"]["weapon"] = "None"
                self.player["damage"] = (self.player["stats"]["strength"] + self.get_weapon_damage())
                print(f"Вы сняли {weapon_data['name']}. Урон изменён.")
            else:
                print("Нет экипированного оружия")

        elif choice == "2":
            armor_id = self.player["equipment"]["armor"]
            if armor_id != "None":
                armor_data = self.armors[armor_id]
                self.add_item(armor_id, armor_data["name"], "armor")
                self.player["equipment"]["armor"] = "None"
                self.update_armor_from_defense()
                print(f"Вы сняли {armor_data['name']}. Защита изменена.")
            else:
                print("Нет экипированной брони")
        else:
            print("Неверный выбор! Используйте 1 или 2.")

    def save_game(self):
        save_data = {
            "player": self.player,
            "current_room": self.current_room,
            "current_floor": self.current_floor,
            "rooms_visited": self.rooms_visited,
            "game_over": self.game_over,
            "monsters": [
                {
                    "id": m["id"],
                    "name": m["name"],
                    "level": m["level"],
                    "health": m["health"],
                    "maxHealth": m["maxHealth"],
                    "attack": m["attack"],
                    "defense": m["defense"],
                    "experience": m["experience"],
                    "goldDrop": m["goldDrop"],
                    "itemsDrop": m["itemsDrop"],
                    "location": m["location"]
                }
                for m in self.monsters
            ]
        }

        try:
            with open(os.path.join("data", "Saves.json"), "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            print("Игра сохранена в data/Saves.json")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def load_game(self):
        save_path = os.path.join("data", "Saves.json")

        if not os.path.exists(save_path):
            print("Файл сохранения не найден: data/Saves.json")
            return

        try:
            with open(save_path, "r", encoding="utf-8") as f:
                save_data = json.load(f)

            self.player = save_data["player"]
            self.current_room = save_data["current_room"]
            self.current_floor = save_data["current_floor"]
            self.rooms_visited = save_data["rooms_visited"]
            self.game_over = save_data["game_over"]

            self.monsters = []
            for m_data in save_data["monsters"]:
                monster = {
                    "id": m_data["id"],
                    "name": m_data["name"],
                    "level": m_data["level"],
                    "health": m_data["health"],
                    "maxHealth": m_data["maxHealth"],
                    "attack": m_data["attack"],
                    "defense": m_data["defense"],
                    "experience": m_data["experience"],
                    "goldDrop": m_data["goldDrop"],
                    "itemsDrop": m_data["itemsDrop"],
                    "location": m_data["location"]
                }
                self.monsters.append(monster)

            print("Игра загружена из data/Saves.json")
        except json.JSONDecodeError:
            print("Ошибка: файл сохранения повреждён (некорректный JSON).")
        except KeyError as e:
            print(f"Ошибка: отсутствует поле в сохранении: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке: {e}")



    def main_loop(self):
        self.create_character()
        while not self.game_over:
            print("\n=== Меню выбора ===")
            print("1. Войти в комнату")
            print("2. Посмотреть статус персонажа")
            print("3. Посмотреть инвентарь")
            print("4. Экипировать оружие")
            print("5. Экипировать броню")
            print("6. Снять экипировку")
            print("7. Сохранить игру")
            print("8. Загрузить игру")
            print("9. Выйти из игры")

            try:
                choice = input("\n> ").strip()

                if choice == "1":
                    self.enter_room()
                elif choice == "2":
                    self.show_status()
                elif choice == "3":
                    self.show_inventory()
                elif choice == "4":
                    self.equip_weapon()
                elif choice == "5":
                    self.equip_armor()
                elif choice == "6":
                    self.unequip()
                elif choice == "7":
                    self.save_game()
                elif choice == "8":
                    self.load_game()
                elif choice == "9":
                    print("Закрытие игры")
                    break
                else:
                    print("Неверное действие. Введите число от 1 до 9.")

            except KeyboardInterrupt:
                print("\nИгра прервана пользователем.")
                break
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")

        if self.game_over:
            print("\n=== Игра окончена ===")


if __name__ == "__main__":
    game = Game()
    game.main_loop()

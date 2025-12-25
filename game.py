import os
import random
import keyboard
import msvcrt

from IPython.lib.pretty import Printable


class Game:
    # Handles the main game loop and turn system

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.player.enemy = self.enemy  # Link player to enemy

    def print_state(self):
        # Clears the screen and prints current game stats
        os.system("cls")
        print("\033[2J", end="")

        print(
            f"""========================
Player:
    HP: {self.player.current_hp}
    Weapon: {self.player.current_weapon}
    Attack: {self.player.attack_power}
----------------------                      
Enemy:
    HP: {self.enemy.current_hp}
    Attack: {self.enemy.attack_power}
========================""")

    def choose_action(self):
        # Displays available player actions and gets input
        print("Please choose an action:")
        for i in self.player.actions:
            print(f"\t{i}: {self.player.actions[i].__name__.replace("_", " ").title()}")

        return int(input())

    def take_turn(self):
        # Player acts first, then enemy performs a random action
        choice = self.choose_action()
        self.player.actions[choice]()
        random.choice(self.enemy.actions)()
        print(f"Player chooses to {self.player.actions[choice].__name__.replace("_", " ").title()}")

    def start_game(self):
        # Main game loop
        while self.player.status == "Alive" and self.enemy.status == "Alive":
            self.print_state()
            self.take_turn()
            keyboard.read_event()  # Wait for keypress
            msvcrt.getch()

        self.print_state()
        print("Game Over")


class Item:
    # Base class for all items

    def __init__(self, name, classname):
        self.name = name
        self.classname = classname


class Weapon(Item):
    # Base weapon class with damage multiplier

    def __init__(self, dmg_multiplier, name):
        super().__init__(name, "Weapon")
        self.dmg_multiplier = dmg_multiplier


class Misc(Item):
    # Non-weapon usable items

    def __init__(self, name):
        super().__init__(name, "Misc")


class Sword(Weapon):
    # Specific weapon implementation

    def __init__(self):
        super().__init__(2, "Sword")

    def swing(self, player_attack_power):
        # Calculates sword damage
        print(self.dmg_multiplier * player_attack_power)
        return self.dmg_multiplier * player_attack_power

    def __str__(self):
        return "Sword"

    def __repr__(self):
        return self.__str__()


class Player:
    # Player stats, inventory, and actions

    def __init__(self):
        self.max_hp = 30
        self.current_hp = 30
        self.attack_power = 7
        self.current_weapon = None
        self.status = "Alive"
        self.enemy = None

        self.actions = {1: self.attack, 2: self.heal, 3: self.block}
        self.blocking = False

        self.items = {"Weapons": {}, "Misc": {}}

    def dmg_done(self):
        # Calculates outgoing damage
        if self.current_weapon is not None:
            return self.current_weapon.dmg_multiplier * self.attack_power
        return self.attack_power

    def decrease_hp(self, damage: int):
        # Reduces HP and checks death
        self.current_hp -= damage
        if self.current_hp < 1:
            self.status = "Dead"
            print("GG")

    def get_attacked(self, damage):
        # Handles incoming damage and blocking
        if self.blocking:
            damage = int(damage / 2)
            self.decrease_hp(damage)
            self.blocking = False
            return

        self.decrease_hp(damage)

    def increase_hp(self, healing: int):
        # Restores HP without exceeding max
        self.current_hp += healing
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def heal(self, amount=9):
        # Heal action
        self.increase_hp(amount)

    def equip_weapon(self, weapon: Weapon):
        # Directly equips a weapon
        self.current_weapon = weapon

    def attack(self):
        # Attacks the enemy
        self.enemy.get_attacked(self.dmg_done())

    def block(self):
        # Reduces next incoming damage
        self.blocking = True

    def collect_item(self, item):
        # Adds items to inventory based on type
        match item.classname:
            case "Weapon":
                self.items["Weapons"][item.name] = item
            case "Misc":
                self.items["Misc"][item.name] = item

    def equip_item(self):
        # Inventory menu for equipping or using items
        misc = self.items["Misc"]
        weapons = self.items["Weapons"]

        menu = {}
        miscmenu = {}

        if weapons:
            print("Weapons: ")
            for i, weapon in enumerate(weapons.values(), start=1):
                menu[i] = weapon
                print(f"{i}: {weapon}")
        else:
            print("No weapons available")

        if misc:
            print("Misc: ")
            for i, misc_item in enumerate(misc.values(), start=1):
                miscmenu[i] = misc_item
                print(f"{i}: {misc_item}")
        else:
            print("No misc available")

        if not weapons and not misc:
            print("You have no items.")
            return

        while True:
            print("\nChoose category:")
            print("1: Weapons")
            print("2: Misc")

            category_choice = int(input("> "))

            match category_choice:
                case 1:
                    if not weapons:
                        print("No weapons to equip.")
                        continue

                    choice = int(input("Choose weapon number: > "))
                    if choice in menu:
                        self.current_weapon = menu[choice]
                        print(f"Equipped {menu[choice]}")
                        return
                    else:
                        print("Invalid weapon choice.")

                case 2:
                    if not misc:
                        print("No misc items.")
                        continue

                    choice = int(input("Choose misc item number: > "))
                    if choice in miscmenu:
                        item = miscmenu[choice]
                        print(f"Used {item}")
                        return
                    else:
                        print("Invalid misc choice.")

                case _:
                    print("Invalid category choice.")


class Enemy:
    # Base enemy class

    def __init__(self, hp: int, attack_power: int, target):
        self.current_hp = hp
        self.attack_power = attack_power
        self.actions = []
        self.target = target
        self.status = "Alive"


class Goblin(Enemy):
    # Simple enemy with only an attack action

    def __init__(self, target):
        super().__init__(30, 7, target)
        self.actions.append(self.attack)
        self.actions.append(self.block)
        self.blocking = False

    def attack(self):
        # Attacks the player
        self.target.get_attacked(self.attack_power)

    def get_attacked(self, damage):
        # Handles goblin damage
        if self.blocking:
            damage = int(damage / 2)
            self.current_hp -= damage
            self.blocking = False

        else:
            self.current_hp -= damage

        if self.current_hp < 1:
            self.current_hp = 0
            self.status = "Dead"

    def block(self):
        # Reduces next incoming damage
        self.blocking = True


if __name__ == "__main__":
    # Basic inventory test
    player = Player()
    player.collect_item(Sword())
    player.equip_item()
    print(player.current_weapon)
    print(player.dmg_done())


        
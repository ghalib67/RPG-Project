import os
import random
import keyboard
import msvcrt
import time


class Game:
    # Handles the main game loop and turn system

    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.choose_enemy()  # Select first enemy at start
        self.player.enemy = self.enemy  # Link player to enemy

    def countdown(self, timer):
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)

    def take_turn(self):
        # Player acts first, then enemy performs a random action
        choice = self.choose_action()
        print(f"Player chooses to {self.player.actions[choice].__name__.replace("_", " ").title()}")
        self.player.actions[choice]()
        # Only allow enemy to act if still alive

        if self.enemy.status == "Alive":
            random.choice(self.enemy.actions)()

    def print_start(self):
        # Display game start message
        print("The game is starting...")
        print(f"The current enemy is {self.enemy}!")
        print("FIGHT!")
        self.countdown(3)

    def enemy_defeated(self):
        # Handle enemy defeat and select next enemy
        print(f"You defeated {self.enemy}")
        self.choose_enemy()
        self.player.enemy = self.enemy
        print(f"The next enemy is {self.enemy}\nGet Ready!")
        self.countdown(3)

    def print_state(self):
        # Clears the screen and prints current game stats
        os.system("cls")
        print("\033[2J", end="")

        print(
            f"""========================
Player:
    HP: {self.player.current_hp} {"🛡️" if self.player.blocking else ""}
    Weapon: {self.player.current_weapon if self.player.current_weapon is not None else "Hands (Rated E)"}
    Attack: {self.player.attack_power}
----------------------                      
{self.enemy}:
    HP: {self.enemy.current_hp} {"🛡️" if self.enemy.blocking else ""}
    Attack: {self.enemy.attack_power}
========================""")

    def choose_action(self):
        # Displays available player actions and gets input
        print("Please choose an action:")
        for i in self.player.actions:
            print(f"\t{i}: {self.player.actions[i].__name__.replace("_", " ").title()}")

        while True:
            try:
                choice = int(input("> "))
                if choice in self.player.actions:
                    return choice
                else:
                    self.print_state()
                    print(f"Invalid choice. Choose from: {list(self.player.actions.keys())}")
            except ValueError:
                self.print_state()
                print("Please enter a valid number.")

    def start_game(self):
        self.print_start()

        # Main game loop - continues while player is alive and enemies remain
        while self.player.status == "Alive":
            # Combat loop for current enemy
            while self.player.status == "Alive" and self.enemy.status == "Alive":
                self.print_state()
                self.take_turn()
                keyboard.read_event()  # Wait for keypress
                msvcrt.getch()

            # Check if player died
            if self.player.status == "Dead":
                break

            # Enemy is dead - check if more enemies exist
            if len(self.enemies) > 0:
                self.enemy_defeated()
            else:
                # No more enemies - player wins!
                break

        # Display final game state and result
        self.print_state()
        if self.player.status == "Alive":
            print("Victory! You defeated all enemies!")
        else:
            print("Game Over - You died!")

    def choose_enemy(self):
        # Randomly select and remove an enemy from the list
        self.enemy = random.choice(self.enemies)
        self.enemies.remove(self.enemy)

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
        # Calculates outgoing damage with weapon multiplier
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
        # Handles incoming damage with blocking reduction
        if self.blocking:
            damage = int(damage / 2)
            self.decrease_hp(damage)
            self.blocking = False  # Reset block after use
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
        damage = self.dmg_done()
        block = self.enemy.blocking
        self.enemy.get_attacked(self.dmg_done())

        if block:
            print(f"The enemy was blocking! you only did {damage//2} damage!")

        else:
            print(f"A clean hit! Did {damage} damage!")

    def block(self):
        # Reduces next incoming damage by half
        self.blocking = True

    def collect_item(self, item):
        # Adds items to inventory based on type
        match item.classname:
            case "Weapon":
                self.items["Weapons"][item.name] = item
            case "Misc":
                self.items["Misc"][item.name] = item

    def equip_item(self):
        misc = self.items["Misc"]
        weapons = self.items["Weapons"]

        menu = {}
        miscmenu = {}

        # Display weapons
        if weapons:
            print("Weapons: ")
            for i, weapon in enumerate(weapons.values(), start=1):
                menu[i] = weapon
                print(f"{i}: {weapon}")
        else:
            print("No weapons available")

        # Display misc
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
            print("0: Cancel")

            try:
                category_choice = int(input("> "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            match category_choice:
                case 0:
                    print("Cancelled.")
                    return

                case 1:
                    if not weapons:
                        print("No weapons to equip.")
                        continue

                    try:
                        choice = int(input("Choose weapon number (0 to cancel): > "))
                        if choice == 0:
                            continue
                        if choice in menu:
                            self.current_weapon = menu[choice]
                            print(f"Equipped {menu[choice]}")
                            return
                        else:
                            print(f"Invalid choice. Choose from: {list(menu.keys())}")
                    except ValueError:
                        print("Please enter a valid number.")

                case 2:
                    if not misc:
                        print("No misc items.")
                        continue

                    try:
                        choice = int(input("Choose misc item number (0 to cancel): > "))
                        if choice == 0:
                            continue
                        if choice in miscmenu:
                            item = miscmenu[choice]
                            print(f"Used {item}")
                            return
                        else:
                            print(f"Invalid choice. Choose from: {list(miscmenu.keys())}")
                    except ValueError:
                        print("Please enter a valid number.")

                case _:
                    print("Invalid category. Choose 1, 2, or 0.")

class Enemy:
    # Base enemy class

    def __init__(self, hp: int, attack_power: int, target):
        self.current_hp = hp
        self.attack_power = attack_power
        self.actions = []
        self.target = target
        self.status = "Alive"


class Goblin(Enemy):
    # Goblin enemy with attack and block abilities

    def __init__(self, target):
        super().__init__(30, 7, target)
        self.actions.append(self.attack)
        self.actions.append(self.block)
        self.blocking = False

    def attack(self):
        damage = self.attack_power
        block = self.target.blocking
        self.target.get_attacked(self.attack_power)

        if block:
            print(f"You were blocking! The enemy only did {damage // 2} damage.")

        else:
            print(f"The enemy got a clean hit: {damage} damage.")

    def get_attacked(self, damage):
        # Handles incoming damage with blocking reduction
        if self.blocking:
            damage = int(damage / 2)
            self.current_hp -= damage
            self.blocking = False  # Reset block after use

        else:
            self.current_hp -= damage

        # Check for death
        if self.current_hp < 1:
            self.current_hp = 0
            self.status = "Dead"

    def block(self):
        # Reduces next incoming damage by half
        self.blocking = True

    def __str__(self):
        return "Goblin"

class Zombie(Enemy):
    # Zombie enemy with high HP and low attack

    def __init__(self, target):
        super().__init__(50, 2, target)
        self.actions.append(self.attack)
        self.actions.append(self.block)
        self.blocking = False

    def attack(self):
        # Attacks the player
        damage = self.attack_power
        block = self.target.blocking
        self.target.get_attacked(self.attack_power)

        if block:
            print(f"You were blocking! The enemy only did {damage // 2} damage.")

        else:
            print(f"The enemy got a clean hit: {damage} damage.")

    def get_attacked(self, damage):
        # Handles incoming damage with blocking reduction
        if self.blocking:
            damage = int(damage / 2)
            self.current_hp -= damage
            self.blocking = False  # Reset block after use

        else:
            self.current_hp -= damage

        # Check for death
        if self.current_hp < 1:
            self.current_hp = 0
            self.status = "Dead"

    def block(self):
        # Reduces next incoming damage by half
        self.blocking = True

    def __str__(self):
        return "Zombie"

if __name__ == "__main__":
    # Initialize game with player and enemies
    player = Player()
    enemy = Goblin(player)
    enemy2 = Zombie(player)
    enemies = [enemy, enemy2]
    game = Game(player, enemies)
    game.start_game()


        
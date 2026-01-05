import os
import random
import msvcrt
import time


class Game:
    def __init__(self, player):
        self.player = player
        self.current_room = 1
        self.max_rooms = 5
        self.enemy = None

    def countdown(self, timer):
        for i in range(timer, 0, -1):
            print(i)
            time.sleep(1)

    def spawn_enemy(self):
        """Spawns enemy based on current room"""
        if self.current_room == 5:
            # Boss room
            print("\n" + "=" * 50)
            print("💀 A MASSIVE BERSERKER CHAMPION BLOCKS YOUR PATH! 💀")
            print("=" * 50)
            self.enemy = Berserker(self.player)
            # Make boss much stronger
            self.enemy.current_hp = 80
            self.enemy.max_hp = 80
            self.enemy.attack_power = 12
        else:
            # Regular rooms - random enemy, gets slightly stronger each room
            enemy_types = [Goblin, Zombie, Berserker]
            enemy_class = random.choice(enemy_types)
            self.enemy = enemy_class(self.player)
            
            # Scale enemy stats with room number
            hp_boost = (self.current_room - 1) * 5
            atk_boost = (self.current_room - 1) * 2
            self.enemy.current_hp += hp_boost
            self.enemy.max_hp = self.enemy.current_hp
            self.enemy.attack_power += atk_boost
            
            print(f"\n⚔️ A {self.enemy} appears!")
        
        self.player.enemy = self.enemy

    def get_room_reward(self):
        """Gives player an item based on current room"""
        # Define reward pool
        all_rewards = [
            Sword(self.player),
            Axe(self.player),
            Dagger(self.player),
            HealthPotion(),
            StrengthPotion(),
            MaxHPPotion()
        ]
        
        # Give guaranteed weapon in room 1, then random
        if self.current_room == 1:
            item = Sword(self.player)
        else:
            item = random.choice(all_rewards)
        
        print(f"\n✨ You found: {item}! ✨")
        self.player.collect_item(item)
        print("(Item added to inventory)")
        time.sleep(2)

    def show_room_intro(self):
        """Display room atmosphere and description"""
        descriptions = {
            1: "🚪 You enter a dimly lit corridor.\n   Torches flicker on the walls. Something moves in the shadows...",
            2: "💀 The smell of decay fills this dank chamber.\n   Ancient bones litter the floor. You hear groaning ahead...",
            3: "⚔️ You step into what was once an armory.\n   Rusted weapons hang on the walls. A figure emerges from the darkness...",
            4: "🔮 Strange runes glow faintly on the stone walls.\n   The air crackles with dark magic. You sense great danger...",
            5: "🏰 A massive chamber opens before you.\n   The final guardian awaits. This is your last battle..."
        }
        
        os.system("cls")
        print("\n" + "=" * 60)
        print(f"   ROOM {self.current_room}/{self.max_rooms}")
        print("=" * 60)
        print(f"\n{descriptions[self.current_room]}\n")
        time.sleep(3)

    def take_turn(self):
        """Single turn of combat"""
        while True:
            choice = self.player.choose_action()

            if choice not in self.player.actions:
                print("Invalid choice.")
                time.sleep(1)
                self.print_state()
                continue

            action = self.player.actions[choice]
            self.print_state()
            print(f"\nPlayer chooses to {action.__name__.replace('_', ' ').title()}")
            print("-" * 40)
            end_turn = action()

            if end_turn:
                break

        # Enemy attacks if still alive
        if self.enemy.status == "Alive":
            print("\n" + "=" * 40)
            print("Enemy's turn:")
            print("=" * 40)
            random.choice(self.enemy.actions)()
            time.sleep(1.5)

    def print_state(self):
        """Display current game state"""
        os.system("cls")
        
        # Room info
        print("=" * 60)
        if self.current_room == 5:
            print("        🔥 BOSS ROOM - FINAL BATTLE 🔥")
        else:
            print(f"        ROOM {self.current_room}/{self.max_rooms}")
        print("=" * 60)
        
        # Player stats with HP bar
        player_hp_percent = self.player.current_hp / self.player.max_hp
        player_hp_blocks = int(player_hp_percent * 20)
        player_hp_bar = "█" * player_hp_blocks + "░" * (20 - player_hp_blocks)
        
        print(f"\n👤 PLAYER:")
        print(f"   HP: {self.player.current_hp}/{self.player.max_hp}")
        print(f"   [{player_hp_bar}] {int(player_hp_percent * 100)}%")
        if self.player.blocking:
            print("   🛡️ BLOCKING")
        print(f"   Weapon: {self.player.current_weapon if self.player.current_weapon else 'Fists'}")
        print(f"   Attack: {self.player.attack_power}")
        
        print("\n" + "-" * 60)
        
        # Enemy stats with HP bar
        if self.enemy:
            enemy_hp_percent = self.enemy.current_hp / self.enemy.max_hp
            enemy_hp_blocks = int(enemy_hp_percent * 20)
            enemy_hp_bar = "█" * enemy_hp_blocks + "░" * (20 - enemy_hp_blocks)
            
            print(f"\n👹 {self.enemy.name.upper()}:")
            print(f"   HP: {self.enemy.current_hp}/{self.enemy.max_hp}")
            print(f"   [{enemy_hp_bar}] {int(enemy_hp_percent * 100)}%")
            if self.enemy.blocking:
                print("   🛡️ BLOCKING")
            print(f"   Attack: {self.enemy.attack_power}")
        
        print("\n" + "=" * 60 + "\n")

    def start_game(self):
        """Main game loop"""
        # Intro
        os.system("cls")
        print("\n" + "=" * 60)
        print("          🏰 DUNGEON CRAWLER ROGUELIKE 🏰")
        print("=" * 60)
        print("\n  Venture through 5 deadly rooms to escape the dungeon!")
        print("  Defeat enemies, collect weapons, and survive the final boss!")
        print("\n" + "=" * 60)
        input("\nPress ENTER to begin your journey...")

        # Room loop
        while self.current_room <= self.max_rooms and self.player.status == "Alive":
            # Show room intro
            self.show_room_intro()
            
            # Spawn enemy
            self.spawn_enemy()
            print("\nPrepare for battle!")
            self.countdown(3)

            # Combat loop
            while self.player.status == "Alive" and self.enemy.status == "Alive":
                self.print_state()
                self.take_turn()
                print("\nPress any key to continue...")
                msvcrt.getch()

            # Check if player died
            if self.player.status == "Dead":
                break

            # Enemy defeated
            os.system("cls")
            print("\n" + "=" * 60)
            print(f"✅ {self.enemy.name} DEFEATED!")
            print("=" * 60)
            
            # Give reward (except after final boss)
            if self.current_room < self.max_rooms:
                self.get_room_reward()
                print("\nPress ENTER to continue to the next room...")
                input()
            
            # Move to next room
            self.current_room += 1

        # Game over - show results
        os.system("cls")
        print("\n" + "=" * 60)
        
        if self.player.status == "Alive":
            print("        🎉 VICTORY! YOU ESCAPED THE DUNGEON! 🎉")
            print("\n  You have proven yourself a true dungeon crawler!")
        else:
            print("           💀 GAME OVER 💀")
            print(f"\n  You fell in Room {self.current_room}")
            print("  Better luck next time, adventurer...")
        
        print("=" * 60)
        print(f"\nFinal Stats:")
        print(f"  Rooms Cleared: {self.current_room - 1}/{self.max_rooms}")
        print(f"  Final HP: {max(0, self.player.current_hp)}/{self.player.max_hp}")
        print(f"  Final Attack: {self.player.attack_power}")
        print("=" * 60 + "\n")


class Item:
    def __init__(self, name, classname):
        self.name = name
        self.classname = classname


class Weapon(Item):
    def __init__(self, dmg_multiplier, name, player):
        super().__init__(name, "Weapon")
        self.dmg_multiplier = dmg_multiplier
        self.actions = []
        self.player = player


class Misc(Item):
    def __init__(self, name):
        super().__init__(name, "Misc")


class Sword(Weapon):
    def __init__(self, player):
        super().__init__(2, "Sword", player)
        self.actions = [self.slash]

    def slash(self):
        damage = int(self.dmg_multiplier * self.player.attack_power + random.randint(1, 8))
        block = self.player.enemy.blocking
        self.player.enemy.get_attacked(damage)

        if block:
            print(f"⚔️ SLASH! Enemy blocked! Only {damage // 2} damage!")
        else:
            print(f"⚔️ POWERFUL SLASH! {damage} damage!")
        return True

    def __str__(self):
        return "⚔️ Sword (2x damage)"


class Axe(Weapon):
    def __init__(self, player):
        super().__init__(2.5, "Axe", player)
        self.actions = [self.heavy_chop]

    def heavy_chop(self):
        damage = int(self.dmg_multiplier * self.player.attack_power * 1.3)
        self.player.enemy.get_attacked(damage)
        print(f"🪓 HEAVY CHOP! {damage} damage!")
        self.player.decrease_hp(3)
        print("The massive swing exhausted you! -3 HP")
        return True

    def __str__(self):
        return "🪓 Axe (2.5x damage, costs 3 HP)"


class Dagger(Weapon):
    def __init__(self, player):
        super().__init__(1.5, "Dagger", player)
        self.actions = [self.quick_stab, self.backstab]

    def quick_stab(self):
        damage = int(self.dmg_multiplier * self.player.attack_power)
        self.player.enemy.get_attacked(damage)
        print(f"🗡️ QUICK STAB! {damage} damage!")
        return True

    def backstab(self):
        if self.player.enemy.blocking:
            print("❌ BACKSTAB FAILED! Enemy was ready!")
            return True
        
        damage = int(self.dmg_multiplier * self.player.attack_power * 2.5)
        self.player.enemy.get_attacked(damage)
        print(f"💀 CRITICAL BACKSTAB! {damage} damage!")
        return True

    def __str__(self):
        return "🗡️ Dagger (1.5x, Quick Stab + Backstab)"


class HealthPotion(Misc):
    def __init__(self):
        super().__init__("Health Potion")
        self.heal_amount = 20

    def use(self, player):
        player.increase_hp(self.heal_amount)
        print(f"🧪 Used Health Potion! Restored {self.heal_amount} HP!")
        return True

    def __str__(self):
        return f"🧪 Health Potion (+{self.heal_amount} HP)"


class StrengthPotion(Misc):
    def __init__(self):
        super().__init__("Strength Potion")

    def use(self, player):
        boost = 5
        player.attack_power += boost
        print(f"💪 Used Strength Potion! Attack +{boost} (now {player.attack_power})!")
        return True

    def __str__(self):
        return "💪 Strength Potion (+5 Attack)"


class MaxHPPotion(Misc):
    def __init__(self):
        super().__init__("Max HP Potion")

    def use(self, player):
        boost = 15
        player.max_hp += boost
        player.current_hp += boost
        print(f"❤️ Used Max HP Potion! Max HP +{boost} (now {player.max_hp})!")
        return True

    def __str__(self):
        return "❤️ Max HP Potion (+15 Max HP)"


class Player:
    def __init__(self):
        self.max_hp = 50
        self.current_hp = 50
        self.attack_power = 10
        self.current_weapon = None
        self.status = "Alive"
        self.enemy = None
        self.base_actions = {1: self.attack, 2: self.heal, 3: self.block, 4: self.equip_item}
        self.actions = self.base_actions.copy()
        self.blocking = False
        self.items = {"Weapons": {}, "Misc": {}}

    def dmg_done(self):
        if self.current_weapon is not None:
            return int(self.current_weapon.dmg_multiplier * self.attack_power)
        return self.attack_power

    def decrease_hp(self, damage: int):
        self.current_hp -= damage
        if self.current_hp < 1:
            self.status = "Dead"

    def get_attacked(self, damage):
        if self.blocking:
            damage = int(damage / 2)
            self.decrease_hp(damage)
            self.blocking = False
            return
        self.decrease_hp(damage)

    def increase_hp(self, healing: int):
        self.current_hp += healing
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def heal(self, amount=15):
        self.increase_hp(amount)
        print(f"💚 Healed for {amount} HP!")
        return True

    def equip_weapon(self, weapon: Weapon):
        self.current_weapon = weapon
        self.actions = self.base_actions.copy()
        next_key = len(self.base_actions) + 1
        for skill in self.current_weapon.actions:
            self.actions[next_key] = skill
            next_key += 1

    def attack(self):
        damage = self.dmg_done()
        block = self.enemy.blocking
        self.enemy.get_attacked(damage)

        if block:
            print(f"👊 Attack! Enemy blocked! Only {damage // 2} damage!")
        else:
            print(f"👊 Clean hit! {damage} damage!")
        return True

    def block(self):
        self.blocking = True
        print("🛡️ You brace for impact! Next attack damage halved!")
        return True

    def collect_item(self, item):
        match item.classname:
            case "Weapon":
                self.items["Weapons"][item.name] = item
            case "Misc":
                self.items["Misc"][item.name] = item

    def equip_item(self):
        misc = self.items["Misc"]
        weapons = self.items["Weapons"]

        if not weapons and not misc:
            print("❌ You have no items!")
            time.sleep(1)
            return False

        print("\n📦 INVENTORY:")
        print("-" * 40)
        
        menu = {}
        miscmenu = {}

        if weapons:
            print("\n⚔️ WEAPONS:")
            for i, weapon in enumerate(weapons.values(), start=1):
                menu[i] = weapon
                print(f"  {i}. {weapon}")

        if misc:
            print("\n🧪 CONSUMABLES:")
            for i, misc_item in enumerate(misc.values(), start=1):
                miscmenu[i] = misc_item
                print(f"  {i}. {misc_item}")

        print("\n-" * 40)
        print("\nChoose category:")
        print("  1: Equip Weapon")
        print("  2: Use Consumable")
        print("  0: Cancel")

        while True:
            try:
                category_choice = int(input("\n> "))
            except ValueError:
                print("❌ Enter a valid number.")
                continue

            if category_choice == 0:
                return False
            elif category_choice == 1:
                if not weapons:
                    print("❌ No weapons available!")
                    continue
                try:
                    choice = int(input("\nChoose weapon (0 to cancel): "))
                    if choice == 0:
                        continue
                    if choice in menu:
                        self.equip_weapon(menu[choice])
                        print(f"✅ Equipped {menu[choice].name}!")
                        time.sleep(1)
                        return False
                except ValueError:
                    print("❌ Enter a valid number.")
            elif category_choice == 2:
                if not misc:
                    print("❌ No consumables available!")
                    continue
                try:
                    choice = int(input("\nChoose item (0 to cancel): "))
                    if choice == 0:
                        continue
                    if choice in miscmenu:
                        item = miscmenu[choice]
                        if hasattr(item, 'use'):
                            item.use(self)
                            del self.items["Misc"][item.name]
                        time.sleep(1)
                        return False
                except ValueError:
                    print("❌ Enter a valid number.")
            else:
                print("❌ Invalid choice!")

    def choose_action(self):
        print("⚡ ACTIONS:")
        for i in self.actions:
            action_name = self.actions[i].__name__.replace("_", " ").title()
            print(f"  {i}. {action_name}")

        while True:
            try:
                choice = int(input("\n> "))
                return choice
            except ValueError:
                print("❌ Enter a valid number.")


class Enemy:
    def __init__(self, hp: int, attack_power: int, target, name: str):
        self.current_hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.actions = []
        self.target = target
        self.status = "Alive"
        self.name = name
        self.blocking = False


class Goblin(Enemy):
    def __init__(self, target):
        super().__init__(25, 6, target, "Goblin")
        self.actions = [self.attack, self.block]

    def attack(self):
        damage = self.attack_power
        block = self.target.blocking
        self.target.get_attacked(self.attack_power)

        if block:
            print(f"Goblin attacks! You blocked! Only {damage // 2} damage taken.")
        else:
            print(f"Goblin slashes you! {damage} damage taken!")

    def get_attacked(self, damage):
        if self.blocking:
            damage = int(damage / 2)
            self.blocking = False
        self.current_hp -= damage
        if self.current_hp < 1:
            self.current_hp = 0
            self.status = "Dead"

    def block(self):
        self.blocking = True
        print("Goblin raises its shield!")

    def __str__(self):
        return "Goblin"


class Zombie(Enemy):
    def __init__(self, target):
        super().__init__(40, 4, target, "Zombie")
        self.actions = [self.attack, self.block]

    def attack(self):
        damage = self.attack_power
        block = self.target.blocking
        self.target.get_attacked(self.attack_power)

        if block:
            print(f"Zombie lunges! You blocked! Only {damage // 2} damage taken.")
        else:
            print(f"Zombie bites you! {damage} damage taken!")

    def get_attacked(self, damage):
        if self.blocking:
            damage = int(damage / 2)
            self.blocking = False
        self.current_hp -= damage
        if self.current_hp < 1:
            self.current_hp = 0
            self.status = "Dead"

    def block(self):
        self.blocking = True
        print("Zombie braces itself!")

    def __str__(self):
        return "Zombie"


class Berserker(Enemy):
    def __init__(self, target):
        super().__init__(35, 8, target, "Berserker")
        self.actions = [self.attack, self.rage_attack]

    def attack(self):
        damage = self.attack_power
        block = self.target.blocking
        self.target.get_attacked(self.attack_power)

        if block:
            print(f"Berserker attacks! You blocked! Only {damage // 2} damage taken.")
        else:
            print(f"Berserker strikes hard! {damage} damage taken!")

    def rage_attack(self):
        hp_percent = self.current_hp / self.max_hp
        if hp_percent <= 0.5:
            damage = int(self.attack_power * 1.8)
            print("💢 BERSERKER ENTERS RAGE MODE!")
        else:
            damage = self.attack_power
        
        self.target.get_attacked(damage)
        print(f"Berserker attacks furiously! {damage} damage taken!")

    def get_attacked(self, damage):
        if self.blocking:
            damage = int(damage / 2)
            self.blocking = False
        self.current_hp -= damage
        if self.current_hp < 1:
            self.current_hp = 0
            self.status = "Dead"

    def __str__(self):
        return "Berserker"


if __name__ == "__main__":
    player = Player()
    game = Game(player)
    game.start_game()

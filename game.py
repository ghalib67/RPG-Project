import os
import random
import keyboard
import msvcrt

class Game:

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.player.enemy = self.enemy
    
    def print_state(self):
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
        print("Please choose an action:")
        for i in self.player.actions:
            print(f"\t{i}: {self.player.actions[i].__name__.replace("_", " ").title()}")
        #print(f"\t{len(self.player.actions) + 1}: Something")

        return int(input())

    def take_turn(self):
        choice = self.choose_action()
        self.player.actions[choice]()
        random.choice(self.enemy.actions)()
        print(f"Player chooses to {self.player.actions[choice].__name__.replace("_", " ").title()}")


    def start_game(self):
        while self.player.status == "Alive":
            self.print_state()
            self.take_turn()
            keyboard.read_event()
            msvcrt.getch()
        print("Game Over")

class Weapon:

    def __init__(self, dmg_multiplier):
        self.dmg_multiplier = dmg_multiplier

class Sword(Weapon):

    def __init__(self):
        super().__init__(2)

    def swing(self, player_attack_power):
        print(self.dmg_multiplier * player_attack_power)
        return self.dmg_multiplier * player_attack_power
    
    def __str__(self):
        return "SWORD!!!!!!"


class Player:
    
    def __init__(self):
        #Initializing the values "Player" class will have during the start
        self.max_hp = 30
        self.current_hp = 30
        self.attack_power = 7
        self.current_weapon = None
        self.status = "Alive"
        self.enemy = None
        self.actions = {1: self.attack, 2: self.heal, 3: self.block}
        self.blocking = False

    def dmg_done(self):#fUNTION TO BE ABLE TO CALCULATE DMG
        if self.current_weapon != None:
            return self.current_weapon.dmg_multiplier * self.attack_power
        
        else:
            return self.attack_power

    def decrease_hp(self, damage: int):#Function for Decreasing hp
        self.current_hp -= damage
        if self.current_hp < 1:
            self.status = "Dead"
            print("GG")

    def get_attacked(self, damage):
        if self.blocking == True:
            damage = int(damage / 2)
            self.decrease_hp(damage)
            self.blocking = False
            return

        self.decrease_hp(damage)

    def increase_hp(self, healing: int):#Function for Increasing hp
        self.current_hp += healing
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def heal(self,amount=9):
        self.increase_hp(amount)

    def equip_weapon(self, weapon: Weapon):
        self.current_weapon = weapon
    
    def attack(self):#Function for attacking
        self.enemy.get_attacked(self.dmg_done())

    def block(self):
        self.blocking = True

class Enemy:

    def __init__(self, hp: int, attack_power: int, target):
        self.current_hp = hp
        self.attack_power = attack_power
        self.actions = []
        self.target = target



class Goblin(Enemy):
    
    def __init__(self,target):
        super().__init__(30, 7,target)
        self.actions.append(self.attack,)

    def attack(self):
        self.target.get_attacked(self.attack_power)

    def get_attacked(self, damage):
        self.current_hp -= damage

if __name__ == "__main__":#For testing
    player = Player()
    goblin = Goblin(player)
    game = Game(player, goblin)
    game.start_game()
    player.equip_weapon(Sword())
    game.start_game()

        
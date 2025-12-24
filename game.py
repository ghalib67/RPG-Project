class Game:

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
    
    def print_state(self):
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
        return int(input(
f"""
Please choose an action:
    1. Attack
    2. Show game state
"""))
                           
    def start_game(self):
        while self.player.status == "Alive":
            self.print_state()
            choice = self.choose_action()
            match choice:
                case 1:
                    self.player.attack(self.enemy)
                    self.enemy.attack(self.player)
                
                case 2:
                    self.print_state()

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

    def incrase_hp(self, healing: int):#Function for Increasing hp
        self.current_hp += healing
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
    
    def equip_weapon(self, weapon: Weapon):
        self.current_weapon = weapon
    
    def attack(self, enemy):#Function for attacking
        enemy.current_hp -= self.dmg_done()

class Enemy:

    def __init__(self, hp: int, attack_power: int):
        self.current_hp = hp
        self.attack_power = attack_power


class Goblin(Enemy):
    
    def __init__(self):
        super().__init__(30, 7)

    def attack(self, player):
        player.decrease_hp(self.attack_power)

if __name__ == "__main__":#For testing
    player = Player()
    goblin = Goblin()
    game = Game(player, goblin)
    game.start_game()
    player.equip_weapon(Sword())
    game.start_game()
    

        
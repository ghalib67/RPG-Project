class Game:

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
    def start_game(self):
        while True:
            print("===================================")
            print(f"Player: \n HP: {self.player.current_hp}\n weapon: {self.player.current_weapon}")
            break




class Weapon:

    def __init__(self, dmg_multiplier):
        self.dmg_multiplier = dmg_multiplier

class Sword(Weapon):

    def __init__(self):
        super().__init__(2)

    def swing(self, player_attack_power):
        print(self.dmg_multiplier * player_attack_power)
        return self.dmg_multiplier * player_attack_power

class Player:
    
    def __init__(self):
        #Initializing the values "Player" class will have during the start
        self.max_hp = 30
        self.current_hp = 30
        self.attack_power = 7
        self.current_weapon = None

    def dmg_done(self):#fUNTION TO BE ABLE TO CALCULATE DMG
        if self.current_weapon != None:
            return self.current_weapon.dmg_multiplier * self.attack_power
        
        else:
            return self.attack_power

    def decrease_hp(self, damage: int):#Function for Decreasing hp
        self.current_hp -= damage
        if self.current_hp < 1:
            print("GG")

    def incrase_hp(self, healing: int):#Function for Increasing hp
        self.current_hp += healing
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
    
    def equip_weapon(self, weapon: Weapon):
        self.current_weapon = weapon
    
    def attack(self, enemy):#Function for attacking
        enemy.hp -= self.dmg_done()

class Enemy:

    def __init__(self, hp: int, attack_power: int):
        self.hp = hp
        self.attack_power = attack_power


class Goblin(Enemy):
    def __init__(self):
        super().__init__(30, 7)

    def attack(self, player):
        player.current_hp -= self.attack_power

if __name__ == "__main__":#For testing
    player = Player()
    goblin = Goblin()
    game = Game(player, goblin)
    game.start_game()

        
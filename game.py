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
    
    def attack(self):#Function for attacking
        if self.current_weapon != None:
            self.current_weapon.swing(self.attack_power)
            return self.current_weapon.swing(self.attack_power)
        
        else:
            print(self.attack_power)
            return print(self.attack_power)

class Enemy:

    def __init__(self, hp: int, attack_power: int):
        self.hp = hp
        self.attack_power = attack_power


class Goblin(Enemy):
    def __init__(self):
        super().__init__(30, 7)

if __name__ == "__main__":#For testing
    player = Player()
    player.decrease_hp(10)
    print(player.current_hp)
    player.attack()
    weapon = Sword()
    player.equip_weapon(weapon)
    player.attack()


        
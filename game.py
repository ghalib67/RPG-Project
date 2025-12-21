class Sword:
    
    def __init__(self):
        pass
    def swing(self):
        print("NO WAYYYYYYYY HE SWING ITTTT")

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
    
    def equip_weapon(self, weapon):
        self.current_weapon = weapon
    
    def attack(self):
        if self.current_weapon != None:
            self.current_weapon.swing()
        
        else:
            print("he didnt..... </3")

if __name__ == "__main__":#For testing
    player = Player()
    player.decrease_hp(10)
    print(player.current_hp)
    player.attack()
    weapon = Sword()
    player.equip_weapon(weapon)
    player.attack()


        
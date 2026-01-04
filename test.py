test = [1,2,3,4]
stuff = ['asda','asdad','asdads','afaf']
for i, j in enumerate(stuff, start=1):
    print(i,j)

from game import Enemy,Goblin,Player
player = Player()

goblin = Goblin(player)

goblin.get_attacked(40)
print(goblin.status)
goblin = Goblin(player)
print(goblin.status)
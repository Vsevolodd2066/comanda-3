class monster:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

    def die(self):
        self.health = 0
        self.xp += monster.health
        print("Убит монстр", self.name)

    def damage(self, pers):
        pers.health = pers.health - (self.damage - self.defense)

    def print_info(self):
        print("Удар:", self.damage)
        print("Здоровье:", self.health)


class Men:
    def __init__(self, name, damage, health, level, xp):
        self.level = 0
        self.xp = 0
        self.name = name
        self.damage = damage
        self.health = health

    def print_info(self):
        print("Удар:", self.damage)
        print("Здоровье:", self.health)
        print("Щит:", self.armor)

    def die(self):
        self.health = 0
        print("Персонаж", self.name, "убит!")


class pers(Men):
    def xp(self):
        self.xp = xp

    def level(self):
        self.level = self.xp%50

    def heal(self, healing):
        self.healing = self.healing + pers.level
        
    def damage(self, pers):
        pers.health = pers.health - self.damage

    def s_attack(self, pers):
        pers.h = pers.h - (self.damage*2)

# функция в которой происходит бой
# в нее передается игрок и монстр
def battle(pers, monster):
    action(pers)
    while True:
        pers.damage(monster)
        if pers.health <= 0:
            pers.die()
            return pers
        else:
            monster.damage(pers)
        if monster.health <= 0:
            monster.die()
            return monster

# функция с различными действиями
def action(pers, monster):
    option = int(input(">>>"))
    if pers.level >=0:
        print("1 - Нанести удар " + pers.damage)
        if option == 1:
            monster.health -= pers.damage
    if pers.level >=1:
        print("2 - Подлечиться " + self.healing)
        if option == 2:
            pers.h = pers.h + 5
    elif option == 3:
        pers.h = pers.h + 5
    elif option == 4:
        pers.s = True
    else:
        print("Неизвестная команда")

# Создание игрока
name = input("Имя игрока: ")

print("Приветствую вас,", pers.name, "! Приготовьтесь к путешествию!")
print("Вас ждут бои с монстрами!")
print("#########################")

# Сражения
monster1 = monster("Гоблин", 5, 25)

battle(pers, monster1)

monster2 = monster("Тролль", 10, 35)

battle(pers, monster2)

monster3 = monster("Оборотень", 20, 35)

battle(pers, monster3)

monster4 = monster("Вампир", 25, 40)

battle(pers, monster4)

# Итоги игры
print("#########################")
print("Игра завершена!")














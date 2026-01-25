from random import randint
import requests
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer 

        #self.health = self.get_health()
        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.level = randint(1, 10)       # Начальный уровень покемона от 1 до 10
        #self.feed_count = 0           # Счетчик кормлений
        self.exp = 0                  # Очки опыта
        self.last_feed_time

        self.hp = randint(70, 150)
        self.power = randint(15, 45)

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_id(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data["id"])
        else:
            return 'Pikachu'

    def get_img(self):
        pass

        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data["sprites"]["other"]["official-artwork"]["front_shiny"])
        else:
            return "https://avatars.mds.yandex.net/i?id=24fdab9701413a467bd2a25b09fbf1580fec4c1e-12637272-images-thumbs&n=13" 
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    def get_health(self):
        url = f'https://pokeapi.co/api/v2/pokemon/%7Bself.pokemon_number%7D'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Ищем статистику HP в данных покемона
            for stat in data['stats']:
                if stat['stat']['name'] == 'hp':
                    return stat['base_stat']
            return 100  # Если не найдено, возвращаем значение по умолчанию
        else:
            return 100  # Если ошибка API, возвращаем значение по умолчанию
            

    # Метод класса для получения информации
    # def info(self):
    #     return f"Имя твоего покеомона: {self.name}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
        
    # def feed(self):
    #     self.feed_count += 1
    #     self.exp += 10  # Добавляем опыт за каждое кормление
        
        # Проверяем, пора ли повышать уровень (каждые 5 кормлений)
        level_up_message = ""
        if self.feed_count % 5 == 0:
            level_up_message = "\n" + self.level_up()
            
        return f"Ты покормил {self.name} {self.feed_count} раз. Опыт: {self.exp}" + level_up_message
        
    # Метод для повышения уровня
    def level_up(self):
        self.level += 1
        # Увеличиваем здоровье при повышении уровня
        self.hp += 10
        return f"{self.name} повысил уровень до {self.level}! Здоровье увеличено до {self.hp}"
        
    def attack(self, enemy):
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            chance = randint(1,5)
            if chance == 1:
                return "Покемон-волшебник увернулся с помощью телепорта во время сражения"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()  
        delta_time = timedelte(seconds=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {current_time-delta_time}"
    
    # Метод для получения всей информации о покемоне
    def get_full_info(self):
        return f"Имя: {self.name}\nУровень: {self.level}\nЗдоровье: {self.health}\nОпыт: {self.exp}\nПокормили раз: {self.feed_count}"

    # def info(self):
    #     return f"Твоего покемона завут: {self.name}, у него {self.hp} здаровья и его сила {self.power}."



class Wizard(Pokemon):
    def feed(self):
        return super().feed(hp_increase=20)

class Fighter(Pokemon):
    def feed(self):
        return super().feed(feed_interval=10)
    def attack(self, enemy):
        super_power = randint(5,15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой:{super_power} "

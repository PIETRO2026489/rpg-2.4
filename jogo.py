import pygame
import random
import json
import os
import math

# ============================================================
# REINO DE ELEMENTARIA
# jogo.py
# ============================================================

pygame.init()

WIDTH, HEIGHT = 1100, 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reino de Elementaria")
clock = pygame.time.Clock()

# ============================================================
# CORES
# ============================================================

WHITE = (245, 245, 245)
BLACK = (15, 15, 20)
GRAY = (80, 80, 90)
DARK_GRAY = (35, 35, 45)

GREEN = (60, 190, 80)
RED = (210, 55, 55)
BLUE = (50, 130, 220)
YELLOW = (240, 210, 50)
ORANGE = (240, 120, 30)
PURPLE = (145, 70, 190)
CYAN = (50, 210, 220)
BROWN = (130, 85, 45)
ICE = (150, 225, 245)

FONT = pygame.font.SysFont("arial", 20)
SMALL = pygame.font.SysFont("arial", 16)
BIG = pygame.font.SysFont("arial", 32, bold=True)
TITLE = pygame.font.SysFont("arial", 48, bold=True)

SAVE_FILE = "elementaria_save.json"

# ============================================================
# ELEMENTOS
# ============================================================

ELEMENTS = {
    "Fogo": {
        "icon": "🔥",
        "color": ORANGE,
        "weak": ["Água"],
        "strong": ["Planta"],
        "attacks": [
            ("Brasa", 20, 25, 10, 15),
            ("Bola de Fogo", 30, 40, 15, 25),
            ("Explosão de Fogo", 45, 55, 30, 45),
        ],
    },

    "Água": {
        "icon": "💧",
        "color": BLUE,
        "weak": ["Elétrico"],
        "strong": ["Fogo"],
        "attacks": [
            ("Jato d'Água", 20, 25, 10, 15),
            ("Surfar", 30, 40, 15, 25),
            ("Hidro Bomba", 45, 55, 30, 45),
        ],
    },

    "Elétrico": {
        "icon": "⚡",
        "color": YELLOW,
        "weak": ["Planta"],
        "strong": ["Água"],
        "attacks": [
            ("Faísca", 20, 25, 10, 15),
            ("Raio", 30, 40, 15, 25),
            ("Trovoada", 45, 55, 30, 45),
        ],
    },

    "Planta": {
        "icon": "🌿",
        "color": GREEN,
        "weak": ["Fogo"],
        "strong": ["Elétrico"],
        "attacks": [
            ("Chicote de Vinha", 20, 25, 10, 15),
            ("Folha Navalha", 30, 40, 15, 25),
            ("Bomba de Sementes", 45, 55, 30, 45),
        ],
    },

    "Sombrio": {
        "icon": "🌑",
        "color": PURPLE,
        "weak": [],
        "strong": ["Fogo", "Água", "Elétrico", "Planta"],
        "attacks": [
            ("Sombra", 18, 24, 10, 15),
            ("Trevas", 30, 40, 15, 25),
            ("Abismo", 45, 60, 30, 45),
        ],
    },

    "Terra": {
        "icon": "⛰",
        "color": BROWN,
        "weak": ["Voador"],
        "strong": ["Veneno"],
        "attacks": [
            ("Pedrada", 20, 25, 10, 15),
            ("Tremor", 30, 40, 15, 25),
            ("Terremoto", 45, 55, 30, 45),
        ],
    },

    "Voador": {
        "icon": "🪽",
        "color": CYAN,
        "weak": ["Gelo"],
        "strong": ["Terra"],
        "attacks": [
            ("Rajada", 20, 25, 10, 15),
            ("Corte de Ar", 30, 40, 15, 25),
            ("Tempestade", 45, 55, 30, 45),
        ],
    },

    "Gelo": {
        "icon": "❄",
        "color": ICE,
        "weak": ["Fogo"],
        "strong": ["Voador"],
        "attacks": [
            ("Estilhaço", 20, 25, 10, 15),
            ("Lança de Gelo", 30, 40, 15, 25),
            ("Nevasca", 45, 55, 30, 45),
        ],
    },

    "Fantasma": {
        "icon": "👻",
        "color": PURPLE,
        "weak": ["Veneno"],
        "strong": ["Água", "Fogo", "Planta", "Elétrico"],
        "attacks": [
            ("Susto", 20, 25, 10, 15),
            ("Alma Sombria", 30, 40, 15, 25),
            ("Possessão", 45, 55, 30, 45),
        ],
    },

    "Veneno": {
        "icon": "☠",
        "color": GREEN,
        "weak": ["Terra"],
        "strong": ["Fantasma"],
        "attacks": [
            ("Veneno", 20, 25, 10, 15),
            ("Ácido", 30, 40, 15, 25),
            ("Explosão Tóxica", 45, 55, 30, 45),
        ],
    },
}

# ============================================================
# ILHAS
# ============================================================

ISLANDS = [
    {
        "name": "Ilha Inicial",
        "element": "Planta",
        "color": (75, 160, 80),
        "description": "A ilha onde a aventura começa.",
    },
    {
        "name": "Ilha Vulcânica",
        "element": "Fogo",
        "color": (190, 65, 35),
        "description": "Vulcões e rios de lava.",
    },
    {
        "name": "Ilha Aquática",
        "element": "Água",
        "color": (40, 130, 200),
        "description": "Uma ilha cercada por mares e corais.",
    },
    {
        "name": "Ilha Eletrônica",
        "element": "Elétrico",
        "color": (100, 100, 150),
        "description": "Fábricas e máquinas elétricas.",
    },
    {
        "name": "Ilha Sombria",
        "element": "Sombrio",
        "color": (55, 45, 70),
        "description": "Uma ilha cheia de construções abandonadas.",
    },
    {
        "name": "Ilha de Terra",
        "element": "Terra",
        "color": (145, 105, 65),
        "description": "Montanhas e terrenos rochosos.",
    },
    {
        "name": "Ilha Voadora",
        "element": "Voador",
        "color": (150, 205, 235),
        "description": "Ilhas flutuantes e muitos pássaros.",
    },
    {
        "name": "Ilha de Gelo",
        "element": "Gelo",
        "color": (165, 220, 240),
        "description": "Uma região congelada.",
    },
    {
        "name": "Ilha Fantasmagórica",
        "element": "Fantasma",
        "color": (90, 70, 110),
        "description": "Prédios abandonados habitados por fantasmas.",
    },
    {
        "name": "Ilha Venenosa",
        "element": "Veneno",
        "color": (90, 145, 65),
        "description": "Uma ilha aparentemente normal, mas cheia de cobras.",
    },
]

# ============================================================
# MONSTROS
# ============================================================

MONSTER_NAMES = {
    "Planta": ["Floragron", "Vinhante", "Sementouro"],
    "Fogo": ["Braseiro", "Lavagor", "Ignifera"],
    "Água": ["Aquanix", "Maréon", "Peixor"],
    "Elétrico": ["Voltix", "Choquim", "Eletrodrone"],
    "Sombrio": ["Sombruxo", "Trevor", "Noctus"],
    "Terra": ["Pedrano", "Terragor", "Montor"],
    "Voador": ["Aviãoz", "Penas", "Ventor"],
    "Gelo": ["Gelix", "Cristalor", "Glacius"],
    "Fantasma": ["Fantomin", "Assustor", "Espectro"],
    "Veneno": ["Serpentox", "Tóxix", "Peçonha"],
}

# ============================================================
# JOGADOR
# ============================================================

class Player:

    def __init__(self):

        self.x = 550
        self.y = 350

        self.level = 1
        self.level_xp = 0

        self.element = None
        self.element_level = 1
        self.element_xp = 0

        self.max_hp = 100
        self.hp = 100

        self.max_mana = 100
        self.mana = 100

        self.coins = 100

        self.armor = None
        self.staff = False
        self.sword = False
        self.shield = False

        self.scrolls = []

        self.monsters_defeated = 0
        self.different_monsters = set()

        self.missions = {
            "first_monster": False,
            "five_monsters": False,
            "final_boss": False,
        }

        self.unlocked_islands = 1
        self.dungeons_completed = []

    def elemental_bonus(self):

        return max(
            0,
            self.element_level - 1
        ) * 5

    def defense(self):

        if self.armor == "Armadura de Ferro":
            return 10

        if self.armor == "Armadura de Escamas":
            return 25

        return 0

    def physical_damage(self):

        if self.sword:
            return 30

        return 10

    def gain_xp(self, amount):

        self.level_xp += amount

        while self.level < 20 and self.level_xp >= 100:

            self.level_xp -= 100
            self.level += 1

            self.max_hp += 20
            self.max_mana += 20

            self.hp = self.max_hp
            self.mana = self.max_mana

    def gain_element_xp(self, amount):

        self.element_xp += amount

        while self.element_level < 5 and self.element_xp >= 100:

            self.element_xp -= 100
            self.element_level += 1

    def heal(self):

        self.hp = self.max_hp
        self.mana = self.max_mana


# ============================================================
# MONSTRO
# ============================================================

class Monster:

    def __init__(self, element, level):

        self.element = element
        self.level = level

        names = MONSTER_NAMES[element]

        self.name = random.choice(names)

        self.max_hp = 70 + level * 30
        self.hp = self.max_hp

        self.max_mana = 50 + level * 15
        self.mana = self.max_mana

        self.attack_bonus = purchased_items_count()

        self.speed = 1.2 + level * 0.15

        self.x = 0
        self.y = 0

    def damage(self):

        return random.randint(
            10 + self.level * 4 + self.attack_bonus,
            18 + self.level * 6 + self.attack_bonus
        )


# ============================================================
# ITENS
# ============================================================

SHOP_ITEMS = {
    "Armadura de Ferro": 250,
    "Armadura de Escamas": 350,
    "Cajado Arcano": 150,
    "Espada de Ferro": 200,
    "Escudo Elemental": 300,
}

POTIONS = {
    "Poção de Regeneração": 15,
    "Poção de Mana": 20,
}

owned_items = []


def purchased_items_count():

    return len(owned_items)


# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================

player = Player()

game_state = "menu"

current_island = 0

current_monster = None

battle_log = []

message = ""
message_timer = 0

# ============================================================
# CONTROLE DA MASMORRA
# ============================================================

# True enquanto o jogador estiver preso na masmorra.
dungeon_active = False

# Quantos monstros faltam no grupo atual.
dungeon_monsters_left = 3

# Quantos monstros já foram derrotados durante a expedição atual.
dungeon_total_defeated = 0

# Quantas rodadas de 3 monstros foram concluídas.
dungeon_round = 0


# ============================================================
# UTILIDADES
# ============================================================

def text(surface, value, x, y, color=WHITE, font=FONT):

    surface.blit(
        font.render(str(value), True, color),
        (x, y)
    )


def center_text(surface, value, y, color=WHITE, font=FONT):

    obj = font.render(
        str(value),
        True,
        color
    )

    surface.blit(
        obj,
        ((WIDTH - obj.get_width()) // 2, y)
    )


def show_message(msg, seconds=3):

    global message
    global message_timer

    message = msg
    message_timer = seconds * FPS


def draw_bar(
    x,
    y,
    width,
    height,
    value,
    maximum,
    color
):

    pygame.draw.rect(
        screen,
        DARK_GRAY,
        (x, y, width, height)
    )

    if maximum > 0:

        current = int(
            width *
            max(0, value) /
            maximum
        )

        pygame.draw.rect(
            screen,
            color,
            (x, y, current, height)
        )

    pygame.draw.rect(
        screen,
        WHITE,
        (x, y, width, height),
        2
    )


# ============================================================
# SAVE
# ============================================================

def save_game():

    data = {
        "x": player.x,
        "y": player.y,

        "level": player.level,
        "level_xp": player.level_xp,

        "element": player.element,
        "element_level": player.element_level,
        "element_xp": player.element_xp,

        "max_hp": player.max_hp,
        "hp": player.hp,

        "max_mana": player.max_mana,
        "mana": player.mana,

        "coins": player.coins,

        "armor": player.armor,
        "staff": player.staff,
        "sword": player.sword,
        "shield": player.shield,

        "scrolls": player.scrolls,

        "monsters_defeated": player.monsters_defeated,
        "different_monsters": list(
            player.different_monsters
        ),

        "missions": player.missions,

        "unlocked_islands": player.unlocked_islands,

        "dungeons_completed":
            player.dungeons_completed,

        "current_island": current_island,

        "owned_items": owned_items,
    }

    with open(
        SAVE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

    show_message("Jogo salvo!")


# ============================================================
# LOAD
# ============================================================

def load_game():

    global player
    global current_island
    global owned_items

    if not os.path.exists(SAVE_FILE):

        show_message(
            "Nenhum jogo salvo."
        )

        return False

    with open(
        SAVE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    player.x = data["x"]
    player.y = data["y"]

    player.level = data["level"]
    player.level_xp = data["level_xp"]

    player.element = data["element"]
    player.element_level = data["element_level"]
    player.element_xp = data["element_xp"]

    player.max_hp = data["max_hp"]
    player.hp = data["hp"]

    player.max_mana = data["max_mana"]
    player.mana = data["mana"]

    player.coins = data["coins"]

    player.armor = data["armor"]
    player.staff = data["staff"]
    player.sword = data["sword"]
    player.shield = data["shield"]

    player.scrolls = data["scrolls"]

    player.monsters_defeated = data[
        "monsters_defeated"
    ]

    player.different_monsters = set(
        data["different_monsters"]
    )

    player.missions = data["missions"]

    player.unlocked_islands = data[
        "unlocked_islands"
    ]

    player.dungeons_completed = data[
        "dungeons_completed"
    ]

    current_island = data["current_island"]

    owned_items.clear()

    owned_items.extend(
        data.get("owned_items", [])
    )

    show_message(
        "Jogo carregado!"
    )

    return True


# ============================================================
# ESCOLHA DO ELEMENTO
# ============================================================

def draw_element_selection():

    screen.fill(BLACK)

    center_text(
        screen,
        "ESCOLHA SEU ELEMENTO",
        50,
        WHITE,
        TITLE
    )

    center_text(
        screen,
        "Essa escolha define seus poderes elementais.",
        110
    )

    elements = [
        "Fogo",
        "Água",
        "Elétrico",
        "Planta"
    ]

    for i, element in enumerate(elements):

        x = 100 + i * 250

        pygame.draw.rect(
            screen,
            ELEMENTS[element]["color"],
            (x, 220, 200, 250),
            border_radius=20
        )

        center = x + 100

        icon = FONT.render(
            ELEMENTS[element]["icon"],
            True,
            WHITE
        )

        screen.blit(
            icon,
            (
                center -
                icon.get_width() // 2,
                260
            )
        )

        obj = BIG.render(
            element,
            True,
            WHITE
        )

        screen.blit(
            obj,
            (
                center -
                obj.get_width() // 2,
                320
            )
        )

        text(
            screen,
            "1 - Ataque inicial",
            x + 25,
            380
        )

        text(
            screen,
            "Nível 2 - Ataque 2",
            x + 25,
            410
        )

        text(
            screen,
            "Nível 4 - Ataque 3",
            x + 25,
            440
        )


# ============================================================
# MENU
# ============================================================

def draw_menu():

    screen.fill(
        (20, 25, 40)
    )

    center_text(
        screen,
        "REINO DE ELEMENTARIA",
        100,
        YELLOW,
        TITLE
    )

    center_text(
        screen,
        "RPG de aventura elemental",
        165
    )

    buttons = [
        ("NOVO JOGO", 270),
        ("CARREGAR JOGO", 340),
        ("SAIR", 410),
    ]

    for label, y in buttons:

        pygame.draw.rect(
            screen,
            (50, 70, 100),
            (400, y, 300, 55),
            border_radius=10
        )

        center_text(
            screen,
            label,
            y + 15,
            WHITE
        )


# ============================================================
# MAPA
# ============================================================

def draw_island():

    island = ISLANDS[current_island]

    screen.fill(
        (30, 130, 190)
    )

    pygame.draw.rect(
        screen,
        island["color"],
        (50, 50, WIDTH - 100, HEIGHT - 100),
        border_radius=35
    )

    if current_island == 0:
        draw_initial_island()

    elif current_island == 1:
        draw_volcano_island()

    elif current_island == 2:
        draw_water_island()

    elif current_island == 3:
        draw_electric_island()

    elif current_island == 4:
        draw_dark_island()

    elif current_island == 5:
        draw_earth_island()

    elif current_island == 6:
        draw_flying_island()

    elif current_island == 7:
        draw_ice_island()

    elif current_island == 8:
        draw_ghost_island()

    elif current_island == 9:
        draw_poison_island()

    # Jogador
    pygame.draw.circle(
        screen,
        ELEMENTS[player.element]["color"],
        (int(player.x), int(player.y)),
        18
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (int(player.x), int(player.y)),
        18,
        2
    )

    text(
        screen,
        "MAGO",
        player.x - 25,
        player.y - 42,
        WHITE,
        SMALL
    )

    draw_hud()

    for monster in monsters_on_map:

        draw_monster(monster)


# ============================================================
# ILHA INICIAL
# ============================================================

def draw_initial_island():

    for x, y in [
        (150, 150),
        (250, 550),
        (850, 160),
        (950, 530)
    ]:

        pygame.draw.rect(
            screen,
            BROWN,
            (x - 8, y, 16, 40)
        )

        pygame.draw.circle(
            screen,
            GREEN,
            (x, y),
            28
        )

    pygame.draw.rect(
        screen,
        (220, 180, 140),
        (450, 120, 100, 80)
    )

    pygame.draw.polygon(
        screen,
        RED,
        [
            (440, 120),
            (500, 70),
            (560, 120)
        ]
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (700, 100, 100, 90)
    )

    text(
        screen,
        "LOJA",
        720,
        135,
        BLACK
    )

    pygame.draw.rect(
        screen,
        (240, 240, 240),
        (120, 400, 100, 90)
    )

    text(
        screen,
        "MÉDICO",
        125,
        435,
        BLACK
    )


# ============================================================
# ILHA VULCÂNICA
# ============================================================

def draw_volcano_island():

    for x, y in [
        (250, 200),
        (500, 150),
        (800, 240)
    ]:

        pygame.draw.polygon(
            screen,
            (75, 45, 40),
            [
                (x - 90, y + 100),
                (x, y - 70),
                (x + 90, y + 100)
            ]
        )

        pygame.draw.polygon(
            screen,
            ORANGE,
            [
                (x - 20, y),
                (x, y - 25),
                (x + 20, y)
            ]
        )

    for i in range(5):

        pygame.draw.line(
            screen,
            ORANGE,
            (100 + i * 200, 550),
            (200 + i * 200, 500),
            18
        )


# ============================================================
# ILHA AQUÁTICA
# ============================================================

def draw_water_island():

    for i in range(12):

        x = random.Random(i).randint(
            100,
            950
        )

        y = random.Random(
            i + 50
        ).randint(
            100,
            580
        )

        pygame.draw.circle(
            screen,
            CYAN,
            (x, y),
            18
        )

        pygame.draw.line(
            screen,
            BLUE,
            (x, y),
            (x, y + 25),
            5
        )


# ============================================================
# ILHA ELÉTRICA
# ============================================================

def draw_electric_island():

    for x in range(
        120,
        1000,
        180
    ):

        h = 120 + (
            x % 150
        )

        pygame.draw.rect(
            screen,
            (45, 45, 60),
            (
                x,
                550 - h,
                100,
                h
            )
        )

        for y in range(
            570 - h,
            540,
            35
        ):

            pygame.draw.rect(
                screen,
                YELLOW,
                (x + 15, y, 15, 10)
            )

            pygame.draw.rect(
                screen,
                CYAN,
                (x + 55, y, 15, 10)
            )


# ============================================================
# ILHA SOMBRIA
# ============================================================

def draw_dark_island():

    for x, y in [
        (160, 160),
        (350, 300),
        (750, 160),
        (850, 450)
    ]:

        pygame.draw.rect(
            screen,
            (45, 40, 50),
            (x, y, 120, 100)
        )

        pygame.draw.polygon(
            screen,
            (30, 25, 35),
            [
                (x - 10, y),
                (x + 60, y - 50),
                (x + 130, y)
            ]
        )


# ============================================================
# ILHA DE TERRA
# ============================================================

def draw_earth_island():

    for x, y in [
        (200, 180),
        (450, 300),
        (750, 200),
        (850, 500)
    ]:

        pygame.draw.polygon(
            screen,
            (100, 75, 55),
            [
                (x - 100, y + 100),
                (x, y - 80),
                (x + 100, y + 100)
            ]
        )


# ============================================================
# ILHA VOADORA
# ============================================================

def draw_flying_island():

    for x, y in [
        (200, 180),
        (500, 350),
        (800, 180)
    ]:

        pygame.draw.ellipse(
            screen,
            (220, 220, 230),
            (x - 100, y - 30, 200, 80)
        )

        pygame.draw.rect(
            screen,
            BROWN,
            (x - 35, y - 100, 70, 70)
        )


# ============================================================
# ILHA DE GELO
# ============================================================

def draw_ice_island():

    for x in range(
        130,
        1000,
        130
    ):

        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (x, 550),
                (x + 40, 180),
                (x + 80, 550)
            ]
        )

    pygame.draw.circle(
        screen,
        WHITE,
        (700, 300),
        70
    )


# ============================================================
# ILHA FANTASMA
# ============================================================

def draw_ghost_island():

    for x, y in [
        (150, 150),
        (450, 200),
        (750, 150),
        (850, 430)
    ]:

        pygame.draw.rect(
            screen,
            (45, 40, 55),
            (x, y, 130, 120)
        )

    for x, y in [
        (300, 500),
        (600, 450),
        (900, 300)
    ]:

        pygame.draw.circle(
            screen,
            WHITE,
            (x, y),
            25
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (x - 25, y, 50, 35)
        )


# ============================================================
# ILHA VENENOSA
# ============================================================

def draw_poison_island():

    for x, y in [
        (150, 180),
        (350, 500),
        (700, 180),
        (850, 450)
    ]:

        pygame.draw.line(
            screen,
            BROWN,
            (x, y),
            (x + 30, y - 30),
            8
        )

        pygame.draw.circle(
            screen,
            GREEN,
            (x + 35, y - 35),
            25
        )

    pygame.draw.arc(
        screen,
        YELLOW,
        (500, 350, 130, 60),
        0,
        math.pi,
        5
    )


# ============================================================
# MONSTROS NO MAPA
# ============================================================

monsters_on_map = []


def spawn_monsters():

    global monsters_on_map

    monsters_on_map = []

    element = ISLANDS[
        current_island
    ]["element"]

    for i in range(3):

        monster = Monster(
            element,
            random.randint(
                1,
                min(
                    5,
                    2 + current_island // 2
                )
            )
        )

        monster.x = random.randint(
            120,
            950
        )

        monster.y = random.randint(
            120,
            570
        )

        monsters_on_map.append(
            monster
        )


def draw_monster(monster):

    color = ELEMENTS[
        monster.element
    ]["color"]

    pygame.draw.circle(
        screen,
        color,
        (
            int(monster.x),
            int(monster.y)
        ),
        23
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            int(monster.x - 8),
            int(monster.y - 5)
        ),
        4
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            int(monster.x + 8),
            int(monster.y - 5)
        ),
        4
    )

    text(
        screen,
        f"{monster.name} Lv.{monster.level}",
        monster.x - 50,
        monster.y - 48,
        WHITE,
        SMALL
    )


def move_monsters():

    for monster in monsters_on_map:

        dx = player.x - monster.x
        dy = player.y - monster.y

        distance = math.hypot(
            dx,
            dy
        )

        if distance > 45:

            monster.x += (
                dx /
                max(distance, 1)
                *
                monster.speed
            )

            monster.y += (
                dy /
                max(distance, 1)
                *
                monster.speed
            )

        if distance < 45:

            start_battle(
                monster
            )

            return


# ============================================================
# HUD
# ============================================================

def draw_hud():

    pygame.draw.rect(
        screen,
        (20, 20, 30),
        (0, 0, WIDTH, 80)
    )

    text(
        screen,
        f"Lv {player.level}",
        20,
        10
    )

    text(
        screen,
        f"Elemento: {player.element}",
        20,
        38,
        ELEMENTS[
            player.element
        ]["color"]
    )

    draw_bar(
        220,
        10,
        200,
        22,
        player.hp,
        player.max_hp,
        RED
    )

    draw_bar(
        220,
        42,
        200,
        22,
        player.mana,
        player.max_mana,
        BLUE
    )

    text(
        screen,
        f"{player.hp}/{player.max_hp}",
        430,
        10,
        WHITE,
        SMALL
    )

    text(
        screen,
        f"{player.mana}/{player.max_mana}",
        430,
        42,
        WHITE,
        SMALL
    )

    text(
        screen,
        f"🪙 {player.coins}",
        520,
        20,
        YELLOW
    )

    text(
        screen,
        f"Elemento Lv.{player.element_level}",
        650,
        20,
        WHITE
    )

    text(
        screen,
        f"Ilha: {ISLANDS[current_island]['name']}",
        830,
        20,
        WHITE,
        SMALL
    )


# ============================================================
# BATALHA
# ============================================================

battle_turn = True


def start_battle(monster):

    global current_monster
    global game_state
    global battle_turn

    current_monster = monster

    battle_turn = True

    game_state = "battle"

    battle_log.clear()

    battle_log.append(
        f"{monster.name} apareceu!"
    )


def draw_battle():

    screen.fill(
        (25, 25, 40)
    )

    center_text(
        screen,
        "BATALHA",
        20,
        YELLOW,
        TITLE
    )

    # Jogador
    pygame.draw.circle(
        screen,
        ELEMENTS[
            player.element
        ]["color"],
        (230, 230),
        70
    )

    text(
        screen,
        "MAGO",
        200,
        320,
        WHITE,
        BIG
    )

    draw_bar(
        130,
        365,
        220,
        25,
        player.hp,
        player.max_hp,
        RED
    )

    draw_bar(
        130,
        400,
        220,
        25,
        player.mana,
        player.max_mana,
        BLUE
    )

    # Inimigo
    color = ELEMENTS[
        current_monster.element
    ]["color"]

    pygame.draw.circle(
        screen,
        color,
        (850, 230),
        80
    )

    text(
        screen,
        current_monster.name,
        760,
        330,
        WHITE,
        BIG
    )

    text(
        screen,
        f"Elemento: {current_monster.element}",
        760,
        370,
        color
    )

    draw_bar(
        730,
        410,
        240,
        25,
        current_monster.hp,
        current_monster.max_hp,
        RED
    )

    draw_bar(
        730,
        445,
        240,
        25,
        current_monster.mana,
        current_monster.max_mana,
        BLUE
    )

    # Log
    pygame.draw.rect(
        screen,
        DARK_GRAY,
        (80, 500, 940, 70)
    )

    for i, log in enumerate(
        battle_log[-3:]
    ):

        text(
            screen,
            log,
            100,
            510 + i * 20,
            WHITE,
            SMALL
        )

    # Ações
    actions = [
        ("1 - Ataque elemental 1", 100, 600),
        ("2 - Ataque elemental 2", 330, 600),
        ("3 - Ataque elemental 3", 560, 600),
        ("4 - Punho/Espada", 790, 600),
    ]

    for label, x, y in actions:

        pygame.draw.rect(
            screen,
            (55, 65, 90),
            (x, y, 200, 45),
            border_radius=8
        )

        text(
            screen,
            label,
            x + 10,
            y + 12,
            WHITE,
            SMALL
        )

    text(
        screen,
        "H - Poção de vida | P - Poção de mana | E - Escapar",
        350,
        660,
        WHITE,
        SMALL
    )


# ============================================================
# MULTIPLICADOR ELEMENTAL
# ============================================================

def elemental_multiplier(
    attacker,
    defender
):

    if defender in ELEMENTS[
        attacker
    ]["weak"]:

        return 0.65

    if defender in ELEMENTS[
        attacker
    ]["strong"]:

        return 1.5

    return 1.0


# ============================================================
# ATAQUE DO JOGADOR
# ============================================================

def player_attack(index):

    global battle_turn

    if not battle_turn:
        return

    if index == 3:

        damage = player.physical_damage()

        current_monster.hp -= damage

        battle_log.append(
            f"Você causou {damage} de dano físico!"
        )

        end_player_turn()

        return

    required_level = {
        0: 1,
        1: 2,
        2: 4,
    }[index]

    if player.element_level < required_level:

        battle_log.append(
            f"Ataque bloqueado! "
            f"Precisa do nível elemental "
            f"{required_level}."
        )

        return

    attack = ELEMENTS[
        player.element
    ]["attacks"][index]

    (
        name,
        min_damage,
        max_damage,
        min_mana,
        max_mana
    ) = attack

    mana_cost = random.randint(
        min_mana,
        max_mana
    )

    if player.mana < mana_cost:

        battle_log.append(
            "Mana insuficiente!"
        )

        return

    player.mana -= mana_cost

    damage = random.randint(
        min_damage,
        max_damage
    )

    damage += player.elemental_bonus()

    if player.staff:
        damage += 15

    multiplier = elemental_multiplier(
        player.element,
        current_monster.element
    )

    damage = int(
        damage * multiplier
    )

    current_monster.hp -= damage

    battle_log.append(
        f"{name}: {damage} dano! "
        f"(-{mana_cost} mana)"
    )

    end_player_turn()


# ============================================================
# FINAL DO TURNO
# ============================================================

def end_player_turn():

    global battle_turn

    if current_monster.hp <= 0:

        win_battle()

        return

    player.mana = min(
        player.max_mana,
        player.mana + random.randint(
            10,
            25
        )
    )

    battle_turn = False

    enemy_attack()

    battle_turn = True


# ============================================================
# ATAQUE DO INIMIGO
# ============================================================

def enemy_attack():

    if current_monster is None:
        return

    if current_monster.hp <= 0:
        return

    damage = current_monster.damage()

    if player.shield:

        if random.random() < 0.30:

            battle_log.append(
                "Você desviou do ataque!"
            )

            return

    defense = player.defense()

    damage = int(
        damage *
        (1 - defense / 100)
    )

    damage = max(
        1,
        damage
    )

    player.hp -= damage

    battle_log.append(
        f"{current_monster.name} "
        f"causou {damage} de dano!"
    )

    if player.hp <= 0:

        player.hp = 0

        game_over()


# ============================================================
# POÇÃO DE VIDA
# ============================================================

def use_health_potion():

    global battle_turn

    if not battle_turn:
        return

    if player.coins < POTIONS[
        "Poção de Regeneração"
    ]:

        battle_log.append(
            "Moedas insuficientes."
        )

        return

    player.coins -= 15

    amount = random.randint(
        20,
        35
    )

    player.hp = min(
        player.max_hp,
        player.hp + amount
    )

    battle_log.append(
        f"Poção recuperou "
        f"{amount} de vida."
    )

    end_player_turn()


# ============================================================
# POÇÃO DE MANA
# ============================================================

def use_mana_potion():

    global battle_turn

    if not battle_turn:
        return

    if player.coins < POTIONS[
        "Poção de Mana"
    ]:

        battle_log.append(
            "Moedas insuficientes."
        )

        return

    player.coins -= 20

    amount = random.randint(
        20,
        35
    )

    player.mana = min(
        player.max_mana,
        player.mana + amount
    )

    battle_log.append(
        f"Poção recuperou "
        f"{amount} de mana."
    )

    end_player_turn()


# ============================================================
# GAME OVER
# ============================================================

def game_over():

    global game_state
    global dungeon_active
    global current_monster

    # Se morreu na masmorra,
    # a masmorra termina porque a única
    # saída permitida é a morte.

    dungeon_active = False

    current_monster = None

    game_state = "game_over"


# ============================================================
# VITÓRIA CONTRA MONSTRO
# ============================================================

def win_battle():

    global game_state
    global current_monster
    global dungeon_monsters_left
    global dungeon_total_defeated
    global dungeon_round
    global dungeon_active

    monster = current_monster

    coins_range = {
        1: (24, 50),
        2: (45, 75),
        3: (70, 100),
        4: (100, 125),
        5: (120, 150),
    }

    xp_range = {
        1: (30, 50),
        2: (45, 50),
        3: (50, 60),
        4: (55, 65),
        5: (65, 80),
    }

    coins = random.randint(
        *coins_range[
            monster.level
        ]
    )

    xp = random.randint(
        *xp_range[
            monster.level
        ]
    )

    element_xp = random.randint(
        10,
        35
    )

    player.coins += coins

    player.gain_xp(xp)

    player.gain_element_xp(
        element_xp
    )

    player.monsters_defeated += 1

    player.different_monsters.add(
        monster.name
    )

    # ========================================================
    # MISSÃO 1º MONSTRO
    # ========================================================

    if not player.missions[
        "first_monster"
    ]:

        player.missions[
            "first_monster"
        ] = True

        player.coins += 25

        player.gain_xp(15)

    # ========================================================
    # MISSÃO 5 MONSTROS DIFERENTES
    # ========================================================

    if (
        len(player.different_monsters) >= 5
        and not player.missions[
            "five_monsters"
        ]
    ):

        player.missions[
            "five_monsters"
        ] = True

        player.coins += 50

        player.gain_xp(30)

    # ========================================================
    # MASMORRA
    # ========================================================

    if dungeon_active:

        dungeon_total_defeated += 1

        dungeon_monsters_left -= 1

        current_monster = None

        # ----------------------------------------------------
        # AINDA EXISTEM MONSTROS NO GRUPO
        # ----------------------------------------------------

        if dungeon_monsters_left > 0:

            battle_log.clear()

            show_message(
                f"Monstro derrotado! "
                f"Faltam {dungeon_monsters_left}."
            )

            # VOLTA PARA A TELA DA MASMORRA,
            # E NÃO PARA O MUNDO.

            game_state = "dungeon"

        # ----------------------------------------------------
        # OS 3 MONSTROS DA MASMORRA FORAM DERROTADOS
        # ----------------------------------------------------

        else:

            # Recompensa por concluir a masmorra
            reward_coins = random.randint(
                45,
                60
            )

            reward_xp = random.randint(
                45,
                60
            )

            player.coins += reward_coins

            player.gain_xp(
                reward_xp
            )

            element = ISLANDS[
                current_island
            ]["element"]

            # Pergaminho da ilha
            if element not in player.scrolls:

                player.scrolls.append(
                    element
                )

            # Desbloqueia a próxima ilha
            # Ex.: ilha 0 libera a ilha 1.
            if current_island + 2 > player.unlocked_islands:

                player.unlocked_islands = min(
                    len(ISLANDS),
                    current_island + 2
                )

            # Registra a masmorra como concluída
            if current_island not in player.dungeons_completed:

                player.dungeons_completed.append(
                    current_island
                )

            # A masmorra termina depois dos 3 monstros.
            dungeon_active = False
            dungeon_monsters_left = 0
            dungeon_round = 0
            battle_log.clear()

            next_island = current_island + 1

            if next_island < len(ISLANDS):

                show_message(
                    f"MASMORRA CONCLUÍDA! "
                    f"Pergaminho de {element} recebido! "
                    f"+{reward_coins} moedas, +{reward_xp} XP. "
                    f"{ISLANDS[next_island]['name']} foi liberada!"
                )

            else:

                show_message(
                    f"MASMORRA CONCLUÍDA! "
                    f"Pergaminho de {element} recebido! "
                    f"+{reward_coins} moedas, +{reward_xp} XP. "
                    f"Todas as ilhas foram liberadas!"
                )

            game_state = "world"

        return

    # ========================================================
    # BATALHA NORMAL
    # ========================================================

    if monster in monsters_on_map:

        monsters_on_map.remove(
            monster
        )

    current_monster = None

    game_state = "world"

    show_message(
        f"Vitória! "
        f"+{coins} moedas, "
        f"+{xp} XP, "
        f"+{element_xp} XP elemental."
    )


# ============================================================
# MASMORRA
# ============================================================

def enter_dungeon():

    global dungeon_active
    global dungeon_monsters_left
    global dungeon_total_defeated
    global dungeon_round
    global game_state

    # Uma masmorra concluída não pode ser repetida.
    if current_island in player.dungeons_completed:

        show_message(
            "Esta masmorra já foi concluída. "
            "Explore a próxima ilha!"
        )

        return

    # Ativa a masmorra.
    dungeon_active = True

    # Cada masmorra possui exatamente 3 monstros.
    dungeon_monsters_left = 3
    dungeon_total_defeated = 0
    dungeon_round = 1

    game_state = "dungeon"

    show_message(
        "Você entrou na masmorra! "
        "Derrote os 3 monstros para pegar o pergaminho "
        "e liberar a próxima ilha.",
        4
    )


def draw_dungeon():

    screen.fill(
        (35, 30, 42)
    )

    # ========================================================
    # TÍTULO
    # ========================================================

    center_text(
        screen,
        "MASMORRA",
        20,
        YELLOW,
        TITLE
    )

    center_text(
        screen,
        f"Ilha: {ISLANDS[current_island]['name']}",
        75,
        WHITE
    )

    # ========================================================
    # AVISO PRINCIPAL
    # ========================================================

    center_text(
        screen,
        "VOCÊ ESTÁ PRESO!",
        120,
        RED,
        BIG
    )

    center_text(
        screen,
        "A única forma de sair é MORRENDO.",
        160,
        WHITE
    )

    # ========================================================
    # INFORMAÇÕES
    # ========================================================

    pygame.draw.rect(
        screen,
        (50, 45, 60),
        (300, 205, 500, 100),
        border_radius=12
    )

    center_text(
        screen,
        "3 MONSTROS NESTA MASMORRA",
        220,
        YELLOW
    )

    center_text(
        screen,
        f"Monstros restantes: {dungeon_monsters_left}",
        255,
        WHITE
    )

    # ========================================================
    # DECORAÇÃO DA MASMORRA
    # ========================================================

    for i in range(3):

        x = 250 + i * 300

        pygame.draw.rect(
            screen,
            (70, 60, 75),
            (
                x - 80,
                350,
                160,
                120
            ),
            border_radius=10
        )

        pygame.draw.circle(
            screen,
            ELEMENTS[
                ISLANDS[
                    current_island
                ]["element"]
            ]["color"],
            (x, 410),
            35
        )

    # ========================================================
    # CONTROLES
    # ========================================================

    if dungeon_monsters_left > 0:

        center_text(
            screen,
            "ENTER - Enfrentar próximo monstro",
            510,
            GREEN,
            BIG
        )

    center_text(
        screen,
        "ESC - BLOQUEADO",
        570,
        RED
    )

    center_text(
        screen,
        "M / I / B - BLOQUEADOS",
        600,
        RED,
        SMALL
    )

    center_text(
        screen,
        f"Monstros derrotados nesta expedição: {dungeon_total_defeated}",
        635,
        WHITE,
        SMALL
    )


def start_dungeon_battle():

    global dungeon_active

    # A masmorra continua ativa.
    dungeon_active = True

    element = ISLANDS[
        current_island
    ]["element"]

    # Os 3 monstros da masmorra pertencem à ilha atual.
    # Não existem grupos infinitos nem novas rodadas.
    monster_level = random.randint(
        1,
        min(
            5,
            2 + current_island // 2
        )
    )

    monster = Monster(
        element,
        monster_level
    )

    start_battle(
        monster
    )


# ============================================================
# LOJA
# ============================================================

def draw_shop():

    screen.fill(
        (35, 35, 45)
    )

    center_text(
        screen,
        "LOJA",
        30,
        YELLOW,
        TITLE
    )

    y = 110

    for i, (item, price) in enumerate(
        SHOP_ITEMS.items()
    ):

        pygame.draw.rect(
            screen,
            (60, 70, 90),
            (120, y, 600, 55),
            border_radius=8
        )

        text(
            screen,
            f"{i + 1}. {item}",
            140,
            y + 16
        )

        text(
            screen,
            f"{price} moedas",
            560,
            y + 16,
            YELLOW
        )

        y += 65

    y += 20

    text(
        screen,
        "H - Poção de Regeneração: 15 moedas",
        120,
        y
    )

    text(
        screen,
        "M - Poção de Mana: 20 moedas",
        120,
        y + 30
    )

    text(
        screen,
        "ESC - Sair",
        120,
        y + 80
    )

    text(
        screen,
        f"Suas moedas: {player.coins}",
        800,
        120,
        YELLOW
    )


def buy_item(index):

    items = list(
        SHOP_ITEMS.items()
    )

    if index >= len(items):
        return

    item, price = items[index]

    if item in owned_items:

        show_message(
            "Você já possui esse item."
        )

        return

    if player.coins < price:

        show_message(
            "Moedas insuficientes."
        )

        return

    player.coins -= price

    owned_items.append(
        item
    )

    if item == "Armadura de Ferro":

        player.armor = item

    elif item == "Armadura de Escamas":

        player.armor = item

    elif item == "Cajado Arcano":

        player.staff = True

    elif item == "Espada de Ferro":

        player.sword = True

    elif item == "Escudo Elemental":

        player.shield = True

    show_message(
        f"{item} comprado!"
    )


# ============================================================
# INVENTÁRIO
# ============================================================

def draw_inventory():

    screen.fill(
        (25, 30, 40)
    )

    center_text(
        screen,
        "INVENTÁRIO",
        30,
        YELLOW,
        TITLE
    )

    text(
        screen,
        f"Elemento: {player.element}",
        100,
        120
    )

    text(
        screen,
        f"Nível: {player.level}",
        100,
        155
    )

    text(
        screen,
        f"XP: {player.level_xp}/100",
        100,
        190
    )

    text(
        screen,
        f"Nível elemental: {player.element_level}",
        500,
        120
    )

    text(
        screen,
        f"XP elemental: {player.element_xp}/100",
        500,
        155
    )

    text(
        screen,
        "Equipamentos:",
        100,
        250,
        YELLOW
    )

    equipment = (
        owned_items
        if owned_items
        else ["Nenhum"]
    )

    for i, item in enumerate(
        equipment
    ):

        text(
            screen,
            f"- {item}",
            120,
            285 + i * 30
        )

    text(
        screen,
        "Pergaminhos:",
        500,
        250,
        YELLOW
    )

    if player.scrolls:

        for i, scroll in enumerate(
            player.scrolls
        ):

            text(
                screen,
                f"📜 Pergaminho de {scroll}",
                520,
                285 + i * 30
            )

    else:

        text(
            screen,
            "Nenhum pergaminho",
            520,
            285
        )

    text(
        screen,
        "ESC - Voltar",
        100,
        620
    )


# ============================================================
# MAPA DAS ILHAS
# ============================================================

def draw_island_menu():

    screen.fill(
        (20, 25, 35)
    )

    center_text(
        screen,
        "MAPA DE ELEMENTARIA",
        25,
        YELLOW,
        BIG
    )

    for i, island in enumerate(
        ISLANDS
    ):

        row = i // 2
        col = i % 2

        x = 100 + col * 480
        y = 100 + row * 105

        unlocked = (
            i < player.unlocked_islands
        )

        color = (
            island["color"]
            if unlocked
            else GRAY
        )

        pygame.draw.rect(
            screen,
            color,
            (x, y, 400, 80),
            border_radius=10
        )

        text(
            screen,
            f"{i + 1}. {island['name']}",
            x + 20,
            y + 15
        )

        text(
            screen,
            island["description"],
            x + 20,
            y + 45,
            WHITE,
            SMALL
        )

        if not unlocked:

            text(
                screen,
                "BLOQUEADA",
                x + 285,
                y + 30,
                RED,
                SMALL
            )

    text(
        screen,
        "Pressione o número da ilha. ESC para voltar.",
        340,
        650
    )


def travel_to(index):

    global current_island
    global game_state

    if index < 0 or index >= len(
        ISLANDS
    ):

        return

    if index >= player.unlocked_islands:

        show_message(
            "Essa ilha ainda está bloqueada!"
        )

        return

    current_island = index

    player.x = 550
    player.y = 350

    spawn_monsters()

    game_state = "world"


# ============================================================
# DRAGÃO
# ============================================================

class Dragon:

    def __init__(self):

        self.name = (
            "Dragão Guardião de Elementaria"
        )

        self.element = "Sombrio"

        self.max_hp = 1200
        self.hp = self.max_hp

        self.max_mana = 500
        self.mana = self.max_mana

        self.level = 20

    def damage(self):

        return random.randint(
            55,
            85
        )


dragon = Dragon()


def all_dungeons_completed():

    return len(
        player.dungeons_completed
    ) >= 10


# ============================================================
# PORTÃO DO DRAGÃO
# ============================================================

def draw_boss_gate():

    screen.fill(
        (15, 10, 20)
    )

    center_text(
        screen,
        "PORTÃO DO DRAGÃO",
        50,
        RED,
        TITLE
    )

    center_text(
        screen,
        "O Guardião de Elementaria aguarda você.",
        120
    )

    if all_dungeons_completed():

        center_text(
            screen,
            "Todas as masmorras foram derrotadas!",
            220,
            GREEN
        )

        center_text(
            screen,
            "Entre no portão pagando 150 moedas.",
            270,
            YELLOW
        )

        center_text(
            screen,
            "ENTER - Entrar",
            360
        )

    else:

        center_text(
            screen,
            "Você precisa derrotar todas as 10 masmorras.",
            220,
            RED
        )

    center_text(
        screen,
        "ESC - Voltar",
        500
    )


def enter_boss():

    global game_state

    if not all_dungeons_completed():

        show_message(
            "Todas as masmorras precisam ser derrotadas!"
        )

        return

    if player.coins < 150:

        show_message(
            "Você precisa de 150 moedas."
        )

        return

    player.coins -= 150

    dragon.hp = dragon.max_hp

    game_state = "boss"


# ============================================================
# BATALHA DO CHEFE
# ============================================================

def draw_boss():

    screen.fill(
        (18, 10, 25)
    )

    center_text(
        screen,
        "BATALHA FINAL",
        25,
        RED,
        TITLE
    )

    pygame.draw.circle(
        screen,
        (130, 30, 160),
        (800, 250),
        120
    )

    text(
        screen,
        "🐉",
        760,
        200,
        WHITE,
        TITLE
    )

    text(
        screen,
        dragon.name,
        650,
        390,
        WHITE,
        BIG
    )

    draw_bar(
        650,
        440,
        300,
        30,
        dragon.hp,
        dragon.max_hp,
        RED
    )

    text(
        screen,
        f"HP: {dragon.hp}/{dragon.max_hp}",
        720,
        480
    )

    pygame.draw.circle(
        screen,
        ELEMENTS[
            player.element
        ]["color"],
        (250, 250),
        75
    )

    text(
        screen,
        "MAGO",
        210,
        350,
        WHITE,
        BIG
    )

    draw_bar(
        130,
        400,
        250,
        25,
        player.hp,
        player.max_hp,
        RED
    )

    draw_bar(
        130,
        435,
        250,
        25,
        player.mana,
        player.max_mana,
        BLUE
    )

    text(
        screen,
        "1 - Ataque elemental",
        150,
        540
    )

    text(
        screen,
        "2 - Ataque forte",
        150,
        580
    )

    text(
        screen,
        "3 - Ataque supremo",
        150,
        620
    )

    text(
        screen,
        "4 - Espada/Punho",
        550,
        540
    )

    text(
        screen,
        "P - Poção de mana",
        550,
        580
    )

    text(
        screen,
        "H - Poção de vida",
        550,
        620
    )


def boss_attack():

    damage = dragon.damage()

    if player.shield:

        if random.random() < 0.30:

            show_message(
                "O Escudo Elemental desviou o ataque!"
            )

            return

    damage = int(
        damage *
        (
            1 -
            player.defense() /
            100
        )
    )

    player.hp -= max(
        1,
        damage
    )

    if player.hp <= 0:

        player.hp = 0

        game_over()


def boss_player_attack(index):

    if index == 3:

        damage = player.physical_damage()

    else:

        required = {
            0: 1,
            1: 2,
            2: 4
        }[index]

        if player.element_level < required:

            show_message(
                f"Você precisa do nível elemental {required}."
            )

            return

        (
            name,
            min_d,
            max_d,
            min_m,
            max_m
        ) = ELEMENTS[
            player.element
        ]["attacks"][index]

        cost = random.randint(
            min_m,
            max_m
        )

        if player.mana < cost:

            show_message(
                "Mana insuficiente!"
            )

            return

        player.mana -= cost

        damage = random.randint(
            min_d,
            max_d
        )

        damage += player.elemental_bonus()

        if player.staff:

            damage += 15

        # Dragão é fraco contra Água
        if player.element == "Água":

            damage = int(
                damage * 1.7
            )

        else:

            damage = int(
                damage * 0.65
            )

    dragon.hp -= damage

    player.mana = min(
        player.max_mana,
        player.mana + random.randint(
            10,
            25
        )
    )

    if dragon.hp <= 0:

        dragon.hp = 0

        player.missions[
            "final_boss"
        ] = True

        game_state = "victory"

        return

    boss_attack()


# ============================================================
# POÇÕES NO CHEFE
# ============================================================

def use_boss_health_potion():

    if player.coins < 15:

        show_message(
            "Moedas insuficientes."
        )

        return

    player.coins -= 15

    amount = random.randint(
        20,
        35
    )

    player.hp = min(
        player.max_hp,
        player.hp + amount
    )

    show_message(
        f"Poção recuperou {amount} de vida."
    )

    boss_attack()


def use_boss_mana_potion():

    if player.coins < 20:

        show_message(
            "Moedas insuficientes."
        )

        return

    player.coins -= 20

    amount = random.randint(
        20,
        35
    )

    player.mana = min(
        player.max_mana,
        player.mana + amount
    )

    show_message(
        f"Poção recuperou {amount} de mana."
    )

    boss_attack()


# ============================================================
# VITÓRIA
# ============================================================

def draw_victory():

    screen.fill(
        (15, 35, 25)
    )

    center_text(
        screen,
        "🏆 VITÓRIA!",
        100,
        YELLOW,
        TITLE
    )

    center_text(
        screen,
        "Você derrotou o Dragão Guardião de Elementaria!",
        200,
        WHITE,
        BIG
    )

    center_text(
        screen,
        "O Reino de Elementaria foi salvo!",
        270,
        GREEN
    )

    center_text(
        screen,
        "Obrigado por jogar!",
        360
    )

    center_text(
        screen,
        "ESC - Voltar ao menu",
        500
    )


# ============================================================
# GAME OVER
# ============================================================

def draw_game_over():

    screen.fill(
        (35, 10, 15)
    )

    center_text(
        screen,
        "VOCÊ FOI DERROTADO",
        180,
        RED,
        TITLE
    )

    center_text(
        screen,
        "A aventura chegou ao fim.",
        260
    )

    center_text(
        screen,
        "ENTER - Voltar ao menu",
        400
    )


# ============================================================
# EVENTOS DO MUNDO
# ============================================================

def interact_world():

    if current_island == 0:

        # Loja
        if (
            680 < player.x < 830
            and
            80 < player.y < 220
        ):

            return "shop"

        # Médico
        if (
            100 < player.x < 250
            and
            360 < player.y < 520
        ):

            player.heal()

            show_message(
                "Médico recuperou toda sua vida e mana!"
            )

    return None


def draw_world_help():

    pygame.draw.rect(
        screen,
        (20, 20, 30),
        (
            10,
            HEIGHT - 70,
            WIDTH - 20,
            55
        )
    )

    text(
        screen,
        "WASD/SETAS: andar | M: mapa | I: inventário | E: interagir | F: masmorra | B: portão | F5: salvar",
        25,
        HEIGHT - 52,
        WHITE,
        SMALL
    )


# ============================================================
# CONTROLES DO MUNDO
# ============================================================

def handle_world_key(key):

    global game_state

    # --------------------------------------------------------
    # Se por algum motivo dungeon_active estiver True,
    # o jogador NÃO pode usar nenhum desses comandos.
    # --------------------------------------------------------

    if dungeon_active:
        return

    if key == pygame.K_m:

        game_state = "islands"

    elif key == pygame.K_i:

        game_state = "inventory"

    elif key == pygame.K_e:

        result = interact_world()

        if result == "shop":

            game_state = "shop"

    elif key == pygame.K_f:

        enter_dungeon()

    elif key == pygame.K_b:

        game_state = "boss_gate"

    elif key == pygame.K_F5:

        save_game()


# ============================================================
# CONTROLES DA BATALHA
# ============================================================

def handle_battle_key(key):

    # --------------------------------------------------------
    # IMPORTANTE:
    # Mesmo dentro da batalha da masmorra,
    # ESC NÃO PODE SAIR.
    # --------------------------------------------------------

    if key == pygame.K_1:

        player_attack(0)

    elif key == pygame.K_2:

        player_attack(1)

    elif key == pygame.K_3:

        player_attack(2)

    elif key == pygame.K_4:

        player_attack(3)

    elif key == pygame.K_h:

        use_health_potion()

    elif key == pygame.K_p:

        use_mana_potion()

    elif key == pygame.K_ESCAPE:

        # ----------------------------------------------------
        # FORA DA MASMORRA:
        # pode escapar.
        #
        # DENTRO DA MASMORRA:
        # ESC NÃO FAZ NADA.
        # ----------------------------------------------------

        if dungeon_active:

            battle_log.append(
                "Você está preso na masmorra!"
            )

        else:

            global game_state

            game_state = "world"


# ============================================================
# LOOP PRINCIPAL
# ============================================================

running = True

while running:

    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # ====================================================
        # MENU
        # ====================================================

        if game_state == "menu":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:

                    player = Player()

                    owned_items.clear()

                    game_state = "choose_element"

                elif event.key == pygame.K_2:

                    if load_game():

                        game_state = "world"

                        spawn_monsters()

                elif event.key == pygame.K_3:

                    running = False

                elif event.key == pygame.K_ESCAPE:

                    running = False

        # ====================================================
        # ESCOLHA DO ELEMENTO
        # ====================================================

        elif game_state == "choose_element":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:

                    player.element = "Fogo"

                    game_state = "world"

                    spawn_monsters()

                elif event.key == pygame.K_2:

                    player.element = "Água"

                    game_state = "world"

                    spawn_monsters()

                elif event.key == pygame.K_3:

                    player.element = "Elétrico"

                    game_state = "world"

                    spawn_monsters()

                elif event.key == pygame.K_4:

                    player.element = "Planta"

                    game_state = "world"

                    spawn_monsters()

        # ====================================================
        # MUNDO
        # ====================================================

        elif game_state == "world":

            if event.type == pygame.KEYDOWN:

                handle_world_key(
                    event.key
                )

        # ====================================================
        # BATALHA
        # ====================================================

        elif game_state == "battle":

            if event.type == pygame.KEYDOWN:

                handle_battle_key(
                    event.key
                )

        # ====================================================
        # MASMORRA
        # ====================================================

        elif game_state == "dungeon":

            if event.type == pygame.KEYDOWN:

                # ------------------------------------------------
                # ENTER:
                # começa o próximo combate.
                # ------------------------------------------------

                if event.key == pygame.K_RETURN:

                    if dungeon_active:

                        start_dungeon_battle()

                # ------------------------------------------------
                # ESC:
                # NÃO FAZ ABSOLUTAMENTE NADA.
                # ------------------------------------------------

                elif event.key == pygame.K_ESCAPE:

                    show_message(
                        "Você está preso! "
                        "Só poderá sair quando morrer."
                    )

                # ------------------------------------------------
                # M:
                # BLOQUEADO
                # ------------------------------------------------

                elif event.key == pygame.K_m:

                    show_message(
                        "O mapa está bloqueado dentro da masmorra."
                    )

                # ------------------------------------------------
                # I:
                # BLOQUEADO
                # ------------------------------------------------

                elif event.key == pygame.K_i:

                    show_message(
                        "O inventário está bloqueado dentro da masmorra."
                    )

                # ------------------------------------------------
                # B:
                # BLOQUEADO
                # ------------------------------------------------

                elif event.key == pygame.K_b:

                    show_message(
                        "Você não pode ir ao portão agora!"
                    )

                # ------------------------------------------------
                # F:
                # BLOQUEADO
                # ------------------------------------------------

                elif event.key == pygame.K_f:

                    show_message(
                        "Você já está dentro da masmorra!"
                    )

        # ====================================================
        # LOJA
        # ====================================================

        elif game_state == "shop":

            if event.type == pygame.KEYDOWN:

                if event.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5
                ]:

                    buy_item(
                        int(
                            event.unicode
                        ) - 1
                    )

                elif event.key == pygame.K_h:

                    if player.coins >= 15:

                        player.coins -= 15

                        amount = random.randint(
                            20,
                            35
                        )

                        player.hp = min(
                            player.max_hp,
                            player.hp + amount
                        )

                        show_message(
                            f"Poção recuperou {amount} de vida."
                        )

                    else:

                        show_message(
                            "Moedas insuficientes."
                        )

                elif event.key == pygame.K_m:

                    if player.coins >= 20:

                        player.coins -= 20

                        amount = random.randint(
                            20,
                            35
                        )

                        player.mana = min(
                            player.max_mana,
                            player.mana + amount
                        )

                        show_message(
                            f"Poção recuperou {amount} de mana."
                        )

                    else:

                        show_message(
                            "Moedas insuficientes."
                        )

                elif event.key == pygame.K_ESCAPE:

                    game_state = "world"

        # ====================================================
        # INVENTÁRIO
        # ====================================================

        elif game_state == "inventory":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    game_state = "world"

        # ====================================================
        # MAPA DAS ILHAS
        # ====================================================

        elif game_state == "islands":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    game_state = "world"

                elif event.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5,
                    pygame.K_6,
                    pygame.K_7,
                    pygame.K_8,
                    pygame.K_9,
                    pygame.K_0
                ]:

                    number = int(
                        event.unicode
                    )

                    if number == 0:

                        number = 10

                    travel_to(
                        number - 1
                    )

        # ====================================================
        # PORTÃO DO DRAGÃO
        # ====================================================

        elif game_state == "boss_gate":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    enter_boss()

                elif event.key == pygame.K_ESCAPE:

                    game_state = "world"

        # ====================================================
        # CHEFE
        # ====================================================

        elif game_state == "boss":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:

                    boss_player_attack(0)

                elif event.key == pygame.K_2:

                    boss_player_attack(1)

                elif event.key == pygame.K_3:

                    boss_player_attack(2)

                elif event.key == pygame.K_4:

                    boss_player_attack(3)

                elif event.key == pygame.K_p:

                    use_boss_mana_potion()

                elif event.key == pygame.K_h:

                    use_boss_health_potion()

        # ====================================================
        # GAME OVER
        # ====================================================

        elif game_state == "game_over":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    game_state = "menu"

        # ====================================================
        # VITÓRIA
        # ====================================================

        elif game_state == "victory":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    game_state = "menu"

    # ========================================================
    # ATUALIZAÇÃO DO MUNDO
    # ========================================================

    if game_state == "world":

        keys = pygame.key.get_pressed()

        speed = 4

        if keys[
            pygame.K_w
        ] or keys[
            pygame.K_UP
        ]:

            player.y -= speed

        if keys[
            pygame.K_s
        ] or keys[
            pygame.K_DOWN
        ]:

            player.y += speed

        if keys[
            pygame.K_a
        ] or keys[
            pygame.K_LEFT
        ]:

            player.x -= speed

        if keys[
            pygame.K_d
        ] or keys[
            pygame.K_RIGHT
        ]:

            player.x += speed

        player.x = max(
            70,
            min(
                WIDTH - 70,
                player.x
            )
        )

        player.y = max(
            90,
            min(
                HEIGHT - 90,
                player.y
            )
        )

        move_monsters()

    # ========================================================
    # DESENHO
    # ========================================================

    if game_state == "menu":

        draw_menu()

    elif game_state == "choose_element":

        draw_element_selection()

    elif game_state == "world":

        draw_island()

        draw_world_help()

    elif game_state == "battle":

        draw_battle()

    elif game_state == "dungeon":

        draw_dungeon()

    elif game_state == "shop":

        draw_shop()

    elif game_state == "inventory":

        draw_inventory()

    elif game_state == "islands":

        draw_island_menu()

    elif game_state == "boss_gate":

        draw_boss_gate()

    elif game_state == "boss":

        draw_boss()

    elif game_state == "game_over":

        draw_game_over()

    elif game_state == "victory":

        draw_victory()

    # ========================================================
    # MENSAGEM
    # ========================================================

    if message_timer > 0:

        pygame.draw.rect(
            screen,
            (15, 15, 20),
            (250, 625, 600, 45),
            border_radius=8
        )

        center_text(
            screen,
            message,
            638,
            YELLOW,
            SMALL
        )

        message_timer -= 1

    pygame.display.flip()


pygame.quit()

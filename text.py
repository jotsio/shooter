from inits import *
from assets import *

# Text positions
textplace_center = (width // 2, height // 2)
textplace_rightdown_first = (width - 64, height - 64)
textplace_rightdown_second = (width - 128, height - 64)

# Language handling
class TextContent():
    def __init__(self, dict):
        self.dict = dict
        self.lang = 0

    def setLanguage(self, language):
        if language == "English":
            self.lang = 0
        if language == "Finnish":
            self.lang = 1

    def showTitle(self, key, place, font):
        value = self.dict[key][self.lang]
        self.showValue(value, place, font)

    def showValue(self, value, place, font):
        text = font.render(value, True, color_text)
        textRect = text.get_rect()
        textRect.center = place
        SCREEN.blit(text, textRect)

game_dictionary = {
    "t_game_finished":[
        "Excellent, game finished!",
        "Hienoa, peli läpäisty!"
    ],
    "t_level_finished":[
        "Level finished",
        "Kenttä läpäisty"
    ],
    "t_player_dead":[
        "You died!",
        "Kuolit!"
        ] 
}

# Create text object
text = TextContent(game_dictionary)

properties = open("properties.txt", "r")
language = properties.read()
properties.close()
text.setLanguage(language)
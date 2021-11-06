from inits import *
class TextContent():
    def __init__(self, language, dict):
        self.dict = dict
        if language == "English":
            self.lang = 0
        if language == "Finnish":
            self.lang = 1
        else:
            self.lang = 0
    
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
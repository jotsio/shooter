from inits import *

# Show game titles
def showText(message, place, font):
    text = font.render(message, True, color_text)
    textRect = text.get_rect()
    textRect.center = place
    SCREEN.blit(text, textRect)
  

def showHearts(amount):
    image = GR_UI_HEART_DEFAULT
    Rect = image[0].get_rect()
    Rect.y = height - Rect.height
    Rect.x = 0
    i = 0
    while i < amount:
        SCREEN.blit(image[0], Rect)
        Rect.x += Rect.width
        i += 1
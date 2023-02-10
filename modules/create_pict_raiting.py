import io
import requests
from PIL import Image, ImageFont, ImageDraw
import os
import textwrap


def create_pict(list_raiting, list_raiting_player, interaction, player):
    message_rank = ''
    message_user_rank = ''
    for character in list_raiting:
        if character['member'] == None:
            character['member'] = ''
            character['position'] = ''
            character['raiting'] = ''
        else:
            character['position'] = f"{character['position']}."
            character['raiting'] = f" - {character['raiting']} Очков"
        message_rank += f"{character['position']} {character['member']}{character['raiting']}\n\n"
    for character in list_raiting_player:
        if character['id_member'] == interaction.user.id: #Поиск ID пользователя
            message_user_rank = f"{character['member']} {character['position']} Место\n\n{character['raiting']} очков"
    # Вставляем пустой фон
    image_background = Image.open('modules/image/canvas.png')
    img = image_background.resize((1080, 1499))
    #Аватар
    responce = requests.get(str(interaction.user.display_avatar), stream=True)
    responce = Image.open(io.BytesIO(responce.content))
    responce = responce.convert('RGBA')
    responce = responce.resize((245, 245), Image.ANTIALIAS)
    img.paste(responce, (790, 1170))
    #Вставляем фон
    image_raiting = Image.open(f"modules/image/{player}_raiting.png")
    image_raiting = image_raiting.resize((1080, 1499), Image.ANTIALIAS)
    img.paste(image_raiting, (0, 0), mask=image_raiting)

    # Шрифты
    headline = ImageFont.truetype(f"modules/fonts/AristotelicaProText-Bold.otf",  size = 60)
    idraw = ImageDraw.Draw(img)
    idraw.text((540, 620), message_rank, font=headline, fill=(0, 90, 255), anchor="mm")
    idraw.text((540, 615), message_rank, font=headline, fill=(255, 255, 255), anchor="mm")
    idraw.text((23, 1220), message_user_rank, font =  ImageFont.truetype(f"modules/fonts/AristotelicaProText-Bold.otf",  size = 55), fill=(0, 90, 255))
    idraw.text((23, 1215), message_user_rank, font =  ImageFont.truetype(f"modules/fonts/AristotelicaProText-Bold.otf",  size = 55), fill=(255, 255, 255))
    idraw = ImageDraw.Draw(img)
    img.save('user_card.png')
from modules.config_creater import CreatingConfig


class Config(CreatingConfig):
    def __init__(self) -> None:
        super().__init__(path = 'config.json')
        self.bot = self.Bot(config = self)
        self.server = self.Server(config = self)
        self.positionstext = self.PositionsText(config = self)
        self.startgame = self.StartGame(config = self)
        self.positions = self.Positions(config = self)
        self.text = self.Text(config = self)
        self.startGame_with_capitans = self.StartGame_with_capitans(config = self)
    class Bot:
        def __init__(self, config : CreatingConfig) -> None:
            self.token = config.config_field(key = 'token', layer = 'bot', default = 'Здесь ваш Discord Токен')
            self.prefix = config.config_field(key = 'prefix', layer = 'bot', default = '!')
    class Server:
        def __init__(self, config: CreatingConfig) -> None:
            self.admin_role = config.config_field(key = 'admin_role', layer = 'server', default= 'Здесь название Админ роли')
            self.moderator_role = config.config_field(key='moderator_role', layer='server', default='Здесь название Модератор роли')
            self.url_pict = config.config_field(key='url_pict', layer='server',  default='Ссылка на Аватарку вашего канала')
            self.channel_id_first_team =  config.config_field(key='channel_id_first_team', layer='server',  default='ID канала первой группы')
            self.channel_id_second_team = config.config_field(key='channel_id_second_team', layer='server',    default='ID канала второй группы')
            self.score_win_player =  config.config_field(key='score_win_player', layer='server',    default='Количество очков для игроков, которые выиграли')
            self.score_lose_player =  config.config_field(key='score_lose_player', layer='server',    default='Количество очков для игроков, которые проиграли')
            self.score_draw_player = config.config_field(key='score_draw_player', layer='server', default='Количество очков для игроков, если ничья')
            self.score_win_trener =  config.config_field(key='score_win_trener', layer='server',    default='Количество очков для тренеров, которые выиграли')
            self.score_lose_trener =  config.config_field(key='score_lose_trener', layer='server',    default='Количество очков для тренеров, которые проиграли')
            self.score_draw_trener = config.config_field(key='score_draw_trener', layer='server', default='Количество очков для тренеров, если ничья')
    class PositionsText:
        def __init__(self, config: CreatingConfig) -> None:
            self.title = config.config_field(key='title', layer='positionstext', default='Заголовок сообщения про выбор позициии')
            self.description = config.config_field(key='description', layer='positionstext',  default='Описание сообщения про выбор позициии')
            self.photo = config.config_field(key='photo', layer='positionstext',  default='Cсылку на картинку для Embed')
    class StartGame:
        def __init__(self, config: CreatingConfig) -> None:
            self.title = config.config_field(key='title', layer='startgame', default='Заголовок регистрации на игру')
            self.description = config.config_field(key='description', layer='startgame',  default='Описание регистрации на игру')
    class StartGame_with_capitans:
        def __init__(self, config: CreatingConfig) -> None:
            self.title = config.config_field(key='title', layer='StartGame_with_capitans', default='Заголовок  на игру')
            self.description = config.config_field(key='description', layer='StartGame_with_capitans',  default='Описание  на игру')
    class Positions:
        def __init__(self, config: CreatingConfig) -> None:
            self.list_postitions = config.config_field(key = 'list_postitions', layer = 'positions', default = ["вратарь", "защитник", "нападающий", "полузащитники", "форвард"])

    class Text:
        def __init__(self, config: CreatingConfig) -> None:
            self.clear = config.config_field(key='clear', layer='text', default='')
            self.successfully = config.config_field(key='successfully', layer='text', default='')


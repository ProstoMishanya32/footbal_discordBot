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
        self.create_game = self.Create_Game(config = self)
        self.next_game = self.Next_Game(config = self)
        self.finish_matches = self.Finish_Matches(config = self)
        self.select_result = self.Select_Results(config = self)
    class Bot:
        def __init__(self, config : CreatingConfig) -> None:
            self.token = config.config_field(key = 'token', layer = 'bot', default = 'Здесь ваш Discord Токен')
            self.prefix = config.config_field(key = 'prefix', layer = 'bot', default = '!')
            self.guilds = config.config_field(key = 'guilds', layer = 'bot', default = [])
    class Server:
        def __init__(self, config: CreatingConfig) -> None:
            self.admin_role = config.config_field(key = 'admin_role', layer = 'server', default= 'Здесь название Админ роли')
            self.moderator_role = config.config_field(key='moderator_role', layer='server', default='Здесь название Модератор роли')
            self.channel_send_result = config.config_field(key='channel_send_result', layer='server', default='Канал с результамми')
            self.url_pict = config.config_field(key='url_pict', layer='server',  default='Ссылка на Аватарку вашего канала')
            self.roles_team  = config.config_field(key='roles_team', layer='server',  default= [])
            self.channel_id_first_team =  config.config_field(key='channel_id_first_team', layer='server',  default='ID канала первой группы')
            self.channel_id_second_team = config.config_field(key='channel_id_second_team', layer='server',    default='ID канала второй группы')
            self.channel_id_three_team =  config.config_field(key='channel_id_three_team', layer='server',  default='ID канала третьей группы')
            self.channel_id_four_team = config.config_field(key='channel_id_four_team', layer='server',    default='ID канала четвертой группы')
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

    class Create_Game:
        def __init__(self, config: CreatingConfig) -> None:
            self.title = config.config_field(key='title', layer='Create_Game', default='Заголовок создание игры')
            self.description = config.config_field(key='description', layer='Create_Game',default='Описание создание игры')
    class Next_Game:
        def __init__(self, config: CreatingConfig) -> None:
            self.title = config.config_field(key='title', layer='Next_Game', default='Заголовок следующей игры')
    class Finish_Matches:
        def __init__(self, config: CreatingConfig) -> None:
            self.title = config.config_field(key='title', layer='Finish_Matches', default='Заголовок завершения игр')
    class Select_Results:
        def __init__(self, config: CreatingConfig) -> None:
            self.title = config.config_field(key='title', layer='Select_Results', default='Заголовок для выбора результата игр')
            self.description = config.config_field(key='description', layer='Select_Results', default='Описание для выбора результата игр')
    class Text:
        def __init__(self, config: CreatingConfig) -> None:
            self.clear = config.config_field(key='clear', layer='text', default='')
            self.successfully = config.config_field(key='successfully', layer='text', default='')
            self.error_access =  config.config_field(key='error_access', layer='text', default='')


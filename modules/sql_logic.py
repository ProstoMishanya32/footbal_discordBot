import sqlite3



class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()


    def create_table_raitins(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS
        raiting(
        member TEXT,
        id_member INT PRIMARY KEY,
        raiting INT Default 0)""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS
        raiting_capitans(
        member TEXT,
        id_member INT PRIMARY KEY,
        raiting INT Default 0)""")
        print(f'{"*"* 50}\nБаза данных успешна подключена\n{"*"* 50}')



    def add_member_in_raiting(self, member_name, member_id, _capitans):
        member = self.cur.execute(f"SELECT id_member, member FROM raiting{_capitans} WHERE id_member = ?", (member_id,)).fetchall()
        if len(member) >= 1:
            if member_name == member[0][1]:
                pass
            else:
                self.cur.execute(f"UPDATE raiting{_capitans} SET member = ? WHERE id_member = ?", (member_name, member_id))
        else:
            self.cur.execute(f"INSERT INTO raiting{_capitans}(id_member, member) VALUES (?, ?)", (member_id, member_name))
            self.connection.commit()

    def get_raiting(self, user_id, user_name):
        raiting = self.cur.execute("SELECT raiting FROM raiting WHERE id_member = ?", (user_id,)).fetchone()
        if raiting == None:
            self.cur.execute('INSERT INTO raiting(id_member, member) VALUES (?, ?)', (user_id, user_name))
            self.connection.commit()
            raiting = self.cur.execute("SELECT raiting FROM raiting WHERE id_member = ?", (user_id,)).fetchone()
        return raiting[0]



    def get_raiting_top(self, user_id, user_name, table):
        if user_id == None and user_name == None:
            raiting = self.cur.execute(f"SELECT member, raiting, id_member FROM {table} ORDER BY raiting DESC LIMIT 10 ").fetchall()
        else:
            players = self.cur.execute(f"SELECT raiting FROM {table} WHERE id_member = ?", (user_id,)).fetchone()
            if players == None:
                self.cur.execute(f"INSERT INTO {table}(id_member, member) VALUES (?, ?)", (user_id, user_name))
                self.connection.commit()
            raiting = self.cur.execute(f"SELECT member, raiting, id_member FROM {table} ORDER BY raiting DESC LIMIT 10 ").fetchall()
        top = []
        current_position = 1
        for row in raiting:
            character = dict()
            character['member'] = row[0]
            character['raiting'] = row[1]
            character['id_member'] = row[2]
            character['position'] = current_position
            top.append(character)
            current_position += 1
        return top



    def create_game(self, time, amount_team):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS
        games(
        id_game INTEGER PRIMARY KEY AUTOINCREMENT,
        game_time TEXT,
        amount_team INT,
        result TEXT)""")
        self.cur.execute('INSERT INTO games(game_time, amount_team) VALUES (?, ?)', (time, amount_team ))

        game = self.cur.execute('SELECT id_game  FROM games').fetchall()
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS
        game_{game[-1][0]}(
        discord_member TEXT,
        discord_member_id INT PRIMARY KEY,
        capitan INT,
        team INT)""") # 0 - первая команда, 1 - вторая 2 - третья, 3-я следователь четвертая

        self.connection.commit()
        return game[-1][0]

    def create_next_match(self, game, time, amount_team):
        self.cur.execute('INSERT INTO games(game_time, amount_team) VALUES (?, ?)', (time, amount_team))
        game_next = self.cur.execute('SELECT id_game  FROM games').fetchall()
        self.cur.execute(f"""
               CREATE TABLE IF NOT EXISTS
               game_{game_next[-1][0]}(
               discord_member TEXT,
               discord_member_id INT PRIMARY KEY,
               capitan INT,
               team INT)""")
        last_game  = self.cur.execute(f"SELECT discord_member, discord_member_id, capitan, team  FROM game_{game}").fetchall()
        for raw in last_game:
            self.cur.execute(f"INSERT INTO game_{game_next[-1][0]}(discord_member, discord_member_id, capitan, team) VALUES (?, ?, ?, ?)", (raw[0], raw[1], raw[2], raw[3]))
        self.cur.execute(f"DROP TABLE game_{game}")
        self.connection.commit()
        return game_next[-1][0]

    def get_amount_match(self, game):
        amount = self.cur.execute(f"SELECT amount_team FROM games WHERE id_game = ?",  (game,)).fetchone()
        return amount[0]


    def get_match(self, game):
        member = self.cur.execute(f"SELECT id_game FROM games WHERE id_game = ?",  (game,)).fetchall()
        if len(member) == 0:
            return False
        else:
            return True

    def get_id_players(self, game):
        list_id = self.cur.execute(f"SELECT discord_member_id FROM game_{game}").fetchall()
        return  list_id

    def delete_match(self, game):
        self.cur.execute(f"DROP TABLE game_{game}")
        self.connection.commit()

    def finish_match(self, game, result_game, team, result, config):
        self.cur.execute(f"UPDATE games SET result = ? WHERE id_game = ?", (result_game, game))
        score = self.cur.execute(f"SELECT discord_member_id, team, capitan FROM game_{game} ").fetchall()
        #TODO дичайшик колхоз, исправить
        if result == "Победа":
            for i in score:
                score_player = self.cur.execute(f"SELECT raiting FROM raiting WHERE id_member = ?",  (i[0],)).fetchall()
                score_trener = self.cur.execute(f"SELECT raiting FROM raiting_capitans WHERE id_member = ?", (i[0],)).fetchall()
                if i[1] == team: #Первая командая
                    if i[2] == 1:  # Если капитан
                        result = score_trener[0][0] + config.server.score_win_trener
                        self.cur.execute(f"UPDATE raiting_capitans SET raiting = ? WHERE id_member = ?", (result, i[0]))
                    result = score_player[0][0] + config.server.score_win_player
                    self.cur.execute(f"UPDATE raiting SET raiting = ? WHERE id_member = ?", (result, i[0]))
        elif result == "Поражение":
            for i in score:
                score_player = self.cur.execute(f"SELECT raiting FROM raiting WHERE id_member = ?", (i[0],)).fetchall()
                score_trener = self.cur.execute(f"SELECT raiting FROM raiting_capitans WHERE id_member = ?",  (i[0],)).fetchall()
                if i[1] == team:  # Первая командая
                    if i[2] == 1:  # Если капитан
                        result = score_trener[0][0] + config.server.score_lose_trener
                        self.cur.execute(f"UPDATE raiting_capitans SET raiting = ? WHERE id_member = ?", (result, i[0]))
                    result = score_player[0][0] + config.server.score_lose_player
                    self.cur.execute(f"UPDATE raiting SET raiting = ? WHERE id_member = ?", (result, i[0]))
        elif result == "Ничья":
            for i in score:
                score_player = self.cur.execute(f"SELECT raiting FROM raiting WHERE id_member = ?", (i[0],)).fetchall()
                score_trener = self.cur.execute(f"SELECT raiting FROM raiting_capitans WHERE id_member = ?",  (i[0],)).fetchall()
                if i[1] == team:  # Первая командая
                    if i[2] == 1:  # Если капитан
                        result = score_trener[0][0] + config.server.score_draw_trener
                        self.cur.execute(f"UPDATE raiting_capitans SET raiting = ? WHERE id_member = ?", (result, i[0]))
                    result = score_player[0][0] + config.server.score_draw_player
                    self.cur.execute(f"UPDATE raiting SET raiting = ? WHERE id_member = ?", (result, i[0]))
        self.connection.commit()

    def add_player_in_team(self, game, player, user_id, capitan, team):
        member = self.cur.execute(f"SELECT discord_member_id, capitan FROM game_{game} WHERE discord_member_id = ?", (user_id,)).fetchall()
        if len(member) >= 1:
            if member[0][1] == 1: # Т.е игрок капитан
                self.cur.execute(f"UPDATE game_{game} SET discord_member = ? WHERE discord_member_id = ?", (player, user_id))
            else:
                self.cur.execute(f"UPDATE game_{game} SET (discord_member, capitan, team) = (?,?,?) WHERE discord_member_id = ?", (player, capitan, team, user_id))
        else:
            self.cur.execute(f"INSERT or IGNORE INTO game_{game}(discord_member, discord_member_id, capitan, team) VALUES (?,?,?,?)", (player, user_id, capitan, team))
            self.connection.commit()

    def delete_player(self, game, user_id):
        self.cur.execute(f"DELETE FROM game_{game} WHERE discord_member_id = ?", (user_id,) )
        self.connection.commit()

    def add_capitans(self, game, player):
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS
        capitans_{game}(
        players TEXT)""")
        member = self.cur.execute(f"SELECT players FROM capitans_{game} WHERE players = ?", (player,)).fetchall()
        if len(member) >= 1:
            return True
        else:
            self.cur.execute(f"INSERT INTO  capitans_{game}(players) VALUES (?)", (player,))
            self.connection.commit()
            return False

    def get_capitans(self, game):
        member = self.cur.execute(f"SELECT players FROM capitans_game_{game}").fetchall()
        return(member)

    def get_id_capitan(self, member):
        capitan_id = self.cur.execute("SELECT id_member FROM raiting WHERE member = ?", (member,)).fetchone()
        return capitan_id[0]

    def get_amount_team_capitan(self, member_id, game):
        number = self.cur.execute(f"SELECT team FROM game_{game} WHERE discord_member_id = ?", (member_id,)).fetchone()
        return  number[0]

    def delete_table(self, game):
        self.cur.execute(f"DROP TABLE capitans_game_{game}")

import re
import redis


class Basketball:
    def __init__(self) -> None:
        self.r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
        
    def create_player(self, name, date_of_birth):
        player_id = str(self.r.incr('player_id'))
        
        self.r.hset('player_' + player_id, name, date_of_birth)
        
        self.r.sadd('players', 'player_' + player_id)
        
    def get_player(self, player_id):
        return self.r.hgetall('player_id')
        
    def list_players_with_date_of_birth(self):
        for x in self.r.smembers('players'):
            player = self.r.hgetall(x)
            
            print(player)
                
    def create_contract_with_team(self, player_id, team):
        if not self.r.sismember('players', player_id):
            print('player does not exists')
            return
        
        for x in self.r.smembers('teams'):
            if self.r.sismember(x, player_id):
                print(player_id + ' has already have a contract with a different team')
                return
        
                
        if not self.r.sismember('teams', team):
            self.r.sadd('teams', team)
            
        self.r.sadd(team, player_id)
        
        
    def break_contract_or_delete_team(self, player_id, team):
        if not self.r.sismember('players', player_id):
            print(player_id + ' does not exists')
            return
        
        if not self.r.smismember('teams', team):
            print('team does not exists')
            return          
        
        if self.r.scard(team)==0:
            self.r.srem('teams', team)
            return
            
        self.r.srem(team, player_id)
        
    def get_players_of_team(self, team):
        if not self.r.sismember('teams', team):
            print('team does not exists')
            return
        
        print(team + ':')
        for x in self.r.smembers(team):
            print(self.r.hgetall(x))
            
    def print_teams(self):
        print('Teams: ')
        print(self.r.smembers('teams'))
        
    def announce_match(self, date, place, team_1, team_2):
        if team_1 == team_2:
            print('The same team cannot play against itself')
            return
        
        if not self.r.sismember('teams', team_1) or not self.r.sismember('teams', team_2):
            print('Team/Teams does not exists')
            return
        
        for x in self.r.smembers("matches"):
            match=self.r.hgetall(x)
            if match["date"] == date and match["place"]==place and match['team_1']==team_1 and match['team_2'] == team_2:
                print("Match exists!")
                return
        
        match_id = str(self.r.incr("match_id"))
        self.r.hmset("match_" + match_id, {
            "date": date,
            "place": place,
            "team_1": team_1,
            "team_2": team_2
        })
        
        self.r.sadd('matches', "match_" + match_id)
        
    def print_matches(self):
        for x in self.r.smembers("matches"):
            print(x + ':')
            for y in self.r.hgetall(x).items():
                print(y)
                
        
                

if __name__=="__main__":
    b=Basketball()
    
    # b.create_player('Bela', 20011203)
    # b.create_player('Janos', 20131002)
    # b.create_player('Jeno', 20011203)
    # b.create_player('Boglarka', 20030315)
    # b.create_player('Peter', 20020417)
    
    b.list_players_with_date_of_birth()
    
    
    b.create_contract_with_team('player_14', 'Felcsut')
    b.create_contract_with_team('player_14', 'Felcsut')
    b.create_contract_with_team('player_13', 'Felcsut')
    b.create_contract_with_team('player_15', 'Felcsut')
    
    
    
    b.create_contract_with_team('player_14', 'Fradi')
    b.create_contract_with_team('player_11', 'Fradi')
    b.create_contract_with_team('player_12', 'Fradi')
    
    b.get_players_of_team('Felcsut')
    
    b.print_teams()
    
    b.announce_match('202203122000', 'Fonix', 'Felcsut', "Fradi")
    b.announce_match('202203202000', 'Fonix', 'Fradi', "Felcsut")
    b.announce_match('202203122000', 'Fonix', 'Felcsasddaut', "Fradi")
    b.announce_match('202203122000', 'Fonix', 'Felcsut', "Felcsut")
    
    
    b.print_matches()
import re
import redis


class Basketball:
    def __init__(self) -> None:
        self.r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
        
    def create_player(self, name, date_of_birth):
        player_id = str(self.r.incr('player_id'))
        
        self.r.hset('player_' + player_id, name, date_of_birth)
        
        self.r.sadd('players', 'player_' + player_id)
        
    def get_player(self, )
        
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
                print('player has already a contract with a different team')
                return
                
        if not self.r.sismember('teams', team):
            self.r.sadd('teams', team)
            
        self.r.sadd(team, player_id)
        
        
    def break_contract(self, player_id, team):
        if not self.r.sismember('players', player_id):
            print('player does not exists')
            return
        
        if not self.r.smismember('teams', team):
            print('team does not exists')
            return          
        
        if self.r.scard(team)==0:
            self.r.srem('teams', team)
            return
            
        self.r.srem(team, player_id)
        
        
                

if __name__=="__main__":
    b=Basketball()
    
    # b.create_player('Bela', 20011203)
    # b.create_player('Janos', 20131002)
    # b.create_player('Jeno', 20011203)
    # b.create_player('Boglarka', 20030315)
    # b.create_player('Peter', 20020417)
    
    b.list_players_with_date_of_birth()
    
    
    
    
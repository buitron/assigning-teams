import random


class TeamSelection:
    '''
    Class instructions, what is this class about???
    '''

    def __init__(self, team_players=None, num_players=None, team_leaders=None, num_leaders=None, non_leaders=None, num_teams=None, narration=None):
        self.team_players = team_players
        self.num_players = num_players
        self.team_leaders = team_leaders
        self.num_leaders = num_leaders
        self.non_leaders = non_leaders
        self.num_teams = num_teams

        # narration takes a dictionary
        self.narration = narration


    # prints narration dialogue
    def narrate(self, act, **kwargs):
        if not kwargs:
            kwargs = self.narration

        print(kwargs[act])


    # prints choosing validations
    def choice(self, num, instruction):
        while True:
            try:
                selection = int(input(f'\n{instruction} > '))
                while True:
                    if selection <= num:
                        break
                    selection = int(input(f'please make a valid selection [whole number <= {num}] > '))
                return selection
            except ValueError:
                print('please input a whole number, thanks.')


    # prints all players
    def show_players(self, _dict):
        print('-' * 20)
        for i in _dict.items():
            print(f'{i[0]}: {i[1]}')


    # prints selected team leaders
    def show_leaders(self, _list):
        print('\n\nteam leaders:')
        for i in range(len(_list)):
            print(f'leader_{i + 1}: {_list[i]}')


    # prints players that are selected to be team leaders
    def show_non_leaders(self, _list):
        print('\n\nother players:')
        for i in range(len(_list)):
            print(f'player_{i + 1}: {_list[i]}')


    # prints finalized teams!
    def show_teams(self, _dict):
        print('-' * 20)
        print('FINAL TEAMS')
        count = 1
        for i in _dict.items():
            print(f'team #{count}|| team leader: {i[0]} -> team players: {i[1]}')
            count += 1


    # generates num_players
    def players(self, num_players=None):
        if num_players is None:
            num_players = self.num_players

        while True:
            try:
                num_players = int(input('number of players > '))
                self.num_players = num_players
                break
            except ValueError:
                print('please input an whole number, thanks.')

        if num_players is None:
            num_players = self.num_players

        team_players = {}
        for i in range(num_players):
            team_players[f'player_{i + 1}'] = input(f'player #{i + 1} name > ')

        self.team_players = team_players
        return team_players, num_players


    # adjusts players
    def players_modify(self, num_players=None, team_players=None):
        if num_players is None:
            num_players = self.num_players
        if team_players is None:
            team_players = self.team_players

        while True:
            decision = input('\nwant to make any changes? [y]es or [n]o > ')
            if decision.lower() in ['y', 'n']:
                break
            else:
                print('\nplease type either \'y\' for yes or \'n\' for no, thanks.')

        while decision.lower() == 'y':
            selection = self.choice(num_players, 'please select the player number to change the name')

            new_name = input('name change > ')
            team_players[f'player_{selection}'] = new_name

            self.show_players(team_players)

            while True:
                decision = input('want to make any changes? [y]es or [n]o > ')
                if decision.lower() in ['y', 'n']:
                    break
                else:
                    print('\nplease type either \'y\' for yes or \'n\' for no, thanks.')

        self.team_players = team_players
        return team_players


    # generates num_leaders and team_leaders
    def leaders(self, team_players=None, num_players=None, team_leaders=None):
        if team_players is None:
            team_players = self.team_players
        if num_players is None:
            num_players = self.num_players
        if team_leaders is None:
            team_leaders = self.team_leaders

        num_leaders = int(input('\nnumber of team leaders > '))
        self.num_leaders = num_leaders

        team_leaders = []
        name = ''
        count = 1
        for _ in range(num_leaders):
            self.show_players(team_players)
            selection = self.choice(num_players, f'please select team leader #{count} player number')
            name = team_players[f'player_{selection}']

            while name in team_leaders:
                selection = self.choice(num_players, 'please select a team leader player number that isn\'t already selected > ')
                name = team_players[f'player_{selection}']

            team_leaders.append(name)
            count += 1

        self.team_leaders = team_leaders
        self.show_leaders(team_leaders)

        non_leaders = [i[1] for i in team_players.items() if i[1] not in team_leaders]
        self.non_leaders = non_leaders
        self.show_non_leaders(non_leaders)

        return team_leaders, num_leaders, non_leaders


    # generates manual selected num_teams
    def team_sizes(self, num_leaders=None):
        if num_leaders is None:
            num_leaders = self.num_leaders

        while True:
            decision = input('\ndo you want to manually select the number of teams? [y]es or [n]o > ')
            if decision.lower() in ['y', 'n']:
                break
            else:
                print('\nplease type either \'y\' for yes or \'n\' for no, thanks.')

        if decision.lower() == 'y':
            while True:
                try:
                    num_teams = int(input('number of teams > '))
                    if num_teams <= num_leaders:
                        self.num_teams = num_teams
                        return num_teams
                    else:
                        print('please select a number less than the number of team leaders.')
                except ValueError:
                    print('please input an whole number, thanks.')
        else:
            self.num_teams = num_leaders
            return num_leaders


    # generate teams! DONE!
    def divide_teams(self, team_leaders=None, non_leaders=None, num_teams=None):
        if team_leaders is None:
            team_leaders = self.team_leaders
        if non_leaders is None:
            non_leaders = self.non_leaders
        if num_teams is None:
            num_teams = self.num_teams

        teams = {}
        random.shuffle(team_leaders)
        random.shuffle(non_leaders)
        _players = non_leaders
        players_per = round(len(non_leaders)/num_teams)
        for i in range(num_teams):
            teams[f'{team_leaders[i]}'] = _players[:players_per]
            _players = _players[players_per:]

        # adding non included non_leaders to existing teams
        _included_players = []
        for i in teams.values():
            _included_players += i

        _not_included = list(set(_players) - set(_included_players))
        random.shuffle(_not_included)
        while _not_included:
            for i in teams.values():
                i += _not_included[:1]
                _not_included = _not_included[1:]

        # adding non included leaders to existing teams
        _not_included_leaders = [i for i in team_leaders if i not in list(teams.keys())]
        random.shuffle(_not_included_leaders)
        while _not_included_leaders:
            for i in teams.values():
                i += _not_included_leaders[:1]
                _not_included_leaders = _not_included_leaders[1:]

        self.show_teams(teams)
        return teams


if __name__ == '__main__':
    intro = '''
    Welcome to this cool random team generator!
    If you find any bugs please let me know @ alex@buitron.com :D
    '''
    outro = f'''
    Thank you for using my app. Please check out my website and github
    @ https://www.alexbuitron.com & https://www.github.com/buitron
    '''
    k = TeamSelection(narration = {'intro': intro, 'outro': outro})
    k.narrate('intro')
    k.players()
    k.players_modify()
    k.leaders()
    k.team_sizes()
    k.divide_teams()
    k.narrate('outro')

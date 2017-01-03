import json
from os import path
import __main__

config = json.load(
    open(path.join(path.dirname(__main__.__file__), 'config', 'butler.json')))

def cutoff(score):
    sign = 1 if score > 0 else -1
    score = abs(score)
    if score > config['cutoff_point']:
        score -= config['cutoff_point']
        score *= config['cutoff_rate']
        score += config['cutoff_point']
    return score * sign

def get_opponents(butler, player):
    table = butler.table
    if player in [table.openE, table.openW]:
        return [table.openN, table.openS]
    if player in [table.openN, table.openS]:
        return [table.openE, table.openW]
    if player in [table.closeE, table.closeW]:
        return [table.closeN, table.closeS]
    if player in [table.closeN, table.closeS]:
        return [table.closeE, table.closeW]

def get_room(butler, player):
    table = butler.table
    if player in [table.openE, table.openW, table.openN, table.openS]:
        return 'open'
    if player in [table.closeE, table.closeW, table.closeN, table.closeS]:
        return 'closed'

def normalize(butler):
    if butler.board_count == 0:
        return 0.0
    return (
        butler.cut_score / butler.board_count
        + butler.opp_score * config['opponent_factor']
    ) * butler.board_count

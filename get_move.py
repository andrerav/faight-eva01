import random as r

# def _get_move(ai,map):

#     avail_pellet_moves = []
#     avail_new_moves = []
#     avail_old_moves = []

#     for possible_move in ai.possible_moves:

#         # Just do this move if it's a super pellet
#         if possible_move in map.super_pellets_positions:
#             return map.get_move_between(ai.you.pos, possible_move)

#         # Record possible pellet move
#         elif possible_move in map.pellet_positions:
#             avail_pellet_moves.append(possible_move)

#         if ai.history.contains(possible_move):
#             avail_old_moves.append(possible_move)
#         else: avail_new_moves.append(possible_move)

#     if len(avail_pellet_moves) > 0: move = r.choice(avail_pellet_moves)
#     else: move = r.choice(avail_new_moves) if len(avail_new_moves) > 0 else r.choice(avail_old_moves)


#     return map.get_move_between(ai.you.pos, move)
rows = {
        1: {
            1: [(15,15)],
            2: [(15,14), (14,15)],
            3: [(15,13), (14,14), (13,15)],
            4: [(15,12), (14,13), (13,14), (12,15)],
            5: [(15,11), (14,12), (13,13), (12,14), (11,15)],
            6: [(14,11), (13,12), (12,13), (11,14)],
        },
        2: {
            1: [(0,0)],
            2: [(0,1), (1,0)],
            3: [(0,2), (1,1), (2,0)],
            4: [(0,3), (1,2), (2,1), (3,0)],
            5: [(0,4), (1,3), (2,2), (3,1), (4,0)],
            6: [(1,4), (2,3), (3,2), (4,1)],
        },
    }


def in_place(board, player):
    placed = []  # List to store positions of player's pieces
    empty = 0  # Counter for empty positions
    for lane in rows[player]:
        for fields in rows[player][lane]:
            if board[fields[0]][fields[1]] == player:
                placed.append(fields)  # Add position to placed list
            elif board[fields[0]][fields[1]] != player:
                empty += 1  # Increment empty counter
        if empty != 0:
            return placed  # Return placed list if any empty positions
    return placed  # Return placed list if all positions are filled
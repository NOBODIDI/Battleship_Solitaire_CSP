import sys
import copy
import argparse

def display(board):
    """
    Display the board
    Used for debugging
    """
    for i in board:
        for j in i:
            print(j, end="")
        print("")
    print("")

def valid(x, y, board): 
    """
    Check if the coordinate is valid for that board
    """
    if x < 0 or x >= len(board[0]):
        return False
    if y < 0 or y >= len(board):
        return False
    return True

def board_valid(row_constraint, col_constraint, board): 
    """
    Check if the board is valid: 
    - row constraint is met
    - col constraint is met
    - no two ships are adjacent
    """
    # Row constraint
    for i, row in enumerate(board): 
        X_row = O_row = 0
        for j, char in enumerate(row): 
            if char == 'X': 
                X_row += 1
            if char == '0': 
                O_row += 1
        if X_row != row_constraint[i] and O_row == 0: 
            return False
        elif X_row + O_row < row_constraint[i]: 
            return False

    # Column constraint
    for i in range(len(board)):
        X_col = O_col = 0
        for j in range(len(board)):
            if board[j][i] == 'X': 
                X_col += 1
            if board[j][i] == '0': 
                O_col += 1
        if X_col > col_constraint[i]:
            return False
        elif X_col + O_col < col_constraint[i]: 
            return False
        
    # Diagonal constraint
    for i, row in enumerate(board): 
        for j, char in enumerate(row): 
            if char == 'X': 
                if valid(i-1, j-1, board) and board[i-1][j-1] == 'X': 
                    return False
                if valid(i-1, j+1, board) and board[i-1][j+1] == 'X': 
                    return False
                if valid(i+1, j-1, board) and board[i+1][j-1] == 'X': 
                    return False
                if valid(i+1, j+1, board) and board[i+1][j+1] == 'X': 
                    return False
    return True

def place_ships(ship_constraint, board):
    """
    Check if the ships are placed correctly according to the constraints
    """
    temp_board = copy.deepcopy(board)
    ships, temp_board = poscount_ships(temp_board)
    if ships == ship_constraint:
        return True
    return False

def poscount_ships(board):
    """
    Count the number of ships of each type on the board
    """
    ships = [0, 0, 0, 0]
    for i, line in enumerate(board):
        for j, ch in enumerate(line):
            if ch == 'X':
                if i+1 < len(board) and board[i+1][j] == 'X':
                    if i+2 < len(board) and board[i+2][j] == 'X':
                        if i+3 < len(board) and board[i+3][j] == 'X':
                            ships[3] += 1
                            board[i][j] = '^'
                            board[i+1][j] = 'M'
                            board[i+2][j] = 'M'
                            board[i+3][j] = 'v'
                        else:
                            ships[2] += 1
                            board[i][j] = '^'
                            board[i+1][j] = 'M'
                            board[i+2][j] = 'v'
                    else:
                        ships[1] += 1
                        board[i][j] = '^'
                        board[i+1][j] = 'v'
                elif (j+1) < (len(board)) and board[i][j+1] == 'X':
                    if j+2 < len(board) and board[i][j+2] == 'X':
                        if j+3 < len(board) and board[i][j+3] == 'X':
                            ships[3] += 1
                            board[i][j] = '<'
                            board[i][j+1] = 'M'
                            board[i][j+2] = 'M'
                            board[i][j+3] = '>'
                        else:
                            ships[2] += 1
                            board[i][j] = '<'
                            board[i][j+1] = 'M'
                            board[i][j+2] = '>'
                    else:
                        ships[1] += 1
                        board[i][j] = '<'
                        board[i][j+1] = '>'
                else:
                    ships[0] += 1
                    board[i][j] = 'S'
    return ships, board

def backtrack(O_val, row_constraint, col_constraint, ship_constraint, board):
    """
    Backtracking algorithm to find the solution for the board
    """
    if len(O_val) == 0:
        if board_valid(row_constraint, col_constraint, board) and place_ships(ship_constraint, board):
            return board
        else:
            return None
    else:
        x, y = O_val[0]
        board[x][y] = '.'
        if board_valid(row_constraint, col_constraint, board):
            temp_board = backtrack(O_val[1:], row_constraint, col_constraint, ship_constraint, board)
            if temp_board != None:
                return board
        board[x][y] = 'X'
        if board_valid(row_constraint, col_constraint, board):
            temp_board = backtrack(O_val[1:], row_constraint, col_constraint, ship_constraint, board)
            if temp_board != None:
                return board
    O_val.append((x, y))
    board[x][y] = '0'
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    # Parse board and ships info
    with open(args.inputfile, "r") as in_file:
        b = in_file.read()
    b2 = b.split()
    size = len(b2[0]) + 2
    b3 = ['0' + b2[0] + '0', '0' + b2[1] + '0', b2[2] + ('0' if len(b2[2]) == 3 else '')] + b2[3:]
    board = "\n".join(b3)

    row_constraint = [int(b2[0][i]) for i in range(len(b2[0]))]
    col_constraint = [int(b2[1][i]) for i in range(len(b2[1]))]
    ship_constraint = [int(b2[2][i]) for i in range(len(b2[2]))]

    board = board.split()[3:]
    board = [list(i) for i in board]

    # Preprocess the board
    for i in range(len(col_constraint)): 
        if col_constraint[i] == 0: 
            for j in range(len(board)): 
                if board[j][i] == '0': 
                    board[j][i] = '.'
    for i in range(len(row_constraint)):
        if row_constraint[i] == 0: 
            for j in range(len(board[i])):
                if board[i][j] == '0': 
                    board[i][j] = '.'
    for i in range(len(board[0])):
        for j in range(len(board)):
            if board[i][j] == 'S': 
                board[i][j] = 'X'
                if valid(i-1, j-1, board):
                    board[i-1][j-1] = '.'
                if valid(i, j-1, board):
                    board[i][j-1] = '.'
                if valid(i+1, j-1, board):
                    board[i+1][j-1] = '.'
                if valid(i-1, j, board):
                    board[i-1][j] = '.'
                if valid(i+1, j, board):
                    board[i+1][j] = '.'
                if valid(i-1, j+1, board):
                    board[i-1][j+1] = '.'
                if valid(i, j+1, board):
                    board[i][j+1] = '.'
                if valid(i+1, j+1, board):
                    board[i+1][j+1] = '.'
            if board[i][j] == '<':
                board[i][j] = 'X'
                if valid(i, j+1, board): 
                    board[i][j+1] = 'X'
                if valid(i-1, j-1, board):
                    board[i-1][j-1] = '.'
                if valid(i, j-1, board):
                    board[i][j-1] = '.'
                if valid(i+1, j-1, board):
                    board[i+1][j-1] = '.'
                if valid(i-1, j, board):
                    board[i-1][j] = '.'
                if valid(i+1, j, board):
                    board[i+1][j] = '.'
                if valid(i-1, j+1, board):
                    board[i-1][j+1] = '.'
                if valid(i+1, j+1, board):
                    board[i+1][j+1] = '.'
            if board[i][j] == '>':  
                board[i][j] = 'X' 
                if valid(i, j-1, board): 
                    board[i][j-1] = 'X'
                if valid(i-1, j-1, board):
                    board[i-1][j-1] = '.'
                if valid(i+1, j-1, board):
                    board[i+1][j-1] = '.'
                if valid(i-1, j, board):
                    board[i-1][j] = '.'
                if valid(i+1, j, board):
                    board[i+1][j] = '.'
                if valid(i-1, j+1, board):
                    board[i-1][j+1] = '.'
                if valid(i, j+1, board):
                    board[i][j+1] = '.'
                if valid(i+1, j+1, board):
                    board[i+1][j+1] = '.'
            if board[i][j] == '^':
                board[i][j] = 'X'
                if valid(i+1, j, board): 
                    board[i+1][j] = 'X'
                if valid(i-1, j-1, board):
                    board[i-1][j-1] = '.'
                if valid(i, j-1, board):
                    board[i][j-1] = '.'
                if valid(i+1, j-1, board):
                    board[i+1][j-1] = '.'
                if valid(i-1, j, board):
                    board[i-1][j] = '.'
                if valid(i-1, j+1, board):
                    board[i-1][j+1] = '.'
                if valid(i, j+1, board):
                    board[i][j+1] = '.'
                if valid(i+1, j+1, board):
                    board[i+1][j+1] = '.'  
            if board[i][j] == 'v':
                board[i][j] = 'X'
                if valid(i-1, j, board): 
                    board[i-1][j] = 'X'
                if valid(i-1, j-1, board):
                    board[i-1][j-1] = '.'
                if valid(i, j-1, board):
                    board[i][j-1] = '.'
                if valid(i+1, j-1, board):
                    board[i+1][j-1] = '.'
                if valid(i+1, j, board):
                    board[i+1][j] = '.'
                if valid(i-1, j+1, board):
                    board[i-1][j+1] = '.'
                if valid(i, j+1, board):
                    board[i][j+1] = '.'
                if valid(i+1, j+1, board):
                    board[i+1][j+1] = '.' 
            if board[i][j] == 'M':
                board[i][j] = 'X'
                if valid(i-1, j-1, board):
                    board[i-1][j-1] = '.'
                if valid(i+1, j-1, board):
                    board[i+1][j-1] = '.'
                if valid(i-1, j+1, board):
                    board[i-1][j+1] = '.'
                if valid(i+1, j+1, board):
                    board[i+1][j+1] = '.' 

    # Find list of '0' coordinates
    O_vars = [(i, j) for i, line in enumerate(board) for j, char in enumerate(line) if char == '0']

    # Find solution for 'X' placement by backtracking
    sol_board = backtrack(O_vars, row_constraint, col_constraint, ship_constraint, board)
    if sol_board is None:
        print("No solution found")
    else: 
        _, sol = poscount_ships(sol_board)
        with open(args.outputfile, "w") as out_file:
            for i in sol_board:
                for j in i:
                    out_file.write(j)
                out_file.write('\n')
        out_file.close()

import random

# Ustawienia planszy
BOARD_SIZE = 3
EMPTY_CELL = "-"

# Funkcja do pobierania symbolu gracza
def get_player_symbol():
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Chcesz grać krzyżykami czy kółkami? (X/O)')
        letter = input().upper()
    return letter

# Inicjalizacja gry
PLAYER_SYMBOL = get_player_symbol()
COMPUTER_SYMBOL = "X" if PLAYER_SYMBOL == "O" else "O"

# Funkcja do rysowania planszy
def draw_board(board):
    print("\n".join([" ".join(row) for row in board]))

def get_player_move(board):
    while True:
        move = input("Podaj numer wiersza i kolumny oddzielonych spacją (np. 1 2): ")
        try:
            row, col = map(int, move.split())
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Numer wiersza i kolumny muszą być liczbami całkowitymi z zakresu od 0 do 2.")
            elif board[row][col] != EMPTY_CELL:
                print("To pole jest już zajęte.")
            else:
                return (row, col)
        except ValueError:
            print("Niepoprawny format. Numer wiersza i kolumny muszą być oddzielone spacją i być liczbami całkowitymi z zakresu od 0 do 2.")

# Funkcja do wyboru najlepszego ruchu przez komputer za pomocą algorytmu minimax
def get_computer_move(board):
    best_score = -float("inf")
    best_move = None
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY_CELL:
                board[i][j] = COMPUTER_SYMBOL
                score = miniMax(False, board)
                board[i][j] = EMPTY_CELL
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

# Funkcja do szukania zwyciezcy (odwrócona logika klasycznego kółko i krzyzyk)
def get_winner(board):
    for i in range(BOARD_SIZE):
        # Sprawdzenie wierszy
        if board[i][0] != EMPTY_CELL and any(all(board[i][j+k] == board[i][0] for k in range(3)) for j in range(BOARD_SIZE-2)):
            return COMPUTER_SYMBOL if board[i][0] == PLAYER_SYMBOL else PLAYER_SYMBOL
        # Sprawdzenie kolumn
        if board[0][i] != EMPTY_CELL and any(all(board[j+k][i] == board[0][i] for k in range(3)) for j in range(BOARD_SIZE-2)):
            return COMPUTER_SYMBOL if board[0][i] == PLAYER_SYMBOL else PLAYER_SYMBOL
    # Sprawdzenie przekątnych
    if board[0][0] != EMPTY_CELL and any(all(board[i+k][i+k] == board[0][0] for k in range(3)) for i in range(BOARD_SIZE-2)):
        return COMPUTER_SYMBOL if board[0][0] == PLAYER_SYMBOL else PLAYER_SYMBOL
    if board[0][BOARD_SIZE-1] != EMPTY_CELL and any(all(board[i+k][BOARD_SIZE-1-i-k] == board[0][BOARD_SIZE-1] for k in range(3)) for i in range(BOARD_SIZE-2)):
        return COMPUTER_SYMBOL if board[0][BOARD_SIZE-1] == PLAYER_SYMBOL else PLAYER_SYMBOL
    # Brak zwycięzcy
    return None


# Algorytm minimax 
def miniMax(maximizingPlayer, board):
    winner = get_winner(board)
    if winner == COMPUTER_SYMBOL:
        return 1
    elif winner == PLAYER_SYMBOL:
        return -1
    elif all(board[i][j] != EMPTY_CELL for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
        return 0
    elif maximizingPlayer:
        best_score = -float("inf")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY_CELL:
                    board[i][j] = COMPUTER_SYMBOL
                    score = miniMax(False, board)
                    board[i][j] = EMPTY_CELL
                    best_score = max(best_score, score)
        return best_score
    else:
        worst_score = float("inf")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY_CELL:
                    board[i][j] = PLAYER_SYMBOL
                    score = miniMax(True, board)
                    board[i][j] = EMPTY_CELL
                    worst_score = min(worst_score, score)
        return worst_score

def main():
    while True:
        # Inicjalizacja planszy
        board = [[EMPTY_CELL] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        # Wybór, kto zaczyna
        player_turn = input("Czy chcesz zacząć pierwszy? Wpisz 'tak' lub 'nie': ")
        if player_turn.lower() in ['tak', 't']:
            player_turn = True
        else:
            player_turn = False
        # Pętla gry
        while True:
            draw_board(board)
            # Ruch gracza
            if player_turn:
                print("Ruch gracza (" + PLAYER_SYMBOL +")")
                move = get_player_move(board)
                board[move[0]][move[1]] = PLAYER_SYMBOL
            # Ruch komputera
            else:
                print("Ruch komputera (" + COMPUTER_SYMBOL +")")
                move = get_computer_move(board)
                board[move[0]][move[1]] = COMPUTER_SYMBOL
            # Sprawdzenie zwycięstwa lub remisu
            winner = get_winner(board)
            if winner is not None:
                draw_board(board)
                print("Zwycięzca: {}".format(winner))
                break
            elif all(board[i][j] != EMPTY_CELL for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
                draw_board(board)
                print("Remis!")
                break
            # Przekazanie ruchu
            player_turn = not player_turn
        
        # Pytanie o rozpoczęcie nowej gry lub wyjście z programu
        while True:
            play_again = input("Czy chcesz zagrać jeszcze raz? Wpisz 'tak' lub 'nie': ")
            if play_again.lower() in ['tak', 't']:
                break
            elif play_again.lower() in ['nie', 'n']:
                return
            else:
                print("Niepoprawna odpowiedź. Spróbuj jeszcze raz.")

if __name__ == "__main__":
    main()

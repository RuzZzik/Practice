# Фигура.
class Piece:
    WHITE = 1
    BLACK = -1

    # ответ на is_valid()
    TRUE: int = 1
    FALSE: int = 0

    # была ли фигура сдвинута
    moved: bool = False

    # символ фигуры (k) для короля
    symbol: str

    # символ подсвеченной фигуры (когда она стоит под боем выбранной фигуры)
    highlighted: str
    capital_highlighted: str

    # цвет игрока
    color: int

    def __init__(self, color: int = WHITE):
        self.color = color

    def is_valid(self, move, board) -> int:
        return self.TRUE

    def get_symbol(self, highlighted: bool = False) -> str:
        if highlighted:
            if self.color == self.WHITE:
                return self.capital_highlighted
            else:
                return self.highlighted
        else:
            if self.color == self.WHITE:
                return self.symbol.upper()
            else:
                return self.symbol


# Ход.
class Move:
    # ход: невозможен или отмена
    IMPOSSIBLE: int = -2
    CANCEL: int = -1

    # фигура, делающая ход
    piece: None

    # позиция фигуры
    start: tuple[int, int] = (IMPOSSIBLE, IMPOSSIBLE)

    # позиция фигуры после хода
    target: tuple[int, int] = (IMPOSSIBLE, IMPOSSIBLE)

    # позиция поглощённой фигуры
    captured: tuple[int, int] = None

    # поглощённая фигура
    captured_piece: Piece = None

    # рокировка или потенциально другой необычный ход
    castled: bool = False

    # в начале хода, какого класса была фигура (для пешки по достижению дальней горизонтали)
    before: type = type(None)


# 2D Доска/поле.
class Board:
    width: int
    height: int
    board: list[list[Piece]]
    moves: list[Move] = list[Move]()

    def __init__(self, width: int = 8, height: int = 8):
        self.width = width
        self.height = height
        self.board = [[None for _ in range(width)] for _ in range(height)]


# Игра на 2D игровой доске для двух поочередно ходящих игроков.
class Game:
    board: Board
    current_player: int = Piece.WHITE

    # названия игроков
    player_strings: dict[int, str] = {Piece.WHITE: "Белый", Piece.BLACK: "Чёрный"}

    # подсвечивать ли ходы под аттакой выбранной фигуры
    highlight_moves: bool = False

    def __init__(self):
        pass

    def start(self):
        self._print()

    def _correct(self, move: Move) -> bool:
        return True

    def _print_board(self, start: tuple[int, int] = (-1, -1)):
        pass

    def _make_move(self, move: Move) -> bool:
        return False

    def _cancel_move(self):
        pass

    # конвертация ввода из строки в координаты на доске
    def _convert(self, xy: str) -> tuple[int, int]:
        return 0, 0

    def _next_player(self):
        if self.current_player == Piece.WHITE:
            self.current_player = Piece.BLACK
        else:
            self.current_player = Piece.WHITE

    def _next_move(self, move: Move) -> int:
        if self._correct(move):
            if self._make_move(move):
                print("Шах!")
                b: bool = False
                for h in range(self.board.height):
                    for w in range(self.board.width):
                        r = self.board.board[w][h]
                        if r is None:
                            continue
                        if r.color == move.piece.color:
                            continue
                        move2: Move = Move()
                        move2.piece = r
                        move2.start = (w, h)
                        for h2 in range(self.board.height):
                            for w2 in range(self.board.width):
                                move2.target = (h2, w2)
                                if self._correct(move2):
                                    b = True
                if not b:    
                    print("Мат!")
                    exit()
            self._next_player()
        else:
            print("Невозможный ход!")
            return Piece.FALSE
        return Piece.TRUE

    #процесс игры
    def _print(self):
        self._print_board()
        print()
        print(f"Ходит: {self.player_strings[self.current_player]}")
        move: Move = Move()
        move.start = self._convert(
            input("Введите начальную позицию фигуры (Enter для отмены ПРОШЛОГО хода): ")
        )
        if move.start[0] == move.IMPOSSIBLE:
            print("Невозможная стартовая позиция!")
            self._print()
            return
        elif move.start[0] == move.CANCEL:
            if len(self.board.moves) >= 1:
                self._cancel_move()
                print("Отмена ПРОШЛОГО хода!")
                self._next_player()
            else:
                time: int = 3
                print(f"Нет ходов для отмены!")
            self._print()
            return
        else:
            print()
            self.highlight_moves = True
            self._print_board(move.start)
            print()
            self.highlight_moves = False
            move.piece = self.board.board[move.start[0]][move.start[1]]
            move.target = self._convert(
                input(
                    "Введите целевую позицию фигуры (Enter для отмены ТЕКУЩЕГО хода): "
                )
            )
            if move.target[0] == move.IMPOSSIBLE:
                print("Невозможная целевая позиция!")
                self._print()
                return
            elif move.target[0] == move.CANCEL:
                print("Отмена ТЕКУЩЕГО хода!")
                self._print()
                return
            else:
                self._next_move(move)
                self._print()
                return
                

# Конь
class Knight(Piece):
    symbol: str = "n"
    capital_highlighted: str = "Ⓝ"
    highlighted: str = "ⓝ"

    def is_valid(self, move: Move, board: Board) -> int:
        valid_moves: list[tuple[int]] = [
            (1, 2),
            (2, 1),
            (1, -2),
            (-2, 1),
            (-1, 2),
            (2, -1),
            (-1, -2),
            (-2, -1),
        ]

        for v in valid_moves:
            if (
                move.start[0] + v[0] == move.target[0]
                and move.start[1] + v[1] == move.target[1]
            ):
                # аналогично ниже:
                # если нет фигуры в целевой позиции, всё ок
                if board.board[move.target[0]][move.target[1]] is None:
                    break

                # если цвет фигуры в целевой позиции совпадает с фигурой в начальной позиции... ход невозможен
                if board.board[move.target[0]][move.target[1]].color == self.color:
                    return self.FALSE

                move.captured = move.target
                move.captured_piece = board.board[move.target[0]][move.target[1]]
                break
        else:
            return self.FALSE

        return self.TRUE


# Слон
class Bishop(Piece):
    symbol: str = "b"
    capital_highlighted: str = "Ⓑ"
    highlighted: str = "ⓑ"

    def is_valid(self, move: Move, board: Board) -> int:
        if abs(move.target[0] - move.start[0]) != abs(move.target[1] - move.start[1]):
            return self.FALSE
        r1: range
        r2: range
        if move.start[0] < move.target[0]:
            r1 = range(move.start[0] + 1, move.target[0])
        elif move.start[0] > move.target[0]:
            r1 = range(move.start[0] - 1, move.target[0], -1)
        if move.start[1] < move.target[1]:
            r2 = range(move.start[1] + 1, move.target[1])
        elif move.start[1] > move.target[1]:
            r2 = range(move.start[1] - 1, move.target[1], -1)
        for i in range(len(r1)):
            if board.board[r1[i]][r2[i]] is not None:
                return self.FALSE
        if board.board[move.target[0]][move.target[1]] is not None:
            if board.board[move.target[0]][move.target[1]].color == self.color:
                return self.FALSE
            # king
            move.captured = move.target
            move.captured_piece = board.board[move.target[0]][move.target[1]]
        return self.TRUE


# Ладья
class Rook(Piece):
    symbol: str = "r"
    capital_highlighted: str = "Ⓡ"
    highlighted: str = "ⓡ"

    def is_valid(self, move: Move, board: Board) -> int:
        if move.target[0] - move.start[0] == 0:
            if move.start[1] == move.target[1]:
                return self.FALSE
            if move.start[1] < move.target[1]:
                for i in range(move.start[1] + 1, move.target[1]):
                    if board.board[move.start[0]][i] is not None:
                        return self.FALSE
            if move.start[1] > move.target[1]:
                for i in range(move.target[1] + 1, move.start[1]):
                    if board.board[move.start[0]][i] is not None:
                        return self.FALSE
            if board.board[move.target[0]][move.target[1]] is None:
                pass
            else:
                if self.color == board.board[move.target[0]][move.target[1]].color:
                    return self.FALSE
                # king
                move.captured = move.target
                move.captured_piece = board.board[move.target[0]][move.target[1]]
        elif move.target[1] - move.start[1] == 0:
            if move.start[0] == move.target[0]:
                return self.FALSE
            if move.start[0] < move.target[0]:
                for i in range(move.start[0] + 1, move.target[0]):
                    if board.board[i][move.start[1]] is not None:
                        return self.FALSE
            if move.start[0] > move.target[0]:
                for i in range(move.target[0] + 1, move.start[0]):
                    if board.board[i][move.start[1]] is not None:
                        return self.FALSE
            if board.board[move.target[0]][move.target[1]] is None:
                pass
            else:
                if self.color == board.board[move.target[0]][move.target[1]].color:
                    return self.FALSE
                # king
                move.captured = move.target
                move.captured_piece = board.board[move.target[0]][move.target[1]]
        else:
            return self.FALSE
        return self.TRUE


# Король
class King(Piece):
    symbol: str = "k"
    capital_highlighted: str = "Ⓚ"
    highlighted: str = "ⓚ"

    castled: bool = False
    to_castle: bool = False
    rook_xy: tuple[int, int] = (None, None)
    rook_to_xy: tuple[int, int] = (None, None)

    def is_valid(self, move: Move, board: Board) -> int:
        valid_moves: list[tuple[int]] = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]

        for v in valid_moves:
            if (
                move.start[0] + v[0] == move.target[0]
                and move.start[1] + v[1] == move.target[1]
            ):
                if board.board[move.target[0]][move.target[1]] is None:
                    break
                if board.board[move.target[0]][move.target[1]].color == self.color:
                    return self.FALSE

                move.captured = move.target
                move.captured_piece = board.board[move.target[0]][move.target[1]]
                break
        else:
            # рокировка
            # проверка необходимых условий для рокировки и её корректности
            if self.moved or self.castled:
                return self.FALSE
            if move.start[1] != move.target[1]:
                return self.FALSE
            if move.start[1] != 0 and move.start[1] != 7:
                return self.FALSE
            if self.castled:
                return self.FALSE
            if move.target[0] - move.start[0] == 2:
                if move.start[0] + 3 >= board.width:
                    return self.FALSE
                r = board.board[move.start[0] + 3][move.start[1]]
                if type(r) != Rook:
                    return self.FALSE
                if r.moved:
                    return self.FALSE
                if r.color != self.color:
                    return self.FALSE
                r = board.board[move.start[0] + 1][move.start[1]]
                if r is not None:
                    return self.FALSE
                r = board.board[move.start[0] + 2][move.start[1]]
                if r is not None:
                    return self.FALSE
                # сохранить ладью, с которой была рокировка (ниже аналогично)
                self.rook_xy = (move.start[0] + 3, move.start[1])
                self.rook_to_xy = (move.start[0] + 1, move.start[1])
                # указание, чтобы make_move сделал рокировку
                self.to_castle = True
            elif move.target[0] - move.start[0] == -2:
                if move.start[0] - 4 < 0:
                    return self.FALSE
                r = board.board[move.start[0] - 4][move.start[1]]
                if type(r) != Rook:
                    return self.FALSE
                if r.moved:
                    return self.FALSE
                if r.color != self.color:
                    return self.FALSE
                r = board.board[move.start[0] - 1][move.start[1]]
                if r is not None:
                    return self.FALSE
                r = board.board[move.start[0] - 2][move.start[1]]
                if r is not None:
                    return self.FALSE
                r = board.board[move.start[0] - 3][move.start[1]]
                if r is not None:
                    return self.FALSE
                self.rook_xy = (move.start[0] - 4, move.start[1])
                self.rook_to_xy = (move.start[0] - 1, move.start[1])
                self.to_castle = True
            else:
                return self.FALSE
        return self.TRUE


# Ферзь
class Queen(Piece):
    symbol: str = "q"
    capital_highlighted: str = "Ⓠ"
    highlighted: str = "ⓠ"

    # ферзь ходит как ладья и слон
    # аналогично EliteKnight, HorsebackQueen, KnightPawn
    def is_valid(self, move: Move, board: Board) -> int:
        if (
            Rook(self.color).is_valid(move, board) == Rook.FALSE
            and Bishop(self.color).is_valid(move, board) == Bishop.FALSE
        ):
            return self.FALSE
        return self.TRUE


# Пешка
class Pawn(Piece):
    symbol: str = "p"
    capital_highlighted: str = "Ⓟ"
    highlighted: str = "ⓟ"

    def is_valid(self, move: Move, board: Board) -> int:
        if move.target[0] - move.start[0] == 0:
            # обычный ход
            if move.target[1] - move.start[1] == 1 * self.color:
                if issubclass(type(board.board[move.target[0]][move.target[1]]), Piece):
                    return self.FALSE
            elif move.target[1] - move.start[1] == 2 * self.color:
                # ход на 2, если он первый
                if issubclass(
                    type(board.board[move.target[0]][move.target[1] - 1 * self.color]),
                    Piece,
                ):
                    return self.FALSE
                if issubclass(type(board.board[move.target[0]][move.target[1]]), Piece):
                    return self.FALSE
                if move.piece.color == Piece.WHITE:
                    if move.start[1] != 1:
                        return self.FALSE
                else:
                    if move.start[1] != 6:
                        return self.FALSE
            else:
                return self.FALSE
        elif abs(move.target[0] - move.start[0]) == 1:
            if issubclass(type(board.board[move.target[0]][move.target[1]]), Piece):
                # поглощение фигуры
                if move.target[1] - move.start[1] == 1 * self.color:
                    if (
                        issubclass(
                            type(board.board[move.target[0]][move.target[1]]), Piece
                        )
                        and -1 * self.color
                        == board.board[move.target[0]][move.target[1]].color
                    ):
                        move.captured = move.target
                        move.captured_piece = board.board[move.target[0]][
                            move.target[1]
                        ]
                    else:
                        return self.FALSE
                else:
                    return self.FALSE
            else:
                # взятие на проходе
                if len(board.moves) == 0:
                    return self.FALSE
                if type(board.moves[-1].piece) != Pawn:
                    return self.FALSE
                if board.moves[-1].target[1] != move.start[1]:
                    return self.FALSE
                if abs(board.moves[-1].target[0] - move.start[0]) != 1:
                    return self.FALSE
                if (
                    board.moves[-1].target[1] - board.moves[-1].start[1]
                    != -2 * self.color
                ):
                    return self.FALSE
                if self.color == self.WHITE:
                    if (
                        move.start[1] == 4
                        and move.target[1] == 5
                        and -1 * self.color
                        == board.board[board.moves[-1].target[0]][
                            board.moves[-1].target[1]
                        ].color
                    ):
                        move.captured = board.moves[-1].target
                        move.captured_piece = board.board[board.moves[-1].target[0]][
                            board.moves[-1].target[1]
                        ]
                    else:
                        return self.FALSE
                elif self.color == self.BLACK:
                    if (
                        move.start[1] == 3
                        and move.target[1] == 2
                        and -1 * self.color
                        == board.board[board.moves[-1].target[0]][
                            board.moves[-1].target[1]
                        ].color
                    ):
                        move.captured = board.moves[-1].target
                        move.captured_piece = board.board[board.moves[-1].target[0]][
                            board.moves[-1].target[1]
                        ]
                    else:
                        return self.FALSE
        else:
            return self.FALSE
        return self.TRUE


class EliteKnight(Piece):
    symbol: str = "e"
    capital_highlighted: str = "Ⓔ"
    highlighted: str = "ⓔ"

    def is_valid(self, move: Move, board: Board) -> int:
        if (
            Knight(self.color).is_valid(move, board) == Knight.FALSE
            and Bishop(self.color).is_valid(move, board) == Bishop.FALSE
        ):
            return self.FALSE
        return self.TRUE


class HorsebackQueen(Piece):
    symbol: str = "h"
    capital_highlighted: str = "Ⓗ"
    highlighted: str = "ⓗ"

    def is_valid(self, move: Move, board: Board) -> int:
        if (
            Knight(self.color).is_valid(move, board) == Knight.FALSE
            and Queen(self.color).is_valid(move, board) == Queen.FALSE
        ):
            return self.FALSE
        return self.TRUE


class KnightPawn(Piece):
    symbol: str = "i"
    capital_highlighted: str = "Ⓘ"
    highlighted: str = "ⓘ"

    def is_valid(self, move: Move, board: Board) -> int:
        if (
            Knight(self.color).is_valid(move, board) == Knight.FALSE
            and Pawn(self.color).is_valid(move, board) == Pawn.FALSE
        ):
            return self.FALSE
        return self.TRUE


# шашка
class Checker(Piece):
    symbol: str = "c"
    capital_highlighted: str = "Ⓘ"
    highlighted: str = "ⓘ"

    def is_valid(self, move: Move, board: Board) -> int:
        if abs(move.target[0] - move.start[0]) == 2:
            # ход с захватом фигуры
            if move.target[1] - move.start[1] != 2 * self.color:
                return self.FALSE
            captured: tuple[int, int] = (
                int((move.target[0] + move.start[0]) / 2),
                int((move.target[1] + move.start[1]) / 2),
            )
            captured_piece: Piece = board.board[captured[0]][captured[1]]
            if captured_piece is None:
                return self.FALSE
            if board.board[move.target[0]][move.target[1]] is not None:
                return self.FALSE
            if captured_piece.color == self.color:
                return self.FALSE
            move.captured_piece = captured_piece
            move.captured = captured
        elif abs(move.target[0] - move.start[0]) == 1:
            # ход без захвата фигуры
            if move.target[1] - move.start[1] != self.color:
                return self.FALSE
            if board.board[move.target[0]][move.target[1]] is not None:
                return self.FALSE
        else:
            return self.FALSE
        return self.TRUE


class Chess(Game):
    def __init__(self, board: str = None):
        if board is None:
            board = """rnbqkbnr
pppppppp
........
........
........
........
PPPPPPPP
RNBQKBNR"""
        self.board = Board(len(board.splitlines()), len(board.splitlines()[0]))
        #конвертация строки на доску
        for h, line in enumerate(reversed(board.splitlines())):
            for w, p in enumerate(line):
                match p:
                    case "c":
                        self.board.board[w][h] = Checker(Piece.BLACK)
                    case "C":
                        self.board.board[w][h] = Checker(Piece.WHITE)
                    case "p":
                        self.board.board[w][h] = Pawn(Piece.BLACK)
                    case "P":
                        self.board.board[w][h] = Pawn(Piece.WHITE)
                    case "r":
                        self.board.board[w][h] = Rook(Piece.BLACK)
                    case "R":
                        self.board.board[w][h] = Rook(Piece.WHITE)
                    case "n":
                        self.board.board[w][h] = Knight(Piece.BLACK)
                    case "N":
                        self.board.board[w][h] = Knight(Piece.WHITE)
                    case "b":
                        self.board.board[w][h] = Bishop(Piece.BLACK)
                    case "B":
                        self.board.board[w][h] = Bishop(Piece.WHITE)
                    case "k":
                        self.board.board[w][h] = King(Piece.BLACK)
                    case "K":
                        self.board.board[w][h] = King(Piece.WHITE)
                    case "q":
                        self.board.board[w][h] = Queen(Piece.BLACK)
                    case "Q":
                        self.board.board[w][h] = Queen(Piece.WHITE)
                    case "e":
                        self.board.board[w][h] = EliteKnight(Piece.BLACK)
                    case "E":
                        self.board.board[w][h] = EliteKnight(Piece.WHITE)
                    case "h":
                        self.board.board[w][h] = HorsebackQueen(Piece.BLACK)
                    case "H":
                        self.board.board[w][h] = HorsebackQueen(Piece.WHITE)
                    case "i":
                        self.board.board[w][h] = KnightPawn(Piece.BLACK)
                    case "I":
                        self.board.board[w][h] = KnightPawn(Piece.WHITE)

    def _correct(self, move: Move) -> bool:
        #некорректные ходы
        if (
            move.piece is None
            or move.piece.color != self.current_player
            or move.start == move.target
            or move.piece.is_valid(move, self.board) != Piece.TRUE
        ):
            return False
        
        # король до хода
        king_current: tuple[int, int] = None
        for h in range(self.board.height):
            for w in range(self.board.width):
                p: Piece = self.board.board[w][h]
                if type(p) != King:
                    continue
                if p.color != move.piece.color:
                    continue
                king_current = (w, h)

        if king_current == None:
            return True
        
        # симуляция хода
        import copy
        board = copy.deepcopy(self.board)
        board.board[move.target[0]][move.target[1]] = board.board[move.start[0]][
            move.start[1]
        ]
        board.board[move.start[0]][move.start[1]] = None
        
        # проверка подставляет ли ход фигуры своего короля под шах
        for h in range(self.board.height):
            for w in range(self.board.width):
                if board.board[w][h] is None:
                    continue
                if board.board[w][h].color == self.current_player:
                    continue
                move2: Move = Move()
                move2.piece = board.board[w][h]
                move2.start = (w, h)

                if type(move.piece) == King:
                    move2.target = move.target
                else:
                    move2.target = king_current
                if move2.piece.is_valid(move2, board) != Piece.TRUE:
                    continue
                return False
        return True

    def _print_board(self, start: tuple[int, int] = (-1, -1)):
        for h in reversed(range(self.board.height + 2)):
            if h == 0 or h == self.board.height + 1:
                print()
                print("  ", end="")
                for w in range(self.board.width):
                    print(f" {chr(ord('A') + w)}", end="")
                print()
                print()
            else:
                print(h, end=" ")
                for w in range(self.board.width):
                    piece: Piece = self.board.board[w][h - 1]
                    if self.highlight_moves and start[0] != -1:
                        move: Move = Move()
                        move.start = start
                        move.target = (w, h - 1)
                        move.piece = self.board.board[start[0]][start[1]]
                        if move.piece is None:
                            if piece is None:
                                print(" .", end="")
                            else:
                                print(f" {piece.get_symbol()}", end="")
                        elif self._correct(move):
                            self.to_castle = False
                            if piece is None:
                                print(" ○", end="")
                            else:
                                print(f" {piece.get_symbol(True)}", end="")
                        else:
                            if piece is None:
                                print(" .", end="")
                            else:
                                print(f" {piece.get_symbol()}", end="")
                    else:
                        if piece is None:
                            print(" .", end="")
                        else:
                            print(f" {piece.get_symbol()}", end="")
                print(f"  {h}", end="")
                print()
        print(f"Количество ходов: {len(self.board.moves)}")

    def _make_move(self, move: Move) -> bool:
        move.piece.moved = True
        if type(move.piece) == Pawn and (
            move.target[1] == self.board.height - 1 or move.target[1] == 0
        ):
            move.before = Pawn
            while True:
                ch: str = input(
                    "Фигура, заменяющая пешку по достижению главной горизонтали [q,n,b,r]: "
                )
                match ch:
                    case "q":
                        move.piece.__class__ = Queen
                        break
                    case "n":
                        move.piece.__class__ = Knight
                        break
                    case "b":
                        move.piece.__class__ = Bishop
                        break
                    case "r":
                        move.piece.__class__ = Rook
                        break
                    case _:
                        print("Неверный ввод заменяющей фигуры!")
        if type(move.piece) == King and move.piece.to_castle == True:
            # рокировка
            move.piece.castled = True
            move.castled = True
            move.piece.to_castle = False
            self.board.board[move.piece.rook_to_xy[0]][move.piece.rook_to_xy[1]] = (
                self.board.board[move.piece.rook_xy[0]][move.piece.rook_xy[1]]
            )
            self.board.board[move.piece.rook_xy[0]][move.piece.rook_xy[1]] = None
            print(self.board.board[move.piece.rook_to_xy[0]][move.piece.rook_to_xy[1]])
        self.board.moves.append(move)
        if move.captured is not None:
            self.board.board[move.captured[0]][move.captured[1]] = None
        self.board.board[move.target[0]][move.target[1]] = move.piece
        self.board.board[move.start[0]][move.start[1]] = None
        king_next: tuple[int, int] = None
        # вражеский король
        for h in range(self.board.height):
            for w in range(self.board.width):
                p: Piece = self.board.board[w][h]
                if type(p) != King:
                    continue
                if p.color == move.piece.color:
                    continue
                king_next = (w, h)
        if king_next is None:
            return True
        # проверка, подставляет ли ход вражеского короля под шах
        for h in range(self.board.height):
            for w in range(self.board.width):
                p: Piece = self.board.board[w][h]
                if p is None:
                    continue
                if type(p) == King:
                    continue
                if p.color != move.piece.color:
                    continue
                move2: Move = Move()
                move2.piece = self.board.board[w][h]
                move2.start = (w, h)
                move2.target = king_next
                if move2.piece.is_valid(move2, self.board) != Piece.TRUE:
                    continue
                return True
        return False

    # отмена хода
    def _cancel_move(self):
        move = self.board.moves.pop()
        if move.before == Pawn:
            move.piece.__class__ = Pawn
        self.board.board[move.start[0]][move.start[1]] = self.board.board[
            move.target[0]
        ][move.target[1]]
        self.board.board[move.target[0]][move.target[1]] = None
        if move.captured is not None:
            self.board.board[move.captured[0]][move.captured[1]] = move.captured_piece
        if type(move.piece) == King and move.castled == True:
            move.piece.castled = False
            move.piece.moved = False
            self.board.board[move.piece.rook_xy[0]][move.piece.rook_xy[1]] = (
                self.board.board[move.piece.rook_to_xy[0]][move.piece.rook_to_xy[1]]
            )
            self.board.board[move.piece.rook_to_xy[0]][move.piece.rook_to_xy[1]] = None
            self.board.board[move.piece.rook_xy[0]][move.piece.rook_xy[1]].moved = False

    def _convert(self, xy: str) -> tuple[int, int]:
        if xy == "":
            return Move().CANCEL, Move().CANCEL
        else:
            try:
                if len(xy) != 2:
                    print("Неправильно задана клетка!")
                    raise
                if ord(xy[0]) not in range(ord("a"), ord("h") + 1) or ord(
                    xy[1]
                ) not in range(ord("1"), ord("9") + 1):
                    print("Неправильно задана клетка!")
                    raise
                x: int = ord(xy[0]) - ord("a")
                y: int = int(xy[1]) - 1
                return x, y
            except Exception:
                return Move().IMPOSSIBLE, Move().IMPOSSIBLE


if __name__ == "__main__":
    c: str = input("Шахматы(1), Модифицированные Шахматы(2), Шашки(3): ")
    match c:
        case "1":
            game = Chess()
            game.start()
        case "2":
            game = Chess(
                """rnbqkbnr
pphiiepp
........
........
........
........
PPHIIEPP
RNBQKBNR"""
            )
            game.start()
        case "3":
            game = Chess(
                """.c.c.c.c
c.c.c.c.
.c.c.c.c
........
........
C.C.C.C.
.C.C.C.C
C.C.C.C."""
            )
            game.start()
        case _:
            print("Неправильный ввод. Завершение!")

# i = конь + пешка
# e = слон + конь
# h = конь + ферзь

#шах и мат: e2-e4, e7-e5, d1-h5, b8-c6, f1-c4, g8-f6, h5-f7.
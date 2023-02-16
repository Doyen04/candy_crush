from random import choice
import pygame


# noinspection PyMethodMayBeStatic
class Game:
    WID_G = 600
    BOXS_G = 8
    GAP_G = 5
    GAP2X_G = GAP_G * 2
    LINEZ_G = (WID_G - (GAP_G * BOXS_G * 2)) // BOXS_G
    DIST_G = (WID_G - (GAP_G * 2)) / BOXS_G  # 73.75
    CENTER_G = (DIST_G / 2) + GAP_G
    PAD_G = 12
    OFF_G = CENTER_G - PAD_G
    SIZEBOX_G = OFF_G * 2
    CLR_G = (100, 100, 100,)
    IMG1_G = pygame.image.load('img\\banana.png')
    IMG2_G = pygame.image.load('img\\rasp.png')
    IMG3_G = pygame.image.load('img\\green.png')
    IMG4_G = pygame.image.load('img\\chiller.png')
    IMG5_G = pygame.image.load('img\\plum.png')

    def __init__(self, win) -> None:
        self.times = 0
        self.win = win
        self.piece_array = []
        self.switch = []
        self.images = [self.IMG1_G, self.IMG2_G, self.IMG3_G, self.IMG4_G, self.IMG5_G]
        self.color = 'red'
        self.to_swap = []
        self.is_sort = False
        self.is_swap = False
        self.was_del = []
        self.new_piece = []
        self.can_swap = True
        self.mouse_up = True
        self.gap = 0
        self.resize()
        self.board()

    def resize(self):
        size = (self.SIZEBOX_G, self.SIZEBOX_G)
        for x, img in enumerate(self.images):
            image = pygame.transform.scale(img, size)
            self.images[x] = image

    def find_adjacent_occurrences(self, arrays, count):
        result = []
        for array in arrays:
            index_dict = {}
            start_index = 0
            count_rr = 1
            for i in range(1, len(array)):
                if array[i][1] and array[i - 1][1]:
                    if array[i][1].id != array[i - 1][1].id:
                        if array[i - 1][1].id in index_dict and count_rr > count:
                            index_dict[array[i - 1][1].id].append((start_index, i - 1))
                        elif count_rr > count:
                            index_dict[array[i - 1][1].id] = [(start_index, i - 1)]
                        start_index = i
                        count_rr = 1
                    else:
                        count_rr += 1
                else:
                    count_rr = 1
                    start_index = i

            if array[-1][1]:
                if array[-1][1].id in index_dict and count_rr > count:
                    index_dict[array[-1][1].id].append((start_index, len(array) - 1))
                elif count_rr > count:
                    index_dict[array[-1][1].id] = [(start_index, len(array) - 1)]
            result.append(index_dict)
        return result

    def get_all(self, array, direc, count):
        res = []
        result = self.find_adjacent_occurrences(array, count)
        for x, dic in enumerate(result):
            if dic != {}:
                for key, value in dic.items():
                    # print(value)
                    for items in value:
                        for c in range(items[0], items[1] + 1):
                            tup = ()
                            if direc == 'h':
                                tup = self.piece_array[x][c]
                            elif direc == 'v':
                                tup = self.piece_array[c][x]
                            res.append(tup)
        return res

    def get_vertical(self):
        result = []
        for x in range(len(self.piece_array[0])):
            temp = []
            for y in self.piece_array:
                temp.append(y[x])
            result.append(temp)
        return result

    def paint_all(self, res):
        for rect, cls in res:
            pygame.draw.rect(self.win, self.color, pygame.Rect(cls.rect.x, cls.rect.y, rect.width, rect.width), 2, 10)

    def make_changes(self, array, crd1, crd2):
        self.can_swap = False
        first, second = array
        r, c = crd1
        y, x = crd2
        first[0].x, first[0].y = first[1].rect.x, first[1].rect.y
        second[0].x, second[0].y = second[1].rect.x, second[1].rect.y
        first[1].row, first[1].col = y, x
        second[1].row, second[1].col = r, c
        self.piece_array[r][c] = second
        self.piece_array[y][x] = first

    def check(self, array):
        first, second = array
        direct = ''
        if first[0].x == second[0].x and abs(first[0].y - second[0].y) <= 74:
            direct = 'v'
        elif first[0].y == second[0].y and abs(first[0].x - second[0].x) <= 74:
            direct = 'h'
        else:
            self.switch = []
            self.is_sort = False  #
        return direct

    def swap(self):
        if len(self.switch) == 2:
            if not self.is_sort:
                self.switch = sorted(self.switch)
                self.is_sort = True
            first, second = self.switch
            crd1, crd2 = (first[1].row, first[1].col), (second[1].row, second[1].col)
            direc = self.check(self.switch)
            if direc:
                self.move(self.switch, direc, crd1, crd2)

    def select(self, pos):
        if len(self.switch) == 2:
            return
        elif self.can_swap:
            for lst in self.piece_array:
                for rect, cls in lst:
                    if rect.collidepoint(pos):
                        if (rect, cls) not in self.switch:
                            self.switch.append((rect, cls))

    def move(self, array, direc, crd1, crd2):
        first, second = array
        if direc == 'h':
            if not self.to_swap:
                self.times += 1
                self.to_swap = [first[0].x, second[0].x]
            self.gap = (second[0].x - first[0].x)

            if (first[1].rect.x + 14) <= (self.to_swap[1]):
                self.can_swap = False
                first[1].rect.move_ip([14, 0])
                second[1].rect.move_ip([-14, 0])
                if (tmp := abs(first[1].rect.x - self.to_swap[1])) <= 14:
                    first[1].rect.move_ip([tmp, 0])
                if (tmp2 := abs(second[1].rect.x - self.to_swap[0])) <= 14:
                    second[1].rect.move_ip([-tmp2, 0])
            else:
                self.make_changes(array, crd1, crd2)
                self.to_swap = []
                self.is_sort = False
                horizontal = self.get_all(self.piece_array, 'h', 2)
                vertical_array = self.get_vertical()
                vertical = self.get_all(vertical_array, 'v', 2)
                if self.times == 2:
                    self.times = 0
                    self.switch = []
                elif horizontal or vertical:
                    self.times = 0
                    self.switch = []

        elif direc == 'v':
            if not self.to_swap:
                self.times += 1
                self.to_swap = [first[0].y, second[0].y]
            self.gap = second[0].y - first[0].y

            if (first[1].rect.y + 14) <= (self.to_swap[1]):
                self.can_swap = False
                first[1].rect.move_ip([0, 14])
                second[1].rect.move_ip([0, -14])
                if (tmp := abs(first[1].rect.y - self.to_swap[1])) <= 14:
                    first[1].rect.move_ip([0, tmp])
                if (tmp2 := abs(second[1].rect.y - self.to_swap[0])) <= 14:
                    second[1].rect.move_ip([0, -tmp2])
            else:
                self.make_changes(array, crd1, crd2)
                self.to_swap = []
                self.is_sort = False
                horizontal = self.get_all(self.piece_array, 'h', 2)
                vertical_array = self.get_vertical()
                vertical = self.get_all(vertical_array, 'v', 2)
                if self.times == 2:
                    self.times = 0
                    self.switch = []
                elif horizontal or vertical:
                    self.times = 0
                    self.switch = []

    def draw_piece(self):
        for lst in self.piece_array:
            for rect, cls in lst:
                if cls:
                    self.win.blit(cls.image, (cls.rect.x, cls.rect.y))
        if self.new_piece:
            for rect, cls in self.new_piece:
                self.win.blit(cls.image, (cls.rect.x, cls.rect.y))

    def clean(self):
        horizontal = self.get_all(self.piece_array, 'h', 2)
        vertical_array = self.get_vertical()
        vertical = self.get_all(vertical_array, 'v', 2)
        if horizontal or vertical:
            self.paint_all(horizontal)
            self.paint_all(vertical)
            self.was_del = self.delete(vertical, horizontal)
            self.new_piece = self.replace()

    def correct(self):
        if self.was_del:
            for array in reversed(self.piece_array):
                for rect, cls in array:
                    if cls and cls.rect.x in self.was_del[0]:
                        res = self.search(cls.rect.x, cls.rect.y)
                        if res is not None:
                            x, y = cls.row, cls.col
                            cls.rect.x, cls.rect.y = res[2], res[3]
                            cls.row, cls.col = res[0], res[1]
                            self.piece_array[res[0]][res[1]] = (self.piece_array[res[0]][res[1]][0], cls)
                            self.piece_array[x][y] = (rect, '')

            for rect, cls in self.new_piece:
                res = self.search(cls.rect.x, cls.rect.y)
                if res is not None:
                    cls.rect.x, cls.rect.y = res[2], res[3]
                    cls.row, cls.col = res[0], res[1]
                    self.piece_array[res[0]][res[1]] = (self.piece_array[res[0]][res[1]][0], cls)
            self.was_del = []
            self.new_piece = []

    def search(self, x, y):
        for r, array in enumerate(self.piece_array):
            for c, (rect, cls) in enumerate(array):
                if rect.x in self.was_del[0] and cls == '':
                    if rect.x == x and abs(rect.y - y) < 14:
                        return r, c, rect.x, rect.y

    def replace(self):
        new_piece = []
        for key, value in self.was_del[0].items():
            for v in range(value):  # -65 -138
                x, y = key, 12 - (74 * (v + 1))
                img = choice(self.images)
                rect = pygame.Rect(x, y, self.SIZEBOX_G, self.SIZEBOX_G)
                rect2 = pygame.Rect(x, y, self.SIZEBOX_G, self.SIZEBOX_G)
                p = Piece(None, -1, -1, img, self.images.index(img), rect)
                new_piece.append((rect2, p))
        return new_piece

    def drop(self):
        dropped = False
        if self.was_del:
            self.can_swap = False
            for array in reversed(self.piece_array):
                for rect, cls in array:
                    if cls:
                        lag = 0
                        if cls.rect.x in self.was_del[1]:
                            lag = self.was_del[1][cls.rect.x]
                        if cls.rect.x in self.was_del[0] and round(cls.rect.y + 14) <= self.was_del[1][cls.rect.x]:
                            cls.rect.move_ip([0, 14])
                            dropped = True
                            if (tmp := (lag - cls.rect.y)) <= 14:
                                cls.rect.move_ip([0, tmp])
                            if cls.rect.y + 14 >= lag:
                                self.was_del[1][cls.rect.x] = lag - 74

            for rect, cls in self.new_piece:
                if cls.rect.x in self.was_del[1]:
                    if cls.rect.x in self.was_del[1] and round(cls.rect.y + 14) <= self.was_del[1][cls.rect.x]:
                        dropped = True
                        cls.rect.move_ip([0, 14])
                        if (tmp := (self.was_del[1][cls.rect.x] - cls.rect.y)) <= 14:
                            cls.rect.move_ip([0, tmp])
                        if cls.rect.y + 14 >= self.was_del[1][cls.rect.x]:
                            self.was_del[1][cls.rect.x] = self.was_del[1][cls.rect.x] - 74
            return dropped

    def delete(self, v, h):
        deleted = []
        data = {}
        y_coord = {}
        if v:
            for rect, cls in v:
                r, c = cls.row, cls.col
                self.piece_array[r][c] = (rect, '')
                deleted.append(self.piece_array[r][c])
        if h:
            for rect, cls in h:
                r, c = cls.row, cls.col
                self.piece_array[r][c] = (rect, '')
                deleted.append(self.piece_array[r][c])
        for rect, cls in deleted:
            if rect.x in y_coord:
                y_coord[rect.x] = max(y_coord[rect.x], rect.y)
            else:
                y_coord[rect.x] = rect.y
            data[rect.x] = data[rect.x] + 1 if rect.x in data else 1
        deleted = []
        deleted.extend([data, y_coord])
        return deleted

    def make_suggestion(self):
        horizontal = self.find_adjacent_occurrences(self.piece_array, 1)
        vertical_array = self.get_vertical()
        vertical = self.find_adjacent_occurrences(vertical_array, 1)
        # print(horizontal, )
        self.suggest(horizontal, 'h')
        pass

    def suggest(self, array, direc):
        result = []
        for x, dic in enumerate(array):
            if dic:
                for key, value in dic.items():
                    for items in value:
                        start, end = items
                        if direc == 'h':
                            data = {items: [x, []]}
                            if x > 0 and start > 0:
                                if (cls := self.piece_array[x - 1][start - 1][1]).id == key:
                                    data[items][1].append(cls)
                                    result.append(data)
                                    # pygame.draw.rect(self.win, self.color,
                                    #                pygame.Rect(cls.rect.x, cls.rect.y, cls.rect.width,
                                    #                            cls.rect.width), 2, 10)
                            if x <= 6 and start > 0:
                                if (cls := self.piece_array[x + 1][start - 1][1]).id == key:
                                    data[items][1].append(cls)
                                    result.append(data)
                                    # pygame.draw.rect(self.win, self.color,
                                    #                pygame.Rect(cls.rect.x, cls.rect.y, cls.rect.width,
                                    #                            cls.rect.width), 2, 10)
                            if start >= 2 and start <= 5:
                                if (cls := self.piece_array[x][start - 2][1]).id == key:
                                    data[items][1].append(cls)
                                    result.append(data)
                                    # pygame.draw.rect(self.win, self.color,
                                    #                pygame.Rect(cls.rect.x, cls.rect.y, cls.rect.width,
                                    #                             cls.rect.width), 2, 10)
                                # if x > 0 and x <= 6 and end <= 6:
                                #     if (cls := self.piece_array[x - 1][start + 1][1]).id == key:
                                #         pygame.draw.rect(self.win, self.color,
                                #                          pygame.Rect(cls.rect.x, cls.rect.y, cls.rect.width,
                                #                                      cls.rect.width), 2, 10)
                                #     if (cls := self.piece_array[x + 1][start + 1][1]).id == key:
                                #         pygame.draw.rect(self.win, self.color,
                                #                          pygame.Rect(cls.rect.x, cls.rect.y, cls.rect.width,
                                #                                      cls.rect.width), 2, 10)
                                pass
        self.paint_sugg(result)

    def paint_sugg(self, to_paint):
        for dic in to_paint:
            for key, value in dic.items():
                for x in range(key[0], key[1] + 1):
                    cls = self.piece_array[value[0]][x][1]
                    pygame.draw.rect(self.win, self.color,
                                     pygame.Rect(cls.rect.x, cls.rect.y, cls.rect.width,
                                                 cls.rect.width), 2, 10)
                for cls in value[1]:
                    pygame.draw.rect(self.win, self.color,
                                     pygame.Rect(cls.rect.x, cls.rect.y, cls.rect.width,
                                                 cls.rect.width), 2, 10)

    def board(self):
        for row_num in range(8):
            self.piece_array.append([])
            for col_num in range(8):
                x = round(((col_num * self.DIST_G) + self.CENTER_G) - self.OFF_G)
                y = round(((row_num * self.DIST_G) + self.CENTER_G) - self.OFF_G)
                rect = pygame.Rect(x, y, self.SIZEBOX_G, self.SIZEBOX_G)
                rect2 = pygame.Rect(x, y, self.SIZEBOX_G, self.SIZEBOX_G)

                img = choice(self.images)
                p = Piece(None, row_num, col_num, img, self.images.index(img), rect2)
                self.piece_array[row_num].append((rect, p))

    def make_line(self):
        for row_num in range(9):
            for col_num in range(9):
                if row_num < 9 and col_num < 8:  # and row_num != 0hori
                    x = round((self.DIST_G * col_num) + self.GAP2X_G)
                    y = round((row_num * self.DIST_G) + self.GAP_G)
                    pygame.draw.line(self.win, self.CLR_G, (x, y), ((x + self.LINEZ_G), y))
                if col_num < 9 and row_num < 8:  # '''and col_num != 0 '''verti
                    a = round((col_num * self.DIST_G) + self.GAP_G)
                    b = round((row_num * self.DIST_G) + self.GAP2X_G)
                    pygame.draw.line(self.win, self.CLR_G, (a, b), (a, b + self.LINEZ_G))

    def update(self):
        self.make_line()
        self.draw_piece()
        pygame.display.update()


class Piece:
    def __init__(self, name, y, x, img, _id, rect) -> None:
        self.name = name
        self.row = y
        self.col = x
        self.image = img
        self.id = _id
        self.rect = rect


'''
    font = pygame.font.SysFont('Times New Roman',16)
    lab = font.render(f'{row_num},{col_num}',1,'white')
    self.win.blit(lab,(x,y))
'''

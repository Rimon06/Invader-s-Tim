class simplematrix(list):
    def __init__(self, lista=[]):
        if all(isinstance(t, list) for t in lista):
            self.extend(lista)

    def line(self):
        p = []
        for t in self.copy():
            p.extend(list(t))
        return p

    def __contains__(self, item):
        return any(item == X for X in self)

    def __iter__(self):
        return iter(self.line())


class dict_grid():
    def __init__(self, height, width=None):
        if width is None:
            width = height
        self.W = width
        self.H = height
        self.index = simplematrix([[(i, j) for j in range(width)] for i in range(height)])
        self.info = dict((coord, None) for coord in self.index)

    def __getitem__(self, key):
        if key not in self.index:
            raise KeyError
        return self.info[key]

    def __setitem__(self, key, value):
        if key not in self.index:
            raise KeyError
        self.info[key] = value

    def __len__(self):
        return self.W*self.H

    def __delitem__(self, key):
        pass

    def __repr__(self):
        x = ''
        for u in self.index:
            x += f'{u}: {self.info[u]} '
        return x

    def __iter__(self):
        return iter(self.index)

    def values(self):
        return tuple(self[coord] for coord in self)

    # def __next__(self):
    #     return next(self.index)


pol = dict_grid(5, 3)

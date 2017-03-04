class Image:

    def copy(self):
        return type(self)()

    @classmethod
    def from_file(cls, path, imagetype):
        return cls(), (0, 0)

    @classmethod
    def from_size(cls, width, height):
        return cls()

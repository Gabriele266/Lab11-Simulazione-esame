from dataclasses import dataclass

@dataclass
class Genre:
    GenreId: int
    Name: str

    def __eq__(self, other):
        return self.GenreId == other.GenreId

    def __hash__(self):
        return hash(self.GenreId)
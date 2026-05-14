from dataclasses import dataclass

@dataclass
class Artist:
    ArtistID: int
    Name: str

    def __hash__(self):
        return hash(self.ArtistID)

    def __str__(self):
        return f"{self.Name}"
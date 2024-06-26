from dataclasses import dataclass


@dataclass
class Track:
    TrackId: int
    Name: str
    AlbumId: int
    MediaTypeId: int
    GenreId: int
    Composer: str
    Milliseconds: int
    Bytes: int
    UnitPrice: float

    def __str__(self):
        return self.Name

    def __repr__(self):
        return self.Name

    def __hash__(self):
        return hash(self.TrackId)

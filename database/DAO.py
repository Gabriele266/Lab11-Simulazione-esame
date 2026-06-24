from database.DB_connect import DBConnect
from model.Artist import Artist
from model.Genre import Genre


class DAO:
    def __init__(self):
        self.connection = DBConnect.get_connection()

    @staticmethod
    def load_genres_list():
        connection = DBConnect.get_connection()
        query = "SELECT * FROM Genre;"

        cursor = connection.cursor(dictionary = True)
        cursor.execute(query)

        arr = []
        for row in cursor:
            arr.append(Genre(
                row["GenreId"],
                row["Name"]
            ))

        cursor.close()
        connection.close()
        return arr

    def __load_artists_by_genre(self, genreId: int) -> list[Artist]:
        """Carica la lista di tutti gli artisti che hanno almeno un brano di quel genere"""
        query = """SELECT A2.ArtistId, A2.Name, (SELECT COUNT(*) FROM Track T WHERE T.AlbumId IN (
	SELECT A.AlbumId FROM Album A, Artist AR WHERE A.ArtistId = A2.ArtistId 
) AND T.GenreId = %s) as numero_brani_genere FROM Artist A2;"""

        cursor = self.connection.cursor(dictionary = True)
        data = tuple([genreId])
        cursor.execute(query, data)

        artists = []
        for row in cursor:
            if row["numero_brani_genere"] > 0:
                artists.append(Artist(
                    ArtistId=row["ArtistId"],
                    Name=row["Name"],
                    popularity=0,
                ))

        cursor.close()
        return artists

    def countTotalAcquiredTracksForArtist(self, artistId: int):
        query = """SELECT COUNT(*) as result FROM InvoiceLine I
WHERE I.TrackId IN (SELECT T.TrackId FROM Track T WHERE T.AlbumId IN (
	SELECT A.AlbumId FROM Album A, Artist AR WHERE A.ArtistId = %s))"""
        cursor = self.connection.cursor(dictionary = True)
        data = tuple([artistId])

        cursor.execute(query, data)
        res = cursor.fetchall()

        cursor.close()
        return int(res[0]["result"])

    def load_customers_for_artist(self, artist_id: int) -> set[int]:
        """Carica la lista di tutti i clienti che hanno acquistato almeno un brano dall'artista"""
        query = """
        SELECT DISTINCT(C.CustomerId)
FROM Customer C 
WHERE C.CustomerId IN (
	SELECT I.CustomerId FROM Invoice I, InvoiceLine L 
	WHERE L.InvoiceId = I.InvoiceId 
	AND L.TrackId IN (
	SELECT T.TrackId FROM Track T WHERE T.AlbumId IN (
	SELECT A.AlbumId FROM Album A, Artist AR WHERE A.ArtistId = %s)
	)
);"""
        data = tuple([artist_id])
        cursor = self.connection.cursor(dictionary = True)
        cursor.execute(query, data)

        l = []
        for row in cursor:
            l.append(row["CustomerId"])

        cursor.close()
        return set(l)

    def close(self):
        self.connection.close()

    def load_artists_info(self, genre_id: int) -> list[Artist]:
        artist_list = self.__load_artists_by_genre(genre_id)
        print(artist_list)

        for artist in artist_list:
            artist_popularity = self.countTotalAcquiredTracksForArtist(artist.ArtistId)
            artist.popularity = artist_popularity

        return list(artist_list)
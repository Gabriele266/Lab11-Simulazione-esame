from database.DB_connect import DBConnect
from model.Artist import Artist

class DAO():

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select distinct g.Name from genre g order by g.Name"

        cursor.execute(query)

        for row in cursor:
            results.append(row["Name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArtistbyGenre(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct art.ArtistId as  ArtistID,  art.Name as Name
                    from artist art, album a, track t, genre g 
                    where art.ArtistId = a.ArtistId 
                    and t.AlbumId = a.AlbumId 
                    and g.GenreId = t.GenreId 
                    and g.Name = %s"""

        cursor.execute(query, (genere,))

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCustomerArtistCounts(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select i.CustomerId, art.ArtistId, count(*) as ntracks
                    from invoice i, invoiceline i2, track t, genre g, artist art,album a
                    where i.InvoiceId  = i2.InvoiceId 
                    and t.TrackId = i2.TrackId 
                    and t.AlbumId = a.AlbumId
                    and g.GenreId = t.GenreId
                    and art.ArtistId = a.ArtistId 
                    and g.Name = %s
                    group by i.CustomerId, art.ArtistId"""
        cursor.execute(query, (genere,))

        for row in cursor:
            results.append((row["CustomerId"], row["ArtistId"], row["ntracks"]))

        cursor.close()
        conn.close()
        return results


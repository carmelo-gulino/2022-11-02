from database.DB_connect import DBConnect
from model.genre import Genre
from model.track import Track


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_genres():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from genre g order by GenreId """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Genre(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_durate_min():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select g.GenreId , min(t.Milliseconds) d_min, max(t.Milliseconds) d_max
        from track t , genre g 
        where t.GenreId = g.GenreId 
        group by g.GenreId """
        cursor.execute(query)
        result = {}
        for row in cursor:
            result[row['GenreId']] = row['d_min'], row['d_max']
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_tracks(genre, d_min, d_max):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select t.*
        from track t , genre g 
        where t.GenreId = g.GenreId and t.GenreId = %s
        and t.Milliseconds > %s and t.Milliseconds < %s"""
        cursor.execute(query, (genre, d_min, d_max))
        result = []
        for row in cursor:
            result.append(Track(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_n_playlist(genre, d_min, d_max):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select t.TrackId , count(distinct p.PlaylistId) n_playlist
        from track t , genre g , playlisttrack p 
        where t.GenreId = g.GenreId and t.GenreId = %s and p.TrackId = t.TrackId 
        and t.Milliseconds > %s and t.Milliseconds < %s
        group by t.TrackId """
        cursor.execute(query, (genre, d_min, d_max))
        result = {}
        for row in cursor:
            result[row['TrackId']] = row['n_playlist']
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_distinct_playlist():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select t.TrackId , p2.Name
        from track t , playlisttrack p , playlist p2 
        where p.TrackId = t.TrackId and p2.PlaylistId = p.PlaylistId
        group by t.TrackId , p2.Name"""
        cursor.execute(query)
        result = {}
        for row in cursor:
            try:
                result[row['TrackId']].add(row['Name'])
            except KeyError:
                result[row['TrackId']] = {row['Name']}
        cursor.close()
        cnx.close()
        return result

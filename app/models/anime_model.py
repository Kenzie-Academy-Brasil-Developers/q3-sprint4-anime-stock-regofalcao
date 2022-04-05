from flask import request
from app.models import DatabaseConnector
from psycopg2 import sql


class Anime:
    def __init__(self, **kwargs):
        self.anime = kwargs["anime"]
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]

    @staticmethod
    def create_table():
        conn, cur = DatabaseConnector.get_conn_cur()

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS animes (
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL);
            """)

        conn.commit()

        cur.close()
        conn.close()

    @staticmethod
    def read_animes():
        conn, cur = DatabaseConnector.get_conn_cur()

        query = "SELECT * FROM animes;"

        cur.execute(query)

        animes = cur.fetchall()

        cur.close()
        conn.close()

        return animes

    def create_anime(self):
        conn, cur = DatabaseConnector.get_conn_cur()

        query = """
                    INSERT INTO animes
                        (anime, released_date, seasons)
                    VALUES
                        (%s, %s, %s)
                    RETURNING *;
                """

        query_values = tuple(self.__dict__.values())

        cur.execute(query, query_values)

        conn.commit()

        inserted_anime = cur.fetchone()

        cur.close()
        conn.close()

        return inserted_anime

    @staticmethod
    def read_anime_by_id(anime_id):
        conn, cur = DatabaseConnector.get_conn_cur()

        query = "SELECT * FROM animes WHERE id = %s;"

        cur.execute(query, [anime_id])

        animes = cur.fetchall()

        cur.close()
        conn.close()

        return animes

    @staticmethod
    def delete_anime(anime_id):
        conn, cur = DatabaseConnector.get_conn_cur()

        query = "DELETE FROM animes where id = %s"

        cur.execute(query, [anime_id])

        conn.commit()

        cur.close()
        conn.close()

    @staticmethod
    def update_anime(anime_id):
        anime_data = request.json
        conn, cur = DatabaseConnector.get_conn_cur()

        if anime_data.get("anime"):
            anime_data["anime"] = anime_data["anime"].title()

        columns = [sql.Identifier(key) for key in anime_data.keys()]
        values = [sql.Literal(value) for value in anime_data.values()]

        query = sql.SQL("""
                    UPDATE
                        animes
                    SET
                        ({columns}) = row({values})
                    WHERE
                        id = {id}
                    RETURNING *
                """
                        ).format(
            id=sql.Literal(anime_id),
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values)
        )

        cur.execute(query)

        updated_anime = cur.fetchone()

        conn.commit()

        cur.close()
        conn.close()

        return updated_anime

from http import HTTPStatus
from xml.dom import NotFoundErr
from flask import jsonify, request
from app.models.anime_model import Anime
from psycopg2.errors import UniqueViolation


def create_table():
    return Anime.create_table()


def get_all():
    create_table()
    animes = Anime.read_animes()

    anime_columns = ["id", "anime", "released_date", "seasons"]

    serialized_animes = [dict(zip(anime_columns, anime)) for anime in animes]

    return {"data": serialized_animes}, HTTPStatus.OK


def create():
    create_table()
    data = request.get_json()
    keys = ["anime", "released_date", "seasons"]
    wrong_keys = [key for key in data.keys() if key not in keys]

    try:
        data = {
            "anime": data["anime"].title(),
            "released_date": data["released_date"],
            "seasons": data["seasons"]
        }

        anime = Anime(**data)

        try:
            inserted_anime = anime.create_anime()
        except UniqueViolation:
            return {"error": "anime already exists"}, HTTPStatus.CONFLICT

        anime_columns = ["id", "anime", "released_date", "seasons"]

        serialized_anime = dict(zip(anime_columns, inserted_anime))

        return serialized_anime, HTTPStatus.CREATED

    except KeyError:
        return {"available_keys": ["anime", "released_date", "seasons"],
                "wrong_keys_sended": wrong_keys}, \
            HTTPStatus.UNPROCESSABLE_ENTITY


def get_by_id(anime_id):
    create_table()

    animes = Anime.read_anime_by_id(anime_id)

    anime_columns = ["id", "anime", "released_date", "seasons"]

    serialized_anime = [dict(zip(anime_columns, anime)) for anime in animes]

    try:
        serialized_anime[0]["anime"]
        return {"data": serialized_anime}, HTTPStatus.OK
    except IndexError:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND


def delete(anime_id):
    anime = Anime.read_anime_by_id(anime_id)
    try:
        if not anime:
            raise NotFoundErr
        Anime.delete_anime(anime_id)
        return "", HTTPStatus.NO_CONTENT
    except NotFoundErr:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND


def update(anime_id):
    data = request.get_json()
    keys = ["anime", "released_date", "seasons"]
    wrong_keys = [key for key in data.keys() if key not in keys]
    anime = Anime.read_anime_by_id(anime_id)

    try:
        if wrong_keys:
            raise KeyError
        if not anime:
            raise NotFoundErr

        animes_columns = ["id", "anime", "released_date", "seasons"]

        updated_anime = Anime.update_anime(anime_id)

        return dict(zip(animes_columns, updated_anime)), HTTPStatus.OK

    except KeyError:
        return {"available_keys": ["anime", "released_date", "seasons"],
                "wrong_keys_sended": wrong_keys}, \
            HTTPStatus.UNPROCESSABLE_ENTITY
    except NotFoundErr:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

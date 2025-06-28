import sys
from typing import Any, Tuple
import pymysql
import settings as se


def connection() -> pymysql.connections.Connection:
    """

    """
    try:
        conn = pymysql.connect(**se.MYSQL_CONFIG)
    except Exception as error:
        print(error)
        sys.exit(0)
    return conn


def quantity_in_movie_by_title(keyword: str) -> int:
    """
    pass
    """
    conn = connection()
    with conn.cursor() as cursor:
        params = {
            "keyword": f"%{keyword}%",
        }
        cursor.execute(se.QUERY_NUMBER_OF_LINES_IN_SEARCH_BY_TITLE, params)
        quantity = cursor.fetchall()[0][0]
    conn.close()
    return quantity


def search_movie_by_title(keyword: str, start: int) -> tuple[tuple[Any, ...], ...]:
    """
    Search function by movie titles in the MySQL database

    param keyword: search string for movie titles
    return: data obtained from the MySQL database
    """
    conn = connection()
    with conn.cursor() as cursor:
        params = {
            "keyword": f"%{keyword}%",
            "start": start,
            "end": se.SEARCH_BY_TITLE_LIMIT
        }
        cursor.execute(se.QUERY_SEARCH_BY_TITLE, params)
        data = cursor.fetchall()
    conn.close()
    return data


def get_genres() -> list:
    """
    pass
    """
    conn = connection()
    with conn.cursor() as cursor:
        cursor.execute(se.QUERY_GET_GENRES)
        genres = [item[0] for item in cursor.fetchall()]
    conn.close()
    return genres


def get_years() -> tuple[Any, ...]:
    """

    """
    conn = connection()
    with conn.cursor() as cursor:
        cursor.execute(se.QUERY_GET_YEARS)
        years = cursor.fetchall()[0]
    conn.close()
    return years


def search_movie_by_genre_year(genre: str, years: list | int | None, start: int) -> \
        tuple[tuple[tuple[Any, ...], ...], int]:
    """

    """
    conn = connection()
    with conn.cursor() as cursor:
        if not years:
            params = {
                "genre": genre,
                "start": start,
                "end": se.SEARCH_BY_TITLE_LIMIT
            }
            query = se.QUERY_SEARCH_BY_GENRE
        elif isinstance(years, int):
            params = {
                "genre": genre,
                "year": years,
                "start": start,
                "end": se.SEARCH_BY_TITLE_LIMIT
            }
            query = se.QUERY_SEARCH_BY_GENRE_UND_YEAR
        else:
            params = {
                "genre": genre,
                "year_1": years[0],
                "year_2": years[1],
                "start": start,
                "end": se.SEARCH_BY_TITLE_LIMIT
            }
            query = se.QUERY_SEARCH_BY_GENRE_UND_YEARS
        quantity_query = query.split("LIMIT")[0]
        cursor.execute(query, params)
        data = cursor.fetchall()
        params.popitem()
        params.popitem()
        cursor.execute(quantity_query, params)
        quantity = len(cursor.fetchall())
    conn.close()
    return data, quantity

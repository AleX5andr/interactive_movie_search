import settings as se
import user_interface as ui
import pymysql
import sys


def connection() -> pymysql.connections.Connection:
    """
    Establishes and returns a MySQL database connection.

    :return: Active MySQL connection object.
    """
    try:
        conn = pymysql.connect(**se.MYSQL_CONFIG)
    except Exception as error:
        ui.error_print(error)
        sys.exit(0)
    return conn


def quantity_in_movie_by_title(keyword: str) -> int:
    """
    Returns the count of movies matching the given title keyword.

    :param keyword: Keyword to search within movie titles.
    :return: Number of matching movies.
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


def search_movie_by_title(keyword: str, start: int) -> tuple:
    """
    Retrieves a batch of movies matching the title keyword with pagination.

    :param keyword: Keyword to search within movie titles.
    :param start: Offset to start fetching results from.
    :return: Tuple of movie records.
    """
    conn = connection()
    with conn.cursor() as cursor:
        params = {
            "keyword": f"%{keyword}%",
            "start": start,
            "end": se.LINE_LIMIT
        }
        cursor.execute(se.QUERY_SEARCH_BY_TITLE, params)
        data = cursor.fetchall()
    conn.close()
    return data


def get_genres() -> list:
    """
    Retrieves a list of all movie genres from the database.

    :return: List of genre names.
    """
    conn = connection()
    with conn.cursor() as cursor:
        cursor.execute(se.QUERY_GET_GENRES)
        genres = [item[0] for item in cursor.fetchall()]
    conn.close()
    return genres


def get_years() -> tuple:
    """
    Retrieves the range of years (min and max) of movies from the database.

    :return: Tuple containing.
    """
    conn = connection()
    with conn.cursor() as cursor:
        cursor.execute(se.QUERY_GET_YEARS)
        years = cursor.fetchall()[0]
    conn.close()
    return years


def search_movie_by_genre_year(genre: str, years: list | int | None, start: int) -> tuple[tuple, int]:
    """
    Retrieves movies filtered by genre and optionally by year or year range with pagination.

    :param genre: Movie genre to filter by.
    :param years: Single year (int), year range (list), or None.
    :param start: Offset to start fetching results from.
    :return: Tuple of movie records and total count of matching entries.
    """
    conn = connection()
    with conn.cursor() as cursor:
        if not years:
            params = {
                "genre": genre,
                "start": start,
                "end": se.LINE_LIMIT
            }
            query = se.QUERY_SEARCH_BY_GENRE
        elif isinstance(years, int):
            params = {
                "genre": genre,
                "year": years,
                "start": start,
                "end": se.LINE_LIMIT
            }
            query = se.QUERY_SEARCH_BY_GENRE_UND_YEAR
        else:
            params = {
                "genre": genre,
                "year_1": years[0],
                "year_2": years[1],
                "start": start,
                "end": se.LINE_LIMIT
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

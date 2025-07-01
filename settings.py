# MySQL credentials
MYSQL_CONFIG = {
    'host': 'ich-db.edu.itcareerhub.de',
    'user': 'ich1',
    'password': 'password',
    'database': 'sakila'
}


# MySQL querys und parameters
LINE_LIMIT = 10
SQL_TABLE_HEADERS = ["ID", "Title", "Year", "Genre", "Language", "Rental cost", "Rental duration"]
QUERY_SEARCH_BY_TITLE = '''
    SELECT f.film_id, f.title, f.release_year, c.name, la.name, f.rental_rate, f.rental_duration
    FROM film AS f
    JOIN film_category AS fc on f.film_id = fc.film_id
    JOIN category AS c on fc.category_id = c.category_id
    JOIN language AS la on f.language_id = la.language_id
    WHERE f.title like %(keyword)s
    LIMIT %(end)s
    OFFSET %(start)s
    '''
QUERY_NUMBER_OF_LINES_IN_SEARCH_BY_TITLE = '''
    SELECT COUNT(*)
    FROM film
    WHERE title like %(keyword)s
    '''

QUERY_GET_GENRES = '''
    SELECT name
    FROM category
    '''
QUERY_GET_YEARS = '''
    SELECT MIN(release_year), MAX(release_year)
    FROM film
    '''
QUERY_SEARCH_BY_GENRE = '''
    SELECT f.film_id, f.title, f.release_year, c.name, la.name, f.rental_rate, f.rental_duration
    FROM film AS f
    JOIN film_category AS fc on f.film_id = fc.film_id
    JOIN category AS c on fc.category_id = c.category_id
    JOIN language AS la on f.language_id = la.language_id
    WHERE c.name = %(genre)s
    LIMIT %(end)s
    OFFSET %(start)s
    '''
QUERY_SEARCH_BY_GENRE_UND_YEAR = '''
    SELECT f.film_id, f.title, f.release_year, c.name, la.name, f.rental_rate, f.rental_duration
    FROM film AS f
    JOIN film_category AS fc on f.film_id = fc.film_id
    JOIN category AS c on fc.category_id = c.category_id
    JOIN language AS la on f.language_id = la.language_id
    WHERE c.name = %(genre)s AND 
        f.release_year = %(year)s
    LIMIT %(end)s
    OFFSET %(start)s
    '''
QUERY_SEARCH_BY_GENRE_UND_YEARS = '''
    SELECT f.film_id, f.title, f.release_year, c.name, la.name, f.rental_rate, f.rental_duration
    FROM film AS f
    JOIN film_category AS fc on f.film_id = fc.film_id
    JOIN category AS c on fc.category_id = c.category_id
    JOIN language AS la on f.language_id = la.language_id
    WHERE c.name = %(genre)s AND
        f.release_year >= %(year_1)s AND
        f.release_year <= %(year_2)s
    LIMIT %(end)s
    OFFSET %(start)s
    '''
QUERY_ABOUT_FILM = """
    SELECT
        f.film_id, 
        f.title, 
        f.description, 
        c.name,
        f.release_year,
        GROUP_CONCAT(CONCAT(ac.first_name, " ", ac.last_name) SEPARATOR ", ") AS actors,
        la.name, 
        CONCAT(f.length, " min"), 
        f.rating, 
        CONCAT(f.rental_duration, " day(s)"), 
        CONCAT(f.rental_rate, "€")
    FROM film AS f
    JOIN film_category AS fc ON f.film_id = fc.film_id
    JOIN category AS c ON fc.category_id = c.category_id
    JOIN language AS la ON f.language_id = la.language_id
    JOIN film_actor AS fa ON f.film_id = fa.film_id
    JOIN actor AS ac ON fa.actor_id = ac.actor_id
    WHERE f.film_id = %(id)s;
    """
ABOUT_FILM_HEADERS = [
    "Film ID",
    "Title",
    "Description",
    "Genre",
    "Release year",
    "Actors",
    "Language",
    "Length",
    "Rating",
    "Rental duration",
    "Rental rate"
    ]
ABOUT_FILM_HEADERS = ["   " + h.ljust(len(max(ABOUT_FILM_HEADERS, key=len)) + 1) + "|" for h in ABOUT_FILM_HEADERS]


# MongoDB credentials
MONGO_URL = (
    "mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/"
    "?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"
)
MONGO_COLLECTION = "final_project_100125dam_oleksandr_m"


# MongoDB parameters
MONGO_TABLE_HEADERS_RECENT = ["Time stamp", "Search type", "Parameters", "Result count"]
MONGO_TABLE_HEADERS_POPULAR = ["Query quantity", "Search type", "Parameters", "Result count"]


# Interface parameters
INTERFACE_WIDTH = 40
FILE_LOG_NAME = "app.log"

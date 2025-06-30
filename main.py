import action
import user_interface as ui
import mysql_connector as sql


def main() -> None:
    """
    Runs the main program loop by displaying the interface and handling user choice.
    """
    choice = ui.main_interface()
    action.main_action(choice)


def search_by_title() -> None:
    """
    Initiates a search by movie title.
    """
    keyword = ui.input_keyword()
    quantity = sql.quantity_in_movie_by_title(keyword)
    action.search_by_title_action(0, quantity, keyword)


def search_by_genre_year(genre: str | None = None) -> None:
    """
    Initiates a search by genre and year.

    :param genre: Optional preselected genre.
    """
    if not genre:
        genres = sql.get_genres()
        choice = ui.choice_genres(genres)
        genre = action.choice_genre(genres, choice)
    years = sql.get_years()
    choice = ui.choice_year(years, genre)
    choice_years = action.choice_year(choice, genre, years)
    action.search_by_genre_year(0, genre, choice_years)


def view_queries() -> None:
    """
    Displays the queries menu and handles user actions for viewing queries.
    """
    choice = ui.view_queries_interface()
    action.view_queries_action(choice)


if __name__ == "__main__":
    main()

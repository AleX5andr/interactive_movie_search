import main
import user_interface as ui
import mysql_connector as sql
import mongo_connector as mong
import sys


def stop() -> None:
    """
    Prints a goodbye message, draws a line, and exits the program.
    """
    print("\nGoodbye!")
    ui.print_line()
    sys.exit(0)


def main_choice(choice: str) -> None:
    """
    Executes an action based on the user's main menu choice.

    :param choice: User's menu choice.
    """
    match choice:
        case "m":
            main.main()
        case "q":
            stop()


def main_action(choice: str) -> None:
    """
    Executes the corresponding action based on the main menu choice.

    :param choice: User's menu choice.
    """
    match choice:
        case "q":
            stop()
        case "1":
            main.search_by_title()
        case "2":
            main.search_by_genre_year()
        case "3":
            main.view_queries(None)
        case _:
            ui.invalid_choice(None)
            main.main()


def search_by_title_action(start: int, quantity: int, keyword: str) -> None:
    """
    Handles the interactive search-by-title flow with pagination.

    :param start: Starting index for SQL query pagination.
    :param quantity: Total number of search results.
    :param keyword: The search keyword for movie titles.
    """
    page = 1
    pages = quantity // 10 + 1
    data = []
    mong.add_request(keyword, quantity)
    while True:
        if not quantity:
            page = 0
            pages = 0
            ui.empty_result(keyword)
        else:
            if not data:
                data = sql.search_movie_by_title(keyword, start)
            ui.show_data_frame(data, page, pages, keyword)
        choice = ui.data_frame_menu(page, pages, "title")
        main_choice(choice)
        match choice:
            case "1":
                if not quantity or page == pages:
                    ui.invalid_choice(None)
                else:
                    start += 10
                    page += 1
                    data = []
            case "2":
                if not quantity or page == 1:
                    ui.invalid_choice(None)
                else:
                    start -= 10
                    page -= 1
                    data = []
            case "c":
                main.search_by_title()
            case _:
                ui.invalid_choice(None)


def choice_genre(genres: list, choice: str) -> str:
    """
    Validates and returns the selected genre from the list based on user input.

    :param genres: List of available genres.
    :param choice: User's raw input choice.
    :return: The selected genre name.
    """
    main_choice(choice)
    try:
        choice = int(choice)
        if choice < 1 or choice > len(genres):
            raise ValueError
    except ValueError:
        ui.invalid_choice(None)
        main.search_by_genre_year()
    return genres[choice - 1]


def choice_year(choice: str, genre: str, years: tuple) -> list | int | None:
    """
    Validates and parses the year or year range input from the user.

    :param choice: User input string for year or year range.
    :param genre: Selected movie genre.
    :param years: Allowed range of years.
    :return: Parsed year(s) or empty string.
    """
    main_choice(choice)
    years_choice = ""
    try:
        if len(choice) == 4:
            year = int(choice)
            if not years[0] <= year <= years[1]:
                raise ValueError(f"The year entered is not within the specified range ({years[0]} - {years[1]})")
            years_choice = year
        elif len(choice) >= 8:
            year_1 = int(choice[:4])
            year_2 = int(choice[-4:])
            if not year_1 == year_2:
                if year_2 < year_1:
                    year_1, year_2 = year_2, year_1
                if not years[0] <= year_1 <= years[1] or not years[0] <= year_2 <= years[1]:
                    raise ValueError(f"The entered range of years is not within the specified range \
({years[0]} - {years[1]})")
                years_choice = [year_1, year_2]
            else:
                years_choice = year_1
        elif choice == "":
            years_choice = ""
        else:
            raise ValueError("Incorrect data entered.\nformat 'YYYY' / 'YYYY YYYY' or do not enter anything")
    except ValueError as error:
        ui.invalid_choice(str(error))
        main.search_by_genre_year(genre)
    return years_choice


def search_by_genre_year(start: int, genre: str, years: int | list | None) -> None:
    """
    Handles interactive search by genre and year with pagination.

    :param start: Starting index for SQL query pagination.
    :param genre: Selected movie genre.
    :param years: Selected year or range of years.
    """
    page = 1
    check = 0
    while True:
        data, quantity = sql.search_movie_by_genre_year(genre, years, start)
        if check == 0:
            mong.add_request([genre, years], quantity)
            check = 1
        pages = quantity // 10 + (1 if quantity % 10 else 0)
        if not quantity:
            page = 0
            pages = 0
            ui.empty_result([genre, years])
        else:
            ui.show_data_frame(data, page, pages, [genre, years])
        choice = ui.data_frame_menu(page, pages, "genre")
        main_choice(choice)
        match choice:
            case "1":
                if not quantity or page == pages:
                    ui.invalid_choice(None)
                else:
                    start += 10
                    page += 1
            case "2":
                if not quantity or page == 1:
                    ui.invalid_choice(None)
                else:
                    start -= 10
                    page -= 1
            case "c":
                genres = sql.get_genres()
                choice = ui.choice_genres(genres)
                genre = choice_genre(genres, choice)
                start = 0
                page = 1
                check = 0
            case "y":
                range_years = sql.get_years()
                choice = ui.choice_year(range_years, genre)
                years = choice_year(choice, genre, range_years)
                start = 0
                page = 1
                check = 0
            case _:
                ui.invalid_choice(None)


def view_queries_action(choice: str) -> None:
    """
    Handles user actions for viewing popular or recent search queries.

    :param choice: User's menu choice.
    """
    main_choice(choice)
    match choice:
        case "1":
            data = mong.get_queries("popular")
            while True:
                choice_q = ui.show_queries_data_frame(data, "popular")
                main_choice(choice_q)
                if choice_q == "1":
                    choice = "2"
                    break
                else:
                    ui.invalid_choice(None)
        case "2":
            data = mong.get_queries("recent")
            while True:
                choice_q = ui.show_queries_data_frame(data, "recent")
                main_choice(choice_q)
                if choice_q == "1":
                    choice = "1"
                    break
                else:
                    ui.invalid_choice(None)
        case _:
            ui.invalid_choice(None)
            choice = None
    main.view_queries(choice)

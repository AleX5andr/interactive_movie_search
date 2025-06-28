import sys
import user_interface as ui
import main
import mysql_connector as sql


def stop() -> None:
    """

    """
    print("\nGoodbye!")
    print("=" * 40)
    sys.exit(0)


def main_action(choice: str) -> None:
    """

    """
    match choice:
        case "q":
            stop()
        case "1":
            main.search_by_title()
        case "2":
            main.search_by_genre_year()
        case _:
            ui.invalid_choice("")
            main.main()


def search_by_title_action(start: int, quantity: int, keyword: str) -> None:
    """

    """
    page = 1
    pages = quantity // 10 + 1
    data = []
    while True:
        if not quantity:
            page = 0
            pages = 0
            ui.empty_result(keyword)
        else:
            if not data:
                data = sql.search_movie_by_title(keyword, start)
            ui.show_data_frame(data, page, pages, keyword)
        match ui.data_frame_menu(page, pages, "title"):
            case "q":
                stop()
            case "1":
                if not quantity or page == pages:
                    ui.invalid_choice("")
                else:
                    start += 10
                    page += 1
                    data = []
            case "2":
                if not quantity or page == 1:
                    ui.invalid_choice("")
                else:
                    start -= 10
                    page -= 1
                    data = []
            case "c":
                main.search_by_title()
            case "m":
                main.main()
            case _:
                ui.invalid_choice("")


def choice_genre(genres: list, choice: str) -> str:
    """

    """
    if choice == "m":
        main.main()
    elif choice == "q":
        stop()
    try:
        choice = int(choice)
        if choice < 1 or choice > len(genres):
            raise ValueError
    except ValueError:
        ui.invalid_choice("")
        main.search_by_genre_year()
    return genres[choice - 1]


def choice_year(choice: str, genre: str, years: tuple) -> list | int | None:
    """

    """
    if choice == "m":
        main.main()
    elif choice == "q":
        stop()
    years_choice = ""
    try:
        if len(choice) == 4:
            year = int(choice)
            if not years[0] <= year <= years[1]:
                raise ValueError(f"The year entered is not within the specified range ({years[0]} - {years[1]})")
            years_choice = year
        elif len(choice) > 8:
            year_1 = int(choice[:4])
            year_2 = int(choice[-5:])
            if year_2 < year_1:
                year_1, year_2 = year_2, year_1
            if not years[0] <= year_1 <= years[1] or not years[0] <= year_2 <= years[1]:
                raise ValueError(f"The entered range of years is not within the specified range\
                 ({years[0]} - {years[1]})")
            years_choice = [year_1, year_2]
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

    """
    data, quantity = sql.search_movie_by_genre_year(genre, years, start)
    page = 1
    pages = quantity // 10 + 1
    while True:
        if not quantity:
            page = 0
            pages = 0
            ui.empty_result([genre, years])
        else:
            if not data:
                data, quantity = sql.search_movie_by_genre_year(genre, years, start)
            ui.show_data_frame(data, page, pages, [genre, years])
        match ui.data_frame_menu(page, pages, "genre"):
            case "q":
                stop()
            case "1":
                if not quantity or page == pages:
                    ui.invalid_choice("")
                else:
                    start += 10
                    page += 1
                    data = []
            case "2":
                if not quantity or page == 1:
                    ui.invalid_choice("")
                else:
                    start -= 10
                    page -= 1
                    data = []
            case "c":
                pass
            case "y":
                pass
            case "m":
                main.main()
            case _:
                ui.invalid_choice("")

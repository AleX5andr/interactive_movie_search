import settings as se
import os
import time
import pandas as pd
from colorama import Fore, Back, Style


def clear_console() -> None:
    """
    Clears the console screen for Windows, Linux, and macOS.
    """
    # Windows → cls, Linux/macOS → clear
    os.system('cls' if os.name == 'nt' else 'clear')


def main_line(text: str) -> None:
    """
    Prints a centered line of text with styled formatting.

    :param text: The text to display.
    """
    text = f"{text:^{se.INTERFACE_WIDTH}}"
    print(Fore.BLACK + Back.WHITE + text + Style.RESET_ALL)


def choice_menu() -> str:
    """
    Displays a simple menu and returns the user's choice.

    :return: The user's selected option, converted to lowercase and stripped of whitespace.
    """
    print("M. Main menu")
    print("Q. Quit")
    print_line()
    return input("Choose an option: ").strip().lower()


def print_line() -> None:
    """
    Prints a horizontal line based on the interface width.
    """
    print("-" * se.INTERFACE_WIDTH)


def invalid_choice(text: str | None) -> None:
    """
    Displays an error message for invalid user input.

    :param text: Optional custom error message.
    """
    sleep_time = 2
    if not text:
        text = "Invalid choice. Try again."
        sleep_time = 1
    print(Fore.RED + "\n" + text + "\n" + Style.RESET_ALL)
    time.sleep(sleep_time)


def empty_result(choice: str | list) -> None:
    """
    Displays a red warning message when no movies are found for the given search.

    :param choice: Search parameter.
    """
    if isinstance(choice, str):
        print(Fore.RED + f"\nThere are no movies containing the keyword '{choice}'\n" + Style.RESET_ALL)
    else:
        text = Fore.RED + f"\nThere are no {choice[0]} movies"
        if isinstance(choice[1], int):
            text += f" released in {choice[1]}."
        if isinstance(choice[1], list):
            text += f" released between {choice[1][0]} and {choice[1][1]}."
        text += Style.RESET_ALL + "\n"
        print(text)


def main_interface() -> str:
    """
    Displays the main menu interface and returns the user's choice.

    :return: User's selected option as a lowercase, stripped string.
    """
    clear_console()
    main_line("Movie search")
    print("1. Search by title")
    print("2. Search by genre and year")
    print("3. View popular or recent queries")
    print("Q. Quit")
    print_line()
    return input("Choose an option: ").strip().lower()


def input_keyword() -> str | None:
    """
    Prompts the user to enter a movie title keyword.

    :return: The entered keyword in lowercase with whitespace stripped.
    """
    clear_console()
    main_line("Search by title")
    return input("\nEnter movie title keyword: ").strip().lower()


def show_data_frame(data: tuple, page: int, pages: int, text: str | list):
    """
    Displays search results in a formatted pandas DataFrame with paging info.

    :param data: Tuple of records to display.
    :param page: Current page number.
    :param pages: Total number of pages.
    :param text: Search parameter.
    """
    clear_console()
    if isinstance(text, str):
        main_line("Search by title")
        print(f"\nSearch by keyword '{text}'")
    if isinstance(text, list):
        main_line("Search by genre and year")
        print(f"\nSelected genre - '{text[0]}'")
        if isinstance(text[1], int):
            print(f"Selected year - '{text[1]}'")
        if isinstance(text[1], list):
            print(f"Selected range of years is from {text[1][0]} to {text[1][1]}")
    print()
    df = pd.DataFrame(data, columns=se.SQL_TABLE_HEADERS)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    df["Rental cost"] = df["Rental cost"].apply(lambda item: f"{item}€")
    df["Rental duration"] = df["Rental duration"].apply(lambda item: f"{item} day(s)")
    print(df.to_markdown(tablefmt="github", index=False))
    table_lines = df.to_string(index=False).split('\n')
    max_length = max(len(line) for line in table_lines) + df.shape[1] * 3 + 1
    print()
    text = f"{page} / {pages}"
    print(f"{text:^{max_length}}\n")


def data_frame_menu(page: int, pages: int, choice: str) -> str:
    """
    Displays navigation options for paginated search results and returns user choice.

    :param page: Current page number.
    :param pages: Total number of pages.
    :param choice: Type of search.
    :return: The user's menu choice as a lowercase string.
    """
    if page < pages:
        print("1. Next page")
    if page > 1:
        print("2. Previous page")
    if choice == "title":
        print("C. Change keyword")
    elif choice == "genre":
        print("C. Change genre")
        print("Y. Change year parameters")
    return choice_menu()


def choice_genres(genres: list) -> str:
    """
    Displays a formatted menu of movie genres and returns the user's choice.

    :param genres: List of genre names.
    :return: The user's selected option as a lowercase, stripped string.
    """
    clear_console()
    col = 4
    quan = len(genres) // col + (1 if len(genres) % col else 0)
    width = len(max(genres, key=len)) + 2
    table_width = (width + 6) * col - 1
    main_line("Select a movie genre")
    for i in range(quan):
        n1 = i + 1
        n2 = i + 1 + quan
        n3 = i + 1 + quan * 2
        n4 = i + 1 + quan * 3
        text = f"{n1:^3}. {genres[n1 - 1]:<{width}}"
        text += f"{n2:^3}. {genres[n2 - 1]:<{width}}"
        text += f"{n3:^3}. {genres[n3 - 1]:<{width}}"
        if n4 <= len(genres):
            text = text + f" {n4:^3}. {genres[n4 - 1]:<{width}}"
        print(text)
    print("-" * table_width)
    print()
    return choice_menu()


def choice_year(years: tuple, genre: str) -> str | None:
    """
    Displays a prompt to specify a movie year or range and returns user input.

    :param years: Tuple with start and end years.
    :param genre: Selected movie genre.
    :return: The user's choice as a lowercase, stripped string.
    """
    clear_console()
    main_line("Specify the year of the movie")
    main_line("or a range of years")
    text = f"from {years[0]} to {years[1]} (inclusive)"
    print(f"{text:^{se.INTERFACE_WIDTH}}")
    print()
    text = "format 'YYYY' or 'YYYY YYYY'"
    print(f"{text:^{se.INTERFACE_WIDTH}}")
    text = "or do not enter anything"
    print(f"{text:^{se.INTERFACE_WIDTH}}")
    print_line()
    print(f"Selected genre - '{genre}'")
    print_line()
    return choice_menu()


def view_queries_interface() -> str:
    """
    Displays options to view popular or recent queries and returns user choice.

    :return: The user's selected option as a lowercase, stripped string.
    """
    clear_console()
    main_line("View popular or recent queries")
    print("1. View popular queries")
    print("2. View recent queries")
    return choice_menu()


def show_queries_data_frame(data: tuple, choice: str) -> str:
    """
    Displays a styled DataFrame of recent or popular queries and prompts for next action.

    :param data: Tuple of query records.
    :param choice: Type of queries to display.
    :return: The user's menu choice as a lowercase, stripped string.
    """
    clear_console()
    if choice == "recent":
        df = pd.DataFrame(data, columns=se.MONGO_TABLE_HEADERS_RECENT)
    else:
        df = pd.DataFrame(data, columns=se.MONGO_TABLE_HEADERS_POPULAR)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    table_lines = df.to_string(index=False).split('\n')
    text = ("Popular" if choice == "popular" else "Recent") + " queries"
    max_length = max(len(line) for line in table_lines) + df.shape[1] * 3 + 1
    text = f"{text:^{max_length}}"
    print(Fore.BLACK + Back.WHITE + text + Style.RESET_ALL)
    print()
    print(df.to_markdown(tablefmt="github", index=False))
    print()
    if choice == "recent":
        print("1. View popular queries")
    else:
        print("1. View recent queries")
    return choice_menu()

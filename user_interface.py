import settings as se
import os
import time
import pandas as pd
from colorama import Fore, Back, Style


def clear_console() -> None:
    """
    The function clears the user's console.
    """
    # Windows → cls, Linux/macOS → clear
    os.system('cls' if os.name == 'nt' else 'clear')


def main_line(text: str) -> None:
    """

    """
    text = f"{text:^{se.INTERFACE_WIDTH}}"
    print(Fore.BLACK + Back.WHITE + text + Style.RESET_ALL)


def choice_menu() -> str:
    """

    """
    print("M. Main menu")
    print("Q. Quit")
    print_line()
    return input("Choose an option: ").strip().lower()


def print_line() -> None:
    """

    """
    print("-" * se.INTERFACE_WIDTH)


def invalid_choice(text: str | None) -> None:
    """
    Function to display a message about an erroneous user input.

    Param text: Optional custom message to display.
    """
    sleep_time = 2
    if not text:
        text = "Invalid choice. Try again."
        sleep_time = 1
    print(Fore.RED + "\n" + text + "\n" + Style.RESET_ALL)
    time.sleep(sleep_time)


def empty_result(choice: str | list) -> None:
    """
    Function to display a message about an erroneous user input.
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
    The function responsible for visualizing the main menu
    
    return: String entered by the user
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
    Keyword input function to search by movie title In the movie database
    
    return: String entered by the user
    """
    clear_console()
    main_line("Search by title")
    return input("\nEnter movie title keyword: ").strip().lower()


def show_data_frame(data: tuple, page: int, pages: int, text: str | list):
    """
    pass
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
    pass
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
    clear_console()
    main_line("View popular or recent queries")
    print("1. View popular queries")
    print("2. View recent queries")
    return choice_menu()


def show_queries_data_frame(data: tuple, choice: str) -> str:
    """
    pass
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

import csv
import os
import re
from typing import List, Dict, Union

PHONEBOOK = "phonebook.csv"


def load_phonebook() -> List[Dict[str, str]]:
    """
    Функция, которая загружает справочник из файла в формате CSV.

    Returns:
        List[Dict[str, str]]: Список записей справочника.
    """
    phonebook = []
    if os.path.exists(PHONEBOOK):
        with open(PHONEBOOK, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                phonebook.append(row)
    return phonebook


def save_phonebook(phonebook: List[Dict[str, str]]) -> None:
    """
    Функция, которая сохраняет справочник в файл в формате CSV.

    Args:
        phonebook (List[Dict[str, str]]): Список записей справочника.
    """
    with open(PHONEBOOK, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Организация', 'Телефон рабочий', 'Телефон личный']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx, entry in enumerate(phonebook, start=1):
            entry['ID'] = idx  # Назначаем ID каждой записи
            writer.writerow(entry)


def display_page(page_num: int, entries_per_page: int, phonebook: List[Dict[str, str]]) -> None:
    """
    Функция, которая отображает на экране указанную страницу записей справочника.

    Args:
        page_num (int): Номер страницы.
        entries_per_page (int): Количество записей на странице.
        phonebook (List[Dict[str, str]]): Список записей справочника.
    """
    start_idx = (page_num - 1) * entries_per_page
    end_idx = start_idx + entries_per_page
    page_entries = phonebook[start_idx:end_idx]

    for entry in page_entries:
        print(entry)


def validate_phone_number(phone_number: str) -> bool:
    """
    Проверяет корректность формата телефонного номера.

    Args:
        phone_number (str): Телефонный номер.

    Returns:
        bool: True, если формат корректен, в противном случае - False.
    """
    # Пример формата: +7 (XXX) XXX-XX-XX
    pattern = re.compile(r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$')
    return bool(re.match(pattern, phone_number))


def validate_string_input(input_str: str, field_name: str) -> str:
    """
    Проверяет корректность строки (не пустая и не состоит только из пробелов).

    Args:
        input_str (str): Ввод пользователя.
        field_name (str): Название поля.

    Returns:
        str: Введенная строка, если корректна.

    Raises:
        ValueError: Если ввод не корректен.
    """
    if input_str.strip():
        return input_str.strip()
    else:
        raise ValueError(f"{field_name} не может быть пустым.")


def input_contact_data() -> Dict[str, str]:
    """
    Функция для ввода контактных данных (фамилия, имя, отчество, организация, рабочий телефон, личный телефон).

    Returns:
        Dict[str, str]: Словарь с контактными данными.
    """
    contact_data = {}
    try:
        contact_data['Фамилия'] = validate_string_input(input("Введите фамилию: "), "Фамилия")
        contact_data['Имя'] = validate_string_input(input("Введите имя: "), "Имя")
        contact_data['Отчество'] = validate_string_input(input("Введите отчество: "), "Отчество")
        contact_data['Организация'] = validate_string_input(input("Введите название организации: "), "Организация")

        while True:
            work_phone = input("Введите рабочий телефон в формате +7 (XXX) XXX-XX-XX: ")
            if validate_phone_number(work_phone):
                contact_data['Телефон рабочий'] = work_phone
                break
            else:
                print("Некорректный формат телефона. Пожалуйста, введите в формате +7 (XXX) XXX-XX-XX")

        while True:
            personal_phone = input("Введите личный телефон (мобильный) в формате +7 (XXX) XXX-XX-XX: ")
            if validate_phone_number(personal_phone):
                contact_data['Телефон личный'] = personal_phone
                break
            else:
                print("Некорректный формат телефона. Пожалуйста, введите в формате +7 (XXX) XXX-XX-XX")

        return contact_data
    except ValueError as e:
        print(f"Ошибка: {e}")
        return {}


def add_entry(phonebook: List[Dict[str, str]]) -> None:
    """
    Функция для добавления новой записи в справочник.

    Args:
        phonebook (List[Dict[str, str]]): Список записей справочника.
    """
    contact_data = input_contact_data()
    if contact_data:
        phonebook.append(contact_data)
        save_phonebook(phonebook)
        print("Запись добавлена успешно.")


def edit_entry(phonebook: List[Dict[str, str]], entry_idx: int) -> None:
    """
    Редактирует указанную запись в справочнике.

    Args:
        phonebook (List[Dict[str, str]]): Список записей справочника.
        entry_idx (int): Индекс записи для редактирования (начиная с 1).
    """
    try:
        # Преобразовываем индекс пользователя в индекс Python (начиная с 0)
        entry_idx -= 1

        if 0 <= entry_idx < len(phonebook):
            entry = phonebook[entry_idx]
            print("Текущая запись:")
            print(entry)

            contact_data = input_contact_data()
            if contact_data:
                entry.update(contact_data)
                save_phonebook(phonebook)
                print("Запись отредактирована успешно.")
        else:
            print("Некорректный индекс записи. Пожалуйста, выберите существующий индекс.")
    except ValueError as e:
        print(f"Ошибка: {e}")


def search_entries(phonebook: List[Dict[str, str]]) -> None:
    """
    Функция для поиска записей в справочнике по заданным характеристикам.

    Args:
        phonebook (List[Dict[str, str]]): Список записей справочника.
    """
    while True:
        search_term = input("Введите текст для поиска: ").lower()

        if not search_term.strip():
            print("Ошибка: Введите корректный текст для поиска.")
        else:
            break

    results = []
    for entry in phonebook:
        if any(search_term in value.lower() for value in entry.values()):
            results.append(entry)

    if results:
        print("Результаты поиска:")
        for result in results:
            print(result)
    else:
        print("Ничего не найдено.")


def main() -> None:
    """
    Функция,  предоставляющая интерфейс для взаимодействия со справочником.
    """
    phonebook = load_phonebook()

    while True:
        print("\nМеню:")
        print("1. Вывод постранично записей из справочника")
        print("2. Добавление новой записи в справочник")
        print("3. Возможность редактирования записей в справочнике")
        print("4. Поиск записей по одной или нескольким характеристикам")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            page_num = int(input("Введите номер страницы: "))
            entries_per_page = int(input("Введите количество записей на странице: "))
            display_page(page_num, entries_per_page, phonebook)
        elif choice == "2":
            add_entry(phonebook)
        elif choice == "3":
            entry_idx = int(input("Введите индекс записи для редактирования: "))
            edit_entry(phonebook, entry_idx)
        elif choice == "4":
            search_entries(phonebook)
        elif choice == "0":
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите снова.")


if __name__ == "__main__":
    main()

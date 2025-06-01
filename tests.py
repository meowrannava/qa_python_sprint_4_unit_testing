from main import BooksCollector

import pytest

positive_books_name = [
    'А',
    'Противостояние',
    'Девушка с татуировкой дракона и котом Бо'
]

invalid_books_name = [
        '',
        'Жутко громко, мерзко и запредельно близко',
        'Из архива Миссис Базиль Э. Франквайлер, самого запутанного в мире'
]

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # общий шаг для тестовых методов вынесен в фикстуру
    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self, collector):
        # создаем экземпляр (объект) класса BooksCollector

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    # проверка добавления новой книги – валидное название книги (сохранено в переменной)
    @pytest.mark.parametrize('name', positive_books_name)
    def test_add_new_book_valid_book_name_book_added(self, collector, name):
        initial_books_count = len(collector.get_books_genre())
        collector.add_new_book(name)
        assert name in collector.get_books_genre()
        assert len(collector.get_books_genre()) == initial_books_count + 1

    # проверка добавления новой книги – невалидное название книги (сохранено в переменной)
    @pytest.mark.parametrize('name', invalid_books_name)
    def test_add_new_book_invalid_book_name_book_not_added(self, collector, name):
        initial_books_genre = collector.get_books_genre()
        initial_books_count = len(initial_books_genre)
        collector.add_new_book(name)
        assert name not in collector.get_books_genre()
        assert len(collector.get_books_genre()) == initial_books_count
        assert collector.get_books_genre() == initial_books_genre


    # проверка установки жанра книги – существующий жанр
    def test_set_book_genre_valid_genre_genre_set(self, collector):
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.get_book_genre('Дюна') == 'Фантастика'

    # проверка установки жанра книги: негативные кейсы – несуществующий жанр / несуществующая книга /
    # пустой жанр / пустое название книги / жанр None
    @pytest.mark.parametrize('name, genre, book_name, expected', [
        (
            'Горе от ума',
            'Анекдоты',
            ['Горе от ума'],
            ''
        ),
        (
             'Шерлок Холмс и Доктор Стрендж',
             'Детективы',
             [],
             None
        ),
        (
            'Горе от ума',
            '',
            ['Горе от ума'],
            ''
        ),
        (
            '',
            'Мультфильмы',
            [],
            None
        ),
        (
            'Горе от ума',
            None,
            ['Горе от ума'],
            ''
        )
    ])
    def test_set_book_genre_invalid_genre_request_genre_not_set(self, collector, name, genre, book_name, expected):
        for book in book_name:
            collector.add_new_book(book)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == expected

    # проверка вывода жанра книги по ее имени
    @pytest.mark.parametrize('name, genre',[
        ('Солярис', 'Фантастика'),
        ('Шерлок Холмс', 'Детективы'),
        ('Каникулы в Простоквашино', 'Мультфильмы'),
        ('Кэрри', 'Ужасы'),
        ('Двенадцать стульев', 'Комедии')

    ])
    def test_get_book_genre_valid_genre_success_genre_output(self, collector, name, genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == genre

    # проверка вывода книг с определенынм жанром
    def test_get_books_with_specific_genre_valid_request_specific_genre_output(self, collector):
        collector.add_new_book('Институт')
        collector.set_book_genre('Институт', 'Ужасы')
        collector.add_new_book('Сумерки')
        collector.set_book_genre('Сумерки', 'Ужасы')

        specific_genre = collector.get_books_with_specific_genre('Ужасы')
        assert 'Институт' in specific_genre
        assert 'Сумерки' in specific_genre
        assert len(specific_genre) == 2

    # проверка вывода текущего словаря books_genre
    def test_get_books_genre_valid_request_get_all_books(self, collector):
        test_books = [
            ('Лес', 'Ужасы'),
            ('Мы', 'Фантастика')
        ]
        for name, genre in test_books:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        expected_dictionary = {
            'Лес': 'Ужасы',
            'Мы': 'Фантастика'
        }
        assert collector.get_books_genre() == expected_dictionary
        assert len(collector.get_books_genre()) == 2

    # проверка фильтра и вывод книг для детей
    @pytest.mark.parametrize('test_books, books_for_children', [
        (
                [
                    ('Кэрри', 'Ужасы'),
                    ('Я, робот', 'Фантастика'),
                    ('Автостопом по галактике', 'Фантастика'),
                    ('Гадкий утенок', 'Мультфильмы'),
                    ('Десять негритят', 'Детективы')
                ],
                ['Я, робот', 'Автостопом по галактике', 'Гадкий утенок']
        )
    ])
    def test_get_books_for_children_multiply_books_output_only_children_books(self, collector, test_books, books_for_children):
        for name, genre in test_books:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        result_books = collector.get_books_for_children()
        assert result_books == books_for_children

    # проверка добавления книги в Избранное
    def test_add_book_in_favorites_existing_book_is_success(self, collector):
        collector.add_new_book('Оно')
        collector.add_book_in_favorites('Оно')
        assert 'Оно' in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 1

    # проверка неудачного добавления в Избранное книги, отсутствующей в словаре
    def test_add_book_in_favorites_non_existing_book_is_failure(self, collector):
        collector.add_book_in_favorites('Легенды Чертаново')
        assert 'Легенды Чертаново' not in collector.get_list_of_favorites_books()

    # проверка удаления книги из избранного
    def test_delete_book_from_favorites_delete_existing_book_success(self, collector):
        collector.add_new_book('Институт')
        collector.add_book_in_favorites('Институт')
        collector.delete_book_from_favorites('Институт')
        assert 'Институт' not in collector.get_list_of_favorites_books()

    # проверка получения списка Избранное
    @pytest.mark.parametrize('name', positive_books_name)
    def test_get_list_of_favorites_books_added_existing_book_success(self, collector, name):
            collector.add_new_book(name)
            collector.add_book_in_favorites(name)
            favorites = collector.get_list_of_favorites_books()
            assert name in favorites
            assert len(favorites) == 1





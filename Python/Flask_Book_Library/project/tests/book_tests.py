import pytest
from project.books.models import Book

# Do prametryzacji
CORRECT_CASE = "correct_case"
INVALID_CASE = "invalid_case"
XSS_CASE = "xss_case"
SQLI_CASE = "sqli_case"
BOUNDARY_CASE = "boundary_case"
EXTREME_CASE = "extreme_case"

# correct cases
correct_parameters = [
    (CORRECT_CASE,"Brave New World","Aldous Huxley",1932,"Dystopian"),
    (CORRECT_CASE,"Love Hacked","Penny Reid",2014,"Romance,Humor")
]

# invalid cases
invalid_parameters = [
    (INVALID_CASE, " ", "Author", "Year", "Genre"),
    (INVALID_CASE, None, "Author", "Year", "Genre"),
    (INVALID_CASE, "Book Title", "\r\n", "Year", "Genre"),
    (INVALID_CASE, "Book Title", "~!@#$%^&*()_+", "Year", "Genre"),
    (INVALID_CASE, "Book Title", "Author", -2012, "Genre"),
    (INVALID_CASE, "Book Title", "Author", 99999, "Genre"),
    (INVALID_CASE, "Book Title", "Author", "Year", "\t"),
    (INVALID_CASE, "Book Title", "Author", "Year", None)
]

# XSS parameters
xss_parameters = [
    (XSS_CASE, "\"-prompt(8)-\"", "Author", 1990, "Genre"),
    (XSS_CASE, "Book Title", "<script\x0Atype=\"text/javascript\">javascript:alert(1);</script>", 1990, "Genre")
]

# SQLi parameters
sqli_parameters = [
    (SQLI_CASE, "' OR 'x'='x", "Author", 2023, "Romance"),
    (SQLI_CASE, "Book Title", "-- or #", 2023, "Romance")
]

# boundary parameters, minimal and maximal length
boundary_parameters = [
    (BOUNDARY_CASE, "x", "x", 1, "x"),
    (BOUNDARY_CASE, "x"*64, "x"*64, 1, "x"*20),
]

#extreme parameters
extreme_parameters = [
    (EXTREME_CASE, "x"*99999, "x"*99999, 99999, "x"*99999),
    (EXTREME_CASE, "x"*99999999, "x"*99999999, 99999999, "x"*99999999)
]


# testy z powyższymi parametrami:

@pytest.mark.parametrize("test_id, name, author, year_published, book_type", correct_parameters)
def test_book_correct_parameters(test_id, name, author, year_published, book_type):
    book = Book(name, author, year_published, book_type)
    assert book.name == name
    assert book.author == author
    assert book.year_published == year_published
    assert book.book_type == book_type
    assert book.status == "available"

@pytest.mark.parametrize("test_id, name, author, year_published, book_type", invalid_parameters)
def test_book_invalid_parameters(test_id, name, author, year_published, book_type):
    with pytest.raises(ValueError):
        Book(name, author, year_published, book_type)

@pytest.mark.parametrize("test_id, name, author, year_published, book_type", xss_parameters)
def test_book_xss_parameters(test_id, name, author, year_published, book_type):
    with pytest.raises(ValueError):
        Book(name, author, year_published, book_type)

@pytest.mark.parametrize("test_id, name, author, year_published, book_type", sqli_parameters)
def test_book_sqli_parameters(test_id, name, author, year_published, book_type):
    with pytest.raises(ValueError):
        Book(name, author, year_published, book_type)

@pytest.mark.parametrize("test_id, name, author, year_published, book_type", boundary_parameters)
def test_book_creation_boundary_parameters(test_id, name, author, year_published, book_type):
    book = Book(name, author, year_published, book_type)
    assert book.name == name
    assert book.author == author
    assert book.year_published == year_published
    assert book.book_type == book_type
    assert book.status == "available"

@pytest.mark.parametrize("test_id, name, author, year_published, book_type", extreme_parameters)
def test_book_creation_extreme_parameters(test_id, name, author, year_published, book_type):
    with pytest.raises(ValueError):
        Book(name, author, year_published, book_type)
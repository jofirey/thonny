from thonny.codeview import _is_in_string_context


def test_quote_context_detects_unfinished_strings():
    assert _is_in_string_context('print("hello', '"')
    assert _is_in_string_context("print('hello", "'")
    assert _is_in_string_context('print("""', '"')


def test_quote_context_ignores_finished_strings_and_comments():
    assert not _is_in_string_context('print("hello")', '"')
    assert not _is_in_string_context("print('hello')", "'")
    assert not _is_in_string_context('print("hello") # "still a comment', '"')

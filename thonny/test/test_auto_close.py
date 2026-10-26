from thonny import codeview
from thonny.codeview import _is_empty_auto_close_pair, _is_in_string_context


def test_quote_context_detects_unfinished_strings():
    assert _is_in_string_context('print("hello', '"')
    assert _is_in_string_context("print('hello", "'")
    assert _is_in_string_context('print("""', '"')


def test_quote_context_ignores_finished_strings_and_comments():
    assert not _is_in_string_context('print("hello")', '"')
    assert not _is_in_string_context("print('hello')", "'")
    assert not _is_in_string_context('print("hello") # "still a comment', '"')


def test_empty_auto_close_pairs_are_recognized_for_backspace():
    for opening, closing in (("(", ")"), ("[", "]"), ("{", "}"), ('"', '"'), ("'", "'")):
        assert _is_empty_auto_close_pair(opening, closing)

    assert not _is_empty_auto_close_pair("(", "]")
    assert not _is_empty_auto_close_pair("x", "x")


def test_backspace_deletes_empty_auto_close_pair(monkeypatch):
    class Workbench:
        def get_option(self, name, default):
            return True

    class Text:
        def __init__(self, opening, closing):
            self.opening = opening
            self.closing = closing
            self.deleted = None
            self.cursor = None

        def has_selection(self):
            return False

        def get(self, first, last):
            if first == "insert - 1c":
                return self.opening
            if first == "insert":
                return self.closing

        def _log_keypress_for_undo(self, event):
            pass

        def index(self, expression):
            return {"insert - 1c": "1.0", "insert + 1c": "1.2"}[expression]

        def delete(self, first, last):
            self.deleted = (first, last)

        def mark_set(self, mark, index):
            self.cursor = (mark, index)

    monkeypatch.setattr(codeview, "get_workbench", lambda: Workbench())

    for opening, closing in (("(", ")"), ("[", "]"), ("{", "}"), ('"', '"'), ("'", "'")):
        text = Text(opening, closing)
        result = codeview.CodeViewText.perform_smart_backspace(text, None)
        assert result == "break"
        assert text.deleted == ("1.0", "1.2")
        assert text.cursor == ("insert", "1.0")

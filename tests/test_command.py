import pytest

import app.command as cmd
from app.calculator import Calculator
from app.calculator_repl import Calculator_REPL

@pytest.fixture
def calculator():
    yield Calculator()

def test_base_command(calculator):
    class TestCommand(cmd.Command):
        def __init__(self, calc: calculator) -> None:
            self._calc = calc

        def execute(self) -> str:
            """Test Command"""
            return "Test"

    test_command_str = "TestCommand: Test Command\n"
    cmd.Command.help_menu_member(TestCommand)
    assert test_command_str in cmd.Command._command_menu 

def test_invalid_register(calculator):
    class BadClass:
        pass
    with pytest.raises(TypeError, \
        match="Registered class must inherit from Command"):
        cmd.Command.help_menu_member(BadClass)

def test_arithmetic_command_bad_ui_pass(calculator):
    with pytest.raises(TypeError, \
        match="Invalid UI reference configuration"):
        cmd.ArithmeticCommand(None, calculator)

def test_clear(calculator):
    clear = cmd.Clear(calculator)
    assert clear.execute() == "History cleared"

def test_exit(calculator):
    ext = cmd.Exit(calculator)
    assert "Thank you for using Python REPL Calculator" \
        in ext.execute()

def test_help(calculator):
    hlp = cmd.Help(calculator)
    assert "Interface Commands" in hlp.execute()
    assert "Arithmetic Commands" in hlp.execute()

def test_history(calculator):
    cmd.Clear(calculator).execute()
    history = cmd.History(calculator)
    assert "No history to display" in history.execute()

def test_load(calculator):
    load = cmd.Load(calculator)
    assert "Load Successful" in load.execute()
    cmd.Clear(calculator).execute()
    cmd.Save(calculator).execute()
    assert "Load Successful, but History file was empty" \
        in load.execute()

def test_redo(calculator):
    redo = cmd.Redo(calculator)
    assert "Nothing to redo" in redo.execute()

def test_save(calculator):
    save = cmd.Save(calculator)
    assert "Save Successful" in save.execute()

def test_undo(calculator):
    undo = cmd.Undo(calculator)
    assert "Nothing to undo" in undo.execute()



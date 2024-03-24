import keyboard

from executor.external import Cosmic


def run_script_handler(e: keyboard.KeyboardEvent) -> None:
    Cosmic.do_run_script = True


def pause_script_handler(e: keyboard.KeyboardEvent) -> None:
    Cosmic.do_pause_script = True


def bond_shortcut() -> None:
    keyboard.hook_key(Cosmic.run_script_shortcut, run_script_handler, suppress=False)
    keyboard.hook_key(
        Cosmic.pause_script_shortcut, pause_script_handler, suppress=False
    )

import json
from time import time

from pynput import mouse, keyboard
from pynput.mouse import Button

from executor import ScriptStep
from executor.external import CommandType
from executor.interfaces import CommandExecutorFactory
from executor.simple import SimpleCommandExecutorFactory
from recorder.interfaces import Recorder


class SimpleRecorder(Recorder):
    def __init__(self):
        self._steps: list[ScriptStep] = []
        self._pre_time: float | None = None
        self._executor_factory: CommandExecutorFactory = SimpleCommandExecutorFactory()

        # 初始化监听器
        self._mouse_listener = mouse.Listener(
            on_move=self._on_mouse_move,
            on_click=self._on_mouse_click,
            on_scroll=self._on_mouse_scroll,
        )
        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press, on_release=self._on_key_release
        )

    def _on_mouse_move(self, x, y):
        self._steps.append(
            ScriptStep(
                self._executor_factory.create(
                    CommandType.MOVE,
                ),
                json.dumps(
                    {
                        'x': x,
                        'y': y,
                        'duration': (cur_time := time()) - self._pre_time,
                    }
                ),
            )
        )
        self._pre_time = cur_time

    def _on_mouse_click(self, x, y, button, pressed):
        command_type: CommandType | None = None
        if button == Button.left and not pressed:
            command_type = CommandType.JUST_LEFT_CLICK
        elif button == Button.right and not pressed:
            command_type = CommandType.RIGHT_CLICK
        elif button == Button.left and pressed:
            command_type = CommandType.JUST_LEFT_PRESS
        elif button == Button.right and pressed:
            command_type = CommandType.JUST_RIGHT_PRESS

        if command_type is None:
            return

        self._steps.append(
            ScriptStep(
                self._executor_factory.create(command_type),
                '',
            )
        )

    # TODO 后续需要优化
    def _on_mouse_scroll(self, x, y, dx, dy):
        self._steps.append(
            ScriptStep(
                self._executor_factory.create(CommandType.SCROLL),
                json.dumps(
                    {
                        'x': dx,
                        'y': dy,
                        'duration': (cur_time := time()) - self._pre_time,
                    }
                ),
            )
        )
        self._pre_time = cur_time

    def _on_key_press(self, key):
        self._steps.append(
            ScriptStep(self._executor_factory.create(CommandType.HOTKEY), key)
        )

    # TODO 考虑是否需要
    def _on_key_release(self, key):
        pass

    def start(self):
        self._pre_time = time()
        self._mouse_listener.start()

        # NOTE 这个wait()很关键 See https://github.com/moses-palmer/pynput/issues/55
        # NOTE 不然不可以同时使用mouse_listener和keyboard_listener
        self._mouse_listener.wait()
        self._keyboard_listener.start()
        self._keyboard_listener.wait()

    # TODO 之后再实现
    def stop(self):
        raise NotImplementedError("Method not implemented yet")

    def record(self) -> list[ScriptStep]:
        self._mouse_listener.stop()
        self._keyboard_listener.stop()
        return self._steps

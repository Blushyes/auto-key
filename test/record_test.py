from time import sleep

from executor import execute
from recorder.interfaces import Recorder
from recorder.simple import SimpleRecorder

recorder: Recorder = SimpleRecorder()
recorder.start()

# 录制三秒钟的脚本
sleep(3)

script = recorder.record()

for it in script:
    print(it)

print(len(script))

execute(..., script)

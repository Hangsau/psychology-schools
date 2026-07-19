#!/usr/bin/env python
"""隱形啟動器：由 pythonw.exe（無 console）呼叫，用 CREATE_NO_WINDOW 跑 bash payload。
讓 P5 排程任務（watchdog / runner）完全不彈黑框。

用法（排程任務 action）：pythonw.exe p5-run-hidden.py "<bash -lc 的內容>"
"""
import subprocess
import sys

BASH = r"C:\Program Files\Git\bin\bash.exe"
CREATE_NO_WINDOW = 0x08000000

if len(sys.argv) < 2:
    sys.exit(1)

payload = sys.argv[1]
# 等待 bash 完成，讓排程任務的執行時長＝實際工作時長（IgnoreNew / ExecutionTimeLimit 才正確）
sys.exit(subprocess.run([BASH, "-lc", payload], creationflags=CREATE_NO_WINDOW).returncode)

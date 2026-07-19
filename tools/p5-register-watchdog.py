#!/usr/bin/env python
"""註冊 P5 管線 watchdog 為每 20 分一次的 schtasks 任務（零 LLM）。

用法：python tools/p5-register-watchdog.py
watchdog 佇列清空後會自刪本任務。重跑本腳本會覆蓋既有任務（/F）。
"""
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

TASK_NAME = "p5-watchdog"
BASH = r"C:\Program Files\Git\bin\bash.exe"
PROJ = "/c/claudehome/projects/psychology-schools"
INTERVAL_MIN = 20

RUN = f"cd '{PROJ}' && bash tools/p5-watchdog.sh"


def xml_escape(t: str) -> str:
    return (t.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def task_xml(start: datetime) -> str:
    sb = start.strftime("%Y-%m-%dT%H:%M:%S")
    cmd = xml_escape(BASH)
    args = xml_escape(f'-lc "{RUN}"')
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>P5 深化管線 watchdog（撞牆後自動重啟 / crash 恢復；零 LLM）</Description>
  </RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <StartBoundary>{sb}</StartBoundary>
      <Repetition>
        <Interval>PT{INTERVAL_MIN}M</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <ExecutionTimeLimit>PT5M</ExecutionTimeLimit>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{cmd}</Command>
      <Arguments>{args}</Arguments>
    </Exec>
  </Actions>
</Task>"""


def main() -> None:
    start = datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=2)
    xml = task_xml(start)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".xml",
                                     encoding="utf-16", delete=False) as f:
        f.write(xml)
        tmp = f.name
    try:
        r = subprocess.run(
            ["schtasks", "/Create", "/TN", TASK_NAME, "/XML", tmp, "/F"],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"schtasks 建立失敗：{r.stderr.strip()}")
            raise SystemExit(1)
        print(f"已註冊 watchdog：每 {INTERVAL_MIN} 分一次，首次 {start.strftime('%H:%M')}")
    finally:
        Path(tmp).unlink(missing_ok=True)


if __name__ == "__main__":
    main()

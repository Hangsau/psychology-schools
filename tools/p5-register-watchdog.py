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
LAUNCH_TASK = "p5-runner-launch"
BASH = r"C:\Program Files\Git\bin\bash.exe"
PROJ = "/c/claudehome/projects/psychology-schools"
INTERVAL_MIN = 20

RUN = f"cd '{PROJ}' && bash tools/p5-watchdog.sh"
# on-demand runner task：watchdog 用 schtasks //Run 觸發，讓 runner 有自己的 job object 而能存活
LAUNCH_RUN = (
    f"cd '{PROJ}' && rm -f logs/p5-runner.HALT logs/p5-runner.pid "
    f"&& bash tools/p5-deepen-runner.sh >> logs/p5-runner.log 2>&1"
)


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


def launch_task_xml() -> str:
    """on-demand（無觸發器）runner 任務；由 watchdog 以 schtasks //Run 觸發，
    讓 runner 跑在自己的 job object 裡、不會隨 watchdog 任務結束被回收。"""
    cmd = xml_escape(BASH)
    args = xml_escape(f'-lc "{LAUNCH_RUN}"')
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>P5 深化管線 runner（on-demand；watchdog 觸發）</Description>
  </RegistrationInfo>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <ExecutionTimeLimit>PT12H</ExecutionTimeLimit>
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


def _create(task_name: str, xml: str) -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".xml",
                                     encoding="utf-16", delete=False) as f:
        f.write(xml)
        tmp = f.name
    try:
        r = subprocess.run(
            ["schtasks", "/Create", "/TN", task_name, "/XML", tmp, "/F"],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"schtasks 建立 {task_name} 失敗：{r.stderr.strip()}")
            raise SystemExit(1)
    finally:
        Path(tmp).unlink(missing_ok=True)


def main() -> None:
    start = datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=2)
    _create(LAUNCH_TASK, launch_task_xml())
    _create(TASK_NAME, task_xml(start))
    print(f"已註冊 {LAUNCH_TASK}（on-demand runner）")
    print(f"已註冊 {TASK_NAME}：每 {INTERVAL_MIN} 分一次，首次 {start.strftime('%H:%M')}")


if __name__ == "__main__":
    main()

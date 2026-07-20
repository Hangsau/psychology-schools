# P6 證據保證試點報告

> 更新：2026-07-20；狀態：進行中。

## 可回復基線

- 基線 commit：`24f2e8ed3ac9e193b3574617f9005d17fc7c81db`
- CBT：synthesis `960f28da091911ff64ed57ecaab7ad5b5955572e`；meta `397a3aeb079b59698a9e1ec9f797cdf13f49d38e`
- 精神分析：synthesis `c917f622f03c08a538017c726c54afdc0849ed54`；meta `d6f0e8784e61e414741afb369af110295042512a`
- 本土心理學：synthesis `309bfa0f02eed3cca06772197d75f3b1c2e4b5d7`；meta `126494bba5b4c6e63d072d548678213e1642e77f`

## 已完成基礎設施

- `methodology/claims-schema.json`：高風險主張契約。
- `tools/verify-claims.py`：JSONL、ID、來源格式、獨立性、verdict、anchor 與 meta 計數驗證；`--strict` 可阻擋。
- `tools/verify.py --strict`：結構錯誤改以非零退出。
- `tests/test_evidence_validation.py`：涵蓋合法、空檔、malformed、部分欄位、重複 ID、壞來源、孤兒 anchor、未開始相容性。

## 首批量測

| 試點 | 已登錄 | corroborated | retrieved | 本輪正文實質修正 |
|---|---:|---:|---:|---:|
| CBT | 4 | 2 | 2 | 0 |
| 精神分析 | 4 | 1 | 3 | 2 |
| 本土心理學 | 6 | 5 | 1 | 4 組人物資料 |
| **合計** | **14** | **8** | **6** | **6 組** |

> 註：機器狀態以各篇 `claims.jsonl`／`meta.json` 為準；本表不可取代 validator。首批只建立資料契約與已知高風險問題的端到端路徑，尚未完成三篇所有高風險主張抽取，故 stage 維持 `in_progress`。

## 初步判讀

- validator 能攔截預先植入的格式、狀態與 anchor 錯誤。
- 精神分析與本土心理學在少量高風險抽取中即需修正，支持「先證據穩定化、暫停擴寫」的決策。
- CBT 首批書目與概括性療效主張較穩，但兩條書目目前只有單一官方出版清單，維持 `retrieved`。
- 下一閘門：完成三篇剩餘高風險句抽取，量測完整錯誤率與每篇成本後，才決定是否擴至 48 篇。

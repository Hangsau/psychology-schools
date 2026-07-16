# 心理學概念受控詞彙表

> 給標籤系統用。每個學派的 `meta.json` 加 `concept_tags: []`，從本表選詞。
> 與 `religions-history/00-overview/concepts.md`（14 教義類）**正交並存**：那邊是宗教教義軸，這裡是心理學建構軸。
> 跨專案對接的**主軸**是 13 領域（見 `crosswalk-13-domains.md`），本表是**輔助**細分。
> 維護：新增概念前在對話/issue 討論，避免膨脹。

---

## A. 心智結構與歷程

| 標籤 | 描述 |
|------|------|
| `unconscious` | 潛意識 / 無意識歷程 |
| `consciousness` | 意識、覺察 |
| `cognition-processing` | 認知即訊息處理（記憶/注意/思考）|
| `perception-gestalt` | 知覺組織、整體性 |
| `emotion-regulation` | 情緒與其調節 |
| `motivation-drive` | 動機、驅力、需求 |
| `self-concept` | 自我概念、自尊、認同 |

## B. 發展與形成

| 標籤 | 描述 |
|------|------|
| `developmental-stages` | 階段發展（性心理/心理社會/認知）|
| `attachment-bond` | 依附連結 |
| `early-experience` | 早期經驗形塑論 |
| `lifespan` | 全人生發展 |

## C. 學習與行為

| 標籤 | 描述 |
|------|------|
| `conditioning` | 制約（古典/操作）|
| `observational-learning` | 觀察學習、模仿 |
| `reinforcement` | 增強與後效 |
| `behavior-change` | 行為改變技術 |

## D. 病理與健康

| 標籤 | 描述 |
|------|------|
| `psychopathology` | 心理病理模型 |
| `defense-mechanism` | 防衛機制 |
| `resilience-wellbeing` | 韌性、幸福感、優勢 |
| `mind-body` | 身心關係、健康行為 |
| `biological-basis` | 神經生理基礎 |
| `adaptation-evolution` | 適應、天擇解釋 |

## E. 治療與介入

| 標籤 | 描述 |
|------|------|
| `therapeutic-relationship` | 治療關係、同理、正向關懷 |
| `insight-oriented` | 洞察導向（潛意識素材）|
| `cognitive-restructuring` | 認知重建、駁斥非理性信念 |
| `mindfulness-acceptance` | 正念、接納、脫鉤 |
| `narrative-meaning` | 敘事、意義建構、外化 |
| `experiential-expressive` | 體驗性 / 表達性（藝術/遊戲/角色）|
| `solution-focused` | 焦點解決、例外導向 |
| `family-systems` | 家庭系統、關係脈絡 |

## F. 存在與超越

| 標籤 | 描述 |
|------|------|
| `meaning-existential` | 意義、自由、責任、死亡焦慮 |
| `self-actualization` | 自我實現、潛能 |
| `transpersonal-spiritual` | 靈性經驗、超越自我、意識擴展 |

## G. 社會與文化

| 標籤 | 描述 |
|------|------|
| `social-influence` | 社會影響、從眾、服從、態度 |
| `social-construction` | 社會建構、語言中介 |
| `cultural-context` | 文化脈絡、本土契合、跨文化 |
| `power-gender` | 權力、性別、多元文化批判 |

---

## 使用方式

1. 讀該學派 `synthesis.md`。
2. 從上表選**最相關 3–8 個** `concept_tags`，填回 `meta.json`。
3. **不允許**自創標籤；必要新概念 → 對話討論加入本表。
4. 反向索引：`tools/build-index.py` → `00-overview/concept-index.json`。

> 跨宗教對接以 `domain_tags`（13 領域）為主，`concept_tags` 供學派間細部檢索。

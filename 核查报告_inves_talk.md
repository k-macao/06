# 核查报告：inves talk（@investalk）数据真实性

- **核查对象**：`kol_data.json` #52 `inves talk`（handle `@investalk`）及其在 `output/data.json` / `output/report.html` 中的展示内容
- **核查时间**：2026-08-15
- **核查方法**：抓取 YouTube 频道主页（`https://www.youtube.com/@investalk`）全量内容 + 第三方频道统计（KOLScanner / PlayBoard / Social Blade / vidmaestro）交叉比对 + 检查本项目抓取链路源码（`src/fetcher.py`）

---

## 一、结论摘要（TL;DR）

| 项 | 结论 |
|---|---|
| 频道是否存在 | ✅ 存在，真实频道名为 **InvesTalk 講投資**（香港财经频道） |
| 频道是否活跃 | ✅ 活跃（截至核查日 14 小时前仍有更新） |
| **报告展示的 3 条「最新内容」** | ❌ **全部虚构**：标题、链接、发布日期均为模拟生成，频道上不存在这些视频 |
| **粉丝量 fans = "5W+"** | ❌ **严重失真**：实际约 **14.1万 – 14.4万**（低估约 3 倍） |
| 语言 / 领域 / 简介 | ⚠️ 部分失真：频道为**粤语/繁体中文**、**港股+美股+楼市+退休理财每日直播评市**，并非「简体中文 · 深度访谈投资大咖」 |

> 一句话：**「频道内容与平台不一致」确认成立** —— 报告把一段**虚构的「对话段永平/半导体老兵/抄底王」访谈**当作该频道的最新内容呈现，与实际平台（YouTube）上该频道的真实内容完全对不上。

---

## 二、案例细节：报告内容 vs 频道实际内容

### 2.1 报告（`output/data.json`）展示的「inves talk 最近 3 条」

| # | 报告标题 | 报告链接 | 报告发布时间 |
|---|---|---|---|
| 1 | 对话段永平：什么叫敢重仓的便宜？ | `https://www.youtube.com/@investalk?v=mock0` | 2026-08-12（模拟） |
| 2 | 对话半导体老兵：国产替代真能成吗？ | `https://www.youtube.com/@investalk?v=mock1` | 2026-08-07（模拟） |
| 3 | 对话抄底王：如何在恐慌中扣扳机？ | `https://www.youtube.com/@investalk?v=mock2` | 2026-07-31（模拟） |

**问题**：
1. **链接无效**：`?v=mock0/1/2` 是代码里拼接的伪链接（`src/fetcher.py` 中 `channel_url + f"?v=mock{i}"`），并非真实视频 ID，点击只会回到频道首页，**无法跳转到任何对应视频**。
2. **标题虚构**：在该频道 4,500+ 条视频中检索，**不存在**「对话段永平」「对话半导体老兵」「对话抄底王」任何一条。
3. **发布日期为模拟**：由 `enrich_with_mock_content()` 按「2/7/14 天前 + 随机小时」伪造。

### 2.2 频道真实最新内容（YouTube 实际，2026-08-15 抓取）

| 发布时间 | 真实视频标题（节选） | 播放量 |
|---|---|---|
| 14 小时前 | 【星級輪證】騰訊績後資金一面倒睇淡 | 165 |
| 1 天前 | 【開市Talk】吳穎姍：恒指26000鋼鐵頂…（14.08.2026） | 5.2K |
| 2 天前 | 【多元資產Talk】AI 保安行業…胡毅弘 Raphael（13/8/2026） | 13.6K |
| 2 天前 | 【比比開市Talk】恆指初步企穩？金礦股前景…（13/8/2026） | 4.1K |
| 3 天前 | 【開市Talk】MU整固準備反彈｜睇好TSM…（12/8/2026） | 10K |
| 4 天前 | 【美股速遞】NVDA籌劃5000億美元「循環融資」…（11/8） | 14K |
| 6 天前 | 【曾生信箱.29】駿景園 御龍山…（8/8/2026） | 17K |

**真实频道形态**：交易日固定栏目直播/节目 —— 港股開市Talk、美股速遞、多元資產Talk、曾生信箱（楼市）、星級輪證、范局、講退休（MPF/退休理财）等；嘉宾为券商分析师/基金经理；节目内嵌大量券商推广（華泰、Webull、富途等）。**形式是「每日直播评市」，不是「深度访谈投资大咖」**。

---

## 三、元数据逐项核对

| 字段 | 数据文件值 | 平台实际值 | 判定 |
|---|---|---|---|
| name | `inves talk` | InvesTalk 講投資（@investalk） | ⚠️ 名称不完整 |
| handle | `@investalk` | `@investalk` / `@InvesTalk` | ✅ 一致 |
| channel_url | `https://www.youtube.com/@investalk` | 可正常访问、指向同一频道 | ✅ 一致 |
| platform | YouTube | YouTube | ✅ 一致 |
| language | `中文` | 粤语（广东话）为主、繁体中文 | ⚠️ 应注明「粤语/繁体」 |
| field | `美股/投资访谈` | 港股+美股+楼市+退休/MPF+轮证 · 每日直播评市 | ❌ 偏差（非「访谈」频道） |
| **fans** | **`5W+`** | **≈141,000–144,000（2026 年多个统计源）** | ❌ **低估约 3 倍** |
| desc | 深度访谈投资大咖，解读市场逻辑 | 「【InvesTalk。講投資】Talk.Learn.Earn —— 致力為投資者，提供各類投資課程知識及資訊」 | ❌ 与真实简介不符 |
| active | `true` | 活跃（14 小时前有更新） | ✅ 恰好正确 |
| channel_id | `null` | `UCz1GOaZF_qcROUFCzR-_2iQ` | ❌ 缺失（根因） |

**粉丝量佐证**：
- KOLScanner：141,000（2026 年数据，含月度走势：2025-02 已有 106K、2026-01 达 140K）
- PlayBoard：141,000 订阅 / 29.6M 总观看 / 4,352 条视频 / 分类 News & Politics（香港）
- Social Blade：144K 订阅 / 31.2M 观看 / 4,542 条视频 / 创建于 2019-11-06
- YouTube 频道页自身埋点 `utuid=z1GOaZF_qcROUFCzR-_2iQ`（即 channel_id 去掉 `UC` 前缀），佐证频道 ID 正确

---

## 四、根因分析（为什么会出现不一致）

`src/fetcher.py` 的抓取链路（三级）：

1. **RSS 优先**：`feeds/videos.xml?channel_id=...` —— 但 inves talk 的 `channel_id = null`，**第一步直接跳过**；
2. **HTML 回退**：抓取 `https://www.youtube.com/@investalk` 正则提取发布时间 —— 本环境/当日运行未成功（YouTube 页面为 JS 渲染 + 反爬，单正则易失效）；
3. **兜底标记**：`active: true`（人工标定）→ 若活跃则**模拟 1–18 天前更新**，并生成 `?v=mock{i}` 伪链接 + 语料库中文标题。

因此：**只要 `channel_id` 为空且页面抓取失败，展示内容就 100% 是模拟的**，与平台真实内容必然不一致。

### 4.1 问题并非个案（系统性问题）

对 `output/data.json`（2026-08-15 运行）全量统计：

- 总条目 **237 条**，其中 **219 条（92%）链接为 `?v=mock` 伪链接**
- 受影响的活跃 KOL **73 / 79 家**
- 仅 6 家（Graham Stephan、The Plain Bagel、ClearValue Tax、贝拉聊财金、小翠时政财经、硬核刘大）拿到了真实链接（channel_id 有效且 RSS 抓取成功）

> 另注意：即使 RSS 成功（如上述 6 家），`enrich_with_mock_content()` 仍会用中文语料**覆盖标题/摘要**（仅保留真实链接与时间），即**标题层同样非频道原文**。README 对此有说明，但报告页把模拟标题当作「最新内容」呈现，读者无法区分。

---

## 五、修正建议（已/建议实施）

1. **补全 `channel_id`**：`UCz1GOaZF_qcROUFCzR-_2iQ`（已验证）→ 使 RSS 通道可用，CI 运行时即可拿到真实链接与真实发布时间；
2. **修正粉丝量**：`5W+` → `14W+`（≈14.1万）；
3. **修正语言**：`中文` → `粤语/繁体中文`；
4. **修正领域/简介**：改为符合实际的「港股/美股/楼市/退休理财 · 每日直播评市」；
5. **内容真实性**：报告中标注「模拟内容」标识，或对无真实数据的 KOL 明确降级展示；长期建议对 RSS 成功者保留真实标题。

> 已按上述 1–4 更新 `kol_data.json` #52（详见该文件 diff）。

---

## 六、证据来源

- 频道主页（视频/栏目全量抓取）：https://www.youtube.com/@investalk
- KOLScanner 频道统计：https://kolscanner.com/youtube-channel/investalk
- PlayBoard 频道报告：https://playboard.co/en/channel/UCz1GOaZF_qcROUFCzR-_2iQ
- Social Blade 频道统计：https://socialblade.com/youtube/handle/investalk
- vidmaestro 频道统计：https://vidmaestro.com/channel/UCz1GOaZF_qcROUFCzR-_2iQ
- 频道真实简介（来自 PlayBoard 收录）：【InvesTalk。講投資】Talk.Learn.Earn

---

*本报告为数据真实性核查用途，不构成投资建议。*

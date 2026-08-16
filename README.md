# 🐙 全球财经金融 KOL 精选名单 · 多空全景战报

> **复古游戏章鱼风格 · 凸显多空战斗元素**  
> **作者：章鱼 AI·全景分析**  
> **Pixel Battlefield Edition — BULL VS BEAR**

[![Generate Report](https://github.com/k-macao/06/actions/workflows/daily.yml/badge.svg)](https://github.com/k-macao/06/actions)
![Python](https://img.shields.io/badge/python-3.11-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## 📸 预览 Preview

![Pixel Battle](assets/pixel_battle.png)

**在线预览 Live Preview** → `output/report.html`  
`python -m http.server --directory output 8000` → http://localhost:8000/report.html

- 8-bit 章鱼边框 + 扫描线 + Neon 网格背景
- 🐂 多头军团 vs 🐻 空头军团 血条可视化
- 每位 KOL 卡片：头像章鱼化 + 平台徽章 + 粉丝量 + 最多 3 条官方 RSS 内容
- 每条内容：频道原始标题 + AI 多空研判 + 置信度 + 战斗力 + 策略建议
- 顶栏：本次已验证频道与真实条目数 · 主导阵营实时计算
- 筛选器：全部 / 多头 / 空头 / 中性 / 中文 / 英文

---

## 🗂️ KOL 精选名单（97 家）

### 英文财经巨头 20 席
| # | 名称 | 平台 | 领域 |
|---|------|------|------|
| 01 | Graham Stephan | YouTube | 个人理财/房地产 400W+ |
| 02 | Andrei Jikh | YouTube | 股息投资 200W+ |
| 03 | Humphrey Yang | TikTok/YT | 金融科普 300W+ |
| 04 | The Plain Bagel | YouTube | CFA投资教育 100W+ |
| 05 | Patrick Boyle | YouTube | 对冲基金/金融史 60W+ |
| 06 | Meet Kevin | YouTube | 美股/宏观 190W+ 高频日更 |
| 07-11 | Joseph Carlson / Sven Carlin / Mark Tilbury / Jeremy Lefebvre / Ben Felix | ... | 价值/成长/指数 |
| 12-15 | Erika Kullberg / Vivien Tu / Jaspreet Singh / Investing with Rose | TikTok/IG | 法律/女性/心态/新手 |
| 16-20 | ClearValue Tax / Everything Money / New Money / Financial Education / Brian Feroldi | YouTube | 税务/估值/巴菲特/实战 |

### 中文财经矩阵 14 席
| # | 名称 | 平台 | 特点 |
|---|------|------|------|
| 21 | 贝拉聊财金 | YT 20W | 美股深度 逻辑严密 |
| 22 | 阳光财经 | YT 30W | 技术+基本面 |
| 23 | 小翠时政财经 | YT 20W | 宏观/金融时事 深度拆解 |
| 24 | 视野环球镜 | YT 50W | 地缘金融（⚠️ 沉寂已剔除） |
| 25-26 | 老李财经 / 瑞威金融 | YT | 科技半导体 / 外汇黄金 |
| 27-34 | 财女Nicole / 孟岩 / 零总 / 孙老师 / 美股投资网 / 逻辑财金 / 大马理财 / 美股说 | ... | ... |

### 全球配置 & 技术派 16 席
Kelvin, Swedish Investor, Preston Pysh, PensionCraft, Maverick, Cameron Stewart, FAST Graphs, TradingView Top Authors, Real Vision 等。

**额外增补 3 席**：`老厉害财经` `inves talk` `硬核刘大 (刘老哥)`

### 港澳、中国与台湾财经扩展 44 席
新增香港财经媒体 `信報財經新聞`、`Finance730`、`香港經濟日報 HKET`、`香港財經時報 HKBT`、`新城財經台`，以及中国宏观、港美股与台湾投资频道，包括 `财经风云`、`视野环球财经`、`财经冷眼`、`老蛮频道`、`付鹏说`、`财经M平方 MacroMicro`、`游庭皓的財經皓角`、`柴鼠兄弟 ZRBros`、`Gooaye股癌`、`股海老牛` 等。完整名单及频道链接请见数据文件。

> 📌 **完整数据**：`kol_data.json`（共 97 家，含 handle/channel_id/fans/field/platform 等）

---

## 🔍 排查逻辑：哪些内容可以入报？

`src/fetcher.py` 采用真实性优先、失败关闭（fail closed）的抓取策略：

1. **尊重人工隔离**：`active: false` 的重复、失实或停用记录不会进行线上探测。
2. **确认真实频道**：优先使用 URL 自带的 `/channel/UCxxx`，其次格式有效的 `channel_id`；只有 `@handle` / `/c/` / `/user/` 链接时从真实频道页解析 `channelId`（自愈）。配置值与频道页不一致时**失败关闭**；搜索结果页和非 YouTube 占位链接一律拒绝。
3. **五级可验证来源链**：官方 RSS → YouTube Data API（可选 `YOUTUBE_API_KEY`）→ [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)（只取元数据，不下载）→ 频道 `/videos` 页结构化数据 → 上次已通过审计且仍在时效内的缓存。每条内容都带 `source` 与来源频道标记。
4. **字幕补全**：来源没有简介时，用 [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api) 的真实字幕生成摘要，不覆盖来源原有简介。
5. **90 天新鲜度门槛**：最新有效条目在 `ACTIVE_THRESHOLD_DAYS` 内才可进入日报。
6. **全部失败即隔离**：不回退到静态 `active` 标记，不伪造日期与内容。

抓取失败、平台暂不支持或来源无法验证时，记录会显示为「⚠️未验证」并隔离，**不会再根据 `active` 标记伪造更新日期**。

```bash
python -m src.fetcher
# 输出示例：✅已验证 [01] Graham Stephan | 最近: 2026-08-14
#            ⚠️未验证 [12] Erika Kullberg   | 最近: 未知
```

---

## 📥 真实内容策略

`enrich_with_real_content()`（别名 `enrich_with_verified_content()`）只补充展示字段，不改写来源内容：

- `title` 必须与 `original_title` 完全一致；
- `link` 必须是 YouTube 视频、Shorts 或直播链接（`?v=mock` 等伪链接直接丢弃）；
- `published` 必须来自真实来源；
- 每条内容带 `source`（`youtube_rss` / `youtube_data_api` / `yt_dlp` / `youtube_channel_page` / `verified_cache`）、`source_channel_id` 与 `is_mock: false`；
- 有几条有效内容就展示几条（最多 3 条），绝不为了固定版面补足模拟条目。

模拟日期与 `?v=mock` 链接已从生产抓取链路中移除。`MOCK_TITLES_POOL` 语料库仅作为**历史伪造标题黑名单**保留，供审计模块比对识别，不再参与内容生成。

---

## 🧠 AI 多空分析

`src/analyzer.py` · 离线启发式引擎（无须 API Key）

- **词库**：多头 30+ 关键词（上涨/利好/买入/突破/牛市/降息…） + 空头 30+（下跌/抛售/泡沫/风险/衰退/做空…） + 中性线索
- **加权**：标题含 “？” +0.5 中性；“！”放大主导情绪
- **判定**：
  - `bull_hits > bear_hits + 0.5` → 多头 (置信 62-92%)
  - `bear_hits > bull_hits + 0.5` → 空头 (60-91%)
  - 否则 中性 (55-67%)
- **战斗力 POW**：`confidence * 0.85 + rand`，1-99
- **理由模板**：根据命中词与标题自动生成中文研判
- **策略**：多头→“逢低分批建仓”；空头→“降低仓位等待恐慌”；中性→“区间操作”

每条内容输出：`sentiment` / `confidence` / `power` / `reason` / `advice`  
每位 KOL 聚合：`bull vs bear vs neutral` → 阵营标签 `多头阵营 / 空头阵营 / 均衡拉锯 / 轻度偏多/空`

全市场战场：`global_battle_stats()` 按本次取得的真实条目动态统计多/空/中性占比并判定主导。

---

## 🎮 章鱼报告生成

`src/report_generator.py` · Jinja2 模板 + 手绘章鱼美术

- 字体：`Press Start 2P`（章鱼标题） + `Noto Sans SC`（正文）
- 边框：4px 白描边 + 黑色偏移阴影 + 内部虚线（纯 CSS 章鱼风）
- 背景：32px 网格 + 扫描线叠加
- 元素：
  - 顶部 `BULL VS BEAR` 街机横幅 + 血条 HP 92/120 vs 68/120
  - 中间 `pixel_battle.png` 斗兽场大图（BOOM! SMASH! 章鱼爆破）
  - 血条：`bull_ratio / bear_ratio / neutral_ratio` 百分比填充
  - 卡片：保留 `kol_data.json` 的 `#01-97` 编号徽章 + 平台标签 + 粉丝爱心 + 战斗徽章
  - 条目：左侧 ▶ 箭头 + POW 能量条 + 迷你多空徽章 + 🧠 研判 + 🎯 策略

```bash
python main.py --no-push  # 仅生成；若没有任何可验证内容则失败退出
# output/report.html  动态大小
# output/data.json    仅含本次验证通过的真实来源条目
```

---

## 📨 推送 PushPlus（微信）

`src/pushplus.py` · `src/digest.py`

- 接口：`http://www.pushplus.plus/send`
- 参数：`token` + `title` + `content` (html) + `template=html` + `channel=wechat`
- **内容：自动使用战斗风精简摘要版**（`src/digest.py` 生成，避免频道数量增长时超过 PushPlus 上限）
  - 战斗排版含：⚔️ 多空战场横幅 · 🐂🐻 HP 血条 · 👑 主导阵营与战场风向 · 🏆 多头/空头 MVP · 🔥 多头猛攻 TOP5 · 💣 空头重击 TOP5 · 🛡️ 军团花名册（5 大阵营分组）· 本次隔离/未验证名单
- 配置方式（优先级递减）：
  1. `python main.py --token YOUR_TOKEN`
  2. 环境变量 `PUSHPLUS_TOKEN`
  3. `config.yaml` 中 `pushplus_token`

```bash
# ① 先发一条测试消息验证链路（token/实名/关注公众号是否正常）
bash push_demo.sh test <你的token>
# 返回 code=200 说明链路正常，微信应收到「✅ PushPlus 链路测试成功」

# ② 完整流水线 + 推送
export PUSHPLUS_TOKEN="你的token"
python main.py              # 自动抓取 + 分析 + 生成 + 推送（摘要版）
python main.py --no-push    # 本地预览不推送
python main.py --push-only  # 仅推送（复用上次 output/data.json，适合补推/重推）
```

> 获取 Token：http://www.pushplus.plus/push1.html  
> 推送标题示例：`🐙章鱼战场·KOL多空战报 2026年08月16日 | 已验证21/97 主导:空头`。`main.py` 与 `--push-only` 都会在推送前执行真实性审计，不能绕过门禁。

**收不到消息？按以下顺序排查：**

1. **微信必须关注「PushPlus」公众号**（服务号，模板消息经它送达）
2. **必须实名认证**：2024-08 起未实名返回 `905`，无法发送（pushplus.plus 微信扫码实名）
3. **token 是否有效**：返回 `903` = token 无效，到 pushplus.plus 重新复制，并同步更新仓库 Secret `PUSHPLUS_TOKEN`
4. **请求次数限制**：相同内容 1 小时最多 3 条；1 分钟最多 5 次；每日超 200 次当日停止（返回 `900`）。在公众号里发送「请求次数」可查询
5. **接口是异步的**：返回 `200` 只代表服务端收到请求，不代表已送达；若返回 200 但没收到，多为上述 1/2 未完成

**推送失败时**：`main.py` 退出码非 0，GitHub Actions 会显示 ❌ 而不是假绿；日志会打印错误码与中文原因（903/905/900/888 等）。

---

---

## 🔍 不作伪检查模块（真实性审计）

`src/authenticity_check.py` —— 对 KOL 名单与生成结果做防伪审计，防止"假数据/假链接"混入报告：

```bash
python -m src.authenticity_check                    # 离线全量审计（97 家）
python -m src.authenticity_check --online --strict  # 在线验证 + 严格门禁（CI 用）
python -m src.authenticity_check --md output/audit_report.md --json output/audit_report.json
python main.py --strict-audit                       # 生成后自动审计，检出伪造即退出码非 0
```

- **元数据层**：检查 channel_id、handle、搜索页占位、域名与 fans。未入报的存疑记录记为 WARN 并保持隔离；若同一问题污染了本次报告则升级为 FAIL。
- **内容层**：`is_mock: true`、`?v=mock` 伪链接、标题与 `original_title` 不一致、命中历史 `MOCK_TITLES_POOL` 语料的伪标题、来源标记不受支持、来源频道不一致、缺失/未来日期均为 FAIL。
- **来源标记**：RSS 与官方 API 条目必须带合法 `source_channel_id`（否则 FAIL）；yt-dlp / 频道页 / 缓存链路拿不到频道 ID 时记 WARN，避免可用性下降被误判为伪造。
- **在线层**（`--online`，需网络）：只复核本次报告实际引用的频道页和 RSS，避免 97 家目录中的隔离项造成无关抖动。
- **CI 门禁**：workflow 先运行回归测试，再生成报告，最后执行 `python -m src.authenticity_check --online --strict`；只有零 FAIL 才允许 PushPlus 推送。

> 📌 2026-08-15 首次全量排查：237 条内容中 **219 条（92.4%）为 mock 伪链接**；已修正 18 家频道的 channel_id/粉丝量/名称等失实字段（详见 `核查报告_全频道.md`）。
>
> 📌 2026-08-16 二轮整改：补全 **45 家** channel_id，消除全部 `results?search_query=` 搜索页占位链接，8 家疑似虚构/无内容/停更频道标记 `active=false`（详见 `核查报告_全频道_20260816b.md`）。
>
> 📌 2026-08-16 三轮整改（本轮）：生产抓取链移除所有 Mock 兜底，条目必须携带 `original_title` 与来源标记；旧报告已清除伪链接与改写标题。目录中暂未核实的记录保留作后续修订，但不会进入日报。

---

## ⚙️ 快速开始

```bash
git clone https://github.com/k-macao/06.git
cd 06
pip install -r requirements.txt   # 或 pip install --break-system-packages -r requirements.txt

# 1. 本地生成预览
python main.py --no-push
python -m http.server --directory output 8000 --bind 0.0.0.0
# 打开 http://localhost:8000/report.html

# 2. 配置推送后一键全链路
export PUSHPLUS_TOKEN=xxxx
bash push_demo.sh test $PUSHPLUS_TOKEN   # 先测链路
python main.py                            # 再正式推送
```

---

## 🗓️ 定时任务

`.github/workflows/daily.yml`：每天 UTC 02:00（北京时间 10:00）自动运行

```yaml
- cron: '0 2 * * *'          # 每天 UTC 02:00（北京时间 10:00）
- pip install -r requirements.txt
- PUSHPLUS_TOKEN=${{ secrets.PUSHPLUS_TOKEN }} python main.py
- 上传 artifact: output/report.html
```

在 GitHub 仓库 `Settings → Secrets → Actions` 添加 `PUSHPLUS_TOKEN` 即可。
> 💡 建议：可将 CI 拆为「生成（`python main.py --no-push`）+ 推送（`python main.py --push-only`）」，
> 缺 token 时明确报错。改进版 `daily.yml` 见工作区 `.github/workflows/`（需有 `workflows` 权限的账号提交）。

---

## 📁 项目结构

```
06/
├── kol_data.json              # 97 家 KOL 元数据与人工隔离开关
├── config.yaml                # PushPlus 与阈值配置
├── requirements.txt
├── main.py                    # 一键流水线
├── src/
│   ├── config.py
│   ├── fetcher.py            # 频道身份验证 + 官方 RSS 抓取
│   ├── analyzer.py           # 多空研判
│   ├── report_generator.py   # 章鱼 HTML
│   └── pushplus.py
├── assets/
│   └── pixel_battle.png      # 8-bit 斗兽场头图
├── output/
│   ├── report.html           # 最终战报（推送本体）
│   ├── data.json             # 结构化数据
│   └── pixel_battle.png
├── .github/workflows/daily.yml
└── README.md
```

---

## 🔧 自定义

- 增减 KOL：编辑 `kol_data.json`；`active: false` 会强制隔离，`active: true` 仍须通过真实频道与 RSS 验证
- 调阈值：`config.yaml` → `active_threshold_days`
- 换 PushPlus 渠道：`channel: webhook` 等
- 换分析逻辑：在 `src/analyzer.py` 扩充 `BULL/BEAR_KEYWORDS` 或接入 LLM API

---

## ⚠️ 声明

- 当前可入报的数据来源仅为 YouTube 官方 RSS；其他平台记录在实现可信抓取器前保持隔离
- 本报告由 AI 启发式引擎生成，仅供研究与演示，不构成投资建议
- 复古章鱼美术由 AI 生成，版权归本项目所有

---

**🐙 章鱼 AI·全景分析 | Pixel Battlefield — 2026.08.07**

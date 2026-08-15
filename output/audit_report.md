# 🔍 全频道真实性审计报告（不作伪检查模块）

- **审计时间**：2026-08-15T07:17:38.712346+00:00
- **KOL 总数**：97　|　**PASS**：0　|　**WARN**：16　|　**FAIL**：81
- **内容条目**：共 237 条，其中**伪链接（mock）219 条（92.4%）**，语料库标题 234 条
- **在线验证**：未开启（离线审计，建议 CI 中 --online 复核）

## 判定口径
- **FAIL**：检测到伪造内容（伪链接等）或在线验证确认元数据严重失实
- **WARN**：元数据不完整（channel_id/fans 缺失等）→ 无法证明真实，需人工核
- **PASS**：无伪造痕迹且元数据完整（在线模式还要求验证通过）

| # | 名称 | 平台 | fans | channel_id | 判定 | mock/总条目 | 主要问题 |
|---|------|------|------|-----------|------|-----------|---------|
|  1 | Graham Stephan | YouTube | 400W+ | UCV6KDgJskWa | **WARN** | 0/3 | 条目1 标题来自模拟语料库（非频道原文）: 「美联储突然转向？2026年降息押注与房贷利率崩跌前夜」；条目2 标题来自模拟语料库（非频道原文）: 「我为什么还在 |
|  2 | Andrei Jikh | YouTube | 200W+ | UCGyqEtB6LDK | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@AndreiJikh?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模拟 |
|  3 | Humphrey Yang | TikTok/YT | 300W+ | UCF8yH-_MqvY | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@humphreytalks?v=mock0（点击无法到达任何真实视频）；条目1 标题来 |
|  4 | The Plain Bagel | YouTube | 100W+ | UCFCEuCsyWP0 | **WARN** | 0/3 | 条目1 标题来自模拟语料库（非频道原文）: 「杠杆ETF是财富加速器还是绞肉机？」；条目2 标题来自模拟语料库（非频道原文）: 「BlackRock与Vangu |
|  5 | Patrick Boyle | YouTube | 60W+ | UCq1JpL5CMF7 | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@PBoyle?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模拟语料库（ |
|  6 | Meet Kevin | YouTube | 190W+ | UCUvvjPO5z2V | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@MeetKevin?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模拟语 |
|  7 | Joseph Carlson | YouTube | 30W+ | UCaWYZFsL5-1 | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@JosephCarlsonShow?v=mock0（点击无法到达任何真实视频）；条目1 |
|  8 | Sven Carlin | YouTube | 25W+ | UCpM2N7Rg5q5 | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@Value-Investing?v=mock0（点击无法到达任何真实视频）；条目1 标 |
|  9 | Mark Tilbury | TikTok/YT | 700W+ | UCxgAuX3XZRO | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@MarkTilbury?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模 |
| 10 | Jeremy Lefebvre | YouTube | 70W+ | UCZ2zU5T4v4s | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@FinancialEducation?v=mock0（点击无法到达任何真实视频）；条目 |
| 11 | Ben Felix | YouTube | 50W+ | UCDaP94y6a6r | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@BenFelixCSI?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模 |
| 12 | Erika Kullberg | IG/TikTok | 500W+ | — | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.tiktok.com/@erikakullberg?v=mock0（点击无法到达任何真实视频）；条目1 标题来自 |
| 13 | Vivien Tu | TikTok/IG | 200W+ | — | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.tiktok.com/@yourrichbff?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模拟 |
| 14 | Jaspreet Singh | YouTube | 160W+ | UC3p5y1b3b3b | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@MinorityMindset?v=mock0（点击无法到达任何真实视频）；条目1 标 |
| 15 | Investing with Rose | YouTube | 60W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 16 | ClearValue Tax | YouTube | 150W+ | UCigUBIf-zt_ | **WARN** | 0/3 | 条目1 标题来自模拟语料库（非频道原文）: 「2026新税法：这4个抵扣让中产多退5000刀」；条目2 标题来自模拟语料库（非频道原文）: 「IRS 审计率飙升 |
| 17 | Everything Money | YouTube | 20W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 18 | New Money | YouTube | 70W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 19 | Financial Education | YouTube | 70W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；channel_url 与 handle 不一致: https:// |
| 20 | Brian Feroldi | YouTube | 5W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 21 | 贝拉聊财金 | YouTube | 40W+ | UCVomjkM_t0E | **WARN** | 0/3 | channel_url 与 handle 不一致: https://www.youtube.com/@user-bella-finance vs @贝拉聊财金； |
| 22 | 阳光财经 | YouTube | 30W+ | UC2I5em6UyBp | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@阳光财经?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模拟语料库（非频 |
| 23 | 小翠时政财经 | YouTube | 20W+ | UCOhck8oLoIw | **WARN** | 0/3 | 条目1 标题来自模拟语料库（非频道原文）: 「社融暴跌背后：居民为什么不敢借钱了？」；条目2 标题来自模拟语料库（非频道原文）: 「地方城投展期潮：谁在为土地财 |
| 24 | 视野环球镜 | YouTube | 50W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；channel_url 与 handle 不一致: https:// |
| 25 | 老李财经 | YouTube | 15W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 26 | 瑞威金融 | YouTube | 10W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 27 | 财女Nicole | YouTube | 15W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 28 | 孟岩的投资笔记 | YouTube/Web | 10W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；channel_url 与 handle 不一致: https:// |
| 29 | 零总投资 | YouTube | 8W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 30 | 孙老师财经 | YouTube | 15W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 31 | 美股投资网 | YouTube | 10W+ | UCWyPo32TSKP | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@美股投资网?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模拟语料库（非 |
| 32 | 逻辑财金 | YouTube | 12W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 33 | 大马理财 | YouTube | 10W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 34 | 美股说 | YouTube | 5W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 35 | Kelvin Learns Investin | YouTube | 10W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 36 | The Swedish Investor | YouTube | 80W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 37 | Preston Pysh | Reddit/YT | 15W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 38 | PensionCraft | YouTube | 20W+ | UC4TCb53He0U | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@PensionCraft?v=mock0（点击无法到达任何真实视频）；条目1 标题来自 |
| 39 | Ramin Nakisa | YouTube | 20W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 40 | Financial Diet | YouTube | 90W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 41 | Maverick of Wall Stree | YouTube | 20W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 42 | Daniel Pronk | YouTube | 20W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 43 | Cameron Stewart | YouTube | 5W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 44 | Fast Graphs (Chuck Car | YouTube | 10W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 45 | The Nomad Wallstreet | YouTube | 8W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 46 | DeepValue | Reddit (u/) | 5W+ | — | **WARN** | 0/0 |  |
| 47 | HK Money Mentor | IG/YT | 2W+ | — | **FAIL** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；channel_url 与 handle 不一致: https:// |
| 48 | Money Coach Nick | IG | 10W+ | — | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.instagram.com/moneycoachnick?v=mock0（点击无法到达任何真实视频）；条目1 标 |
| 49 | TradingView (Top Autho | TradingView | N/A | — | **FAIL** | 3/3 | fans 缺失/未填写；条目1 链接为伪链接: https://cn.tradingview.com/top-authors/?v=mock0（点击无法到达任何 |
| 50 | Real Vision (Individua | YouTube | 60W+ | UCBH5VZEhF8f | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@RealVisionFinance?v=mock0（点击无法到达任何真实视频）；条目1 |
| 51 | 老厉害 | YouTube | 10W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 52 | inves talk | YouTube | 14W+ | UCz1GOaZF_qc | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/@investalk?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模拟语 |
| 53 | 硬核刘大 | YouTube | 8W+ | UCF_qIUUVPM3 | **WARN** | 0/3 | 条目1 标题来自模拟语料库（非频道原文）: 「香港账户全攻略：2026年还能开哪家？」；条目2 标题来自模拟语料库（非频道原文）: 「USDT 换汇暗流：走资的 |
| 54 | 信報財經新聞 | 香港財經媒體 | N/A | — | **FAIL** | 3/3 | fans 缺失/未填写；条目1 链接为伪链接: https://www.hkej.com/?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模拟语料 |
| 55 | Finance730 | 香港財經媒體 | N/A | — | **FAIL** | 3/3 | fans 缺失/未填写；条目1 链接为伪链接: https://finance730.com.hk/?v=mock0（点击无法到达任何真实视频）；条目1 标题来 |
| 56 | 香港經濟日報 HKET | 香港財經媒體 | N/A | — | **FAIL** | 3/3 | fans 缺失/未填写；条目1 链接为伪链接: https://inews.hket.com/?v=mock0（点击无法到达任何真实视频）；条目1 标题来自模拟 |
| 57 | 香港財經時報 HKBT | YouTube / 網頁 | N/A | — | **FAIL** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: HKBT（应为 @xxx）；channel |
| 58 | 新城財經台 | 香港財經電台 | N/A | — | **FAIL** | 3/3 | fans 缺失/未填写；条目1 链接为伪链接: https://www.metroradio.com.hk/finance/?v=mock0（点击无法到达任何真 |
| 59 | 财经风云 (@ChineseFinance) | YouTube | 24W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 60 | 视野环球财经 (@RhinoFinance) | YouTube | 30W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 61 | ChineseFN 中文投資網 | 中文投資網站 | N/A | — | **FAIL** | 3/3 | fans 缺失/未填写；条目1 链接为伪链接: https://www.chinesefn.com/?v=mock0（点击无法到达任何真实视频）；条目1 标题来 |
| 62 | 财经全世界 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 财经全世界（应为 @xxx）；channe |
| 63 | 老李玩钱 | YouTube | 10W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 老李玩钱（应为 @xxx）；channel |
| 64 | 土妹美股 | YouTube | 5W+ | UCWvjeM3d1GN | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCWvjeM3d1GNj8pK7o_AN_ |
| 65 | 贝拉说美股 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 贝拉说美股（应为 @xxx）；channe |
| 66 | 美投讲美股 | YouTube | 66W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 67 | 财经冷眼 | YouTube | 18W+ | UCn9_KbNANey | **FAIL** | 3/3 | 条目1 链接为伪链接: https://www.youtube.com/results?search_query=%E8%B4%A2%E7%BB%8F%E5%8 |
| 68 | 老蛮频道（数据帝老蛮） | YouTube | N/A | — | **FAIL** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 老蛮频道（应为 @xxx）；channel |
| 69 | 秦鹏观察 | YouTube | N/A | — | **FAIL** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 秦鹏观察（应为 @xxx）；channel |
| 70 | 子朝出走中 | YouTube | N/A | — | **FAIL** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 子朝出走中（应为 @xxx）；channe |
| 71 | 马江博说趋势 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 马江博说趋势（应为 @xxx）；chann |
| 72 | 付鹏的财经世界 | YouTube | 20W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 73 | 兰香财经 | YouTube | N/A | — | **FAIL** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 兰香财经（应为 @xxx）；channel |
| 74 | 财经M平方 MacroMicro | 宏觀數據平台 | N/A | — | **FAIL** | 3/3 | fans 缺失/未填写；条目1 链接为伪链接: https://www.macromicro.me/?v=mock0（点击无法到达任何真实视频）；条目1 标题来 |
| 75 | Gamma 财经 | YouTube | N/A | — | **FAIL** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: Gamma 财经（应为 @xxx）；cha |
| 76 | Ray 观点 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: Ray 观点（应为 @xxx）；chann |
| 77 | 公子沈 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 公子沈（应为 @xxx）；channel_ |
| 78 | 文昭谈古论今 | YouTube | 150W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 文昭谈古论今（应为 @xxx）；chann |
| 79 | 雅虎财经（Yahoo Finance 台湾/ | 財經媒體 | N/A | — | **FAIL** | 3/3 | fans 缺失/未填写；条目1 链接为伪链接: https://finance.yahoo.com/?v=mock0（点击无法到达任何真实视频）；条目1 标题来 |
| 80 | 大康有话说 | YouTube | 25W+ | UCG6ADYIl4Gx | **FAIL** | 3/3 | handle 格式异常: 大康有话说（应为 @xxx）；channel_url 与 handle 不一致: https://www.youtube.com/ch |
| 81 | 游庭皓的財經皓角 | YouTube | 68W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 游庭皓的財經皓角（应为 @xxx）；cha |
| 82 | 柴鼠兄弟 ZRBros | YouTube | 100W+ | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；条目1 链接为伪链接: https://www.youtube.co |
| 83 | 风傳媒-下班经济學 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 下班经济學（应为 @xxx）；channe |
| 84 | 老王愛說笑（老王/王倚隆） | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 老王愛說笑（应为 @xxx）；channe |
| 85 | SHIN LI | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: SHIN LI（应为 @xxx）；chan |
| 86 | 自由女神邱沁宜 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 邱沁宜（应为 @xxx）；channel_ |
| 87 | Better Leaf 好葉 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: Better Leaf 好葉（应为 @xx |
| 88 | 慢活夫妻 George & Dewi | YouTube | N/A | — | **FAIL** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: George & Dewi（应为 @xxx |
| 89 | 大俠武林 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 大俠武林（应为 @xxx）；channel |
| 90 | 股乾爹 KuKanTieh | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: KuKanTieh（应为 @xxx）；ch |
| 91 | Gooaye股癌 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: Gooaye股癌（应为 @xxx）；cha |
| 92 | 理財不能等（獅公李永年） | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 理財不能等（应为 @xxx）；channe |
| 93 | 懶錢包LazyWallet | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: LazyWallet（应为 @xxx）；c |
| 94 | M觀點 | YouTube | 20W+ | UCT3uWFvKLVp | **FAIL** | 3/3 | handle 格式异常: M觀點（应为 @xxx）；channel_url 与 handle 不一致: https://www.youtube.com/resu |
| 95 | 蕾咪Rami | YouTube | 37W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 蕾咪 Rami（应为 @xxx）；chan |
| 96 | 元大投顧財金頻道-理財最錢線 | YouTube | N/A | — | **FAIL** | 3/3 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 元大投顧 理財最錢線（应为 @xxx）；c |
| 97 | 股海老牛 | YouTube | 15W+ | UCwxU6JWj0oO | **FAIL** | 3/3 | handle 格式异常: 股海老牛（应为 @xxx）；channel_url 与 handle 不一致: https://www.youtube.com/res |

---
*本报告由 `src/authenticity_check.py` 自动生成，仅供真实性核查，不构成投资建议。*

# 🔍 全频道真实性审计报告（不作伪检查模块）

- **审计时间**：2026-08-16T07:29:45.706409+00:00
- **KOL 总数**：97　|　**PASS**：0　|　**WARN**：97　|　**FAIL**：0
- **内容条目**：共 0 条，其中**伪链接（mock）0 条（0.0%）**，语料库标题 0 条
- **在线验证**：未开启（离线审计，建议 CI 中 --online 复核）

> 说明：离线/无网络环境无法抓取任何真实内容，所有 KOL 均判 WARN（无法证明真实，但**无伪造**）。
> 联网 CI（GitHub Actions）会用 channel_id 拉取真实 RSS 后重新判定，已补全 channel_id 的频道将升级为 PASS。

## 判定口径
- **FAIL**：检测到伪造内容（伪链接等）或在线验证确认元数据严重失实
- **WARN**：元数据不完整（channel_id/fans 缺失等）→ 无法证明真实，需人工核
- **PASS**：无伪造痕迹且元数据完整（在线模式还要求验证通过）

| # | 名称 | 平台 | fans | channel_id | 判定 | mock/总条目 | 主要问题 |
|---|------|------|------|-----------|------|-----------|---------|
|  1 | Graham Stephan | YouTube | 500W+ | UCV6KDgJskWa | **WARN** | 0/0 |  |
|  2 | Andrei Jikh | YouTube | 330W+ | UCGy7SkBjcIA | **WARN** | 0/0 |  |
|  3 | Humphrey Yang | TikTok/YT | 300W+ | UCFBpVaKCC0a | **WARN** | 0/0 |  |
|  4 | The Plain Bagel | YouTube | 100W+ | UCFCEuCsyWP0 | **WARN** | 0/0 |  |
|  5 | Patrick Boyle | YouTube | 130W+ | UCASM0cgfkJx | **WARN** | 0/0 |  |
|  6 | Meet Kevin | YouTube | 205W+ | UCUvvj5lwue7 | **WARN** | 0/0 |  |
|  7 | Joseph Carlson | YouTube | 51W+ | UCbta0n8i6Rl | **WARN** | 0/0 |  |
|  8 | Sven Carlin | YouTube | 25W+ | UCrTTBSUr0zh | **WARN** | 0/0 |  |
|  9 | Mark Tilbury | TikTok/YT | 880W+ | UCxgAuX3XZRO | **WARN** | 0/0 |  |
| 10 | Jeremy Lefebvre | YouTube | 94W+ | UCnMn36GT_H0 | **WARN** | 0/0 |  |
| 11 | Ben Felix | YouTube | 62W+ | UCDXTQ8nWmx_ | **WARN** | 0/0 |  |
| 12 | Erika Kullberg | TikTok/YT | 500W+ | UCoSw1rKMkCb | **WARN** | 0/0 | handle 缺失 |
| 13 | Vivien Tu | TikTok/YT | 200W+ | UCgbXT2QuTj4 | **WARN** | 0/0 |  |
| 14 | Jaspreet Singh | YouTube | 240W+ | UCT3EznhW_CN | **WARN** | 0/0 |  |
| 15 | Investing with Rose | YouTube | 100W+ | UCIbslwukNCy | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCIbslwukNCyVp-XMz_2-g |
| 16 | ClearValue Tax | YouTube | 290W+ | UCigUBIf-zt_ | **WARN** | 0/0 |  |
| 17 | Everything Money | YouTube | 40W+ | UChBVf9Ynour | **WARN** | 0/0 |  |
| 18 | New Money | YouTube | 100W+ | UCvSXMi2Lebw | **WARN** | 0/0 |  |
| 19 | Financial Education | YouTube | 70W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；channel_url 与 handle 不一致: https:// |
| 20 | Brian Feroldi | YouTube | 5W+ | UCs60_Z83HU7 | **WARN** | 0/0 |  |
| 21 | 贝拉聊财金 | YouTube | 20W+ | UCVomjkM_t0E | **WARN** | 0/0 |  |
| 22 | 阳光财经 | YouTube | 30W+ | UC2I5em6UyBp | **WARN** | 0/0 |  |
| 23 | 小翠时政财经 | YouTube | 34W+ | UCOhck8oLoIw | **WARN** | 0/0 |  |
| 24 | 视野环球镜 | YouTube | 50W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 缺失 |
| 25 | 老李财经 | YouTube | 15W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 26 | 瑞威金融 | YouTube | 10W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 27 | 财女Nicole | YouTube | 15W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 28 | 孟岩的投资笔记 | YouTube/Web | 10W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 29 | 零总投资 | YouTube | 8W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 30 | 孙老师财经 | YouTube | 15W+ | UC1Lk6WO-eKu | **WARN** | 0/0 |  |
| 31 | 美股投资网 | YouTube | 10W+ | UCWyPo32TSKP | **WARN** | 0/0 | handle 缺失 |
| 32 | 逻辑财金 | YouTube | 12W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 33 | 大马理财 | YouTube | 10W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 34 | 美股说 | YouTube | 5W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 35 | Kelvin Learns Investin | YouTube | 12W+ | UCJmaaSJX_Pk | **WARN** | 0/0 |  |
| 36 | The Swedish Investor | YouTube | 100W+ | UCAeAB8ABXGo | **WARN** | 0/0 |  |
| 37 | Preston Pysh | Reddit/YT | 15W+ | UCLTdCY-fNXc | **WARN** | 0/0 |  |
| 38 | PensionCraft | YouTube | 20W+ | UC9OIwUcx-Us | **WARN** | 0/0 |  |
| 39 | Ramin Nakisa | YouTube | 20W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 缺失 |
| 40 | Financial Diet | YouTube | 120W+ | UCSPYNpQ2fHv | **WARN** | 0/0 |  |
| 41 | Maverick of Wall Stree | YouTube | 14W+ | UCvk0KB4Ue0v | **WARN** | 0/0 |  |
| 42 | Daniel Pronk | YouTube | 20W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 43 | Cameron Stewart | YouTube | 5W+ | UCpJRuue8x5Q | **WARN** | 0/0 |  |
| 44 | Fast Graphs (Chuck Car | YouTube | 15W+ | UCJggpN5VY0P | **WARN** | 0/0 |  |
| 45 | The Nomad Wallstreet | YouTube | 8W+ | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险） |
| 46 | DeepValue | Reddit (u/) | 5W+ | — | **WARN** | 0/0 |  |
| 47 | HK Money Mentor | IG | 2W+ | — | **WARN** | 0/0 | channel_url 缺失 |
| 48 | Money Coach Nick | IG | 10W+ | — | **WARN** | 0/0 | channel_url 缺失 |
| 49 | TradingView (Top Autho | TradingView | N/A | — | **WARN** | 0/0 | fans 缺失/未填写 |
| 50 | Real Vision (Individua | YouTube | 60W+ | UC1CVw2YKIun | **WARN** | 0/0 |  |
| 51 | 老厉害 | YouTube | 10W+ | UC8gZZWIWmBu | **WARN** | 0/0 |  |
| 52 | inves talk | YouTube | 14W+ | UCz1GOaZF_qc | **WARN** | 0/0 |  |
| 53 | 硬核刘大 | YouTube | 11W+ | UCCeMdcZw1LJ | **WARN** | 0/0 |  |
| 54 | 信報財經新聞 | YouTube/財經媒體 | N/A | UClRaYVzu5DI | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UClRaYVzu5DIh3kRZkXIX9 |
| 55 | Finance730 | YouTube/財經媒體 | 26W+ | UCzM2jQWmoeT | **WARN** | 0/0 |  |
| 56 | 香港經濟日報 HKET | YouTube/財經媒體 | 12W+ | UCFgvtFvTFRj | **WARN** | 0/0 |  |
| 57 | 香港財經時報 HKBT | YouTube/財經媒體 | 1W+ | UCAwfc603xR0 | **WARN** | 0/0 |  |
| 58 | 新城財經台 | YouTube/財經電台 | 17W+ | UCAUiU6pnaEa | **WARN** | 0/0 |  |
| 59 | 财经风云 (@ChineseFinance) | YouTube | 24W+ | UC-1F7DZmxTd | **WARN** | 0/0 |  |
| 60 | 视野环球财经 (@RhinoFinance) | YouTube | 30W+ | UCFQsi7WaF5X | **WARN** | 0/0 |  |
| 61 | ChineseFN 中文投資網 | 中文投資網站 | N/A | — | **WARN** | 0/0 | fans 缺失/未填写 |
| 62 | 财经全世界 | YouTube | N/A | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 财经全世界（应为 @xxx）；fans 缺 |
| 63 | 老李玩钱 | YouTube | 10W+ | UCo2gxyermsL | **WARN** | 0/0 |  |
| 64 | 土妹美股 | YouTube | 5W+ | UCWvjeM3d1GN | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCWvjeM3d1GNj8pK7o_AN_ |
| 65 | 贝拉说美股 | YouTube | N/A | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 贝拉说美股（应为 @xxx）；fans 缺 |
| 66 | 美投讲美股 | YouTube | 68W+ | UCBUH38E0ngq | **WARN** | 0/0 |  |
| 67 | 财经冷眼 | YouTube | 18W+ | UCn9_KbNANey | **WARN** | 0/0 |  |
| 68 | 老蛮频道（数据帝老蛮） | YouTube | 1W+ | UCrAC23izk57 | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCrAC23izk57G7jCBPfdXG |
| 69 | 秦鹏观察 | YouTube | N/A | UCrYc9TEMHji | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCrYc9TEMHjiHNrNl6WpqL |
| 70 | 子朝出走中 | YouTube | N/A | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 子朝出走中（应为 @xxx）；fans 缺 |
| 71 | 马江博说趋势 | YouTube | N/A | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；fans 缺失/未填写 |
| 72 | 付鹏的财经世界 | YouTube | 2W+ | UCb_4xq1KgaY | **WARN** | 0/0 |  |
| 73 | 兰香财经 | YouTube | N/A | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: 兰香财经（应为 @xxx）；fans 缺失 |
| 74 | 财经M平方 MacroMicro | YouTube/宏觀數據 | 6W+ | UC6LU7FUBvbF | **WARN** | 0/0 |  |
| 75 | Gamma 财经 | YouTube | N/A | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: Gamma 财经（应为 @xxx）；fan |
| 76 | Ray 观点 | YouTube | N/A | — | **WARN** | 0/0 | channel_id 缺失 → RSS 抓取必然跳过，内容走 Mock 兜底（高伪造风险）；handle 格式异常: Ray 观点（应为 @xxx）；fans  |
| 77 | 公子沈 | YouTube | N/A | UCrGSFNEBmCN | **WARN** | 0/0 | fans 缺失/未填写 |
| 78 | 文昭谈古论今 | YouTube | 160W+ | UCtAIPjABiQD | **WARN** | 0/0 |  |
| 79 | 雅虎财经（Yahoo Finance 台湾/ | 財經媒體 | N/A | — | **WARN** | 0/0 | fans 缺失/未填写 |
| 80 | 大康有话说 | YouTube | 25W+ | UCG6ADYIl4Gx | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCG6ADYIl4GxaQib1HKIsR |
| 81 | 游庭皓的財經皓角 | YouTube | 68W+ | UC0lbAQVpenv | **WARN** | 0/0 |  |
| 82 | 柴鼠兄弟 ZRBros | YouTube | 100W+ | UC45i13dEfEV | **WARN** | 0/0 |  |
| 83 | 风傳媒-下班经济學 | YouTube | 250W+ | UCwWXGnvVmi- | **WARN** | 0/0 |  |
| 84 | 老王愛說笑（老王/王倚隆） | YouTube | N/A | UCvnLmiWt_zI | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCvnLmiWt_zIVIh0zUm_j4 |
| 85 | SHIN LI | YouTube | 10W+ | UCK-qc_POQZw | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCK-qc_POQZwWrMg-Pr-oY |
| 86 | 自由女神邱沁宜 | YouTube | 27W+ | UCe7BLtnYfxT | **WARN** | 0/0 |  |
| 87 | Better Leaf 好葉 | YouTube | 100W+ | UChjHWpmNm-3 | **WARN** | 0/0 |  |
| 88 | 慢活夫妻 George & Dewi | YouTube | 12W+ | UCVNqvJSKVl0 | **WARN** | 0/0 |  |
| 89 | 大俠武林 | YouTube | N/A | UC-b6b7CGlRs | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UC-b6b7CGlRsdcRS7bXDvT |
| 90 | 股乾爹 KuKanTieh | YouTube | N/A | UCDDneQi63kJ | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCDDneQi63kJAdr3i5VCPz |
| 91 | Gooaye股癌 | YouTube | 17W+ | UC23rnlQU_qE | **WARN** | 0/0 |  |
| 92 | 理財不能等（獅公李永年） | YouTube | 27W+ | UC21AfB2CIbv | **WARN** | 0/0 |  |
| 93 | 懶錢包LazyWallet | YouTube | 20W+ | UChYg2EINv5U | **WARN** | 0/0 |  |
| 94 | M觀點 | YouTube | 20W+ | UCT3uWFvKLVp | **WARN** | 0/0 |  |
| 95 | 蕾咪Rami | YouTube | 37W+ | UCGX-lnOzsVj | **WARN** | 0/0 | channel_url 与 handle 不一致: https://www.youtube.com/channel/UCGX-lnOzsVjbdzb1VJxmW |
| 96 | 元大投顧財金頻道-理財最錢線 | YouTube | 15W+ | UCS1bMmw249R | **WARN** | 0/0 |  |
| 97 | 股海老牛 | YouTube |  | UCwxU6JWj0oO | **WARN** | 0/0 | fans 缺失/未填写 |

---
*本报告由 `src/authenticity_check.py` 自动生成，仅供真实性核查，不构成投资建议。*

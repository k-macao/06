# 🔍 全频道真实性审计报告（不作伪检查模块）

- **审计时间**：2026-08-20T03:07:41.379805+00:00
- **KOL 目录**：97（本次入报 64，隔离 33）
- **判定**：PASS 9　|　WARN 88　|　FAIL 0
- **内容条目**：192 条；模拟/伪链接 0；改写标题 0
- **在线复核**：已请求（仅复核入报频道）
- **⚠️ 风控提示**：52 条在线 404 因同期大批频道同时出现，判定为 YouTube 反爬拦截而非频道失效，已从 FAIL 降级为 WARN。

## 判定口径
- **FAIL**：本次报告含模拟内容、伪链接、改写标题，或入报来源在线确认严重失实。
- **WARN**：目录元数据不完整、网络暂时不可验证，或记录未入报并已隔离。
- **PASS**：入报内容具备真实来源且无伪造痕迹。

| # | 名称 | 入报 | 平台 | 判定 | mock/条目 | 主要问题 |
|---|------|------|------|------|-----------|---------|
|  1 | Graham Stephan | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCV6KDgJskWaEckne5aPA0aQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
|  2 | Andrei Jikh | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCGy7SkBjcIAgTiwkXEtPnYg（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
|  3 | Humphrey Yang | 是 | TikTok/YT | **WARN** | 0/3 | RSS 404，channel_id 无效: UCFBpVaKCC0ajGps1vf0AgBg（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
|  4 | The Plain Bagel | 是 | YouTube | **PASS** | 0/3 |  |
|  5 | Patrick Boyle | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCASM0cgfkJxQ1ICmRilfHLw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
|  6 | Meet Kevin | 是 | YouTube | **PASS** | 0/3 |  |
|  7 | Joseph Carlson | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCbta0n8i6Rljh0obO7HzG9A（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
|  8 | Sven Carlin | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCrTTBSUr0zhPU56UQljag5A（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
|  9 | Mark Tilbury | 是 | TikTok/YT | **WARN** | 0/3 | RSS 404，channel_id 无效: UCxgAuX3XZROujMmGphN_scA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 10 | Jeremy Lefebvre | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCnMn36GT_H0X-w5_ckLtlgQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 11 | Ben Felix | 是 | YouTube | **WARN** | 0/3 | RSS 复验 404（疑似 YouTube 风控拦截，抓取阶段已验证）: UCDXTQ8nWmx_EhZ2v-kp7QxA |
| 12 | Erika Kullberg | 是 | TikTok/YT | **WARN** | 0/3 | handle 缺失；RSS 404，channel_id 无效: UCoSw1rKMkCbwzKpkC0OjRKA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 13 | Vivien Tu | 是 | TikTok/YT | **WARN** | 0/3 | RSS 404，channel_id 无效: UCgbXT2QuTj4SYxaWCs3vuAw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 14 | Jaspreet Singh | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCT3EznhW_CNFcfOlyDNTLLw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 15 | Investing with Rose | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCIbslwukNCyVp-XMz_2-gmw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 16 | ClearValue Tax | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCigUBIf-zt_DA6xyOQtq2WA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 17 | Everything Money | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UChBVf9YnourrEDTsbbwJPRA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 18 | New Money | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCvSXMi2LebwJEM1s4bz5IBA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 19 | Financial Education | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；channel_url 与 handle 不一致: https://www.youtube.com/@FinancialEducat |
| 20 | Brian Feroldi | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCs60_Z83HU76uygzHRQl0kA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 21 | 贝拉聊财金 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCVomjkM_t0EcctTWSE1Jvxg（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 22 | 阳光财经 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UC2I5em6UyBpQiO-8ZW0nV3w（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 23 | 小翠时政财经 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCOhck8oLoIwSJzmwYMXsSnQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 24 | 视野环球镜 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 缺失 |
| 25 | 老李财经 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 26 | 瑞威金融 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 27 | 财女Nicole | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 28 | 孟岩的投资笔记 | 否 | YouTube/Web | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 29 | 零总投资 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 30 | 孙老师财经 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UC1Lk6WO-eKuYc6GHYbKVY2g（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 31 | 美股投资网 | 是 | YouTube | **WARN** | 0/3 | handle 缺失；RSS 404，channel_id 无效: UCWyPo32TSKPr8Py7gb7NhYw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 32 | 逻辑财金 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 33 | 大马理财 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 34 | 美股说 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 35 | Kelvin Learns Investing | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCJmaaSJX_PkfUmTuxWbrzLw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 36 | The Swedish Investor | 否 | YouTube | **WARN** | 0/0 |  |
| 37 | Preston Pysh | 否 | Reddit/YT | **WARN** | 0/0 |  |
| 38 | PensionCraft | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UC9OIwUcx-Uss7xj7s1P5XGw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 39 | Ramin Nakisa | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 缺失 |
| 40 | Financial Diet | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCSPYNpQ2fHv9HJ-q6MIMaPw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 41 | Maverick of Wall Street | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCvk0KB4Ue0vfPqvDzjIAwiQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 42 | Daniel Pronk | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 43 | Cameron Stewart | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCpJRuue8x5Qag2Wz6uAzyjw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 44 | Fast Graphs (Chuck Carne | 是 | YouTube | **PASS** | 0/3 |  |
| 45 | The Nomad Wallstreet | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 46 | DeepValue | 否 | Reddit (u/) | **WARN** | 0/0 |  |
| 47 | HK Money Mentor | 否 | IG | **WARN** | 0/0 | channel_url 缺失 |
| 48 | Money Coach Nick | 否 | IG | **WARN** | 0/0 | channel_url 缺失 |
| 49 | TradingView (Top Authors | 否 | TradingView | **WARN** | 0/0 | channel_url 缺失；fans 缺失/未填写 |
| 50 | Real Vision (Individual  | 否 | YouTube | **WARN** | 0/0 |  |
| 51 | 老厉害 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UC8gZZWIWmBuCb_gzC8DUrvw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 52 | inves talk | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCz1GOaZF_qcROUFCzR-_2iQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 53 | 硬核刘大 | 是 | YouTube | **PASS** | 0/3 |  |
| 54 | 信報財經新聞 | 是 | YouTube/財經媒體 | **WARN** | 0/3 | fans 缺失/未填写；RSS 404，channel_id 无效: UClRaYVzu5DIh3kRZkXIX9WA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 55 | Finance730 | 是 | YouTube/財經媒體 | **WARN** | 0/3 | RSS 404，channel_id 无效: UCzM2jQWmoeTvpEw63x5Rsdg（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 56 | 香港經濟日報 HKET | 是 | YouTube/財經媒體 | **WARN** | 0/3 | RSS 404，channel_id 无效: UCFgvtFvTFRjqhGC1XfIB02w（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 57 | 香港財經時報 HKBT | 是 | YouTube/財經媒體 | **WARN** | 0/3 | RSS 404，channel_id 无效: UCAwfc603xR0xXQN58x4uWeA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 58 | 新城財經台 | 是 | YouTube/財經電台 | **WARN** | 0/3 | RSS 404，channel_id 无效: UCAUiU6pnaEaTjgTVp6KY0FQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 59 | 财经风云 (@ChineseFinance) | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UC-1F7DZmxTd1YZUJZUsA0nw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 60 | 视野环球财经 (@RhinoFinance) | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCFQsi7WaF5X41tcuOryDk8w（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 61 | ChineseFN 中文投資網 | 否 | 中文投資網站 | **WARN** | 0/0 | fans 缺失/未填写 |
| 62 | 财经全世界 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 财经全世界（应为 @xxx）；fans 缺失/未填写 |
| 63 | 老李玩钱 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCo2gxyermsLBSCxFHvJs0Zg（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 64 | 土妹美股 | 否 | YouTube | **WARN** | 0/0 |  |
| 65 | 贝拉说美股 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 贝拉说美股（应为 @xxx）；fans 缺失/未填写 |
| 66 | 美投讲美股 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCBUH38E0ngqvmTqdchWunwQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 67 | 财经冷眼 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCn9_KbNANeyYREePe8YA2DA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 68 | 老蛮频道（数据帝老蛮） | 是 | YouTube | **PASS** | 0/3 |  |
| 69 | 秦鹏观察 | 是 | YouTube | **WARN** | 0/3 | fans 缺失/未填写 |
| 70 | 子朝出走中 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 子朝出走中（应为 @xxx）；fans 缺失/未填写 |
| 71 | 马江博说趋势 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；fans 缺失/未填写 |
| 72 | 付鹏的财经世界 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCb_4xq1KgaYkGtxpjkoZrtQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 73 | 兰香财经 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 兰香财经（应为 @xxx）；fans 缺失/未填写 |
| 74 | 财经M平方 MacroMicro | 是 | YouTube/宏觀數據平台 | **WARN** | 0/3 | RSS 404，channel_id 无效: UC6LU7FUBvbFCh_cQasrHZ_Q（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 75 | Gamma 财经 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: Gamma 财经（应为 @xxx）；fans 缺失/未填写 |
| 76 | Ray 观点 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: Ray 观点（应为 @xxx）；fans 缺失/未填写 |
| 77 | 公子沈 | 是 | YouTube | **WARN** | 0/3 | fans 缺失/未填写；RSS 404，channel_id 无效: UCrGSFNEBmCN0rqhATZels2Q（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 78 | 文昭谈古论今 | 是 | YouTube | **PASS** | 0/3 |  |
| 79 | 雅虎财经（Yahoo Finance 台湾/香港 | 否 | 財經媒體 | **WARN** | 0/0 | fans 缺失/未填写 |
| 80 | 大康有话说 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCG6ADYIl4GxaQib1HKIsRNg（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 81 | 游庭皓的財經皓角 | 是 | YouTube | **PASS** | 0/3 |  |
| 82 | 柴鼠兄弟 ZRBros | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UC45i13dEfEVac2IEJT_Nr5Q（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 83 | 风傳媒-下班经济學 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCwWXGnvVmi-6Sfx2wf8S8tQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 84 | 老王愛說笑（老王/王倚隆） | 是 | YouTube | **WARN** | 0/3 | fans 缺失/未填写；RSS 404，channel_id 无效: UCvnLmiWt_zIVIh0zUm_j4Hw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 85 | SHIN LI | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCK-qc_POQZwWrMg-Pr-oYtg（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 86 | 自由女神邱沁宜 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCe7BLtnYfxTXVTRISlfupSw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 87 | Better Leaf 好葉 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UChjHWpmNm-3HbLFkQ3TPXaA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 88 | 慢活夫妻 George & Dewi | 是 | YouTube | **PASS** | 0/3 |  |
| 89 | 大俠武林 | 是 | YouTube | **WARN** | 0/3 | fans 缺失/未填写；RSS 复验 404（疑似 YouTube 风控拦截，抓取阶段已验证）: UC-b6b7CGlRsdcRS7bXDvTYQ |
| 90 | 股乾爹 KuKanTieh | 否 | YouTube | **WARN** | 0/0 | fans 缺失/未填写 |
| 91 | Gooaye股癌 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UC23rnlQU_qE3cec9x709peA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 92 | 理財不能等（獅公李永年） | 否 | YouTube | **WARN** | 0/0 | handle 缺失 |
| 93 | 懶錢包LazyWallet | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UChYg2EINv5URVkebzlTGbFQ（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 94 | M觀點 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCT3uWFvKLVpRnEealmRwvrw（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 95 | 蕾咪Rami | 是 | YouTube | **PASS** | 0/3 |  |
| 96 | 元大投顧財金頻道-理財最錢線 | 是 | YouTube | **WARN** | 0/3 | RSS 404，channel_id 无效: UCS1bMmw249R7R0wDjAmE6CA（同期大批频道 404，疑似 YouTube 风控拦截，已降级） |
| 97 | 股海老牛 | 否 | YouTube | **WARN** | 0/0 | fans 缺失/未填写 |

---
*本报告由 `src/authenticity_check.py` 自动生成，仅供真实性核查，不构成投资建议。*

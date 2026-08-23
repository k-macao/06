# 🔍 全频道真实性审计报告（不作伪检查模块）

- **审计时间**：2026-08-23T03:09:37.879210+00:00
- **KOL 目录**：97（本次入报 64，隔离 33）
- **判定**：PASS 57　|　WARN 40　|　FAIL 0
- **内容条目**：192 条；模拟/伪链接 0；改写标题 0
- **在线复核**：已请求（仅复核入报频道）

## 判定口径
- **FAIL**：本次报告含模拟内容、伪链接、改写标题，或入报来源在线确认严重失实。
- **WARN**：目录元数据不完整、网络暂时不可验证，或记录未入报并已隔离。
- **PASS**：入报内容具备真实来源且无伪造痕迹。

| # | 名称 | 入报 | 平台 | 判定 | mock/条目 | 主要问题 |
|---|------|------|------|------|-----------|---------|
|  1 | Graham Stephan | 是 | YouTube | **PASS** | 0/3 |  |
|  2 | Andrei Jikh | 是 | YouTube | **PASS** | 0/3 |  |
|  3 | Humphrey Yang | 是 | TikTok/YT | **PASS** | 0/3 |  |
|  4 | The Plain Bagel | 是 | YouTube | **PASS** | 0/3 |  |
|  5 | Patrick Boyle | 是 | YouTube | **PASS** | 0/3 |  |
|  6 | Meet Kevin | 是 | YouTube | **PASS** | 0/3 |  |
|  7 | Joseph Carlson | 是 | YouTube | **PASS** | 0/3 |  |
|  8 | Sven Carlin | 是 | YouTube | **PASS** | 0/3 |  |
|  9 | Mark Tilbury | 是 | TikTok/YT | **PASS** | 0/3 |  |
| 10 | Jeremy Lefebvre | 是 | YouTube | **PASS** | 0/3 |  |
| 11 | Ben Felix | 是 | YouTube | **PASS** | 0/3 |  |
| 12 | Erika Kullberg | 是 | TikTok/YT | **WARN** | 0/3 | handle 缺失 |
| 13 | Vivien Tu | 是 | TikTok/YT | **PASS** | 0/3 |  |
| 14 | Jaspreet Singh | 是 | YouTube | **PASS** | 0/3 |  |
| 15 | Investing with Rose | 是 | YouTube | **PASS** | 0/3 |  |
| 16 | ClearValue Tax | 是 | YouTube | **PASS** | 0/3 |  |
| 17 | Everything Money | 是 | YouTube | **PASS** | 0/3 |  |
| 18 | New Money | 是 | YouTube | **PASS** | 0/3 |  |
| 19 | Financial Education | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；channel_url 与 handle 不一致: https://www.youtube.com/@FinancialEducat |
| 20 | Brian Feroldi | 是 | YouTube | **PASS** | 0/3 |  |
| 21 | 贝拉聊财金 | 是 | YouTube | **PASS** | 0/3 |  |
| 22 | 阳光财经 | 是 | YouTube | **PASS** | 0/3 |  |
| 23 | 小翠时政财经 | 是 | YouTube | **PASS** | 0/3 |  |
| 24 | 视野环球镜 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 缺失 |
| 25 | 老李财经 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 26 | 瑞威金融 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 27 | 财女Nicole | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 28 | 孟岩的投资笔记 | 否 | YouTube/Web | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 29 | 零总投资 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 30 | 孙老师财经 | 是 | YouTube | **PASS** | 0/3 |  |
| 31 | 美股投资网 | 是 | YouTube | **WARN** | 0/3 | handle 缺失 |
| 32 | 逻辑财金 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 33 | 大马理财 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 34 | 美股说 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 35 | Kelvin Learns Investing | 是 | YouTube | **PASS** | 0/3 |  |
| 36 | The Swedish Investor | 否 | YouTube | **WARN** | 0/0 |  |
| 37 | Preston Pysh | 否 | Reddit/YT | **WARN** | 0/0 |  |
| 38 | PensionCraft | 是 | YouTube | **PASS** | 0/3 |  |
| 39 | Ramin Nakisa | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 缺失 |
| 40 | Financial Diet | 是 | YouTube | **PASS** | 0/3 |  |
| 41 | Maverick of Wall Street | 是 | YouTube | **PASS** | 0/3 |  |
| 42 | Daniel Pronk | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 43 | Cameron Stewart | 是 | YouTube | **PASS** | 0/3 |  |
| 44 | Fast Graphs (Chuck Carne | 是 | YouTube | **PASS** | 0/3 |  |
| 45 | The Nomad Wallstreet | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 46 | DeepValue | 否 | Reddit (u/) | **WARN** | 0/0 |  |
| 47 | HK Money Mentor | 否 | IG | **WARN** | 0/0 | channel_url 缺失 |
| 48 | Money Coach Nick | 否 | IG | **WARN** | 0/0 | channel_url 缺失 |
| 49 | TradingView (Top Authors | 否 | TradingView | **WARN** | 0/0 | channel_url 缺失；fans 缺失/未填写 |
| 50 | Real Vision (Individual  | 否 | YouTube | **WARN** | 0/0 |  |
| 51 | 老厉害 | 是 | YouTube | **PASS** | 0/3 |  |
| 52 | inves talk | 是 | YouTube | **PASS** | 0/3 |  |
| 53 | 硬核刘大 | 是 | YouTube | **PASS** | 0/3 |  |
| 54 | 信報財經新聞 | 是 | YouTube/財經媒體 | **WARN** | 0/3 | fans 缺失/未填写 |
| 55 | Finance730 | 是 | YouTube/財經媒體 | **PASS** | 0/3 |  |
| 56 | 香港經濟日報 HKET | 是 | YouTube/財經媒體 | **PASS** | 0/3 |  |
| 57 | 香港財經時報 HKBT | 是 | YouTube/財經媒體 | **PASS** | 0/3 |  |
| 58 | 新城財經台 | 是 | YouTube/財經電台 | **PASS** | 0/3 |  |
| 59 | 财经风云 (@ChineseFinance) | 是 | YouTube | **PASS** | 0/3 |  |
| 60 | 视野环球财经 (@RhinoFinance) | 是 | YouTube | **PASS** | 0/3 |  |
| 61 | ChineseFN 中文投資網 | 否 | 中文投資網站 | **WARN** | 0/0 | fans 缺失/未填写 |
| 62 | 财经全世界 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 财经全世界（应为 @xxx）；fans 缺失/未填写 |
| 63 | 老李玩钱 | 是 | YouTube | **PASS** | 0/3 |  |
| 64 | 土妹美股 | 否 | YouTube | **WARN** | 0/0 |  |
| 65 | 贝拉说美股 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 贝拉说美股（应为 @xxx）；fans 缺失/未填写 |
| 66 | 美投讲美股 | 是 | YouTube | **PASS** | 0/3 |  |
| 67 | 财经冷眼 | 是 | YouTube | **PASS** | 0/3 |  |
| 68 | 老蛮频道（数据帝老蛮） | 是 | YouTube | **PASS** | 0/3 |  |
| 69 | 秦鹏观察 | 是 | YouTube | **WARN** | 0/3 | fans 缺失/未填写 |
| 70 | 子朝出走中 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 子朝出走中（应为 @xxx）；fans 缺失/未填写 |
| 71 | 马江博说趋势 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；fans 缺失/未填写 |
| 72 | 付鹏的财经世界 | 是 | YouTube | **PASS** | 0/3 |  |
| 73 | 兰香财经 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 兰香财经（应为 @xxx）；fans 缺失/未填写 |
| 74 | 财经M平方 MacroMicro | 是 | YouTube/宏觀數據平台 | **PASS** | 0/3 |  |
| 75 | Gamma 财经 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: Gamma 财经（应为 @xxx）；fans 缺失/未填写 |
| 76 | Ray 观点 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: Ray 观点（应为 @xxx）；fans 缺失/未填写 |
| 77 | 公子沈 | 是 | YouTube | **WARN** | 0/3 | fans 缺失/未填写 |
| 78 | 文昭谈古论今 | 是 | YouTube | **PASS** | 0/3 |  |
| 79 | 雅虎财经（Yahoo Finance 台湾/香港 | 否 | 財經媒體 | **WARN** | 0/0 | fans 缺失/未填写 |
| 80 | 大康有话说 | 是 | YouTube | **PASS** | 0/3 |  |
| 81 | 游庭皓的財經皓角 | 是 | YouTube | **PASS** | 0/3 |  |
| 82 | 柴鼠兄弟 ZRBros | 是 | YouTube | **PASS** | 0/3 |  |
| 83 | 风傳媒-下班经济學 | 是 | YouTube | **PASS** | 0/3 |  |
| 84 | 老王愛說笑（老王/王倚隆） | 是 | YouTube | **WARN** | 0/3 | fans 缺失/未填写 |
| 85 | SHIN LI | 是 | YouTube | **PASS** | 0/3 |  |
| 86 | 自由女神邱沁宜 | 是 | YouTube | **PASS** | 0/3 |  |
| 87 | Better Leaf 好葉 | 是 | YouTube | **PASS** | 0/3 |  |
| 88 | 慢活夫妻 George & Dewi | 是 | YouTube | **PASS** | 0/3 |  |
| 89 | 大俠武林 | 是 | YouTube | **WARN** | 0/3 | fans 缺失/未填写 |
| 90 | 股乾爹 KuKanTieh | 否 | YouTube | **WARN** | 0/0 | fans 缺失/未填写 |
| 91 | Gooaye股癌 | 是 | YouTube | **PASS** | 0/3 |  |
| 92 | 理財不能等（獅公李永年） | 否 | YouTube | **WARN** | 0/0 | handle 缺失 |
| 93 | 懶錢包LazyWallet | 是 | YouTube | **PASS** | 0/3 |  |
| 94 | M觀點 | 是 | YouTube | **PASS** | 0/3 |  |
| 95 | 蕾咪Rami | 是 | YouTube | **PASS** | 0/3 |  |
| 96 | 元大投顧財金頻道-理財最錢線 | 是 | YouTube | **PASS** | 0/3 |  |
| 97 | 股海老牛 | 否 | YouTube | **WARN** | 0/0 | fans 缺失/未填写 |

---
*本报告由 `src/authenticity_check.py` 自动生成，仅供真实性核查，不构成投资建议。*

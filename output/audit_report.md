# 🔍 全频道真实性审计报告（不作伪检查模块）

- **审计时间**：2026-08-16T08:21:13.854322+00:00
- **KOL 目录**：97（本次入报 5，隔离 92）
- **判定**：PASS 5　|　WARN 92　|　FAIL 0
- **内容条目**：15 条；模拟/伪链接 0；改写标题 0
- **在线复核**：未开启

## 判定口径
- **FAIL**：本次报告含模拟内容、伪链接、改写标题，或入报来源在线确认严重失实。
- **WARN**：目录元数据不完整、网络暂时不可验证，或记录未入报并已隔离。
- **PASS**：入报内容具备真实来源且无伪造痕迹。

| # | 名称 | 入报 | 平台 | 判定 | mock/条目 | 主要问题 |
|---|------|------|------|------|-----------|---------|
|  1 | Graham Stephan | 是 | YouTube | **PASS** | 0/3 |  |
|  2 | Andrei Jikh | 否 | YouTube | **WARN** | 0/0 |  |
|  3 | Humphrey Yang | 否 | TikTok/YT | **WARN** | 0/0 |  |
|  4 | The Plain Bagel | 是 | YouTube | **PASS** | 0/3 |  |
|  5 | Patrick Boyle | 否 | YouTube | **WARN** | 0/0 |  |
|  6 | Meet Kevin | 否 | YouTube | **WARN** | 0/0 |  |
|  7 | Joseph Carlson | 否 | YouTube | **WARN** | 0/0 |  |
|  8 | Sven Carlin | 否 | YouTube | **WARN** | 0/0 |  |
|  9 | Mark Tilbury | 否 | TikTok/YT | **WARN** | 0/0 |  |
| 10 | Jeremy Lefebvre | 否 | YouTube | **WARN** | 0/0 |  |
| 11 | Ben Felix | 否 | YouTube | **WARN** | 0/0 |  |
| 12 | Erika Kullberg | 否 | IG/TikTok | **WARN** | 0/0 |  |
| 13 | Vivien Tu | 否 | TikTok/IG | **WARN** | 0/0 |  |
| 14 | Jaspreet Singh | 否 | YouTube | **WARN** | 0/0 |  |
| 15 | Investing with Rose | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 16 | ClearValue Tax | 是 | YouTube | **PASS** | 0/3 |  |
| 17 | Everything Money | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 18 | New Money | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 19 | Financial Education | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；channel_url 与 handle 不一致: https://www.youtube.com/@FinancialEducat |
| 20 | Brian Feroldi | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 21 | 贝拉聊财金 | 是 | YouTube | **PASS** | 0/3 |  |
| 22 | 阳光财经 | 否 | YouTube | **WARN** | 0/0 |  |
| 23 | 小翠时政财经 | 是 | YouTube | **PASS** | 0/3 |  |
| 24 | 视野环球镜 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；channel_url 与 handle 不一致: https://www.youtube.com/@全球视野 vs @global |
| 25 | 老李财经 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 26 | 瑞威金融 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 27 | 财女Nicole | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 28 | 孟岩的投资笔记 | 否 | YouTube/Web | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；channel_url 与 handle 不一致: https://www.youtube.com/@孟岩的投资笔记 vs @孟岩投 |
| 29 | 零总投资 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 30 | 孙老师财经 | 否 | YouTube | **WARN** | 0/0 |  |
| 31 | 美股投资网 | 否 | YouTube | **WARN** | 0/0 |  |
| 32 | 逻辑财金 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 33 | 大马理财 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 34 | 美股说 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 35 | Kelvin Learns Investing | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 36 | The Swedish Investor | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 37 | Preston Pysh | 否 | Reddit/YT | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 38 | PensionCraft | 否 | YouTube | **WARN** | 0/0 |  |
| 39 | Ramin Nakisa | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 40 | Financial Diet | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 41 | Maverick of Wall Street | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 42 | Daniel Pronk | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 43 | Cameron Stewart | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 44 | Fast Graphs (Chuck Carne | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 45 | The Nomad Wallstreet | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 46 | DeepValue | 否 | Reddit (u/) | **WARN** | 0/0 |  |
| 47 | HK Money Mentor | 否 | IG/YT | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；YouTube 记录使用非 YouTube 来源: https://www.instagram.com/hkmoneymentor… |
| 48 | Money Coach Nick | 否 | IG | **WARN** | 0/0 |  |
| 49 | TradingView (Top Authors | 否 | TradingView | **WARN** | 0/0 | fans 缺失/未填写 |
| 50 | Real Vision (Individual  | 否 | YouTube | **WARN** | 0/0 |  |
| 51 | 老厉害 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 52 | inves talk | 否 | YouTube | **WARN** | 0/0 |  |
| 53 | 硬核刘大 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 54 | 信報財經新聞 | 否 | 香港財經媒體 | **WARN** | 0/0 | fans 缺失/未填写 |
| 55 | Finance730 | 否 | 香港財經媒體 | **WARN** | 0/0 | fans 缺失/未填写 |
| 56 | 香港經濟日報 HKET | 否 | 香港財經媒體 | **WARN** | 0/0 | fans 缺失/未填写 |
| 57 | 香港財經時報 HKBT | 否 | YouTube / 網頁 | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: HKBT（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.you |
| 58 | 新城財經台 | 否 | 香港財經電台 | **WARN** | 0/0 | fans 缺失/未填写 |
| 59 | 财经风云 (@ChineseFinance) | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 60 | 视野环球财经 (@RhinoFinance) | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 61 | ChineseFN 中文投資網 | 否 | 中文投資網站 | **WARN** | 0/0 | fans 缺失/未填写 |
| 62 | 财经全世界 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 财经全世界（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.yo |
| 63 | 老李玩钱 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 老李玩钱（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.you |
| 64 | 土妹美股 | 否 | YouTube | **WARN** | 0/0 |  |
| 65 | 贝拉说美股 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 贝拉说美股（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.yo |
| 66 | 美投讲美股 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 67 | 财经冷眼 | 否 | YouTube | **WARN** | 0/0 |  |
| 68 | 老蛮频道（数据帝老蛮） | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 老蛮频道（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.you |
| 69 | 秦鹏观察 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 秦鹏观察（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.you |
| 70 | 子朝出走中 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 子朝出走中（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.yo |
| 71 | 马江博说趋势 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 马江博说趋势（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.y |
| 72 | 付鹏的财经世界 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 73 | 兰香财经 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 兰香财经（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.you |
| 74 | 财经M平方 MacroMicro | 否 | 宏觀數據平台 | **WARN** | 0/0 | fans 缺失/未填写 |
| 75 | Gamma 财经 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: Gamma 财经（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www |
| 76 | Ray 观点 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: Ray 观点（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.y |
| 77 | 公子沈 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 公子沈（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.yout |
| 78 | 文昭谈古论今 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 文昭谈古论今（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.y |
| 79 | 雅虎财经（Yahoo Finance 台湾/香港 | 否 | 財經媒體 | **WARN** | 0/0 | fans 缺失/未填写 |
| 80 | 大康有话说 | 否 | YouTube | **WARN** | 0/0 | handle 格式异常: 大康有话说（应为 @xxx） |
| 81 | 游庭皓的財經皓角 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 游庭皓的財經皓角（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www |
| 82 | 柴鼠兄弟 ZRBros | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离 |
| 83 | 风傳媒-下班经济學 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 下班经济學（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.yo |
| 84 | 老王愛說笑（老王/王倚隆） | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 老王愛說笑（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.yo |
| 85 | SHIN LI | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: SHIN LI（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www. |
| 86 | 自由女神邱沁宜 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 邱沁宜（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.yout |
| 87 | Better Leaf 好葉 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: Better Leaf 好葉（应为 @xxx）；channel_url 是搜索页占位而非频道: https |
| 88 | 慢活夫妻 George & Dewi | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: George & Dewi（应为 @xxx）；channel_url 是搜索页占位而非频道: https: |
| 89 | 大俠武林 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 大俠武林（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.you |
| 90 | 股乾爹 KuKanTieh | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: KuKanTieh（应为 @xxx）；channel_url 是搜索页占位而非频道: https://ww |
| 91 | Gooaye股癌 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: Gooaye股癌（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www |
| 92 | 理財不能等（獅公李永年） | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 理財不能等（应为 @xxx）；channel_url 是搜索页占位而非频道: https://www.yo |
| 93 | 懶錢包LazyWallet | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: LazyWallet（应为 @xxx）；channel_url 是搜索页占位而非频道: https://w |
| 94 | M觀點 | 否 | YouTube | **WARN** | 0/0 |  |
| 95 | 蕾咪Rami | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 蕾咪 Rami（应为 @xxx） |
| 96 | 元大投顧財金頻道-理財最錢線 | 否 | YouTube | **WARN** | 0/0 | channel_id 缺失；运行时必须从真实频道页解析，失败则隔离；handle 格式异常: 元大投顧 理財最錢線（应为 @xxx）；channel_url 是搜索页占位而非频道: https://w |
| 97 | 股海老牛 | 否 | YouTube | **WARN** | 0/0 |  |

---
*本报告由 `src/authenticity_check.py` 自动生成，仅供真实性核查，不构成投资建议。*

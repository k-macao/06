"""
KOL 存活探测与内容抓取
策略：
1. 优先尝试 YouTube RSS (https://www.youtube.com/feeds/videos.xml?channel_id=...)
2. 依次备用官方 YouTube Data API、开源 yt-dlp、频道 /videos 页结构化数据
3. 网络短暂故障时使用上次已审计通过且仍在时效内的真实条目
4. 所有方案都失败才标记为未验证；绝不生成兜底标题、日期或链接
"""
import json
import os
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import feedparser

from .config import KOL_DATA_PATH, OUTPUT_DIR, REQUEST_TIMEOUT, USER_AGENT, ACTIVE_THRESHOLD_DAYS

HEADERS = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8"}

# 用于中文模拟数据的真实感语料 - 覆盖全部 45 个活跃 KOL
MOCK_TITLES_POOL = {
    "Graham Stephan": [
        ("美联储突然转向？2026年降息押注与房贷利率崩跌前夜", "美联储官员放鸽，Graham 分析房贷利率跌破6%对刚需买家的抄底窗口，并警告高杠杆投资者的流动性风险。"),
        ("我为什么还在定投VOO：标普500估值泡沫下的生存指南", "用数据回测 2000 与 2008 崩盘期的定投收益，强调现金流与低费率 ETF 的防御价值。"),
        ("月入1万如何一年存下6万：极简生活的残酷实操", "拆解日常开销、信用卡返现与副业收入，给出可复制的存钱清单。"),
    ],
    "Andrei Jikh": [
        ("37万亿美债重置已启动！普通人必做的3件事", "详解美国债务货币化与美元信用裂缝，建议配置比特币、黄金与股息资产的三角防御。"),
        ("股息贵族崩了？我清仓了这只20年分红股", "复盘 3M 与 Walgreens 暴跌，强调股息可持续性审查框架。"),
        ("信用卡0利率套利还能玩吗？2026年实测", "实测 Chase 与 Amex 余额转移，结合信用分影响给出操作红线。"),
    ],
    "Humphrey Yang": [
        ("用一张图看懂期权：5年级版 Call/Put 科普", "用买奶茶券类比期权，拆解时间价值与行权价选择。"),
        ("15条提前退休路径大排名：时薪10万刀多久能FIRE？", "对比房地产、指数基金、副业等路径，给出3年到30年的时间表。"),
        ("比特币2026还值得买吗？我的仓位与止损线", "回顾减半周期，结合ETF资金流入判断牛熊分界。"),
    ],
    "The Plain Bagel": [
        ("杠杆ETF是财富加速器还是绞肉机？", "用数学推导每日重置的损耗，证明长期持有 3x ETF 的隐形税。"),
        ("BlackRock与Vanguard真的控制全世界吗？", "拆解被动基金的投票权与所有权迷思，还原真实影响力边界。"),
        ("量化紧缩QT：美联储缩表如何抽干你的流动性", "解释国债到期与银行准备金的关系，推演对股市估值的影响。"),
    ],
    "Patrick Boyle": [
        ("散户的末日狂欢：Meme股与伪大师的泡沫史", "回顾南海泡沫到GameStop，讽刺网红荐股的话术陷阱。"),
        ("对冲基金如何做空你的信仰？", "揭秘融券、CDS与波动率交易的阴暗面，带英式幽默。"),
        ("为什么每次危机都一样？金融史的诅咒循环", "对比1929与2008，指出监管套利永不眠。"),
    ],
    "Meet Kevin": [
        ("突发：CPI爆表！美股盘前崩跌，我的操作", "CPI超预期0.4%，Kevin 直播解读对冲策略，呼吁现金为王。"),
        ("加州房产税提案通过？房东的噩梦来了", "分析Prop 13改革对租金与房价的连锁冲击。"),
        ("特斯拉Q2交付暴雷：Elon 还能讲故事吗？", "拆解交付量与毛利率，给出 $180 支撑位判断。"),
    ],
    "Joseph Carlson": [
        ("股息增长组合7月调仓：我卖掉了这只30年分红王", "审查 Johnson & Johnson 现金流覆盖率，下调预期后止盈。"),
        ("被动收入月入5000刀的真相：需要多少本金？", "用 4% 法则倒推 150 万本金门槛，提示股息陷阱。"),
        ("为什么我只买能涨股息的公司？", "对比高股息与股息增长的长期总回报，倡导质量优先。"),
    ],
    "Sven Carlin": [
        ("AI泡沫的终局：价值投资者的最后防线", "用 DC­F 重算英伟达与微软，警告估值偏离内在价值 60%。"),
        ("这家被抛弃的欧洲银行，隐含回报率 25%？", "深度研报：拨备覆盖率与账面价值折扣的错杀机会。"),
        ("通胀真的死了吗？大宗商品周期的危险信号", "分析铜油库存与货币增速，提示滞胀卷土重来。"),
    ],
    "Mark Tilbury": [
        ("19岁开始投资 vs 30岁：复利差了整整 100万", "用 7% 年化演示晚 10 年的代价，号召年轻人立刻开户。"),
        ("我如何用3家小生意滚到800万英镑", "复盘洗车、房产与 YouTube 的资本叠加路径。"),
        ("别再存钱了，先买资产！穷人与富人的分水岭", "对比储蓄与资产负债表思维，鼓励现金流资产。"),
    ],
    "Jeremy Lefebvre": [
        ("Palantir 财报炸裂：AI 故事还能涨多久？", "拆解政府订单与商业化拐点，给出持有与止盈区间。"),
        ("我的重仓股暴跌40%：复盘与教训", "坦承 CrowdStrike 持仓失误，强调分散与仓位管理。"),
        ("成长股 vs 价值股：2026下半场押哪边？", "对比利率敏感度与盈利增速，给出 60/40 配置。"),
    ],
    "Ben Felix": [
        ("学术研究证明：95%的选股者跑不赢指数", "引用 SPIVA 与 Fama-French，论证低费率全球分散的威力。"),
        ("为什么你不该听财经新闻做投资？", "用噪声与信号理论解释媒体对收益的破坏。"),
        ("最优资产配置：30岁、50岁该怎么配？", "基于生命周期模型给出股债比例与再平衡纪律。"),
    ],
    "Erika Kullberg": [
        ("航空公司拒赔？这条法律让你白拿1000刀", "解读美欧航班延误赔偿条款，手把手教索赔话术。"),
        ("别再为这5个费用买单：律师教你省2万", "拆解租约、健身房与订阅陷阱的法律漏洞。"),
        ("学生贷款减免新政：符合条件的3类人", "梳理拜登新计划与申请截止，提示材料清单。"),
    ],
    "Vivien Tu": [
        ("华尔街前交易员坦白：女性理财的5个坑", "揭示收入差距与风险厌恶，教你谈薪与定投。"),
        ("月薪5000也能理财：我的50/30/20实操", "演示自动转账与高息储蓄的懒人组合。"),
        ("为什么你该先还高息债再投资？", "对比 7% 债务与 8% 预期收益，强调无风险回报。"),
    ],
    "Jaspreet Singh": [
        ("穷人思维 vs 富人思维：1个转变让你多赚10倍", "Minority Mindset 核心：从消费者到生产者视角。"),
        ("美联储印钞的隐形税：谁在偷走你的购买力？", "解释通胀是穷人税，呼吁持有生产性资产。"),
        ("2026年最危险的投资：你正在买的这个东西", "点名长期债券与僵尸企业，警告利率风险。"),
    ],
    "Investing with Rose": [
        ("零基础买ETF：3只基金搞定全球配置", "推荐 VT + BND + VNQ 的一站式懒人组合。"),
        ("女生投资第一课：别怕，你比想象中更懂钱", "用咖啡价类比复利，消除入门恐惧。"),
        ("股息ETF vs 成长ETF：新手该怎么选？", "对比 SCHD 与 VUG 的波动与现金流差异。"),
    ],
    "ClearValue Tax": [
        ("2026新税法：这4个抵扣让中产多退5000刀", "详解 SALT 上限、子女抵免与清洁能源补贴。"),
        ("IRS 审计率飙升：这5类人最危险", "盘点加密货币、现金生意与高扣除申报的红旗。"),
        ("小企业主必看：QBI 20% 抵扣还能薅多久？", "推演日落条款与转换 S-Corp 的节税窗口。"),
    ],
    "Everything Money": [
        ("八柱分析法实战：这只股票被高估了40%？", "用软件跑毛利率、债务与估值八项打分，亮红灯。"),
        ("财报藏雷：3个数字识破利润操纵", "演示应收账款与库存周转的异常信号。"),
        ("何时卖出？我的8分制止盈纪律", "低于 6 分即清仓，回测胜率与回撤控制。"),
    ],
    "New Money": [
        ("巴菲特2026股东信：现金3000亿在等什么？", "解读为何股神宁可持有国债也不追高。"),
        ("芒格的最后忠告：别碰你不懂的生意", "用喜诗糖果与比亚迪案例诠释能力圈。"),
        ("段永平 vs 芒格：中美价值投资的异同", "对比集中与分散的哲学，提炼可复制心法。"),
    ],
    "Financial Education": [
        ("我刚卖了特斯拉：持仓逻辑全复盘", "止盈 30% 后转向现金，等待 150 支撑。"),
        ("这只AI小盘股，我重仓的理由", "展示仓位 25% 的高 conviction，下注算力赛道。"),
        ("跟单有风险：为什么别抄我的作业？", "强调个人风险承受与时间 horizon 差异。"),
    ],
    "Brian Feroldi": [
        ("打分表测评：Shopify 商业模式能打几分？", "从护城河、定价权到创始人，给出 7.5/10。"),
        ("财报拆解：这家SaaS为何永远不赚钱？", "揭示 SBC 稀释与客户流失的真相。"),
        ("10年10倍股的共同基因", "总结高毛利、轻资产与复利增长的三要素。"),
    ],
    "贝拉聊财金": [
        ("AI超级碗与万亿宣言！机构史诗级抛售潮来了？", "英伟达GTC后的产业链推演，提示机构借利好出货的风险。"),
        ("中美顶级金融暗战：这个周末发生了什么", "拆解中美利差与外资流动，判断港股与中概的短线反弹窗口。"),
        ("美股七巨头财报周：谁在裸泳一目了然", "对比云、广告与硬件毛利，给出强弱排序与调仓建议。"),
    ],
    "阳光财经": [
        ("上证 vs 纳指：技术面背离的生死抉择", "用 MACD 与成交量分析双市场节奏，提示轮动。"),
        ("黄金分割+筹码峰：A股反弹目标位在哪？", "测算 3200 点压力与下方 2850 支撑。"),
        ("北向资金连续流出：外资在怕什么？", "关联汇率与美债利率，判断企稳信号。"),
    ],
    "小翠时政财经": [
        ("社融暴跌背后：居民为什么不敢借钱了？", "拆解7月社融与M1数据，揭示资产负债表衰退迹象。"),
        ("地方城投展期潮：谁在为土地财政买单？", "追踪城投债展期案例，评估银行坏账风险。"),
        ("人民币破7.3：央行工具箱还有多少子弹？", "分析中间价与离岸空头博弈，预测汇率底线。"),
    ],
    "老李财经": [
        ("半导体寒冬还是拐点？台积电财报给答案", "拆解 3nm 产能利用率与 AI 订单能见度。"),
        ("英伟达 vs AMD：谁能吃到AI芯片第二波？", "对比 CUDA 生态与性价比，押注供应链。"),
        ("美股科技股估值回落30%：抄底还是接飞刀？", "用 PEG 与现金流折现给出安全边际。"),
    ],
    "瑞威金融": [
        ("黄金日线三连阳：1980美元能否突破？", "结合非农与实际利率，推演多空分水岭。"),
        ("外汇日内秘籍：伦敦开盘15分钟定胜负", "分享突破与假突破的过滤技巧。"),
        ("原油暴涨10%：地缘溢价还是需求复苏？", "分析 OPEC+ 减产与库存去化博弈。"),
    ],
    "零总投资": [
        ("交易员的噩梦：为什么你总在高点买入？", "揭示 FOMO 与锚定效应，教你预设止损。"),
        ("港股打板心得：3个指标过滤假突破", "用成交量、换手与板块联动提高胜率。"),
        ("从爆仓到翻身：我的资金管理铁律", "固定 1% 风险敞口，活下来才有资格赚钱。"),
    ],
    "孙老师财经": [
        ("黄金新高后暴跌5%：牛市结束了吗？", "对比 1980 与 2011 顶部形态，判断回调是洗盘。"),
        ("美联储点阵图藏玄机：今年还能降几次？", "解读票委分歧与通胀粘性，给出利率路径。"),
        ("石油美元松动：人民币结算能走多远？", "追踪沙特与中俄能源协议的地缘冲击。"),
    ],
    "美股投资网": [
        ("盘前必读：七巨头期权异动与大单揭秘", "扫描 Unusual Options Activity，提示方向选择。"),
        ("量化信号：标普500站上200日均线意味着什么？", "回测 50 年突破后的 6 个月收益分布。"),
        ("今夜非农：预期 18 万，前瞻与交易预案", "给出数据超预期与不及预期的两套剧本。"),
    ],
    "逻辑财金": [
        ("CPI 3.2% 背后：哪些分项在说谎？", "拆解住房、能源与核心服务的权重扭曲。"),
        ("M2增速转正：钱真的流向实体了吗？", "追踪社融与存款搬家，揭示空转风险。"),
        ("从库存周期看A股：现在处于什么位置？", "用 PMI 与产成品库存定位周期拐点。"),
    ],
    "美股说": [
        ("财报拆解：Meta 广告帝国还能涨多久？", "分析 Reels 变现与 Reality Labs 烧钱的平衡。"),
        ("竞争格局：特斯拉 vs 理想 vs 蔚来", "对比交付、毛利与现金流，给出排序。"),
        ("为什么我看空这只明星股？", "揭示高估值与增速放缓的剪刀差。"),
    ],
    "Kelvin Learns Investing": [
        ("FIRE实战：30岁攒够100万需要多少年？", "用 50% 储蓄率演示 12 年路径，含新加坡案例。"),
        ("指数基金 vs 买房：年轻人的第一桶金怎么选？", "对比流动性与杠杆，给出混合策略。"),
        ("副业增收的3条跑道：我如何月入多1万", "分享内容创作与咨询变现的可复制路径。"),
    ],
    "The Swedish Investor": [
        ("《穷查理宝典》10句精华：芒格的终极智慧", "提炼多学科思维与逆向思考的核心。"),
        ("《原则》精读：达利欧的投资圣经", "总结极度透明与可信度加权的组织智慧。"),
        ("《随机漫步》：为什么你跑不赢市场？", "用醉汉走路类比有效市场假说。"),
    ],
    "Preston Pysh": [
        ("比特币估值模型：S2F 还有效吗？", "结合存量流量与链上成本，测算公允区间。"),
        ("美联储缩表 vs 财政放水：谁在决定流动性？", "拆解 TGA 与逆回购的水位博弈。"),
        ("如何给一家不赚钱的AI公司估值？", "用 PS 与 TAM 推演终局市占率。"),
    ],
    "PensionCraft": [
        ("退休组合回测：60/40 还能用吗？", "回测 1970-2026，引入黄金与短债的改良版。"),
        ("英国养老金危机启示：LDI 的死亡螺旋", "复盘 2022  gilt 崩盘，警示杠杆风险。"),
        ("通胀挂钩债券：退休者的隐形盾牌", "对比 TIPS 与 nominal 债的真实收益。"),
    ],
    "Ramin Nakisa": [
        ("多资产相关性崩了？股债为何同跌", "解释通胀 regime 下相关性翻转，应对策略。"),
        ("战略配置：如何用3个ETF覆盖全球？", "用因子分散降低尾部风险。"),
        ("退休提款率：4% 法则已死？", "结合高估值与长寿风险，给出动态提款表。"),
    ],
    "Financial Diet": [
        ("月薪3000的预算美学：如何体面地穷", "分享信封预算法与快乐消费清单。"),
        ("为什么你总存不下钱？3个心理陷阱", "揭示生活方式膨胀与社交比较。"),
        ("副业焦虑：不上进还是被割韭菜？", "批判 hustle culture，倡导可持续。"),
    ],
    "Maverick of Wall Street": [
        ("标普500 泡沫警报：席勒PE已超1929", "对比历次顶部估值，警告均值回归。"),
        ("技术面顶背离：纳指的最后疯狂？", "用 RSI 与成交量揭示动能衰竭。"),
        ("做空指南：如何用期权对冲崩盘风险", "演示保护性看跌与价差策略。"),
    ],
    "Cameron Stewart": [
        ("DCF实战：给英伟达算个公允价", "假设 20% 增速 5 年，贴现率 10% 得出 $720。"),
        ("为什么DCF是唯一诚实的估值法？", "对比 PE 的操纵空间，强调现金为王。"),
        ("手把手：用10-K算自由现金流", "从经营现金流扣除维持性资本开支。"),
    ],
    "Fast Graphs (Chuck Carnevale)": [
        ("估值回归：这只股息王被错杀了30%", "用 FAST Graphs 展示历史 PE 通道与预期。"),
        ("图形化财报：3秒看懂一家公司", "蓝橙线揭示盈利与估值的背离。"),
        ("为什么我从不追高？", "用 15% 年化预期筛选低估标的。"),
    ],
    "Money Coach Nick": [
        ("每日1分钟：今天的理财微行动", "自动转 10 刀到高息账户，积少成多。"),
        ("3个App帮你年省2000刀", "对比返现与比价工具的实测。"),
        ("别再为银行付费：免费账户清单", "罗列零费用与高 APY 的替代。"),
    ],
    "TradingView (Top Authors)": [
        ("BTC 4小时头肩顶：6万关口保卫战", "多名 Top 作者共识看空，目标 5.2 万。"),
        ("黄金周线突破：2000美元只是起点？", "技术派看多2000-2200箱体突破。"),
        ("标普500 期权墙：5700 是多空决战线", "用 gamma 敞口测算最大痛点。"),
    ],
    "Real Vision (Individual Guest Analysts)": [
        ("Raoul Pal：流动性海啸将至，All in 加密？", "讲述债务货币化与指数级科技的叠加。"),
        ("Druckenmiller：我为何重仓做空长债？", "押注财政赤字与通胀二次抬头。"),
        ("中美脱钩：地缘重构下的大宗商品新秩序", "圆桌讨论铜、锂与稀土的定价权转移。"),
    ],
    "老厉害财经": [
        ("A股3000点保卫战：谁在砸盘谁在护盘？", "点名量化与外资流向，犀利吐槽。"),
        ("割韭菜新套路：增发+减持的完美收割", "拆解定增折价与清仓式减持。"),
        ("牛市不言顶？这次不一样的5个幻觉", "讽刺激情喊单，呼吁敬畏。"),
    ],
    "inves talk": [
        ("对话段永平：什么叫敢重仓的便宜？", "访谈实录：只买懂的，敢下重手的逻辑。"),
        ("对话半导体老兵：国产替代真能成吗？", "拆解设备与材料卡脖子环节。"),
        ("对话抄底王：如何在恐慌中扣扳机？", "分享仓位与心理建设的反人性训练。"),
    ],
    "硬核刘大": [
        ("香港账户全攻略：2026年还能开哪家？", "实测 5 家银行开户门槛与冻结风险。"),
        ("USDT 换汇暗流：走资的灰色地带", "揭示商户与冻卡风险，合规路径。"),
        ("新加坡家族办公室：100万刀够格吗？", "对比13O与13U的税务与移民联动。"),
    ],
}

# 默认三条兜底标题（用于未知KOL）
GENERIC_TITLES = [
    ("美股高位震荡：财报季是蜜糖还是砒霜？", "拆解标普500成分股盈利超预期率与指引下调，判断回调风险。"),
    ("黄金再创新高：避险还是泡沫？", "对比实际利率与央行购金，提示追高与回调的临界点。"),
    ("降息交易拥挤度爆表：谁会成为最后的接盘侠？", "分析利率期货定价与美联储点阵图的分歧，给出防御配置。"),
]
HISTORICAL_MOCK_TITLES = (
    {title for rows in MOCK_TITLES_POOL.values() for title, _ in rows}
    | {title for title, _ in GENERIC_TITLES}
)


def parse_last_update_from_rss(channel_id):
    """方案 A：通过 YouTube RSS 获取最近更新（显式超时，避免 CI 卡死）。"""
    if not channel_id:
        return None, []
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        response = requests.get(rss_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        if not feed.entries:
            return None, []
        entries = feed.entries[:3]
        latest = entries[0]
        if hasattr(latest, "published_parsed") and latest.published_parsed:
            dt = datetime(*latest.published_parsed[:6], tzinfo=timezone.utc)
        else:
            dt = datetime.now(timezone.utc)
        items = []
        for e in entries:
            pub = datetime(*e.published_parsed[:6], tzinfo=timezone.utc) if hasattr(e, "published_parsed") and e.published_parsed else dt
            items.append({
                "title": e.title,
                "link": e.link,
                "published": pub.isoformat(),
                "summary": e.get("summary", "")[:220],
                "source": "youtube_rss",
            })
        return dt, items
    except Exception as ex:
        print(f"[RSS] {channel_id} failed: {ex}")
        return None, []


def fetch_from_youtube_api(channel_id):
    """方案 B：可选 YouTube Data API；设置 YOUTUBE_API_KEY 后启用。"""
    api_key = os.getenv("YOUTUBE_API_KEY", "").strip()
    if not channel_id or not api_key:
        return None, []
    try:
        common = {"key": api_key, "part": "contentDetails", "id": channel_id}
        channel_resp = requests.get(
            "https://www.googleapis.com/youtube/v3/channels",
            params=common, headers=HEADERS, timeout=REQUEST_TIMEOUT,
        )
        channel_resp.raise_for_status()
        channels = channel_resp.json().get("items", [])
        if not channels:
            return None, []
        uploads = channels[0]["contentDetails"]["relatedPlaylists"]["uploads"]
        videos_resp = requests.get(
            "https://www.googleapis.com/youtube/v3/playlistItems",
            params={"key": api_key, "part": "snippet", "playlistId": uploads, "maxResults": 3},
            headers=HEADERS, timeout=REQUEST_TIMEOUT,
        )
        videos_resp.raise_for_status()
        items = []
        for row in videos_resp.json().get("items", []):
            snippet = row.get("snippet", {})
            video_id = snippet.get("resourceId", {}).get("videoId")
            title = snippet.get("title")
            published = snippet.get("publishedAt") or ""
            if not video_id or not title or title in ("Private video", "Deleted video"):
                continue
            items.append({
                "title": title,
                "link": f"https://www.youtube.com/watch?v={video_id}",
                "published": published,
                "summary": (snippet.get("description") or "")[:220],
                "source": "youtube_data_api",
            })
        if not items:
            return None, []
        latest = datetime.fromisoformat(items[0]["published"].replace("Z", "+00:00"))
        return latest, items
    except Exception as ex:
        print(f"[YouTube API] {channel_id} failed: {ex}")
        return None, []


def fetch_from_ytdlp(channel_url):
    """方案 C：使用开源 yt-dlp 提取频道最近视频，不下载媒体文件。"""
    if not channel_url or "youtube.com" not in channel_url:
        return None, []
    try:
        import yt_dlp
    except ImportError:
        print("[yt-dlp] 未安装，跳过备用方案")
        return None, []

    videos_url = channel_url.rstrip("/") + "/videos"
    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
        "playlist_items": "1:3",
        "socket_timeout": REQUEST_TIMEOUT,
        "retries": 1,
        "ignoreerrors": True,
    }
    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            result = downloader.extract_info(videos_url, download=False)
        entries = (result or {}).get("entries") or []
        items = []
        dates = []
        for entry in entries:
            if not entry:
                continue
            video_id = entry.get("id")
            title = entry.get("title")
            webpage_url = entry.get("webpage_url")
            if not webpage_url and video_id:
                webpage_url = f"https://www.youtube.com/watch?v={video_id}"
            timestamp = entry.get("timestamp") or entry.get("release_timestamp")
            published = ""
            dt = None
            if timestamp:
                dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                published = dt.isoformat()
            elif entry.get("upload_date"):
                try:
                    dt = datetime.strptime(entry["upload_date"], "%Y%m%d").replace(tzinfo=timezone.utc)
                    published = dt.isoformat()
                except ValueError:
                    pass
            # 无发布日期无法判断是否仍在时效内，因此不纳入战报。
            if not title or not webpage_url or not published or dt is None:
                continue
            dates.append(dt)
            items.append({
                "title": title,
                "link": webpage_url,
                "published": published,
                "summary": (entry.get("description") or "")[:220],
                "source": "yt_dlp",
            })
        return (max(dates), items[:3]) if items and dates else (None, [])
    except Exception as ex:
        print(f"[yt-dlp] {videos_url} failed: {ex}")
        return None, []


def _find_initial_data(page_text):
    """从频道 HTML 中安全提取 ytInitialData JSON。"""
    decoder = json.JSONDecoder()
    for marker in ("var ytInitialData = ", "window[\"ytInitialData\"] = ", "ytInitialData = "):
        start = page_text.find(marker)
        if start < 0:
            continue
        raw = page_text[start + len(marker):].lstrip()
        try:
            return decoder.raw_decode(raw)[0]
        except (ValueError, json.JSONDecodeError):
            continue
    return None


def _walk_video_renderers(node):
    if isinstance(node, dict):
        for key in ("videoRenderer", "gridVideoRenderer"):
            if isinstance(node.get(key), dict):
                yield node[key]
        for value in node.values():
            yield from _walk_video_renderers(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk_video_renderers(value)


def scrape_channel_items(channel_url):
    """方案 C：从频道 /videos 页的结构化数据提取真实视频链接。"""
    if not channel_url or "youtube.com" not in channel_url:
        return None, []
    videos_url = channel_url.rstrip("/") + "/videos"
    try:
        response = requests.get(videos_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = _find_initial_data(response.text)
        if not data:
            return None, []
        items = []
        seen = set()
        now = datetime.now(timezone.utc)
        for renderer in _walk_video_renderers(data):
            video_id = renderer.get("videoId")
            title_runs = renderer.get("title", {}).get("runs", [])
            title = title_runs[0].get("text", "") if title_runs else renderer.get("title", {}).get("simpleText", "")
            if not video_id or not title or video_id in seen:
                continue
            seen.add(video_id)
            relative = renderer.get("publishedTimeText", {}).get("simpleText", "")
            published = now - timedelta(days=parse_relative_time(relative))
            desc_runs = renderer.get("descriptionSnippet", {}).get("runs", [])
            summary = "".join(run.get("text", "") for run in desc_runs)[:220]
            items.append({
                "title": title,
                "link": f"https://www.youtube.com/watch?v={video_id}",
                "published": published.isoformat(),
                "summary": summary,
                "source": "youtube_channel_page",
            })
            if len(items) == 3:
                break
        return (datetime.fromisoformat(items[0]["published"]), items) if items else (None, [])
    except Exception as ex:
        print(f"[channel videos] {videos_url} failed: {ex}")
        return None, []


def scrape_channel_page(channel_url):
    """轻量抓取频道页，尝试提取最近视频的 publish 信息"""
    try:
        resp = requests.get(channel_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return None
        text = resp.text
        m = re.search(r'"publishedTimeText"\s*:\s*\{"simpleText"\s*:\s*"([^"]+)"', text)
        if m:
            raw = m.group(1)
            days_ago = parse_relative_time(raw)
            dt = datetime.now(timezone.utc) - timedelta(days=days_ago)
            return dt
        m2 = re.search(r'"uploadDate"\s*:\s*"([^"]+)"', text)
        if m2:
            try:
                dt = datetime.fromisoformat(m2.group(1).replace("Z", "+00:00"))
                return dt
            except:
                pass
        return None
    except Exception as ex:
        print(f"[scrape] {channel_url} {ex}")
        return None

def parse_relative_time(s: str) -> int:
    s = s.lower()
    num = re.search(r"(\d+)", s)
    n = int(num.group(1)) if num else 0
    if "minute" in s or "hour" in s:
        return 0
    if "day" in s:
        return n
    if "week" in s:
        return n * 7
    if "month" in s:
        return n * 30
    if "year" in s:
        return n * 365
    return n

def load_verified_cache(data_path=OUTPUT_DIR / "data.json"):
    """方案 D：读取上次成功产物中的真实条目，网络短暂故障时降级使用。"""
    path = Path(data_path)
    if not path.exists():
        return {}
    try:
        output = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    cached = {}
    for entry in output.get("active_kols", []):
        kid = entry.get("kol", {}).get("id")
        valid = []
        for item in entry.get("items", []):
            link = item.get("link", "")
            title = item.get("title", "")
            if (item.get("is_mock") is True or not title or not link.startswith("https://")
                    or re.search(r"[?&]v=mock\d*", link, re.I)
                    or title in HISTORICAL_MOCK_TITLES):
                continue
            clean = {k: item.get(k, "") for k in ("title", "link", "published", "summary", "lang")}
            clean.update({"original_title": title, "is_mock": False, "source": "verified_cache"})
            valid.append(clean)
        if kid is not None and valid:
            cached[kid] = valid[:3]
    return cached


def _latest_datetime(items):
    dates = []
    for item in items or []:
        try:
            dt = datetime.fromisoformat((item.get("published") or "").replace("Z", "+00:00"))
            dates.append(dt.replace(tzinfo=dt.tzinfo or timezone.utc))
        except ValueError:
            continue
    return max(dates) if dates else None


def is_active_kol(kol, threshold_days=ACTIVE_THRESHOLD_DAYS, cached_items=None):
    channel_id = kol.get("channel_id")
    channel_url = kol.get("channel_url")
    # 按可信度与实时性依次降级，所有方案都必须返回可点击的真实来源。
    strategies = (
        ("RSS", lambda: parse_last_update_from_rss(channel_id)),
        ("YouTube API", lambda: fetch_from_youtube_api(channel_id)),
        ("yt-dlp", lambda: fetch_from_ytdlp(channel_url)),
        ("频道页", lambda: scrape_channel_items(channel_url)),
    )
    for _, strategy in strategies:
        last_dt, items = strategy()
        if last_dt and items:
            age_days = (datetime.now(timezone.utc) - last_dt).days
            return age_days <= threshold_days, last_dt, items

    cached_items = cached_items or []
    cached_dt = _latest_datetime(cached_items)
    if cached_dt:
        age_days = (datetime.now(timezone.utc) - cached_dt).days
        if age_days <= threshold_days:
            return True, cached_dt, cached_items

    # 最后的 HTML 日期探测只用于确认沉寂，不会制造内容。
    if channel_url:
        dt2 = scrape_channel_page(channel_url)
        if dt2:
            return False, dt2, []
    return False, None, []


def enrich_with_real_content(kol, real_items):
    """标准化最多三条真实抓取结果；没有真实条目时返回空列表。"""
    enriched = []
    for ri in (real_items or [])[:3]:
        # 缺少来源链接或标题的条目不可追溯，不进入报告。
        if not ri.get("title") or not ri.get("link"):
            continue
        enriched.append({
            "title": ri["title"],
            "original_title": ri["title"],
            "link": ri["link"],
            "published": ri.get("published", ""),
            "summary": ri.get("summary", ""),
            "lang": kol.get("language", ""),
            "source": ri.get("source", "verified_source"),
            "is_mock": False,
        })
    return enriched


# 保留旧函数名，避免外部调用方升级时中断；其行为已改为只接受真实内容。
def enrich_with_mock_content(kol, real_items):
    return enrich_with_real_content(kol, real_items)

def scan_kols(kol_list=None, verbose=True):
    import pathlib, json
    if kol_list is None:
        with open(KOL_DATA_PATH, "r", encoding="utf-8") as f:
            kol_list = json.load(f)
    active_kols = []
    inactive_kols = []
    enriched_map = {}
    verified_cache = load_verified_cache()
    for kol in kol_list:
        active, last_dt, items = is_active_kol(kol, cached_items=verified_cache.get(kol.get("id"), []))
        status = "✅活跃" if active else ("⚪未验证" if last_dt is None else "💤沉寂")
        last_str = last_dt.strftime("%Y-%m-%d") if last_dt else "未知"
        if verbose:
            print(f"{status} [{kol['id']:02d}] {kol['name']:20s} | {kol['platform']:12s} | 最近: {last_str} | {kol['fans']}")
        enriched = enrich_with_real_content(kol, items) if active else []
        if active and enriched:
            active_kols.append(kol)
            enriched_map[kol["id"]] = enriched
        else:
            # “活跃”但抓不到可追溯条目时也不进入战报，防止下游补造内容。
            inactive_kols.append(kol)
        time.sleep(0.15)
    return active_kols, inactive_kols, enriched_map

if __name__ == "__main__":
    a, b, m = scan_kols()
    print(f"\n活跃: {len(a)} / 总数: {len(a)+len(b)}")
    for kol in a[:2]:
        print(kol["name"], m[kol["id"]])

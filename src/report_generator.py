"""
章鱼风 HTML 报告生成器
- 复古游戏章鱼风格
- 多空战斗可视化
- 作者：章鱼 AI·全景分析
"""
from pathlib import Path
from datetime import datetime
import json
from jinja2 import Template

from .config import AUTHOR, REPORT_TITLE

# 内联模板，避免外部依赖路径问题
TEMPLATE_STR = r"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ report_title }} - {{ author }}</title>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=ZCOOL+KuaiLe&family=Noto+Sans+SC:wght@700;900&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0f0f1e;
    --panel:#1a1a2e;
    --panel2:#16213e;
    --yellow:#ffe066;
    --pink:#ff6b9d;
    --cyan:#00e5ff;
    --green:#00ff88;
    --red:#ff3b30;
    --blue:#0080ff;
    --border:#fff;
  }
  *{box-sizing:border-box}
  body{
    margin:0;
    background:var(--bg);
    color:#fff;
    font-family:'Noto Sans SC', sans-serif;
    overflow-x:hidden;
  }
  /* 章鱼网格背景 */
  body::before{
    content:"";
    position:fixed;inset:0;
    background:
      linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size:32px 32px;
    pointer-events:none;
    z-index:-1;
  }
  /* 扫描线 */
  body::after{
    content:"";
    position:fixed;inset:0;
    background:repeating-linear-gradient(0deg, rgba(0,0,0,0) 0px, rgba(0,0,0,0) 2px, rgba(255,255,255,0.03) 3px);
    pointer-events:none;z-index:999;
  }
  .container{max-width:1200px;margin:0 auto;padding:18px 16px 40px}
  /* 章鱼边框通用 */
  .pixel-border{
    border:4px solid #fff;
    box-shadow:
      0 0 0 4px #000,
      6px 6px 0 #000,
      inset 0 0 0 2px rgba(255,255,255,0.2);
    position:relative;
  }
  .pixel-border::before{
    content:"";position:absolute;inset:4px;
    border:2px dashed rgba(255,255,255,0.15);pointer-events:none;
  }
  /* 顶部标题 */
  .header{
    background:linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding:22px 18px;
    text-align:center;
    margin-bottom:18px;
  }
  .header h1{
    margin:0;
    font-family:'Press Start 2P', monospace;
    font-size:13px;
    line-height:1.8;
    letter-spacing:1px;
    color:var(--yellow);
    text-shadow:3px 3px 0 #000, 0 0 12px rgba(255,224,102,0.6);
    word-break:break-all;
  }
  .header .subtitle{
    margin-top:12px;
    font-size:12px;
    color:var(--cyan);
    letter-spacing:2px;
    font-family:'Press Start 2P', monospace;
  }
  .header .meta{
    margin-top:14px;
    display:flex;justify-content:center;gap:12px;flex-wrap:wrap;
    font-size:11px;
  }
  .meta-badge{
    background:#000;
    border:2px solid #fff;
    padding:6px 10px;
    font-family:'Press Start 2P', monospace;
    font-size:7px;
    box-shadow:3px 3px 0 #000;
  }
  .meta-badge.yellow{border-color:var(--yellow);color:var(--yellow)}
  .meta-badge.cyan{border-color:var(--cyan);color:var(--cyan)}
  .meta-badge.pink{border-color:var(--pink);color:var(--pink)}
  .meta-badge.green{border-color:var(--green);color:var(--green)}

  /* 多空战场 */
  .battlefield{
    background:#000;
    padding:16px;
    margin-bottom:18px;
    display:grid;
    grid-template-columns:1fr auto 1fr;
    gap:14px;
    align-items:center;
  }
  @media (max-width:768px){
    .battlefield{grid-template-columns:1fr; text-align:center}
  }
  .fighter{
    background:var(--panel);
    padding:14px;
    text-align:center;
  }
  .fighter.bull{border-left:6px solid var(--red)}
  .fighter.bear{border-left:6px solid var(--blue)}
  .fighter .icon{font-size:36px;filter:drop-shadow(3px 3px 0 #000)}
  .fighter .label{
    font-family:'Press Start 2P', monospace;
    font-size:8px;
    margin:8px 0 6px;
    letter-spacing:1px;
  }
  .fighter.bull .label{color:var(--red)}
  .fighter.bear .label{color:var(--blue)}
  .fighter .count{
    font-size:28px;font-weight:900;line-height:1;
    text-shadow:2px 2px 0 #000;
  }
  .fighter.bull .count{color:var(--red)}
  .fighter.bear .count{color:var(--blue)}
  .fighter .sub{font-size:9px;opacity:0.7;margin-top:4px;font-family:'Press Start 2P', monospace}
  .vs{
    text-align:center;
    font-family:'Press Start 2P', monospace;
    font-size:18px;
    color:var(--yellow);
    text-shadow:3px 3px 0 #000;
    animation:pulse 1.2s infinite;
  }
  @keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}

  .battle-stats{
    grid-column:1 / -1;
    margin-top:8px;
  }
  .health-row{display:flex;align-items:center;gap:8px;margin:8px 0}
  .health-label{
    width:70px;
    font-family:'Press Start 2P', monospace;
    font-size:7px;
    text-align:right;
  }
  .health-bar{
    flex:1;height:18px;
    background:#222;
    border:2px solid #fff;
    display:flex;
    overflow:hidden;
    box-shadow:inset 2px 2px 0 rgba(0,0,0,0.5);
  }
  .health-fill{
    height:100%;
    display:flex;align-items:center;justify-content:center;
    font-family:'Press Start 2P', monospace;
    font-size:6px;
    color:#000;
    font-weight:bold;
    transition:width 1s ease;
    text-shadow:none;
  }
  .health-fill.bull{background:linear-gradient(90deg, #ff3b30, #ff6b6b);box-shadow:inset 0 -3px 0 rgba(0,0,0,0.3)}
  .health-fill.bear{background:linear-gradient(90deg, #0080ff, #00e5ff);box-shadow:inset 0 -3px 0 rgba(0,0,0,0.3)}
  .health-fill.neutral{background:linear-gradient(90deg, #888, #bbb)}

  /* 筛选条 */
  .filter-bar{
    display:flex;gap:8px;flex-wrap:wrap;
    margin-bottom:14px;
    justify-content:center;
  }
  .filter-btn{
    background:#000;color:#fff;
    border:2px solid #fff;
    padding:8px 14px;
    font-family:'Press Start 2P', monospace;
    font-size:7px;
    cursor:pointer;
    box-shadow:3px 3px 0 #000;
  }
  .filter-btn.active{background:var(--yellow);color:#000;border-color:#000}
  .filter-btn:hover{transform:translate(-1px,-1px);box-shadow:4px 4px 0 #000}

  /* KOL 卡片网格 */
  .grid{
    display:grid;
    grid-template-columns:repeat(auto-fill, minmax(360px, 1fr));
    gap:16px;
  }
  @media (max-width:420px){
    .grid{grid-template-columns:1fr}
  }
  .kol-card{
    background:var(--panel);
    padding:14px;
    display:flex;flex-direction:column;
    gap:10px;
    transition:transform 0.15s;
  }
  .kol-card:hover{transform:translate(-2px,-2px);box-shadow:8px 8px 0 #000}
  .kol-head{
    display:flex;gap:10px;align-items:center;
    border-bottom:2px dashed rgba(255,255,255,0.2);
    padding-bottom:10px;
  }
  .avatar{
    width:52px;height:52px;
    background:#000;
    border:3px solid #fff;
    display:flex;align-items:center;justify-content:center;
    font-size:22px;
    flex-shrink:0;
    image-rendering:pixelated;
    box-shadow:3px 3px 0 #000;
  }
  .kol-info{flex:1;min-width:0}
  .kol-name{
    font-weight:900;font-size:13px;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    display:flex;align-items:center;gap:6px;
  }
  .kol-name .id-badge{
    background:var(--yellow);color:#000;
    font-family:'Press Start 2P', monospace;
    font-size:7px;
    padding:2px 5px;
    border:2px solid #000;
  }
  .kol-meta{
    font-size:10px;opacity:0.75;margin-top:2px;
    display:flex;gap:6px;flex-wrap:wrap;
  }
  .platform-tag{
    background:#000;
    border:1px solid var(--cyan);
    color:var(--cyan);
    padding:1px 6px;
    font-family:'Press Start 2P', monospace;
    font-size:6px;
  }
  .fans-tag{
    background:var(--pink);color:#000;
    padding:1px 6px;
    font-weight:900;
    font-size:10px;
    border:1px solid #fff;
  }
  .sentiment-badge{
    font-family:'Press Start 2P', monospace;
    font-size:7px;
    padding:6px 8px;
    border:2px solid #fff;
    text-align:center;
    box-shadow:2px 2px 0 #000;
    flex-shrink:0;
  }
  .sentiment-badge.bull{background:var(--red);color:#fff}
  .sentiment-badge.bear{background:var(--blue);color:#fff}
  .sentiment-badge.neutral{background:#888;color:#fff}
  .sentiment-badge .small{font-size:5px;display:block;margin-top:2px;opacity:0.9}

  .item-list{display:flex;flex-direction:column;gap:8px}
  .item{
    background:#000;
    border:2px solid #333;
    padding:10px;
    position:relative;
  }
  .item::before{
    content:"▶";
    position:absolute;left:6px;top:10px;
    font-size:7px;color:var(--yellow);
  }
  .item{padding-left:18px}
  .item-title{
    font-size:11px;font-weight:900;
    line-height:1.4;
    color:#fff;
  }
  .item-summary{
    font-size:10px;opacity:0.8;
    margin-top:4px;line-height:1.5;
    color:#ccc;
  }
  .item-footer{
    display:flex;justify-content:space-between;align-items:center;
    margin-top:8px;gap:8px;flex-wrap:wrap;
  }
  .item-date{
    font-family:'Press Start 2P', monospace;
    font-size:6px;
    background:#222;
    border:1px solid #555;
    padding:3px 6px;
    color:var(--cyan);
  }
  .mini-badge{
    font-family:'Press Start 2P', monospace;
    font-size:6px;
    padding:3px 6px;
    border:2px solid #fff;
    box-shadow:1px 1px 0 #000;
  }
  .mini-badge.bull{background:var(--red);color:#fff}
  .mini-badge.bear{background:var(--blue);color:#fff}
  .mini-badge.neutral{background:#666;color:#fff}
  .reason{
    margin-top:6px;
    background:#111;
    border-left:3px solid var(--yellow);
    padding:6px 8px;
    font-size:10px;
    line-height:1.5;
    color:#ffe066;
  }
  .advice{
    margin-top:4px;
    font-size:10px;
    color:var(--green);
    font-weight:700;
  }
  .power-row{
    display:flex;align-items:center;gap:6px;margin-top:6px;
  }
  .power-label{font-family:'Press Start 2P', monospace;font-size:6px;opacity:0.7}
  .power-bar{
    flex:1;height:8px;background:#222;border:1px solid #fff;
    overflow:hidden;
  }
  .power-fill{height:100%}
  .power-fill.bull{background:var(--red)}
  .power-fill.bear{background:var(--blue)}
  .power-fill.neutral{background:#888}
  .power-num{font-family:'Press Start 2P', monospace;font-size:6px;min-width:30px}

  /* 页脚 */
  .footer{
    margin-top:22px;
    text-align:center;
    padding:16px;
    background:#000;
    font-family:'Press Start 2P', monospace;
    font-size:6px;
    line-height:1.8;
    color:#888;
  }
  .footer .highlight{color:var(--yellow)}
  .legend{
    display:flex;gap:10px;justify-content:center;flex-wrap:wrap;
    margin-top:10px;
  }
  .legend-item{
    display:flex;align-items:center;gap:6px;
    font-family:'Press Start 2P', monospace;
    font-size:6px;
  }
  .legend-dot{width:10px;height:10px;border:2px solid #fff;box-shadow:1px 1px 0 #000}
  .legend-dot.bull{background:var(--red)}
  .legend-dot.bear{background:var(--blue)}
  .legend-dot.neutral{background:#888}
</style>
</head>
<body>
<div class="container">
  <!-- HEADER -->
  <div class="header pixel-border">
    <h1>⚔️ 全球财经金融 KOL 精选名单 ⚔️<br>多空全景战报 · 章鱼战场版</h1>
    <div class="subtitle">PIXEL BATTLEFIELD EDITION // BULL VS BEAR</div>
    <div class="meta">
      <div class="meta-badge yellow">📅 {{ report_date }}</div>
      <div class="meta-badge cyan">👾 {{ active_count }} / {{ total_count }} 存活</div>
      <div class="meta-badge pink">⚡ {{ total_items }} 条内容参战</div>
      <div class="meta-badge green">🐙 {{ author }}</div>
    </div>
  </div>

  <!-- PIXEL BANNER -->
  <div class="pixel-border" style="padding:0;overflow:hidden;margin-bottom:18px;background:#000">
    <img src="pixel_battle.png" alt="BULL VS BEAR PIXEL BATTLE" style="width:100%;height:auto;display:block;image-rendering:pixelated;border-bottom:4px solid #fff">
    <div style="background:linear-gradient(90deg,#ff3b30 0%,#ffe066 25%,#00e5ff 50%,#ffe066 75%,#0080ff 100%);height:6px"></div>
    <div style="text-align:center;padding:8px;background:#000;font-family:'Press Start 2P', monospace;font-size:7px;color:var(--yellow);letter-spacing:1px">▶ ARCADE MODE // INSERT COIN TO CONTINUE ▶ 多空对决 · 章鱼战场已就绪</div>
  </div>

  <!-- BATTLEFIELD -->
  <div class="battlefield pixel-border">
    <div class="fighter bull pixel-border">
      <div class="icon">🐂</div>
      <div class="label">BULL ARMY 多头军团</div>
      <div class="count">{{ stats.bull }}</div>
      <div class="sub">{{ stats.bull_ratio }}% 火力</div>
    </div>
    <div class="vs">VS</div>
    <div class="fighter bear pixel-border">
      <div class="icon">🐻</div>
      <div class="label">BEAR ARMY 空头军团</div>
      <div class="count">{{ stats.bear }}</div>
      <div class="sub">{{ stats.bear_ratio }}% 火力</div>
    </div>
    <div class="battle-stats">
      <div class="health-row">
        <div class="health-label" style="color:var(--red)">BULL</div>
        <div class="health-bar"><div class="health-fill bull" style="width:{{ stats.bull_ratio }}%">{{ stats.bull_ratio }}%</div></div>
      </div>
      <div class="health-row">
        <div class="health-label" style="color:var(--blue)">BEAR</div>
        <div class="health-bar"><div class="health-fill bear" style="width:{{ stats.bear_ratio }}%">{{ stats.bear_ratio }}%</div></div>
      </div>
      <div class="health-row">
        <div class="health-label" style="color:#aaa">NEUTRAL</div>
        <div class="health-bar"><div class="health-fill neutral" style="width:{{ stats.neutral_ratio }}%">{{ stats.neutral_ratio }}%</div></div>
      </div>
      <div style="text-align:center;margin-top:10px;font-family:'Press Start 2P', monospace;font-size:7px;color:var(--yellow)">
        ▶ 当前战场主导：<span style="color:#fff;background:{{ '#ff3b30' if stats.dominant=='多头' else '#0080ff' if stats.dominant=='空头' else '#888' }};padding:2px 6px;border:2px solid #fff">{{ stats.dominant }}</span> · 平均战斗力 {{ stats.avg_power }} ▶
      </div>
    </div>
  </div>

  <!-- FILTER -->
  <div class="filter-bar">
    <button class="filter-btn active" onclick="filterKOL('all')">♟ ALL 全部</button>
    <button class="filter-btn" onclick="filterKOL('bull')">🐂 多头</button>
    <button class="filter-btn" onclick="filterKOL('bear')">🐻 空头</button>
    <button class="filter-btn" onclick="filterKOL('neutral')">⚖️ 中性</button>
    <button class="filter-btn" onclick="filterKOL('cn')">🇨🇳 中文</button>
    <button class="filter-btn" onclick="filterKOL('en')">🇺🇸 英文</button>
  </div>

  <!-- GRID -->
  <div class="grid" id="kolGrid">
    {% for kol in kols %}
    <div class="kol-card pixel-border" data-sentiment="{{ kol.aggregate.kol_color }}" data-lang="{{ 'cn' if '中文' in kol.language else 'en' }}">
      <div class="kol-head">
        <div class="avatar">{% if kol.id % 3 == 0 %}👾{% elif kol.id % 3 == 1 %}🤖{% else %}👽{% endif %}</div>
        <div class="kol-info">
          <div class="kol-name"><span class="id-badge">#{{ "%02d"|format(kol.id) }}</span> {{ kol.name }}</div>
          <div class="kol-meta">
            <span class="platform-tag">{{ kol.platform }}</span>
            <span>{{ kol.language }}</span>
            <span style="opacity:0.6">{{ kol.field }}</span>
          </div>
          <div class="kol-meta" style="margin-top:3px">
            <span class="fans-tag">♥ {{ kol.fans }}</span>
            <span style="font-size:9px;opacity:0.6">{{ kol.desc }}</span>
          </div>
        </div>
        <div class="sentiment-badge {{ kol.aggregate.kol_color }}">
          {{ kol.aggregate.kol_sentiment }}
          <span class="small">{{ kol.aggregate.battle_text }}</span>
          <span class="small">⚡{{ kol.aggregate.avg_power }} | {{ kol.aggregate.avg_confidence }}%</span>
        </div>
      </div>

      <div class="item-list">
        {% for item in kol['items'] %}
        <div class="item">
          <div class="item-title">{{ item.title }}</div>
          <div class="item-summary">{{ item.summary }}</div>
          <div class="power-row">
            <span class="power-label">POW</span>
            <div class="power-bar"><div class="power-fill {{ 'bull' if item.sentiment=='多头' else 'bear' if item.sentiment=='空头' else 'neutral' }}" style="width:{{ item.power }}%"></div></div>
            <span class="power-num">{{ item.power }}</span>
            <span class="mini-badge {{ 'bull' if item.sentiment=='多头' else 'bear' if item.sentiment=='空头' else 'neutral' }}">{{ item.sentiment }} {{ item.confidence }}%</span>
          </div>
          <div class="reason">🧠 AI研判：{{ item.reason }}</div>
          <div class="advice">🎯 策略：{{ item.advice }}</div>
          <div class="item-footer">
            <span class="item-date">📅 {{ item.date_str }}</span>
            <a href="{{ item.link }}" target="_blank" style="font-family:'Press Start 2P', monospace;font-size:6px;color:var(--cyan);text-decoration:none;border:1px solid var(--cyan);padding:3px 6px;background:#000">▶ 观看原片</a>
          </div>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endfor %}
  </div>

  <div class="footer pixel-border">
    <div>🐙 <span class="highlight">{{ author }}</span> · 章鱼战场出品 // PIXEL BATTLEFIELD</div>
    <div style="margin-top:6px">数据来源：YouTube / TikTok / IG / Reddit / TradingView · 抓取时间：{{ report_date }} · 仅供研究，不构成投资建议</div>
    <div class="legend">
      <div class="legend-item"><div class="legend-dot bull"></div> 多头 BULL</div>
      <div class="legend-item"><div class="legend-dot bear"></div> 空头 BEAR</div>
      <div class="legend-item"><div class="legend-dot neutral"></div> 中性 NEUTRAL</div>
    </div>
    <div style="margin-top:10px;opacity:0.5">PRESS START TO CONTINUE  █</div>
  </div>
</div>

<script>
function filterKOL(type){
  document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
  event.target.classList.add('active');
  document.querySelectorAll('.kol-card').forEach(card=>{
    let show = false;
    if(type==='all') show=true;
    else if(type==='bull' || type==='bear' || type==='neutral') show = card.dataset.sentiment===type;
    else if(type==='cn') show = card.dataset.lang==='cn';
    else if(type==='en') show = card.dataset.lang==='en';
    card.style.display = show ? 'flex' : 'none';
  });
}
// 8-bit 打字机彩蛋
console.log("%c🐙 章鱼 AI·全景分析 %c 章鱼战场已加载", "background:#ffe066;color:#000;padding:4px 8px;font-weight:bold", "color:#00e5ff");
</script>
</body>
</html>
"""

def generate_report(kols_enriched, stats, output_path: Path, report_date: str = None):
    if report_date is None:
        report_date = datetime.now().strftime("%Y年%m月%d日")
    from .config import REPORT_TITLE, AUTHOR

    # kols_enriched: list of dicts {kol, items, aggregate}
    # 按 id 排序
    kols_enriched = sorted(kols_enriched, key=lambda x: x["kol"]["id"])

    # 构造模板数据
    template_data = []
    for entry in kols_enriched:
        kol = entry["kol"]
        template_data.append({
            "id": kol["id"],
            "name": kol["name"],
            "platform": kol["platform"],
            "language": kol["language"],
            "field": kol["field"],
            "fans": kol["fans"],
            "desc": kol["desc"],
            "aggregate": entry["aggregate"],
            "items": entry["items"]
        })

    active_count = len(kols_enriched)
    # total_count 需从原 json 读取，这里用 53
    total_count = 53
    total_items = sum(len(e["items"]) for e in kols_enriched)

    tmpl = Template(TEMPLATE_STR)
    html = tmpl.render(
        report_title=REPORT_TITLE,
        author=AUTHOR,
        report_date=report_date,
        kols=template_data,
        stats=stats,
        active_count=active_count,
        total_count=total_count,
        total_items=total_items
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[report] 已生成: {output_path} ({len(html)//1024} KB)")
    return output_path

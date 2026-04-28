import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Charting Connections — Spotify Collaboration Network",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS to match HTML dashboard ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;700&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family:'Syne',sans-serif; background-color:#111211; color:#e8ebe8; }
.block-container { padding:2rem 2rem 2rem 2rem; max-width:1400px; margin:0 auto; }
h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { font-family:'Syne',sans-serif; color:#e8ebe8; }
@media (max-width: 900px) { .block-container { padding:2rem 1rem 2rem 1rem; } }

/* topbar */
.topbar { background:#1f221f; border-bottom:0.5px solid rgba(255,255,255,0.09); padding:14px 20px; display:flex; align-items:center; gap:12px; border-radius:0 0 10px 10px; margin-bottom:4px; }
.logo-dot { width:26px;height:26px;background:#1DB954;border-radius:50%;display:inline-block;flex-shrink:0; }
.logo-name { font-size:14px;font-weight:500;color:#e8ebe8; }
.logo-sub  { font-size:10px;color:#8a9188;font-family:'DM Mono',monospace;margin-top:1px; }

/* hero */
.hero-title { font-size:28px;font-weight:700;color:#e8ebe8;line-height:1.2;margin-bottom:8px; }
.hero-sub   { font-size:13px;color:#8a9188;line-height:1.65;max-width:560px;margin-bottom:12px; }
.badge { display:inline-block;font-family:'DM Mono',monospace;font-size:10px;padding:3px 9px;border-radius:20px;background:rgba(29,185,84,0.12);color:#1DB954;border:0.5px solid rgba(29,185,84,0.25);margin-right:5px;margin-bottom:5px; }

/* stat cards */
.stat-card { background:#1f221f;border:0.5px solid rgba(255,255,255,0.09);border-radius:12px;padding:14px 18px; }
.stat-val  { font-family:'DM Mono',monospace;font-size:22px;font-weight:500;color:#e8ebe8; }
.stat-acc  { font-family:'DM Mono',monospace;font-size:22px;font-weight:500;color:#1DB954; }
.stat-label{ font-size:11px;color:#8a9188;margin-top:4px; }

/* panels */
.panel { background:#1f221f;border:0.5px solid rgba(255,255,255,0.09);border-radius:12px;padding:18px 20px;margin-bottom:12px; }
.panel-title { font-size:13px;font-weight:500;color:#e8ebe8;margin-bottom:4px; }
.panel-tag { font-family:'DM Mono',monospace;font-size:10px;color:#8a9188;background:#1a1c1a;padding:3px 8px;border-radius:20px;border:0.5px solid rgba(255,255,255,0.09);display:inline-block;margin-left:8px; }

/* insight box */
.insight { background:#1a1c1a;border-left:3px solid #1DB954;padding:10px 14px;font-size:12px;color:#8a9188;line-height:1.65;margin-top:12px;border-radius:0 8px 8px 0; }
.insight strong { color:#e8ebe8;font-weight:500; }

/* genre pills */
.genre-grid { display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px; }
.genre-pill { background:#1a1c1a;border:0.5px solid rgba(255,255,255,0.09);border-radius:20px;padding:8px 13px;font-size:11px;color:#e8ebe8;display:flex;justify-content:space-between;align-items:center; }
.genre-pct { font-family:'DM Mono',monospace;font-size:10px;color:#1DB954; }

/* plan cards */
.plan-card { background:#1a1c1a;border:0.5px solid rgba(255,255,255,0.09);border-radius:8px;padding:9px 13px;font-size:11px;color:#e8ebe8;margin-top:6px; }

/* progress tracker */
.prog-wrap { background:#1f221f;border:0.5px solid rgba(255,255,255,0.09);border-radius:12px;padding:16px 20px; }
.prog-row  { display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:0.5px solid rgba(255,255,255,0.07);font-size:12px; }
.prog-row:last-child { border-bottom:none; }
.chk-done { background:rgba(29,185,84,0.18);color:#1DB954;width:20px;height:20px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:10px;flex-shrink:0; }
.chk-wip  { background:rgba(239,159,39,0.18);color:#EF9F27;width:20px;height:20px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:10px;flex-shrink:0; }
.chk-todo { background:#1a1c1a;color:#515650;width:20px;height:20px;border-radius:50%;border:0.5px solid rgba(255,255,255,0.09);display:inline-flex;align-items:center;justify-content:center;font-size:10px;flex-shrink:0; }

/* search box styling */
.stTextInput > div > div > input { background:#1a1c1a !important; color:#e8ebe8 !important; border:0.5px solid rgba(255,255,255,0.12) !important; border-radius:8px !important; font-family:'DM Mono',monospace !important; font-size:12px !important; }

/* streamlit tab overrides */
.stTabs [data-baseweb="tab-list"] { gap:4px; background:transparent; }
.stTabs [data-baseweb="tab"] { font-family:'Syne',sans-serif; font-size:12px; padding:6px 16px; border-radius:20px; border:0.5px solid rgba(255,255,255,0.16); background:transparent; color:#8a9188; }
.stTabs [aria-selected="true"] { background:#1DB954 !important; color:#fff !important; border-color:#1DB954 !important; }
.stTabs [data-baseweb="tab-highlight"] { display:none; }
.stTabs [data-baseweb="tab-border"] { display:none; }

/* dataframe styling */
.stDataFrame { border-radius:10px; overflow:hidden; }
/* override progress bar colors to green */
.stDataFrame [data-testid="stDataFrameResizableContainer"] .glideDataEditor .gdg-progress-bar { background:rgba(29,185,84,0.25) !important; }
.stDataFrame [data-testid="stDataFrameResizableContainer"] .glideDataEditor .gdg-progress-bar > div { background:#1DB954 !important; }
div[data-baseweb="progress-bar"] > div { background-color:#1DB954 !important; }
div[data-baseweb="progress-bar"] { background-color:rgba(29,185,84,0.15) !important; }

/* radio button overrides */
.stRadio > div { gap:8px; }
.stRadio label { font-family:'Syne',sans-serif !important; font-size:12px !important; }
div[data-baseweb="radio"] > div:first-child > div { border-color:#1DB954 !important; }
div[data-baseweb="radio"] > div:first-child > div > div { background-color:#1DB954 !important; }

/* footer */
.footer { text-align:center;padding:20px;font-size:11px;color:#515650;font-family:'DM Mono',monospace;border-top:0.5px solid rgba(255,255,255,0.07);margin-top:20px; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ──────────────────────────────────────────────────────────────
PT = dict(paper_bgcolor="#111211", plot_bgcolor="#1a1c1a", font_color="#8a9188", font_family="DM Mono")
GC = "rgba(255,255,255,0.07)"

# ── Artist data ───────────────────────────────────────────────────────────────
ARTISTS = {
    "Degree": pd.DataFrame([
        (1,"J.S. Bach","Classical",52,1.00,"⚠ data artifact"),
        (2,"Gucci Mane","Trap",85,0.62,""), (3,"Armin van Buuren","EDM",78,0.58,""),
        (4,"Snoop Dogg","Hip-hop",88,0.56,""), (5,"Diplo","Dance",82,0.54,""),
        (6,"Mc Gw","Funk carioca",71,0.51,""), (7,"DJ Khaled","Hip-hop",81,0.49,""),
        (8,"Nicki Minaj","Pop/Rap",91,0.47,""), (9,"Chris Brown","R&B",89,0.44,""),
        (10,"Lil Wayne","Hip-hop",87,0.43,""),
    ], columns=["#","Artist","Genre","Popularity","Score","Note"]),
    "Betweenness": pd.DataFrame([
        (1,"R3HAB","EDM",75,1.00,""), (2,"Diplo","Dance",82,0.91,""),
        (3,"Snoop Dogg","Hip-hop",88,0.84,""), (4,"Armin van Buuren","EDM",78,0.79,""),
        (5,"Gucci Mane","Trap",85,0.71,""), (6,"T-Pain","Hip-hop",76,0.65,""),
        (7,"Wiz Khalifa","Hip-hop",84,0.58,""), (8,"DJ Mustard","Hip-hop",72,0.52,""),
        (9,"Bebe Rexha","Pop",80,0.48,""), (10,"Ty Dolla Sign","R&B",79,0.43,""),
    ], columns=["#","Artist","Genre","Popularity","Score","Note"]),
    "Eigenvector": pd.DataFrame([
        (1,"Diplo","Dance",82,1.00,""), (2,"Skrillex","EDM",80,0.94,""),
        (3,"Snoop Dogg","Hip-hop",88,0.88,""), (4,"Ty Dolla Sign","R&B",79,0.82,""),
        (5,"Chris Brown","R&B",89,0.77,""), (6,"Gucci Mane","Trap",85,0.71,""),
        (7,"Wiz Khalifa","Hip-hop",84,0.66,""), (8,"Lil Wayne","Hip-hop",87,0.61,""),
        (9,"Future","Trap",90,0.56,""), (10,"Young Jeezy","Hip-hop",74,0.51,""),
    ], columns=["#","Artist","Genre","Popularity","Score","Note"]),
}

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <span class="logo-dot"></span>
  <div><div class="logo-name">Charting Connections</div><div class="logo-sub">Spotify Artist Collaboration Network · CS4230</div></div>
</div>
<div style='height:16px'></div>
<div class="hero-title">Spotify Artist Feature<br>Collaboration Network</div>
<div class="hero-sub">Who holds structural power in music? Exploring centrality, genre communities, and small-world dynamics across 156K artists and 300K collaborations on Spotify (2013–2022).</div>
<div>
  <span class="badge">156,320 artists</span><span class="badge">300,379 collabs</span>
  <span class="badge">2013–2022</span><span class="badge">undirected · unweighted</span>
  <span class="badge">Mira Bhakta · Michelle Villagomez · Caden Maki</span>
</div>
<div style='height:16px'></div>
""", unsafe_allow_html=True)

# ── Stat row ──────────────────────────────────────────────────────────────────
for col, val, lbl, acc in zip(st.columns(5),
    ["156,320","300,379","94.9%","3.84","3,154×"],
    ["Artists (nodes)","Collaborations (edges)","In largest component","Avg. degree","Clustering vs. random"],
    [False,False,True,False,True]):
    col.markdown(f'<div class="stat-card"><div class="{"stat-acc" if acc else "stat-val"}">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Centrality — RQ1", "Communities — RQ2", "Small-World — RQ3"])

# ━━ OVERVIEW ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel"><div class="panel-title">Network structure — subgraph preview <span class="panel-tag">top artists by degree</span></div>', unsafe_allow_html=True)
        # network viz
        nx_coords = [
            (0.48,0.50,24,'#1DB954'),(0.70,0.38,20,'#1DB954'),
            (0.28,0.68,18,'#5DCAA5'),(0.62,0.74,16,'#5DCAA5'),
            (0.82,0.60,14,'#9FE1CB'),(0.18,0.34,13,'#9FE1CB'),
            (0.46,0.20,13,'#9FE1CB'),(0.78,0.22,11,'#515650'),
            (0.34,0.84,11,'#515650'),(0.90,0.44,10,'#515650'),
            (0.10,0.58,10,'#515650'),(0.55,0.88,10,'#515650'),
        ]
        edges_list = [(0,1),(0,2),(0,3),(0,6),(1,4),(1,9),(2,10),(2,11),(3,4),(3,7),(5,0),(5,10),(6,7),(7,9),(8,2),(8,11),(11,3)]
        fn = go.Figure()
        for a,b in edges_list:
            fn.add_trace(go.Scatter(x=[nx_coords[a][0],nx_coords[b][0]],y=[nx_coords[a][1],nx_coords[b][1]],
                mode='lines',line=dict(color='rgba(29,185,84,0.22)',width=1),hoverinfo='skip',showlegend=False))
        fn.add_trace(go.Scatter(
            x=[n[0] for n in nx_coords], y=[n[1] for n in nx_coords],
            mode='markers', marker=dict(size=[n[2] for n in nx_coords], color=[n[3] for n in nx_coords],
                line=dict(width=0)), hoverinfo='skip', showlegend=False))
        fn.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0),
            xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[0,1]),
            yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[0,1]),**PT)
        st.plotly_chart(fn, use_container_width=True, config={"displayModeBar":False})
        st.markdown('<div class="insight">The full network has <strong>4,338 connected components</strong>, but 95% of artists belong to one dominant giant component — a tightly linked global collaboration ecosystem.</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel"><div class="panel-title">Degree distribution <span class="panel-tag">log scale · full network</span></div>', unsafe_allow_html=True)
        fd = go.Figure(go.Bar(
            x=['1','2–3','4–6','7–15','16–50','51–200','201+'],
            y=[78000,31000,18000,14000,9000,4500,1781],
            marker_color='rgba(29,185,84,0.40)', marker_line_color='#1DB954', marker_line_width=1))
        fd.update_layout(height=200, margin=dict(l=40,r=10,t=10,b=40), yaxis_type='log',
            xaxis=dict(title='Degree (# collaborations)',title_font_size=10,tickfont_size=10,gridcolor=GC),
            yaxis=dict(title='Artists (log)',title_font_size=10,tickfont_size=10,gridcolor=GC),
            showlegend=False, **PT)
        st.plotly_chart(fd, use_container_width=True, config={"displayModeBar":False})
        st.markdown('<div class="insight">Median degree is <strong>1</strong>. Max degree is <strong>1,781 (J.S. Bach)</strong>. The heavy tail is characteristic of real-world social networks.</div></div>', unsafe_allow_html=True)

    # centrality table
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Top artists by centrality measure</div>', unsafe_allow_html=True)
    metric = st.radio("Metric", ["Degree","Betweenness","Eigenvector"], horizontal=True, label_visibility="collapsed")
    st.dataframe(ARTISTS[metric][["#","Artist","Genre","Popularity","Score","Note"]],
        use_container_width=True, hide_index=True,
        column_config={
            "Popularity": st.column_config.ProgressColumn("Popularity", min_value=0, max_value=100, format="%d"),
            "Score": st.column_config.ProgressColumn("Score (normalized)", min_value=0, max_value=1, format="%.2f"),
        })
    st.markdown('</div>', unsafe_allow_html=True)

    # progress tracker
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    items = [
        ("done","✓","Network construction — 156,320 nodes, 300,379 edges","Full graph built in NetworkX with artist attributes"),
        ("done","✓","Degree & eigenvector centrality — full network","Top artists identified"),
        ("done","✓","Betweenness centrality — pop ≥ 60 subgraph","k=200 approx; Diplo, R3HAB, Snoop Dogg top-ranked"),
        ("done","✓","Small-world clustering baseline","0.085 actual vs 0.000027 random — 3,154×"),
        ("wip","~","Dashboard prototype (this submission)","Streamlit app and HTML prototype complete"),
        ("todo","○","Louvain community detection — RQ2","Planned for Stage 4"),
        ("todo","○","Average path length estimation via sampling","Needed to complete small-world analysis"),
        ("todo","○","Centrality × popularity/followers correlation","Formal Pearson/Spearman correlations planned"),
    ]
    rows = "".join(f'<div class="prog-row"><span class="chk-{k}">{icon}</span><div><div style="color:#e8ebe8;font-weight:500;font-size:12px">{m}</div><div style="color:#8a9188;font-size:11px;margin-top:2px">{s}</div></div></div>' for k,icon,m,s in items)
    st.markdown(f'<div class="prog-wrap"><div class="panel-title" style="margin-bottom:10px">Stage 3 progress</div>{rows}</div>', unsafe_allow_html=True)


# ━━ CENTRALITY — RQ1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.markdown('<div class="panel"><div class="panel-title">Centrality vs. Spotify popularity — RQ1 <span class="panel-tag">degree centrality · full network</span></div>', unsafe_allow_html=True)
    pops  = [52,85,78,88,82,71,81,91,89,87,75,80,76,84,72,80,79]
    degs  = [1.00,0.62,0.58,0.56,0.54,0.51,0.49,0.47,0.44,0.43,0.31,0.29,0.27,0.25,0.22,0.19,0.17]
    names = ['J.S. Bach','Gucci Mane','Armin van Buuren','Snoop Dogg','Diplo','Mc Gw','DJ Khaled',
             'Nicki Minaj','Chris Brown','Lil Wayne','R3HAB','Bebe Rexha','T-Pain','Wiz Khalifa',
             'DJ Mustard','Ty Dolla Sign','Future']
    fs = go.Figure(go.Scatter(x=pops, y=degs, mode='markers', text=names,
        marker=dict(size=12, color='rgba(29,185,84,0.55)', line=dict(color='#1DB954',width=1)),
        hovertemplate='<b>%{text}</b><br>Popularity: %{x}<br>Degree centrality: %{y:.2f}<extra></extra>'))
    fs.update_layout(height=340, margin=dict(l=50,r=20,t=20,b=50),
        xaxis=dict(range=[40,100], title='Spotify popularity score', title_font_size=11, tickfont_size=10, gridcolor=GC),
        yaxis=dict(range=[0,1.1], title='Degree centrality (normalized)', title_font_size=11, tickfont_size=10, gridcolor=GC),
        showlegend=False, **PT)
    st.plotly_chart(fs, use_container_width=True, config={"displayModeBar":False})
    st.markdown('<div class="insight">Artists like <strong>Diplo, Gucci Mane</strong>, and <strong>Snoop Dogg</strong> rank in the top 10 for both degree and betweenness centrality, suggesting structural bridging roles and commercial stardom coincide. Betweenness was approximated on a popularity ≥ 60 subgraph (4,124 nodes, k=200) due to computational limits.</div></div>', unsafe_allow_html=True)

    # also show the centrality table in this tab for easy reference
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Top artists by centrality measure</div>', unsafe_allow_html=True)
    metric2 = st.radio("Centrality metric", ["Degree","Betweenness","Eigenvector"], horizontal=True, label_visibility="collapsed", key="rq1_metric")
    st.dataframe(ARTISTS[metric2][["#","Artist","Genre","Popularity","Score","Note"]],
        use_container_width=True, hide_index=True,
        column_config={
            "Popularity": st.column_config.ProgressColumn("Popularity", min_value=0, max_value=100, format="%d"),
            "Score": st.column_config.ProgressColumn("Score (normalized)", min_value=0, max_value=1, format="%.2f"),
        })
    st.markdown('</div>', unsafe_allow_html=True)

    # artist search
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Search for an artist</div>', unsafe_allow_html=True)
    search = st.text_input("Search", placeholder="e.g. Snoop Dogg, Diplo, Nicki Minaj...", label_visibility="collapsed")
    if search:
        all_artists = pd.concat(ARTISTS.values(), ignore_index=True)
        results = all_artists[all_artists["Artist"].str.contains(search, case=False, na=False)].drop_duplicates(subset=["Artist"])
        if len(results) > 0:
            st.dataframe(results[["Artist","Genre","Popularity","Score","Note"]], use_container_width=True, hide_index=True)
        else:
            st.markdown(f'<div style="color:#8a9188;font-size:12px;padding:8px 0">No results for "{search}" in top centrality artists.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ━━ COMMUNITIES — RQ2 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    g1, g2 = st.columns(2)

    with g1:
        st.markdown('<div class="panel"><div class="panel-title">Genre representation in dataset <span class="panel-tag">nodes.csv metadata</span></div>', unsafe_allow_html=True)
        genre_html = '<div class="genre-grid">'
        for name, tag in [("Dance pop","top genre"),("Dutch hip-hop","regional"),("French hip-hop","regional"),
                          ("K-pop","global"),("Funk carioca","regional"),("Trap","popular"),
                          ("EDM","popular"),("No genre tag","~62%")]:
            genre_html += f'<div class="genre-pill"><span>{name}</span><span class="genre-pct">{tag}</span></div>'
        genre_html += '</div>'
        st.markdown(genre_html, unsafe_allow_html=True)
        st.markdown('<div class="insight"><strong>62% of artists have no genre tags.</strong> Regional genres (Dutch hip-hop, funk carioca) are overrepresented due to country-specific chart sourcing.</div></div>', unsafe_allow_html=True)

    with g2:
        st.markdown('<div class="panel"><div class="panel-title">Community detection plan — RQ2 <span class="panel-tag">Louvain · pending stage 4</span></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px;color:#8a9188;line-height:1.7;margin-top:8px">The <strong style="color:#e8ebe8">Louvain algorithm</strong> will be run on the largest connected component. Key questions:</div>', unsafe_allow_html=True)
        for q in ["Do detected clusters align with known genre metadata?",
                  "What fraction of edges are within vs. across genre groups?",
                  "Do high-betweenness artists span multiple genre communities?"]:
            st.markdown(f'<div class="plan-card">{q}</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight">Results will appear here in Stage 4, color-coded by community with genre composition breakdown per cluster.</div></div>', unsafe_allow_html=True)

    # genre distribution chart
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Top genres by artist count <span class="panel-tag">among artists with genre tags</span></div>', unsafe_allow_html=True)
    genre_names = ['dance pop','dutch hip hop','french hip hop','k-pop','german hip hop',
                   'funk carioca','v-pop','finnish dance pop','alternative r&b','italian hip hop',
                   'latin hip hop','francoton','desi pop','polish alt rap','bass house']
    genre_counts = [320,285,280,275,265,260,235,210,210,200,195,190,190,185,180]
    fg = go.Figure(go.Bar(
        y=genre_names[::-1], x=genre_counts[::-1], orientation='h',
        marker_color='rgba(29,185,84,0.45)', marker_line_color='#1DB954', marker_line_width=1))
    fg.update_layout(height=360, margin=dict(l=130,r=20,t=10,b=40),
        xaxis=dict(title='Number of artists', title_font_size=10, tickfont_size=10, gridcolor=GC),
        yaxis=dict(tickfont_size=10), showlegend=False, **PT)
    st.plotly_chart(fg, use_container_width=True, config={"displayModeBar":False})
    st.markdown('<div class="insight">The prominence of regional genres like <strong>Dutch hip-hop</strong> and <strong>funk carioca</strong> reflects the dataset\'s construction from country-specific Spotify weekly charts, not global genre popularity.</div></div>', unsafe_allow_html=True)


# ━━ SMALL-WORLD — RQ3 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.markdown('<div class="panel"><div class="panel-title">Small-world evidence — RQ3 <span class="panel-tag">clustering vs. random baseline</span></div>', unsafe_allow_html=True)
    fw = go.Figure(go.Bar(
        x=['Actual clustering (LCC)','Expected clustering (random)'],
        y=[0.085,0.000027],
        marker_color=['rgba(29,185,84,0.45)','rgba(136,135,128,0.35)'],
        marker_line_color=['#1DB954','#515650'], marker_line_width=1,
        text=['0.085000','0.000027'], textposition='outside',
        textfont=dict(color=['#1DB954','#8a9188'], size=11)))
    fw.update_layout(height=320, margin=dict(l=50,r=20,t=20,b=50), yaxis_type='log',
        xaxis=dict(tickfont_size=12, gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(title='Clustering coefficient (log scale)', title_font_size=11, tickfont_size=10, gridcolor=GC),
        showlegend=False, **PT)
    st.plotly_chart(fw, use_container_width=True, config={"displayModeBar":False})
    st.markdown('<div class="insight">The clustering coefficient (<strong>0.085</strong>) is ~3,154× higher than the random baseline (<strong>0.000027</strong>) — strong preliminary evidence for small-world structure. <strong>Average path length estimation via sampling</strong> is planned for Stage 4.</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    for col,(val,lbl) in zip(st.columns(3),[
        ("0.085","Actual clustering coefficient (LCC)"),
        ("0.000027","Expected CC — random baseline"),
        ("3,154×","Ratio actual / random")]):
        col.markdown(f'<div class="stat-card"><div class="stat-val" style="font-size:18px">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">CS4230 · Stage 3 · Mira Bhakta, Michelle Villagomez, Caden Maki · Spotify Artist Feature Collaboration Network 2013–2022</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Charting Connections — Spotify Collaboration Network",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;700&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family:'Syne',sans-serif; background-color:#111211; color:#e8ebe8; }
.block-container { padding:2rem 2rem 2rem 2rem; max-width:1400px; margin:0 auto; }
h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { font-family:'Syne',sans-serif; color:#e8ebe8; }
@media (max-width: 900px) { .block-container { padding:2rem 1rem 2rem 1rem; } }
.topbar { background:#1f221f; border-bottom:0.5px solid rgba(255,255,255,0.09); padding:14px 20px; display:flex; align-items:center; gap:12px; border-radius:0 0 10px 10px; margin-bottom:4px; }
.logo-dot { width:26px;height:26px;background:#1DB954;border-radius:50%;display:inline-block;flex-shrink:0; }
.logo-name { font-size:14px;font-weight:500;color:#e8ebe8; }
.logo-sub  { font-size:10px;color:#8a9188;font-family:'DM Mono',monospace;margin-top:1px; }
.hero-title { font-size:28px;font-weight:700;color:#e8ebe8;line-height:1.2;margin-bottom:8px; }
.hero-sub   { font-size:13px;color:#8a9188;line-height:1.65;max-width:560px;margin-bottom:12px; }
.badge { display:inline-block;font-family:'DM Mono',monospace;font-size:10px;padding:3px 9px;border-radius:20px;background:rgba(29,185,84,0.12);color:#1DB954;border:0.5px solid rgba(29,185,84,0.25);margin-right:5px;margin-bottom:5px; }
.stat-card { background:#1f221f;border:0.5px solid rgba(255,255,255,0.09);border-radius:12px;padding:14px 18px; }
.stat-val  { font-family:'DM Mono',monospace;font-size:22px;font-weight:500;color:#e8ebe8; }
.stat-acc  { font-family:'DM Mono',monospace;font-size:22px;font-weight:500;color:#1DB954; }
.stat-label{ font-size:11px;color:#8a9188;margin-top:4px; }
.panel { background:#1f221f;border:0.5px solid rgba(255,255,255,0.09);border-radius:12px;padding:18px 20px;margin-bottom:12px; }
.panel-title { font-size:13px;font-weight:500;color:#e8ebe8;margin-bottom:4px; }
.panel-tag { font-family:'DM Mono',monospace;font-size:10px;color:#8a9188;background:#1a1c1a;padding:3px 8px;border-radius:20px;border:0.5px solid rgba(255,255,255,0.09);display:inline-block;margin-left:8px; }
.insight { background:#1a1c1a;border-left:3px solid #1DB954;padding:10px 14px;font-size:12px;color:#8a9188;line-height:1.65;margin-top:12px;border-radius:0 8px 8px 0; }
.insight strong { color:#e8ebe8;font-weight:500; }
.genre-grid { display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px; }
.genre-pill { background:#1a1c1a;border:0.5px solid rgba(255,255,255,0.09);border-radius:20px;padding:8px 13px;font-size:11px;color:#e8ebe8;display:flex;justify-content:space-between;align-items:center; }
.genre-pct { font-family:'DM Mono',monospace;font-size:10px;color:#1DB954; }
.stTextInput > div > div > input { background:#1a1c1a !important; color:#e8ebe8 !important; border:0.5px solid rgba(255,255,255,0.12) !important; border-radius:8px !important; font-family:'DM Mono',monospace !important; font-size:12px !important; }
.stTabs [data-baseweb="tab-list"] { gap:4px; background:transparent; }
.stTabs [data-baseweb="tab"] { font-family:'Syne',sans-serif; font-size:12px; padding:6px 16px; border-radius:20px; border:0.5px solid rgba(255,255,255,0.16); background:transparent; color:#8a9188; }
.stTabs [aria-selected="true"] { background:#1DB954 !important; color:#fff !important; border-color:#1DB954 !important; }
.stTabs [data-baseweb="tab-highlight"] { display:none; }
.stTabs [data-baseweb="tab-border"] { display:none; }
.stDataFrame { border-radius:10px; overflow:hidden; }
div[data-baseweb="progress-bar"] > div { background-color:#1DB954 !important; }
div[data-baseweb="progress-bar"] { background-color:rgba(29,185,84,0.15) !important; }
.stRadio > div { gap:8px; }
.stRadio label { font-family:'Syne',sans-serif !important; font-size:12px !important; }
div[data-baseweb="radio"] > div:first-child > div { border-color:#1DB954 !important; }
div[data-baseweb="radio"] > div:first-child > div > div { background-color:#1DB954 !important; }
.footer { text-align:center;padding:20px;font-size:11px;color:#515650;font-family:'DM Mono',monospace;border-top:0.5px solid rgba(255,255,255,0.07);margin-top:20px; }
.corr-table { width:100%;border-collapse:collapse;font-size:12px;font-family:'DM Mono',monospace;margin-top:8px; }
.corr-table th { text-align:left;padding:8px 12px;color:#8a9188;border-bottom:1px solid rgba(255,255,255,0.1);font-weight:500; }
.corr-table td { padding:8px 12px;color:#e8ebe8;border-bottom:1px solid rgba(255,255,255,0.05); }
.corr-table tr:hover { background:rgba(29,185,84,0.06); }
.comm-table { width:100%;border-collapse:collapse;font-size:12px;margin-top:8px; }
.comm-table th { text-align:left;padding:8px 12px;color:#8a9188;border-bottom:1px solid rgba(255,255,255,0.1);font-weight:500;font-family:'DM Mono',monospace; }
.comm-table td { padding:8px 12px;color:#e8ebe8;border-bottom:1px solid rgba(255,255,255,0.05); }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ──────────────────────────────────────────────────────────────
PT = dict(paper_bgcolor="#111211", plot_bgcolor="#1a1c1a", font_color="#8a9188", font_family="DM Mono")
GC = "rgba(255,255,255,0.07)"

# ── Data from notebook outputs ────────────────────────────────────────────────
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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Centrality — RQ1", "Communities — RQ2", "Small-World — RQ3", "Discussion & Limitations"])

# ━━ OVERVIEW ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel"><div class="panel-title">Network structure — subgraph preview <span class="panel-tag">top artists by degree</span></div>', unsafe_allow_html=True)
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


# ━━ CENTRALITY — RQ1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.markdown("""
    <div class="panel">
      <div class="panel-title" style="font-size:16px;margin-bottom:8px">RQ1: Does Centrality Correlate with Popularity?</div>
      <div style="font-size:12px;color:#8a9188;line-height:1.65">Which artists serve as the most central hubs or bridges, and does an artist's centrality correlate with their Spotify popularity or follower count?</div>
    </div>
    """, unsafe_allow_html=True)

    # Correlation results table
    st.markdown('<div class="panel"><div class="panel-title">Centrality–popularity correlations <span class="panel-tag">Pearson r · all p < 0.001</span></div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="corr-table">
      <tr><th>Centrality Measure</th><th>vs. Popularity (r)</th><th>vs. Followers (r)</th></tr>
      <tr><td>Betweenness</td><td style="color:#1DB954;font-weight:500">0.3429</td><td>—</td></tr>
      <tr><td>Degree</td><td style="color:#1DB954;font-weight:500">0.3391</td><td style="color:#1DB954">0.2831</td></tr>
      <tr><td>PageRank</td><td>0.2875</td><td>—</td></tr>
      <tr><td>Eigenvector</td><td>0.2197</td><td>—</td></tr>
    </table>
    <div class="insight"><strong>Betweenness centrality has the strongest correlation with popularity (r = 0.34)</strong>, suggesting that artists who bridge different communities tend to be more popular than those who are only well-connected within one cluster. However, centrality explains only about 10–12% of popularity variance — fame also depends on marketing, virality, and label support.</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Scatter plot
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Degree centrality vs. Spotify popularity <span class="panel-tag">full network</span></div>', unsafe_allow_html=True)
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
    st.markdown('<div class="insight">Artists like <strong>Diplo, Gucci Mane</strong>, and <strong>Snoop Dogg</strong> rank in the top 10 for both degree and betweenness centrality, suggesting structural bridging roles and commercial success coincide.</div></div>', unsafe_allow_html=True)

    # Centrality table
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Top artists by centrality measure</div>', unsafe_allow_html=True)
    metric2 = st.radio("Centrality metric", ["Degree","Betweenness","Eigenvector"], horizontal=True, label_visibility="collapsed", key="rq1_metric")
    st.dataframe(ARTISTS[metric2][["#","Artist","Genre","Popularity","Score","Note"]],
        use_container_width=True, hide_index=True,
        column_config={
            "Popularity": st.column_config.ProgressColumn("Popularity", min_value=0, max_value=100, format="%d"),
            "Score": st.column_config.ProgressColumn("Score (normalized)", min_value=0, max_value=1, format="%.2f"),
        })
    st.markdown('</div>', unsafe_allow_html=True)

    # Artist search
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
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
    st.markdown("""
    <div class="panel">
      <div class="panel-title" style="font-size:16px;margin-bottom:8px">RQ2: Do Genre Communities Emerge from Collaboration?</div>
      <div style="font-size:12px;color:#8a9188;line-height:1.65">Do meaningful genre-based communities emerge from the structure of artist collaboration alone, and to what extent do artists collaborate within versus across genre boundaries?</div>
    </div>
    """, unsafe_allow_html=True)

    # Community detection results
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel"><div class="panel-title">Louvain community detection results <span class="panel-tag">full network</span></div>', unsafe_allow_html=True)
        for col, val, lbl, acc in zip(st.columns(3),
            ["4,434","0.827","89.3%"],
            ["Communities detected","Modularity score","Edges within communities"],
            [False,True,True]):
            col.markdown(f'<div class="stat-card"><div class="{"stat-acc" if acc else "stat-val"}" style="font-size:18px">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="insight"><strong>High modularity (0.827)</strong> confirms strong community structure. <strong>89.3%</strong> of edges occur within communities — artists overwhelmingly collaborate within their genre cluster.</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel"><div class="panel-title">Genre representation <span class="panel-tag">nodes.csv metadata</span></div>', unsafe_allow_html=True)
        genre_html = '<div class="genre-grid">'
        for name, tag in [("Dance pop","top genre"),("Dutch hip-hop","regional"),("French hip-hop","regional"),
                          ("K-pop","global"),("Funk carioca","regional"),("Trap","popular"),
                          ("EDM","popular"),("No genre tag","~62%")]:
            genre_html += f'<div class="genre-pill"><span>{name}</span><span class="genre-pct">{tag}</span></div>'
        genre_html += '</div>'
        st.markdown(genre_html, unsafe_allow_html=True)
        st.markdown('<div class="insight"><strong>62% of artists have no genre tags.</strong> Regional genres are overrepresented due to country-specific chart sourcing.</div></div>', unsafe_allow_html=True)

    # Top 10 communities table
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Top 10 communities by size <span class="panel-tag">Louvain · labeled by dominant genre</span></div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="comm-table">
      <tr><th>Rank</th><th>Community</th><th>Artists</th><th>Dominant Genre</th></tr>
      <tr><td>1</td><td>11</td><td>19,347</td><td>dance pop</td></tr>
      <tr><td>2</td><td>6</td><td>13,517</td><td>Latin hip-hop</td></tr>
      <tr><td>3</td><td>26</td><td>9,856</td><td>ATL hip-hop</td></tr>
      <tr><td>4</td><td>32</td><td>9,645</td><td>adult standards</td></tr>
      <tr><td>5</td><td>24</td><td>8,638</td><td>funk carioca</td></tr>
      <tr><td>6</td><td>69</td><td>6,461</td><td>desi pop</td></tr>
      <tr><td>7</td><td>1</td><td>4,828</td><td>German hip-hop</td></tr>
      <tr><td>8</td><td>43</td><td>4,459</td><td>French hip-hop</td></tr>
      <tr><td>9</td><td>71</td><td>4,353</td><td>hands up</td></tr>
      <tr><td>10</td><td>121</td><td>3,944</td><td>UK drill</td></tr>
    </table>
    <div class="insight">Communities align clearly with <strong>genre and regional traditions</strong> — the algorithm had no access to genre labels, yet detected clusters that map to dance pop, Latin hip-hop, funk carioca, K-pop, and more.</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Within vs across edges
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Within vs. cross-community edges <span class="panel-tag">full network</span></div>', unsafe_allow_html=True)
    fw_comm = go.Figure(go.Bar(
        x=['Within community','Cross community'],
        y=[268216, 32163],
        marker_color=['rgba(29,185,84,0.45)','rgba(232,51,109,0.45)'],
        marker_line_color=['#1DB954','#E8336D'], marker_line_width=1,
        text=['268,216 (89.3%)','32,163 (10.7%)'], textposition='outside',
        textfont=dict(color=['#1DB954','#E8336D'], size=11)))
    fw_comm.update_layout(height=280, margin=dict(l=40,r=20,t=30,b=40),
        yaxis=dict(title='Number of edges',title_font_size=10,tickfont_size=10,gridcolor=GC),
        xaxis=dict(tickfont_size=11),
        showlegend=False, **PT)
    st.plotly_chart(fw_comm, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Top cross-community pairs
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">Top cross-community genre bridges <span class="panel-tag">top 10 pairs by edge count</span></div>', unsafe_allow_html=True)
    cross_genres = ['dance pop ↔ ATL hip-hop','dance pop ↔ UK drill','Latin hip-hop ↔ ATL hip-hop',
                    'dance pop ↔ hands up','alt. dance ↔ dance pop','Latin hip-hop ↔ dance pop',
                    'ATL hip-hop ↔ UK drill','dance pop ↔ Dutch hip-hop','dance pop ↔ adult standards',
                    'ATL hip-hop ↔ adult standards']
    cross_counts = [4282,1766,1580,1371,1208,1084,991,705,583,562]
    fc = go.Figure(go.Bar(
        y=cross_genres[::-1], x=cross_counts[::-1], orientation='h',
        marker_color='rgba(29,185,84,0.40)', marker_line_color='#1DB954', marker_line_width=1))
    fc.update_layout(height=340, margin=dict(l=200,r=20,t=10,b=40),
        xaxis=dict(title='Cross-community edges', title_font_size=10, tickfont_size=10, gridcolor=GC),
        yaxis=dict(tickfont_size=10), showlegend=False, **PT)
    st.plotly_chart(fc, use_container_width=True, config={"displayModeBar":False})
    st.markdown('<div class="insight"><strong>Dance pop</strong> appears in 7 of the top 10 cross-community pairs, acting as the connective tissue of the collaboration network. It bridges ATL hip-hop, UK drill, Latin hip-hop, and many other genre clusters.</div></div>', unsafe_allow_html=True)


# ━━ SMALL-WORLD — RQ3 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.markdown("""
    <div class="panel">
      <div class="panel-title" style="font-size:16px;margin-bottom:8px">RQ3: Is This a Small World?</div>
      <div style="font-size:12px;color:#8a9188;line-height:1.65">Does the Spotify artist collaboration network exhibit small-world properties — high clustering and short path lengths — and what does this imply about how trends spread?</div>
    </div>
    """, unsafe_allow_html=True)

    # Clustering comparison
    st.markdown('<div class="panel"><div class="panel-title">Clustering coefficient: actual vs. random baseline <span class="panel-tag">log scale</span></div>', unsafe_allow_html=True)
    fw = go.Figure(go.Bar(
        x=['Actual clustering (LCC)','Expected clustering (random)'],
        y=[0.085,0.000027],
        marker_color=['rgba(29,185,84,0.45)','rgba(136,135,128,0.35)'],
        marker_line_color=['#1DB954','#515650'], marker_line_width=1,
        text=['0.085000','0.000027'], textposition='outside',
        textfont=dict(color=['#1DB954','#8a9188'], size=11)))
    fw.update_layout(height=300, margin=dict(l=50,r=20,t=20,b=50), yaxis_type='log',
        xaxis=dict(tickfont_size=12, gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(title='Clustering coefficient (log scale)', title_font_size=11, tickfont_size=10, gridcolor=GC),
        showlegend=False, **PT)
    st.plotly_chart(fw, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Small-world summary stats
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    for col,(val,lbl,acc) in zip(st.columns(4),[
        ("0.085","Actual clustering (LCC)",False),
        ("0.000027","Random baseline",False),
        ("3,154×","C / C_random",True),
        ("6.199","Est. avg. path length",True)]):
        col.markdown(f'<div class="stat-card"><div class="{"stat-acc" if acc else "stat-val"}" style="font-size:18px">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="panel">
      <div class="panel-title">Small-world comparison summary</div>
      <table class="corr-table">
        <tr><th>Metric</th><th>Actual</th><th>Random Baseline</th><th>Ratio</th></tr>
        <tr><td>Clustering coefficient</td><td style="color:#1DB954;font-weight:500">0.085</td><td>0.000027</td><td style="color:#1DB954;font-weight:500">3,154×</td></tr>
        <tr><td>Avg. path length</td><td style="color:#1DB954;font-weight:500">6.199</td><td>8.589</td><td>0.72</td></tr>
      </table>
      <div class="insight"><strong>The network exhibits clear small-world properties.</strong> Clustering is 3,154× higher than random (C >> C_random), while average path length is shorter than the baseline (L ≈ L_random). This means artists form tight genre clusters, but bridge artists create shortcuts — any two artists are separated by only about <strong>6 collaboration steps</strong>. Musical trends could spread rapidly across the industry.</div>
    </div>
    """, unsafe_allow_html=True)


# ━━ DISCUSSION & LIMITATIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab5:
    st.markdown("""
    <div class="panel">
      <div class="panel-title" style="font-size:14px;margin-bottom:10px">RQ1 — Centrality and Popularity</div>
      <div style="font-size:12px;color:#8a9188;line-height:1.7">
        All four centrality measures show moderate positive correlations with popularity (r ≈ 0.22–0.34, all p < 0.001). Centrality explains only about 10–12% of popularity's variance — being structurally well-connected helps, but popularity also depends on marketing, virality, and label support.
        <br><br>
        Betweenness had the strongest correlation, suggesting artists who bridge different communities (R3HAB, Diplo, Snoop Dogg) tend to be more popular than those simply well-connected within a single cluster. One notable artifact: J.S. Bach tops degree centrality with 1,781 connections — not through modern collaborations, but because centuries of performers have re-recorded his works. Among contemporary artists, the top-degree nodes span EDM, hip-hop, and regional genres, suggesting prolific collaborators tend to work across genre lines.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
      <div class="panel-title" style="font-size:14px;margin-bottom:10px">RQ2 — Genre Communities</div>
      <div style="font-size:12px;color:#8a9188;line-height:1.7">
        Louvain identified <strong style="color:#e8ebe8">4,434 communities</strong> with high modularity (<strong style="color:#e8ebe8">0.827</strong>). The top communities align clearly with genre and regional traditions — dance pop, Latin hip-hop, ATL hip-hop, funk carioca, desi pop, German hip-hop, and more. The algorithm had no access to genre labels. It found them anyway.
        <br><br>
        <strong style="color:#e8ebe8">89.3%</strong> of edges occur within communities and only 10.7% cross boundaries. Among cross-community edges, dance pop is the most common bridge genre by a wide margin, connecting to ATL hip-hop (4,282 edges), UK drill (1,766), and Latin hip-hop (1,084). Dance pop/EDM is the connective tissue of the collaboration network.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
      <div class="panel-title" style="font-size:14px;margin-bottom:10px">RQ3 — Small-World Structure</div>
      <div style="font-size:12px;color:#8a9188;line-height:1.7">
        The network satisfies both criteria for small-world structure. Clustering (0.085) is 3,154× higher than random, confirming tight-knit artist clusters. Average path length (6.2) is shorter than the random baseline (8.6), so both conditions hold: tight local clustering, short global paths.
        <br><br>
        The bridge artists from RQ1 are doing the work — they connect dense genre clusters to each other, keeping average distance low even though most collaboration happens within communities. Any two artists in the largest connected component are separated by about 6 steps.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    l1, l2 = st.columns(2)
    with l1:
        st.markdown("""
        <div class="panel">
          <div class="panel-title" style="font-size:14px;margin-bottom:10px">Limitations</div>
          <div style="font-size:12px;color:#8a9188;line-height:1.7">
            <strong style="color:#e8ebe8">Missing genre data:</strong> ~62% of artists have no genre tags. Community-genre comparisons rely on the 38% with known genres, skewing toward established artists.<br><br>
            <strong style="color:#e8ebe8">Classical artifact:</strong> Composers like Bach inflate degree counts through re-recordings, not modern collaborations.<br><br>
            <strong style="color:#e8ebe8">Sampling bias:</strong> Chart-based collection overrepresents collaborative regional scenes and underrepresents rock, metal, and indie.<br><br>
            <strong style="color:#e8ebe8">Approximations:</strong> Betweenness used k=200 on a filtered subgraph; path length estimated from 1,000 sampled pairs.<br><br>
            <strong style="color:#e8ebe8">Static snapshot:</strong> 2013–2022 collapsed into one network with no temporal dimension.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with l2:
        st.markdown("""
        <div class="panel">
          <div class="panel-title" style="font-size:14px;margin-bottom:10px">Ethical Considerations</div>
          <div style="font-size:12px;color:#8a9188;line-height:1.7">
            <strong style="color:#e8ebe8">Representation bias:</strong> Collecting from charts means we start with commercially successful artists. Those from underrepresented regions or genres without chart presence barely appear — the network reflects the industry's mainstream more than the industry itself.<br><br>
            <strong style="color:#e8ebe8">Spotify's popularity metric:</strong> The popularity score is proprietary and opaque — it almost certainly reflects algorithmic promotion as much as genuine listener preference. Our correlations may be measuring Spotify's curation decisions as much as anything else.<br><br>
            <strong style="color:#e8ebe8">Privacy:</strong> All data is publicly available on Spotify and Kaggle. No private user data was used.
          </div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">CS4230 · Final Project · Mira Bhakta, Michelle Villagomez, Caden Maki · Spotify Artist Feature Collaboration Network 2013–2022</div>', unsafe_allow_html=True)

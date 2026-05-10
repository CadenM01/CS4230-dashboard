from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Charting Connections",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

OUTPUT_DIR = Path("output")


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Inter:wght@500;700;800&display=swap');

    :root {
        --bg: #0d1117;
        --panel: #1a1f1a;
        --panel-2: #1c211c;
        --border: #303630;
        --text: #f3f5ee;
        --muted: #a7b3a9;
        --green: #20c963;
        --green-soft: rgba(32, 201, 99, 0.16);
    }

    .stApp {
        background: var(--bg);
        color: var(--muted);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    code, pre, .mono, .pill, .kicker, .stTabs [data-baseweb="tab"] {
        font-family: 'DM Mono', monospace !important;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1760px;
        padding-top: 24px;
        padding-left: 60px;
        padding-right: 60px;
    }

    h1, h2, h3, h4, p {
        margin: 0;
    }

    .topbar {
        background: var(--panel);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 0 0 8px 8px;
        min-height: 64px;
        padding: 14px 24px;
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 28px;
    }

    .logo-dot {
        width: 31px;
        height: 31px;
        background: var(--green);
        border-radius: 999px;
    }

    .brand {
        color: var(--text);
        font-weight: 800;
        font-size: 1rem;
        margin-bottom: 4px;
    }

    .brand-sub {
        color: var(--muted);
        font-family: 'DM Mono', monospace;
        font-size: 0.78rem;
    }

    .title {
        color: var(--text);
        font-size: 2.1rem;
        line-height: 1.22;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 14px;
        max-width: 680px;
    }

    .subtitle {
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.7;
        max-width: 720px;
        margin-bottom: 18px;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 24px;
    }

    .pill {
        border: 1px solid rgba(32,201,99,0.45);
        background: rgba(32,201,99,0.09);
        border-radius: 999px;
        color: var(--green);
        padding: 7px 12px;
        font-size: 0.78rem;
        white-space: nowrap;
    }

    .stat-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px 22px 18px 22px;
        min-height: 102px;
    }

    .stat-val {
        color: var(--text);
        font-family: 'DM Mono', monospace;
        font-size: 1.55rem;
        font-weight: 500;
        letter-spacing: -0.05em;
        margin-bottom: 12px;
    }

    .stat-val.green {
        color: var(--green);
    }

    .stat-lbl {
        color: var(--muted);
        font-size: 0.78rem;
    }

    .card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .card.tight {
        padding: 0;
        overflow: hidden;
    }

    .card-title {
        color: var(--text);
        font-weight: 800;
        font-size: 1rem;
        margin-bottom: 18px;
    }

    .card-heading-row {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 26px 24px;
        margin-bottom: 14px;
        min-height: 84px;
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .tag {
        font-family: 'DM Mono', monospace;
        font-size: 0.78rem;
        color: var(--muted);
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(0,0,0,0.12);
        border-radius: 999px;
        padding: 6px 11px;
    }

    .small {
        color: var(--muted);
        font-size: 0.87rem;
        line-height: 1.65;
    }

    .accent-note {
        background: rgba(0,0,0,0.13);
        border-left: 3px solid var(--green);
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.6;
        margin-top: 10px;
    }

    .panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .overview-heading {
        color: var(--text);
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 26px;
    }

    .overview-subhead {
        color: var(--text);
        font-size: 0.95rem;
        font-weight: 800;
        margin-bottom: 14px;
    }

    .overview-copy {
        color: #dce5d8;
        font-size: 0.88rem;
        line-height: 1.65;
        margin-bottom: 20px;
    }

    .insight {
        background: rgba(0,0,0,0.13);
        border-left: 3px solid var(--green);
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.6;
    }

    .section-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 36px;
        margin-top: 24px;
    }

    .mini-title {
        color: var(--text);
        font-weight: 800;
        margin-bottom: 10px;
        padding-top: 14px;
        border-top: 1px solid var(--border);
        font-size: 0.88rem;
    }

    .rq-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin-top: 18px;
    }

    .rq {
        border-top: 1px solid rgba(32,201,99,0.45);
        padding-top: 12px;
    }

    .rq-label {
        font-family: 'DM Mono', monospace;
        color: var(--green);
        font-size: 0.78rem;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    .rq-text {
        color: var(--text);
        font-size: 0.86rem;
        line-height: 1.6;
        font-weight: 600;
    }

    .genre-pill {
        display: inline-flex;
        gap: 8px;
        align-items: center;
        padding: 7px 10px;
        border-radius: 999px;
        background: rgba(32,201,99,0.08);
        border: 1px solid rgba(32,201,99,0.22);
        margin: 4px;
        color: var(--text);
        font-size: 0.78rem;
    }

    .genre-tag {
        color: var(--green);
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 18px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 999px;
        border: 1px solid var(--border);
        color: var(--muted);
        padding: 12px 20px;
        height: 48px;
        font-size: 0.92rem;
    }

    .stTabs [aria-selected="true"] {
        background: var(--green) !important;
        color: white !important;
        border-color: var(--green) !important;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid var(--border);
    }

    div[data-testid="stRadio"] > label {
        display: none;
    }

    div[role="radiogroup"] {
        gap: 10px;
    }

    div[role="radiogroup"] label {
        background: transparent;
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 6px 12px;
        color: var(--muted);
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: 22px;
            padding-right: 22px;
        }

        .section-grid,
        .rq-grid {
            grid-template-columns: 1fr;
        }

        .title {
            font-size: 1.8rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


PT = dict(
    paper_bgcolor="#111211",
    plot_bgcolor="#171c17",
    font_color="#c7d0c6",
    font_family="Inter",
)

GRID = "rgba(255,255,255,0.10)"
GREEN = "#20c963"


SUMMARY = {
    "artists": "156,320",
    "collaborations": "300,379",
    "largest_component": "94.9%",
    "average_degree": "3.84",
    "clustering_ratio": "3,154×",
    "components": "4,338",
}


ARTISTS = {
    "Degree": pd.DataFrame(
        [
            (1, "J.S. Bach", "Classical", 52, 1.00, "⚠ data artifact"),
            (2, "Gucci Mane", "Trap", 85, 0.62, ""),
            (3, "Armin van Buuren", "EDM", 78, 0.58, ""),
            (4, "Snoop Dogg", "Hip-hop", 88, 0.56, ""),
            (5, "Diplo", "Dance", 82, 0.54, ""),
            (6, "Mc Gw", "Funk carioca", 71, 0.51, ""),
            (7, "DJ Khaled", "Hip-hop", 81, 0.49, ""),
            (8, "Nicki Minaj", "Pop/Rap", 91, 0.47, ""),
            (9, "Chris Brown", "R&B", 89, 0.44, ""),
            (10, "Lil Wayne", "Hip-hop", 87, 0.43, ""),
        ],
        columns=["#", "Artist", "Genre", "Popularity", "Score", "Note"],
    ),
    "Betweenness": pd.DataFrame(
        [
            (1, "R3HAB", "EDM", 75, 1.00, ""),
            (2, "Diplo", "Dance", 82, 0.91, ""),
            (3, "Snoop Dogg", "Hip-hop", 88, 0.84, ""),
            (4, "Armin van Buuren", "EDM", 78, 0.79, ""),
            (5, "Gucci Mane", "Trap", 85, 0.71, ""),
            (6, "T-Pain", "Hip-hop", 76, 0.65, ""),
            (7, "Wiz Khalifa", "Hip-hop", 84, 0.58, ""),
            (8, "DJ Mustard", "Hip-hop", 72, 0.52, ""),
            (9, "Bebe Rexha", "Pop", 80, 0.48, ""),
            (10, "Ty Dolla Sign", "R&B", 79, 0.43, ""),
        ],
        columns=["#", "Artist", "Genre", "Popularity", "Score", "Note"],
    ),
    "Eigenvector": pd.DataFrame(
        [
            (1, "Diplo", "Dance", 82, 1.00, ""),
            (2, "Skrillex", "EDM", 80, 0.94, ""),
            (3, "Snoop Dogg", "Hip-hop", 88, 0.88, ""),
            (4, "Ty Dolla Sign", "R&B", 79, 0.82, ""),
            (5, "Chris Brown", "R&B", 89, 0.77, ""),
            (6, "Gucci Mane", "Trap", 85, 0.71, ""),
            (7, "Wiz Khalifa", "Hip-hop", 84, 0.66, ""),
            (8, "Lil Wayne", "Hip-hop", 87, 0.61, ""),
            (9, "Future", "Trap", 90, 0.56, ""),
            (10, "Young Jeezy", "Hip-hop", 74, 0.51, ""),
        ],
        columns=["#", "Artist", "Genre", "Popularity", "Score", "Note"],
    ),
}


CORRELATIONS = pd.DataFrame(
    [
        ("degree_score", "popularity", 0.19, "< 0.001", 0.23, "< 0.001"),
        ("degree_score", "followers", 0.21, "< 0.001", 0.25, "< 0.001"),
        ("betweenness", "popularity", 0.16, "< 0.001", 0.19, "< 0.001"),
        ("betweenness", "followers", 0.18, "< 0.001", 0.22, "< 0.001"),
        ("eigenvector", "popularity", 0.14, "< 0.001", 0.17, "< 0.001"),
        ("eigenvector", "followers", 0.15, "< 0.001", 0.18, "< 0.001"),
    ],
    columns=[
        "centrality_metric",
        "spotify_measure",
        "pearson_r",
        "pearson_p",
        "spearman_rho",
        "spearman_p",
    ],
)


def load_louvain_outputs():
    community_path = OUTPUT_DIR / "community_summary.csv"
    artist_path = OUTPUT_DIR / "artist_communities.csv"

    community_summary = pd.read_csv(community_path) if community_path.exists() else None
    artist_communities = pd.read_csv(artist_path) if artist_path.exists() else None

    return community_summary, artist_communities


def stat_card(col, value, label, accent=False):
    color_class = "green" if accent else ""

    col.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-val {color_class}">{value}</div>
            <div class="stat-lbl">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def network_preview_figure():
    coords = [
        (0.48, 0.50, 26, "#20c963"),
        (0.70, 0.38, 20, "#0fa54f"),
        (0.28, 0.68, 17, "#65c5aa"),
        (0.62, 0.74, 14, "#60b5a0"),
        (0.82, 0.60, 13, "#8fcdbd"),
        (0.18, 0.34, 13, "#8fcdbd"),
        (0.46, 0.20, 13, "#8fcdbd"),
        (0.78, 0.22, 10, "#4c554f"),
        (0.34, 0.84, 10, "#4c554f"),
        (0.90, 0.44, 9, "#4c554f"),
        (0.10, 0.58, 9, "#4c554f"),
        (0.55, 0.88, 9, "#4c554f"),
    ]

    edges = [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 6),
        (1, 4),
        (1, 9),
        (2, 10),
        (2, 11),
        (3, 4),
        (3, 7),
        (5, 0),
        (5, 10),
        (6, 7),
        (7, 9),
        (8, 2),
        (8, 11),
        (11, 3),
    ]

    fig = go.Figure()

    for a, b in edges:
        fig.add_trace(
            go.Scatter(
                x=[coords[a][0], coords[b][0]],
                y=[coords[a][1], coords[b][1]],
                mode="lines",
                line=dict(color="rgba(32,201,99,0.25)", width=1),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[n[0] for n in coords],
            y=[n[1] for n in coords],
            mode="markers",
            marker=dict(
                size=[n[2] for n in coords],
                color=[n[3] for n in coords],
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.update_layout(
        height=250,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        **PT,
    )

    return fig


def degree_distribution_figure():
    x = ["1", "2–3", "4–6", "7–15", "16–50", "51–200", "201+"]
    y = [78000, 31000, 18000, 14000, 9000, 4500, 1781]

    fig = go.Figure(
        go.Bar(
            x=x,
            y=y,
            marker_color="rgba(32,201,99,0.42)",
            marker_line_color=GREEN,
            marker_line_width=1.6,
        )
    )

    fig.update_layout(
        height=250,
        margin=dict(l=70, r=12, t=10, b=52),
        yaxis_type="log",
        xaxis=dict(
            title="Degree (# collaborations)",
            title_font_size=12,
            tickfont_size=11,
            gridcolor=GRID,
        ),
        yaxis=dict(
            title="Artists (log)",
            title_font_size=12,
            tickfont_size=11,
            gridcolor=GRID,
        ),
        showlegend=False,
        **PT,
    )

    return fig


def centrality_scatter():
    pops = [52, 85, 78, 88, 82, 71, 81, 91, 89, 87, 75, 80, 76, 84, 72, 80, 79]
    degs = [1.00, 0.62, 0.58, 0.56, 0.54, 0.51, 0.49, 0.47, 0.44, 0.43, 0.31, 0.29, 0.27, 0.25, 0.22, 0.19, 0.17]

    names = [
        "J.S. Bach",
        "Gucci Mane",
        "Armin van Buuren",
        "Snoop Dogg",
        "Diplo",
        "Mc Gw",
        "DJ Khaled",
        "Nicki Minaj",
        "Chris Brown",
        "Lil Wayne",
        "R3HAB",
        "Bebe Rexha",
        "T-Pain",
        "Wiz Khalifa",
        "DJ Mustard",
        "Ty Dolla Sign",
        "Future",
    ]

    fig = go.Figure(
        go.Scatter(
            x=pops,
            y=degs,
            mode="markers",
            text=names,
            marker=dict(
                size=12,
                color="rgba(32,201,99,0.58)",
                line=dict(color=GREEN, width=1),
            ),
            hovertemplate="%{text}<br>Popularity: %{x}<br>Degree centrality: %{y:.3f}<extra></extra>",
        )
    )

    fig.update_layout(
        height=340,
        margin=dict(l=55, r=20, t=10, b=55),
        xaxis=dict(
            range=[0, 100],
            title="Spotify popularity score",
            title_font_size=12,
            tickfont_size=11,
            gridcolor=GRID,
        ),
        yaxis=dict(
            title="Degree centrality (normalized)",
            title_font_size=12,
            tickfont_size=11,
            gridcolor=GRID,
        ),
        showlegend=False,
        **PT,
    )

    return fig


def genre_distribution_figure():
    genre_names = [
        "dance pop",
        "dutch hip hop",
        "french hip hop",
        "k-pop",
        "german hip hop",
        "funk carioca",
        "v-pop",
        "finnish dance pop",
        "alternative r&b",
        "italian hip hop",
        "latin hip hop",
        "francoton",
        "desi pop",
        "polish alt rap",
        "bass house",
    ]

    genre_counts = [320, 285, 280, 275, 265, 260, 235, 210, 210, 200, 195, 190, 190, 185, 180]

    fig = go.Figure(
        go.Bar(
            y=genre_names[::-1],
            x=genre_counts[::-1],
            orientation="h",
            marker_color="rgba(32,201,99,0.42)",
            marker_line_color=GREEN,
            marker_line_width=1.3,
        )
    )

    fig.update_layout(
        height=360,
        margin=dict(l=132, r=20, t=10, b=48),
        xaxis=dict(
            title="Number of artists",
            title_font_size=12,
            tickfont_size=11,
            gridcolor=GRID,
        ),
        yaxis=dict(tickfont_size=11),
        showlegend=False,
        **PT,
    )

    return fig


def small_world_figure():
    actual = 0.085037
    random_val = 0.000027

    fig = go.Figure(
        go.Bar(
            x=["Actual clustering (LCC)", "Expected clustering (random)"],
            y=[actual, random_val],
            marker_color=["rgba(32,201,99,0.42)", "rgba(136,135,128,0.35)"],
            marker_line_color=[GREEN, "#515650"],
            marker_line_width=1.4,
            text=[f"{actual:.6f}", f"{random_val:.6f}"],
            textposition="outside",
            textfont=dict(color=[GREEN, "#a7b3a9"], size=12),
        )
    )

    fig.update_layout(
        height=320,
        margin=dict(l=55, r=20, t=20, b=55),
        yaxis_type="log",
        xaxis=dict(tickfont_size=12, gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(
            title="Clustering coefficient (log scale)",
            title_font_size=12,
            tickfont_size=11,
            gridcolor=GRID,
        ),
        showlegend=False,
        **PT,
    )

    return fig


def show_top_table(df):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Popularity": st.column_config.ProgressColumn(
                "Popularity",
                min_value=0,
                max_value=100,
                format="%d",
            ),
            "Score": st.column_config.ProgressColumn(
                "Score (normalized)",
                min_value=0,
                max_value=1,
                format="%.2f",
            ),
        },
    )


community_summary_df, artist_communities_df = load_louvain_outputs()


st.markdown(
    """
    <div class="topbar">
        <div class="logo-dot"></div>
        <div>
            <div class="brand">Charting Connections</div>
            <div class="brand-sub">Spotify Artist Collaboration Network · CS4230</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="title">Spotify Artist Feature<br>Collaboration Network</div>
    <div class="subtitle">
        Who holds structural power in music? Exploring centrality, genre communities, and small-world
        dynamics across 156K artists and 300K collaborations on Spotify (2013–2022).
    </div>
    <div class="pill-row">
        <span class="pill">156,320 artists</span>
        <span class="pill">300,379 collabs</span>
        <span class="pill">2013–2022</span>
        <span class="pill">undirected · unweighted</span>
        <span class="pill">Mira Bhakta · Michelle Villagomez · Caden Maki</span>
    </div>
    """,
    unsafe_allow_html=True,
)

stat_cols = st.columns(5)
stat_card(stat_cols[0], SUMMARY["artists"], "Artists (nodes)")
stat_card(stat_cols[1], SUMMARY["collaborations"], "Collaborations (edges)")
stat_card(stat_cols[2], SUMMARY["largest_component"], "In largest component", accent=True)
stat_card(stat_cols[3], SUMMARY["average_degree"], "Avg. degree")
stat_card(stat_cols[4], SUMMARY["clustering_ratio"], "Clustering vs. random", accent=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Centrality — RQ1", "Communities — RQ2", "Small-World — RQ3", "Discussion & Limitations"]
)

with tab1:
    st.markdown(
        """
        <div class="card">
            <div class="card-title" style="font-size:1.35rem;">Overview</div>
            <div class="small" style="font-weight:800;color:#f3f5ee;margin-bottom:12px;">Guiding question</div>
            <div class="small" style="color:#f3f5ee;">
                In this network, <b>who appears structurally central</b>, and how does that relate to
                <b>popularity, genre communities, and small-world structure?</b>
            </div>
            <div class="rq-grid">
                <div class="rq">
                    <div class="rq-label">RQ1 · Centrality</div>
                    <div class="rq-text">Which artists serve as the most central hubs or bridges, and does centrality relate to Spotify popularity or followers?</div>
                </div>
                <div class="rq">
                    <div class="rq-label">RQ2 · Communities</div>
                    <div class="rq-text">Do meaningful genre-based communities emerge from collaboration patterns, and do artists collaborate within or across genres?</div>
                </div>
                <div class="rq">
                    <div class="rq-label">RQ3 · Small-world</div>
                    <div class="rq-text">Does the network show small-world properties, with high clustering and short paths that could help trends spread?</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
            <div class="card-title" style="font-size:1.35rem;">What this network represents</div>
            <div class="section-grid">
                <div>
                    <div class="mini-title">Nodes</div>
                    <div class="small">Unique Spotify artists with attributes like popularity, followers, genres, and chart hits.</div>
                </div>
                <div>
                    <div class="mini-title">Edges</div>
                    <div class="small">Feature collaborations between two artists, with duplicate collaborations collapsed.</div>
                </div>
                <div>
                    <div class="mini-title">Model</div>
                    <div class="small">Undirected and unweighted, so each unique collaboration counts once in both directions.</div>
                </div>
                <div>
                    <div class="mini-title">Scope</div>
                    <div class="small">A static 2013–2022 snapshot rather than a timeline of collaboration changes.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Network structure — subgraph preview</div><div class="tag">top artists by degree</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="card tight">', unsafe_allow_html=True)
        st.plotly_chart(
            network_preview_figure(),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            f'<div class="accent-note">The full network has <b style="color:#f3f5ee;">{SUMMARY["components"]} connected components</b>, but 95% of artists belong to one dominant giant component — a tightly linked global collaboration ecosystem.</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Degree distribution</div><div class="tag">log scale · full network</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="card tight">', unsafe_allow_html=True)
        st.plotly_chart(
            degree_distribution_figure(),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="accent-note">Median degree is <b style="color:#f3f5ee;">1</b>. Max degree is <b style="color:#f3f5ee;">1,781 (J.S. Bach)</b>. The heavy tail is characteristic of real-world social networks.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Top artists by centrality measure</div></div>',
        unsafe_allow_html=True,
    )

    metric = st.radio(
        "Metric",
        ["Degree", "Betweenness", "Eigenvector"],
        horizontal=True,
        label_visibility="collapsed",
    )

    show_top_table(ARTISTS[metric])


with tab2:
    st.markdown("""
    <div class="panel">
      <div class="overview-heading">Who Is Central?</div>
      <div class="overview-subhead">RQ1 · Centrality</div>
      <div class="overview-copy"><strong>Question:</strong> Which artists serve as the most central hubs or bridges in the Spotify collaboration network, and does their centrality relate to popularity or follower count?</div>
      <div class="insight"><strong>What this means for this data:</strong> Centrality is about structural position, not just fame. Degree highlights artists with many direct collaborators, betweenness highlights artists who connect different parts of the network, and eigenvector centrality highlights artists connected to other well-connected artists. Comparing these scores with Spotify popularity helps us ask whether network power and commercial visibility move together.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Centrality vs. Spotify popularity</div><div class="tag">RQ1</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card tight">', unsafe_allow_html=True)
    st.plotly_chart(
        centrality_scatter(),
        use_container_width=True,
        config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Correlation results</div></div>',
        unsafe_allow_html=True,
    )

    st.dataframe(CORRELATIONS, use_container_width=True, hide_index=True)

    st.markdown(
        '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Search top artists</div></div>',
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "Search",
        placeholder="e.g. Snoop Dogg, Diplo, Nicki Minaj...",
        label_visibility="collapsed",
    )

    if search:
        all_artists = pd.concat(ARTISTS.values(), ignore_index=True).drop_duplicates(
            subset=["Artist"]
        )

        results = all_artists[
            all_artists["Artist"].str.contains(search, case=False, na=False)
        ]

        if len(results) > 0:
            st.dataframe(results, use_container_width=True, hide_index=True)
        else:
            st.markdown(
                f'<div class="small">No results for "{search}" in the top artist tables.</div>',
                unsafe_allow_html=True,
            )


with tab3:
    st.markdown("""
    <div class="panel">
      <div class="overview-heading">Where Do Communities Form?</div>
      <div class="overview-subhead">RQ2 · Communities</div>
      <div class="overview-copy"><strong>Question:</strong> Do meaningful genre-based communities emerge from artist collaboration patterns, and do artists collaborate mostly within or across genre boundaries?</div>
      <div class="insight"><strong>What this means for this data:</strong> A community is a group of artists who collaborate more with each other than with the rest of the network. In this dataset, genre can help explain those groups, but it is imperfect: many artists have no genre tag, and others belong to multiple genres. The Louvain results summarize where dense collaboration communities appear in the network.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)

    with g1:
        st.markdown(
            '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Genre representation</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="card">', unsafe_allow_html=True)

        for name, tag in [
            ("Dance pop", "top genre"),
            ("Dutch hip-hop", "regional"),
            ("French hip-hop", "regional"),
            ("K-pop", "global"),
            ("Funk carioca", "regional"),
            ("Trap", "popular"),
            ("EDM", "popular"),
            ("No genre tag", "~62%"),
        ]:
            st.markdown(
                f'<span class="genre-pill">{name}<span class="genre-tag">{tag}</span></span>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with g2:
        st.markdown(
            '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Louvain communities</div><div class="tag">computed</div></div>',
            unsafe_allow_html=True,
        )

        if community_summary_df is not None and len(community_summary_df) > 0:
            st.dataframe(
                community_summary_df[
                    [
                        "community_rank",
                        "community",
                        "artist_count",
                        "top_genre",
                        "sample_artists",
                    ]
                ].head(10),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.markdown(
                '<div class="card"><div class="small">Run <code>python precompute_louvain.py</code> to generate Louvain community results.</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Top genres by artist count</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card tight">', unsafe_allow_html=True)
    st.plotly_chart(
        genre_distribution_figure(),
        use_container_width=True,
        config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if artist_communities_df is not None and len(artist_communities_df) > 0:
        st.markdown(
            '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Browse Louvain community</div></div>',
            unsafe_allow_html=True,
        )

        community_options = (
            community_summary_df["community"].head(30).tolist()
            if community_summary_df is not None
            and "community" in community_summary_df.columns
            else sorted(artist_communities_df["community"].unique().tolist())
        )

        selected = st.selectbox("Select a community", community_options)

        view = (
            artist_communities_df[artist_communities_df["community"] == selected][
                ["artist", "genre", "popularity", "followers", "community"]
            ]
            .sort_values("popularity", ascending=False, na_position="last")
            .head(50)
        )

        st.dataframe(view, use_container_width=True, hide_index=True)


with tab4:
    st.markdown("""
    <div class="panel">
      <div class="overview-heading">Is This a Small World?</div>
      <div class="overview-subhead">RQ3 · Small-world structure</div>
      <div class="overview-copy"><strong>Question:</strong> Does the Spotify artist collaboration network show small-world properties, with high clustering and short average path lengths?</div>
      <div class="insight"><strong>What this means for this data:</strong> Small-world networks have tight local clusters while still allowing most nodes to be reached through relatively short chains. Here, clustering tests whether an artist's collaborators also collaborate with each other. The random baseline helps show whether that clustering is unusually high, while average path length helps explain how quickly influence or trends could spread.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card-heading-row"><div class="card-title" style="margin-bottom:0;">Small-world evidence</div><div class="tag">RQ3</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card tight">', unsafe_allow_html=True)
    st.plotly_chart(
        small_world_figure(),
        use_container_width=True,
        config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)

    metric_cols = st.columns(4)
    stat_card(metric_cols[0], "0.085037", "Actual clustering coefficient")
    stat_card(metric_cols[1], "0.000027", "Expected random clustering")
    stat_card(metric_cols[2], SUMMARY["clustering_ratio"], "Ratio actual / random", accent=True)
    stat_card(metric_cols[3], "6.18", "Estimated average path length", accent=True)

with tab5:
    st.markdown("""
    <div class="panel">
      <div class="overview-heading">Discussion & Limitations</div>
      <div class="overview-subhead">Interpreting findings in context of the research questions</div>

      <div class="overview-copy">
        This dashboard shows that network analysis can reveal patterns in Spotify artist collaborations that
        would not be as clear from popularity, follower count, or genre labels alone. Across the three research
        questions, the results suggest that artist influence depends not only on fame, but also on where an
        artist is positioned within the collaboration network.
      </div>

      <div class="insight">
        <strong>Overall interpretation:</strong> The network contains a large connected collaboration ecosystem,
        a small number of highly central artists, genre and regional clustering, and evidence of small-world
        structure. These patterns suggest that music collaborations may help artists spread influence across
        tightly connected communities.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="card-title">RQ1 · Centrality and Influence</div>
      <div class="small">
        The centrality results show that structural power is not the same as popularity. Artists with high degree
        centrality have many direct collaborators, making them major hubs in the network. Artists with high
        betweenness centrality are important in a different way because they may connect separate communities,
        genres, or regional scenes. This means an artist can be influential because they act as a bridge, even if
        they are not simply the most popular artist.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="card-title">RQ2 · Genre Communities</div>
      <div class="small">
        The community and genre results suggest that some collaboration groups may form around genre or regional
        music scenes. However, this result should be interpreted carefully because many artists have missing genre
        metadata. Since about 62% of artists do not have genre tags, the dashboard can suggest possible genre
        patterns, but it cannot fully prove that collaboration communities are always genre-based.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="card-title">RQ3 · Small-World Structure</div>
      <div class="small">
        The small-world results show that the network has much higher clustering than a comparable random network.
        This suggests that artists tend to form tightly connected groups. At the same time, the large connected
        component and estimated average path length suggest that artists can still be connected through relatively
        short collaboration chains. In the music industry, this could help explain how collaborations, audiences,
        and trends spread across communities.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="card-title">Limitations</div>
      <div class="small">
        One major limitation is missing genre data. Since many artists have unknown genres, genre-based conclusions
        are incomplete. Another limitation is that some highly connected artists may appear important because of
        dataset artifacts, re-recordings, or metadata issues rather than modern collaborations. The dataset may
        also overrepresent certain popular artists, regions, or genres depending on how the Spotify chart and
        collaboration data were collected.
        <br><br>
        There were also computational limitations. Because the network is very large, some measures such as
        betweenness centrality had to be approximated or calculated on a filtered subgraph instead of the entire
        full network.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="card-title">Ethical Issues</div>
      <div class="small">
        An ethical concern is that popularity and collaboration data can reinforce existing visibility gaps.
        Artists who are already famous or highly connected may appear more influential, while smaller or
        independent artists may be overlooked. If this type of analysis were used for recommendations, it could
        unintentionally favor mainstream artists and reduce visibility for niche or independent creators.
        <br><br>
        Privacy concerns are limited because the project uses public artist metadata rather than private user data.
        However, bias and fairness are still important because the dataset may not represent all artists equally.
      </div>
    </div>
    """, unsafe_allow_html=True)
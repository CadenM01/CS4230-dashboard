"""
precompute_louvain.py

Computes Louvain communities from data/nodes.csv and data/edges.csv.

Run:
    python precompute_louvain.py
"""

import ast
from pathlib import Path

import networkx as nx
import pandas as pd

try:
    import community as community_louvain
except Exception:
    community_louvain = None


DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

NODES_FILE = DATA_DIR / "nodes.csv"
EDGES_FILE = DATA_DIR / "edges.csv"


def normalize_col_names(df):
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df


def first_existing_column(df, options):
    for option in options:
        if option in df.columns:
            return option
    return None


def parse_primary_genre(value):
    if pd.isna(value):
        return "Unknown"

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none", "[]"}:
        return "Unknown"

    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list) and len(parsed) > 0:
            return str(parsed[0])
    except Exception:
        pass

    if "," in text:
        return text.split(",")[0].strip()

    return text


def load_data():
    if not NODES_FILE.exists():
        raise FileNotFoundError("Missing data/nodes.csv")

    if not EDGES_FILE.exists():
        raise FileNotFoundError("Missing data/edges.csv")

    nodes_raw = normalize_col_names(pd.read_csv(NODES_FILE))
    edges_raw = normalize_col_names(pd.read_csv(EDGES_FILE))

    id_col = first_existing_column(
        nodes_raw,
        ["spotify_id", "id", "node_id", "artist_id"]
    )

    name_col = first_existing_column(
        nodes_raw,
        ["name", "artist", "artist_name", "label"]
    )

    pop_col = first_existing_column(
        nodes_raw,
        ["popularity", "spotify_popularity"]
    )

    followers_col = first_existing_column(
        nodes_raw,
        ["followers", "follower_count"]
    )

    genre_col = first_existing_column(
        nodes_raw,
        ["genres", "genre", "primary_genre"]
    )

    source_col = first_existing_column(
        edges_raw,
        ["id_0", "source", "src", "from", "artist_0", "spotify_id_0"]
    )

    target_col = first_existing_column(
        edges_raw,
        ["id_1", "target", "dst", "to", "artist_1", "spotify_id_1"]
    )

    if id_col is None:
        raise ValueError(
            "nodes.csv needs an ID column like spotify_id, id, node_id, or artist_id."
        )

    if source_col is None or target_col is None:
        raise ValueError(
            "edges.csv needs edge columns like id_0/id_1 or source/target."
        )

    nodes = pd.DataFrame()
    nodes["spotify_id"] = nodes_raw[id_col].astype(str)
    nodes["artist"] = nodes_raw[name_col].astype(str) if name_col else nodes["spotify_id"]
    nodes["popularity"] = pd.to_numeric(nodes_raw[pop_col], errors="coerce") if pop_col else pd.NA
    nodes["followers"] = pd.to_numeric(nodes_raw[followers_col], errors="coerce") if followers_col else pd.NA
    nodes["genre"] = nodes_raw[genre_col].apply(parse_primary_genre) if genre_col else "Unknown"
    nodes = nodes.drop_duplicates(subset=["spotify_id"])

    edges = pd.DataFrame()
    edges["source"] = edges_raw[source_col].astype(str)
    edges["target"] = edges_raw[target_col].astype(str)

    edges = edges.dropna().drop_duplicates()
    edges = edges[edges["source"] != edges["target"]]

    valid_ids = set(nodes["spotify_id"])
    edges = edges[
        edges["source"].isin(valid_ids)
        & edges["target"].isin(valid_ids)
    ]

    return nodes, edges


def build_graph(nodes, edges):
    G = nx.Graph()

    for row in nodes.itertuples(index=False):
        G.add_node(
            row.spotify_id,
            artist=row.artist,
            genre=row.genre,
            popularity=row.popularity,
            followers=row.followers,
        )

    G.add_edges_from(edges[["source", "target"]].itertuples(index=False, name=None))

    return G


def largest_component(G):
    if G.number_of_nodes() == 0:
        return G.copy()

    lcc_nodes = max(nx.connected_components(G), key=len)
    return G.subgraph(lcc_nodes).copy()


def summarize_communities(artist_communities):
    if artist_communities.empty:
        return pd.DataFrame(
            columns=[
                "community_rank",
                "community",
                "artist_count",
                "top_genre",
                "sample_artists",
            ]
        )

    summary = (
        artist_communities.groupby("community")
        .agg(
            artist_count=("spotify_id", "count"),
            top_genre=(
                "genre",
                lambda s: s.value_counts().index[0]
                if len(s.dropna())
                else "Unknown",
            ),
            sample_artists=(
                "artist",
                lambda s: ", ".join(list(s.dropna().astype(str).head(5))),
            ),
        )
        .reset_index()
        .sort_values("artist_count", ascending=False)
    )

    summary.insert(0, "community_rank", range(1, len(summary) + 1))

    return summary


def main():
    if community_louvain is None:
        raise ImportError("Missing python-louvain. Run: pip install python-louvain")

    print("Loading nodes.csv and edges.csv...")
    nodes, edges = load_data()

    print(f"Loaded {len(nodes):,} artists and {len(edges):,} collaborations.")

    print("Building graph...")
    G = build_graph(nodes, edges)
    G_lcc = largest_component(G)

    print(
        f"Largest component: {G_lcc.number_of_nodes():,} artists, "
        f"{G_lcc.number_of_edges():,} edges"
    )

    print("Running Louvain community detection...")
    partition = community_louvain.best_partition(G_lcc, random_state=42)

    artist_communities = pd.DataFrame(
        {
            "spotify_id": list(partition.keys()),
            "community": list(partition.values()),
        }
    )

    artist_communities = artist_communities.merge(nodes, on="spotify_id", how="left")
    community_summary = summarize_communities(artist_communities)

    artist_communities.to_csv(OUTPUT_DIR / "artist_communities.csv", index=False)
    community_summary.to_csv(OUTPUT_DIR / "community_summary.csv", index=False)

    print("Saved:")
    print("output/artist_communities.csv")
    print("output/community_summary.csv")
    print("Done. Now run: streamlit run dashboard.py")


if __name__ == "__main__":
    main()
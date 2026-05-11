# Charting Connections: Spotify Artist Collaboration Network

This project is a Streamlit dashboard that analyzes the Spotify Artist Feature Collaboration Network. The dashboard explores how artists are connected through feature collaborations and uses network analysis to study central artists, genre communities, and small-world structure.

## Project Overview

Artist collaborations are an important part of the music industry because they can help artists reach new audiences, connect different genres, and increase visibility. This project uses a network analysis approach to look beyond popularity and follower count by examining how artists are structurally connected to one another.

## Research Questions

**RQ1:** Which artists serve as the most central hubs or bridges in the Spotify collaboration network, and does an artist’s centrality relate to Spotify popularity or follower count?

**RQ2:** Do meaningful genre-based communities emerge from artist collaboration patterns, and do artists collaborate mostly within or across genre boundaries?

**RQ3:** Does the Spotify artist collaboration network show small-world properties, with high clustering and short path lengths that could help collaborations or music trends spread?

## Dataset

The project uses two main CSV files:

- `nodes.csv`: Contains artist information such as Spotify ID, artist name, followers, popularity, genres, and chart hits.
- `edges.csv`: Contains collaboration relationships between artists using Spotify artist IDs.

## Network Model

- **Nodes:** Spotify artists
- **Edges:** Feature collaborations between two artists
- **Network type:** Undirected and unweighted
- **Scope:** Static collaboration snapshot from 2013–2022

## Dashboard Features

The dashboard includes:

- Overview of the project and research questions
- Network summary metrics
- Centrality analysis for RQ1
- Genre and community analysis for RQ2
- Small-world analysis for RQ3
- Discussion, limitations, and ethical issues tab

## How to Run

1. Clone the repo

Install the required packages:

```bash
pip install -r requirements.txt
```
Then run the dashboard: 
```bash
streamlit run dashboard.py
```

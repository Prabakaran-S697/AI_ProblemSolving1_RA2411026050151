import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import copy
from matplotlib.patches import Patch

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Map Coloring CSP Solver",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
.stApp { background-color: #0f1219; color: #f1f5f9; }
[data-testid="stSidebar"] {
    background-color: #1a1f2e !important;
    border-right: 1px solid #2d3548;
}

/* Sidebar Text & Labels */
.stSidebar label, .stSidebar p, .stSidebar div {
    color: #cbd5e1 !important;
}
.stSidebar h1, .stSidebar h2, .stSidebar h3 {
    color: #f8fafc !important;
}

/* Input Fields - FORCED WHITE TEXT */
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    color: #ffffff !important;
    background-color: #242938 !important;
    -webkit-text-fill-color: #ffffff !important;
}

[data-testid="stTextInput"] > div > div,
[data-testid="stTextArea"] > div > div {
    background-color: #242938 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}

/* Primary Button */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    height: 52px !important;
    width: 100% !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
}

/* Secondary Button */
[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    width: 100% !important;
}

/* Metrics Cards - FIXED CONTRAST */
[data-testid="stMetric"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
[data-testid="stMetricLabel"] > div {
    color: #94a3b8 !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] > div {
    color: #f8fafc !important;
    font-weight: 800 !important;
}

[data-testid="stExpander"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}
hr { border-color: #334155 !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════
if "solution" not in st.session_state:
    st.session_state.solution = None
if "stats" not in st.session_state:
    st.session_state.stats = None
if "solved_regions" not in st.session_state:
    st.session_state.solved_regions = None
if "solved_neighbors" not in st.session_state:
    st.session_state.solved_neighbors = None
if "regions_input" not in st.session_state:
    st.session_state.regions_input = "A, B, C, D"
if "adjacency_input" not in st.session_state:
    st.session_state.adjacency_input = "A-B\nA-C\nB-C\nB-D\nC-D"

# ═══════════════════════════════════════════════════════════════
# CSP SOLVER BACKEND
# ═══════════════════════════════════════════════════════════════
colors_3 = ["Red", "Green", "Blue"]
colors_4 = ["Red", "Green", "Blue", "Yellow"]

color_map = {
    "Red": "#FF6B6B",
    "Green": "#6BCB77",
    "Blue": "#4D96FF",
    "Yellow": "#FFD93D"
}

emoji_map = {"Red": "🔴", "Green": "🟢", "Blue": "🔵", "Yellow": "🟡"}


def parse_input(regions_text, adjacency_text):
    regions = [r.strip().title() for r in regions_text.split(",") if r.strip()]
    neighbors = {r: set() for r in regions}
    errors = []
    for line in adjacency_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if "-" not in line:
            errors.append(f"Invalid format: '{line}' — use A-B format")
            continue
        parts = line.split("-", 1)
        a = parts[0].strip().title()
        b = parts[1].strip().title()
        if a == b:
            continue  # ignore self-loops
        if a not in regions:
            errors.append(f"Unknown region: '{a}'")
            continue
        if b not in regions:
            errors.append(f"Unknown region: '{b}'")
            continue
        neighbors[a].add(b)
        neighbors[b].add(a)
    return regions, neighbors, errors


def is_consistent(region, color, assignment, neighbors):
    for neighbor in neighbors.get(region, set()):
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True


def backtrack(assignment, regions, neighbors, colors, stats):
    if len(assignment) == len(regions):
        return assignment
    unassigned = [r for r in regions if r not in assignment]
    region = unassigned[0]
    for color in colors:
        stats["nodes"] += 1
        if is_consistent(region, color, assignment, neighbors):
            assignment[region] = color
            result = backtrack(assignment, regions, neighbors, colors, stats)
            if result is not None:
                return result
            del assignment[region]
            stats["backtracks"] += 1
    return None


def solve_map_coloring(regions, neighbors, colors):
    stats = {"nodes": 0, "backtracks": 0}
    result = backtrack({}, regions, neighbors, colors, stats)
    return result, stats


# ═══════════════════════════════════════════════════════════════
# TOP HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1a1f2e, #242938);
    border: 1px solid #2d3548;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
">
    <div style="display:flex; align-items:center; gap:14px;">
        <span style="font-size:40px;">🗺️</span>
        <div>
            <h1 style="margin:0; font-size:26px; font-weight:800;
                background: linear-gradient(135deg, #6366f1, #a5b4fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;">
                Map Coloring CSP Solver
            </h1>
            <p style="margin:4px 0 0; color:#94a3b8; font-size:13px;">
                Constraint Satisfaction Problem — Backtracking Algorithm
            </p>
        </div>
    </div>
    <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <span style="background:#064e3b; color:#10b981; padding:6px 14px;
            border-radius:50px; font-size:12px; font-weight:600;">
            🟢 CSP Engine Active
        </span>
        <span style="background:#1e1b4b; color:#a5b4fc; padding:6px 14px;
            border-radius:50px; font-size:12px; font-weight:600;">
            🎨 Backtracking Solver
        </span>
        <span style="background:#2d1b4e; color:#c084fc; padding:6px 14px;
            border-radius:50px; font-size:12px; font-weight:600;">
            ⚡ Graph Visualization
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# LEFT SIDEBAR
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style="text-align:center; padding:16px 0 20px;">
    <div style="font-size:36px; margin-bottom:8px;">🗺️</div>
    <div style="font-size:17px; font-weight:700; color:#f1f5f9;">
        Map Input Panel
    </div>
    <div style="font-size:12px; color:#94a3b8; margin-top:4px;">
        Define regions and adjacency
    </div>
    <div style="height:2px; background:linear-gradient(90deg,#6366f1,#a5b4fc);
        border-radius:2px; margin-top:16px;"></div>
</div>
""", unsafe_allow_html=True)

# ── Quick Load Examples ──
st.sidebar.markdown("""
<div style="background:#1e2330; border-left:3px solid #6366f1;
    border-radius:8px; padding:10px 14px; margin:16px 0 12px;">
    <span style="font-size:14px; font-weight:700; color:#f1f5f9;">
        ⚡ Quick Load Examples
    </span>
</div>
""", unsafe_allow_html=True)

ql_col1, ql_col2, ql_col3 = st.sidebar.columns([1, 1, 1.2])
with ql_col1:
    if st.button("Default"):
        st.session_state["regions_field"] = "A, B, C, D"
        st.session_state["adjacency_field"] = "A-B\nA-C\nB-C\nB-D\nC-D"
        st.session_state.solution = None
        st.rerun()
with ql_col2:
    if st.button("South India"):
        st.session_state["regions_field"] = "Maharashtra, Goa, Karnataka, Andhra Pradesh, Telangana, Kerala"
        st.session_state["adjacency_field"] = (
            "Maharashtra-Goa\nMaharashtra-Karnataka\nMaharashtra-Andhra Pradesh\n"
            "Maharashtra-Telangana\nGoa-Karnataka\nKarnataka-Andhra Pradesh\n"
            "Karnataka-Kerala\nKarnataka-Telangana\nAndhra Pradesh-Telangana"
        )
        st.session_state.solution = None
        st.rerun()
with ql_col3:
    if st.button("North India"):
        st.session_state["regions_field"] = "Punjab, Haryana, Himachal Pradesh, Rajasthan, Uttarakhand, UP, Delhi, J&K"
        st.session_state["adjacency_field"] = (
            "Punjab-Haryana\nPunjab-Himachal Pradesh\nPunjab-Rajasthan\nPunjab-J&K\n"
            "Haryana-Rajasthan\nHaryana-UP\nHaryana-Delhi\nHimachal Pradesh-Uttarakhand\n"
            "Himachal Pradesh-J&K\nUttarakhand-UP\nRajasthan-UP\nDelhi-UP"
        )
        st.session_state.solution = None
        st.rerun()

# ── Manual Entry Guide ──
with st.sidebar.expander("📖 How to Create Your Own"):
    st.markdown("""
    <div style="font-size:12px; color:#94a3b8;">
        1. <b>List States:</b> Type names in the first box (e.g. <i>Bihar, Sikkim</i>).<br><br>
        2. <b>Define Borders:</b> In the second box, type <i>State1-State2</i> for every pair that touches.<br><br>
        3. <b>Solve:</b> Click the button below to see the AI color your custom map!
    </div>
    """, unsafe_allow_html=True)

# ── Region Names ──
st.sidebar.markdown("""
<div style="background:#1e2330; border-left:3px solid #10b981;
    border-radius:8px; padding:10px 14px; margin:16px 0 12px;">
    <span style="font-size:14px; font-weight:700; color:#f1f5f9;">
        📍 Region Names
    </span>
</div>
""", unsafe_allow_html=True)

regions_text = st.sidebar.text_input(
    "Enter regions separated by commas",
    placeholder="A, B, C, D",
    key="regions_field"
)

# ── Adjacency Pairs ──
st.sidebar.markdown("""
<div style="background:#1e2330; border-left:3px solid #f59e0b;
    border-radius:8px; padding:10px 14px; margin:16px 0 12px;">
    <span style="font-size:14px; font-weight:700; color:#f1f5f9;">
        🔗 Adjacency Pairs
    </span>
</div>
""", unsafe_allow_html=True)

adjacency_text = st.sidebar.text_area(
    "Enter one pair per line (format: A-B)",
    height=180,
    key="adjacency_field"
)

st.sidebar.markdown("""
<div style="background:#1a1f2e; border:1px solid #2d3548; border-radius:8px;
    padding:10px 14px; margin-bottom:12px;">
    <span style="color:#94a3b8; font-size:12px;">
        💡 If A and B are neighbors, write A-B on one line
    </span>
</div>
""", unsafe_allow_html=True)

# ── Color Settings ──
st.sidebar.markdown("""
<div style="background:#1e2330; border-left:3px solid #ef4444;
    border-radius:8px; padding:10px 14px; margin:16px 0 12px;">
    <span style="font-size:14px; font-weight:700; color:#f1f5f9;">
        🎨 Color Settings
    </span>
</div>
""", unsafe_allow_html=True)

num_colors = st.sidebar.radio(
    "Number of Colors",
    options=[3, 4],
    index=0,
    horizontal=True
)

if num_colors == 3:
    st.sidebar.markdown("""
    <div style="display:flex; gap:8px; margin:8px 0 16px;">
        <span style="background:#FF6B6B; padding:4px 12px; border-radius:50px;
            color:white; font-size:12px; font-weight:600;">🔴 Red</span>
        <span style="background:#6BCB77; padding:4px 12px; border-radius:50px;
            color:white; font-size:12px; font-weight:600;">🟢 Green</span>
        <span style="background:#4D96FF; padding:4px 12px; border-radius:50px;
            color:white; font-size:12px; font-weight:600;">🔵 Blue</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div style="display:flex; gap:8px; margin:8px 0 16px; flex-wrap:wrap;">
        <span style="background:#FF6B6B; padding:4px 12px; border-radius:50px;
            color:white; font-size:12px; font-weight:600;">🔴 Red</span>
        <span style="background:#6BCB77; padding:4px 12px; border-radius:50px;
            color:white; font-size:12px; font-weight:600;">🟢 Green</span>
        <span style="background:#4D96FF; padding:4px 12px; border-radius:50px;
            color:white; font-size:12px; font-weight:600;">🔵 Blue</span>
        <span style="background:#FFD93D; padding:4px 12px; border-radius:50px;
            color:#333; font-size:12px; font-weight:600;">🟡 Yellow</span>
    </div>
    """, unsafe_allow_html=True)

# ── Action Buttons ──
solve_btn = st.sidebar.button("🎨 Solve Coloring", type="primary")
clear_btn = st.sidebar.button("↺ Clear All", type="secondary")

# ═══════════════════════════════════════════════════════════════
# BUTTON LOGIC
# ═══════════════════════════════════════════════════════════════
if clear_btn:
    st.session_state.solution = None
    st.session_state.stats = None
    st.session_state.solved_regions = None
    st.session_state.solved_neighbors = None
    st.session_state.regions_input = "A, B, C, D"
    st.session_state.adjacency_input = "A-B\nA-C\nB-C\nB-D\nC-D"
    st.rerun()

if solve_btn:
    regions, neighbors, errors = parse_input(regions_text, adjacency_text)
    if errors:
        for e in errors:
            st.warning(e)
    else:
        chosen_colors = colors_3 if num_colors == 3 else colors_4
        solution, stats = solve_map_coloring(regions, neighbors, chosen_colors)
        st.session_state.solution = solution
        st.session_state.stats = stats
        st.session_state.solved_regions = regions
        st.session_state.solved_neighbors = neighbors

# ═══════════════════════════════════════════════════════════════
# MAIN OUTPUT PANEL
# ═══════════════════════════════════════════════════════════════
solution = st.session_state.solution
stats = st.session_state.stats
regions = st.session_state.solved_regions
neighbors = st.session_state.solved_neighbors

if solution is None and stats is None:
    # ── Welcome Card ──
    st.markdown("""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-size:80px; margin-bottom:20px;">🗺️</div>
        <h2 style="color:#f1f5f9; font-size:24px; font-weight:700;">
            Map Coloring CSP Solver
        </h2>
        <p style="color:#94a3b8; font-size:15px; max-width:500px;
            margin:12px auto;">
            Enter regions and their adjacency relationships, then click
            Solve Coloring to see the AI assign colors using CSP backtracking
        </p>
        <div style="display:flex; justify-content:center; gap:20px;
            margin-top:32px; flex-wrap:wrap;">
            <div style="background:#242938; border:1px solid #2d3548;
                border-radius:12px; padding:20px 28px; min-width:140px;">
                <div style="font-size:28px;">📍</div>
                <div style="color:#f1f5f9; font-weight:600; margin-top:8px;">
                    Input Regions
                </div>
                <div style="color:#94a3b8; font-size:12px; margin-top:4px;">
                    Name your map areas
                </div>
            </div>
            <div style="background:#242938; border:1px solid #2d3548;
                border-radius:12px; padding:20px 28px; min-width:140px;">
                <div style="font-size:28px;">🔗</div>
                <div style="color:#f1f5f9; font-weight:600; margin-top:8px;">
                    Set Adjacency
                </div>
                <div style="color:#94a3b8; font-size:12px; margin-top:4px;">
                    Define neighbors
                </div>
            </div>
            <div style="background:#242938; border:1px solid #2d3548;
                border-radius:12px; padding:20px 28px; min-width:140px;">
                <div style="font-size:28px;">🎨</div>
                <div style="color:#f1f5f9; font-weight:600; margin-top:8px;">
                    Get Solution
                </div>
                <div style="color:#94a3b8; font-size:12px; margin-top:4px;">
                    AI assigns colors
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif solution is not None:
    # ── SECTION A: Result Banner (Success) ──
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 1px solid #10b981;
        border-left: 6px solid #10b981;
        border-radius: 16px;
        padding: 28px 36px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(16,185,129,0.2);
    ">
        <div style="display:flex; align-items:center; gap:16px;">
            <span style="font-size:44px;">✅</span>
            <div>
                <div style="font-size:26px; font-weight:800; color:#ffffff;">
                    VALID COLORING FOUND
                </div>
                <div style="font-size:14px; color:#6ee7b7; margin-top:4px;">
                    All adjacent regions have different colors
                </div>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:12px; color:#6ee7b7;">COLORS USED</div>
            <div style="font-size:32px; font-weight:800; color:#10b981;">
                {len(set(solution.values()))}
            </div>
            <div style="font-size:12px; color:#6ee7b7;">of {num_colors} available</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION B: Metrics Row ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📍 Total Regions", len(regions))
    with col2:
        st.metric("🔗 Adjacency Pairs", sum(len(v) for v in neighbors.values()) // 2)
    with col3:
        st.metric("🎨 Colors Used", len(set(solution.values())))
    with col4:
        st.metric("🔄 Backtracks", stats["backtracks"])

    # ── SECTION C: Table + Graph ──
    col_left, col_right = st.columns([1, 1.5])

    with col_left:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
            <span style="font-size:18px;">📋</span>
            <span style="font-size:16px; font-weight:700; color:#f1f5f9;">
                Color Assignment
            </span>
        </div>
        """, unsafe_allow_html=True)

        df = pd.DataFrame([
            {
                "Region": region,
                "Assigned Color": color,
                "Preview": emoji_map.get(color, "⚪")
            }
            for region, color in solution.items()
        ])
        st.dataframe(df, use_container_width=True)

    with col_right:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
            <span style="font-size:18px;">🕸️</span>
            <span style="font-size:16px; font-weight:700; color:#f1f5f9;">
                Graph Visualization
            </span>
        </div>
        """, unsafe_allow_html=True)

        G = nx.Graph()
        G.add_nodes_from(regions)
        for region, nbrs in neighbors.items():
            for nbr in nbrs:
                G.add_edge(region, nbr)

        node_colors = [color_map[solution[r]] for r in G.nodes()]

        fig, ax = plt.subplots(figsize=(7, 5))
        fig.patch.set_facecolor("#1a1f2e")
        ax.set_facecolor("#1a1f2e")

        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                               node_size=2000, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=11,
                                font_color="white", font_weight="bold", ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="#94a3b8",
                               width=2, ax=ax)

        used_colors = set(solution.values())
        legend_elements = [
            Patch(facecolor=color_map[c], label=c)
            for c in used_colors
        ]
        ax.legend(handles=legend_elements, loc="upper right",
                  facecolor="#242938", labelcolor="white",
                  edgecolor="#2d3548")

        ax.set_title("Map Coloring Result", color="#f1f5f9",
                      fontsize=14, fontweight="bold", pad=15)
        ax.axis("off")
        st.pyplot(fig)
        plt.close(fig)

    # ── SECTION D: CSP Backtracking Steps ──
    with st.expander("🔗 View CSP Backtracking Steps"):
        st.markdown(f"""
        <div style="color:#94a3b8; font-size:14px; line-height:1.8;">
            The CSP backtracking solver explored
            <strong style="color:#6366f1;">{stats['nodes']} nodes</strong>
            and made
            <strong style="color:#f59e0b;">{stats['backtracks']} backtracks</strong>
            to find the solution.
            <br><br>
            <strong style="color:#f1f5f9;">Assignment Order:</strong>
        </div>
        """, unsafe_allow_html=True)

        for i, (region, color) in enumerate(solution.items(), 1):
            emoji = emoji_map.get(color, "⚪")
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#064e3b,#065f46);
                border:1px solid #10b981; border-radius:10px;
                padding:12px 20px; margin-bottom:8px;
                display:flex; align-items:center; gap:14px;">
                <div style="background:#10b981; color:#fff; border-radius:50%;
                    width:28px; height:28px; display:flex; align-items:center;
                    justify-content:center; font-weight:700; font-size:13px;
                    flex-shrink:0;">{i}</div>
                <div style="color:#ecfdf5; font-size:14px; font-weight:500;">
                    Region <strong>{region}</strong> →
                    tried colors → assigned
                    <strong>{emoji} {color}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e1b4b,#2d1b69);
            border:2px solid #6366f1; border-radius:12px;
            padding:16px 24px; margin-top:8px;
            display:flex; align-items:center; gap:14px;">
            <span style="font-size:22px;">⚖️</span>
            <span style="color:#e0e7ff; font-size:15px; font-weight:700;">
                Final: Valid {len(set(solution.values()))}-coloring found
                — No two adjacent regions share the same color ✅
            </span>
        </div>
        """, unsafe_allow_html=True)

else:
    # ── No solution found ──
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        border: 1px solid #ef4444;
        border-left: 6px solid #ef4444;
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
    ">
        <div style="display:flex; align-items:center; gap:16px;">
            <span style="font-size:44px;">❌</span>
            <div>
                <div style="font-size:26px; font-weight:800; color:#ffffff;">
                    NO SOLUTION FOUND
                </div>
                <div style="font-size:14px; color:#fca5a5; margin-top:4px;">
                    Try increasing colors to 4
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if regions and neighbors:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📍 Total Regions", len(regions))
        with col2:
            st.metric("🔗 Adjacency Pairs", sum(len(v) for v in neighbors.values()) // 2)
        with col3:
            st.metric("🎨 Colors Used", 0)
        with col4:
            st.metric("🔄 Backtracks", stats["backtracks"])

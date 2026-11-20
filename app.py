import streamlit as st
import pandas as pd
import plotly.express as px
import time
from core.models import Task, Server
from strategies.round_robin import RoundRobinStrategy
from strategies.least_load import LeastLoadStrategy

st.set_page_config(page_title="Distributed Resource Optimizer", page_icon="⚡", layout="wide")

st.title("⚡ Distributed Resource Optimizer (DRO)")
st.caption("Discrete-Event Simulation & Real-Time Load Balancer Metrics")

with st.expander("ℹ️ System Architecture & Mechanics", expanded=False):
    st.markdown("""
    * **Task Queue:** Ingests non-uniform compute payloads uniformly sampled between 1 and 10 duration units.
    * **Round Robin ($O(1)$):** Blindly cycles through server nodes, risking skewness under heterogeneous tasks.
    * **Least Load ($O(1)$ lookup via Min-Heap):** Dynamically inspects server loads, targeting optimal system equilibrium.
    """)

# Sidebar
st.sidebar.header("⚙️ Simulation Controls")
num_servers = st.sidebar.slider("Active Server Nodes", 3, 10, 5)
num_tasks = st.sidebar.slider("Task Ingestion Size", 20, 200, 100, 10)
step_speed = st.sidebar.slider("Telemetry Delay (s)", 0.0, 0.1, 0.02, 0.01)
run_btn = st.sidebar.button("🚀 Execute Comparative Benchmark", type="primary")

col_rr, col_ll = st.columns(2)
with col_rr:
    st.subheader("1️⃣ Static: Round Robin")
    rr_chart = st.empty()
    rr_stat = st.empty()

with col_ll:
    st.subheader("2️⃣ Dynamic: Least Load (Heap-Optimized)")
    ll_chart = st.empty()
    ll_stat = st.empty()

if run_btn:
    servers_rr = [Server(f"Node-{i+1}") for i in range(num_servers)]
    servers_ll = [Server(f"Node-{i+1}") for i in range(num_servers)]
    tasks = [Task(i) for i in range(num_tasks)]
    
    rr_algo = RoundRobinStrategy()
    ll_algo = LeastLoadStrategy(servers_ll)

    prog_bar = st.progress(0, text="Simulating distributed workload...")

    for idx, task in enumerate(tasks):
        rr_algo.assign_task(servers_rr, task)
        ll_algo.assign_task(servers_ll, task)

        prog_bar.progress((idx + 1) / len(tasks))

        if idx % 2 == 0 or idx == len(tasks) - 1:
            # Update RR Chart
            df_rr = pd.DataFrame({
                "Server": [s.name for s in servers_rr],
                "Cumulative Load": [s.total_load for s in servers_rr]
            })
            fig_rr = px.bar(df_rr, x="Server", y="Cumulative Load", color="Cumulative Load", color_continuous_scale="Reds")
            fig_rr.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
            rr_chart.plotly_chart(fig_rr, use_container_width=True, key=f"rr_{idx}")

            # Update LL Chart
            df_ll = pd.DataFrame({
                "Server": [s.name for s in servers_ll],
                "Cumulative Load": [s.total_load for s in servers_ll]
            })
            fig_ll = px.bar(df_ll, x="Server", y="Cumulative Load", color="Cumulative Load", color_continuous_scale="Teal")
            fig_ll.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
            ll_chart.plotly_chart(fig_ll, use_container_width=True, key=f"ll_{idx}")

            if step_speed > 0:
                time.sleep(step_speed)

    prog_bar.empty()

    # Metrics computation
    loads_rr = [s.total_load for s in servers_rr]
    loads_ll = [s.total_load for s in servers_ll]
    imb_rr = max(loads_rr) - min(loads_rr)
    imb_ll = max(loads_ll) - min(loads_ll)
    reduction = ((imb_rr - imb_ll) / imb_rr * 100) if imb_rr > 0 else 0

    with col_rr:
        rr_stat.metric("Load Imbalance (Max - Min)", f"{imb_rr} units", f"Peak Node: {max(loads_rr)}", delta_color="off")
    with col_ll:
        ll_stat.metric("Load Imbalance (Max - Min)", f"{imb_ll} units", f"{reduction:.1f}% Bottleneck Reduction", delta_color="normal")
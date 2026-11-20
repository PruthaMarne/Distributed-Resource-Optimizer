# ⚡ Distributed Resource Optimizer (DRO)

A modular, high-throughput discrete-event task scheduling simulation comparing static and state-aware load balancing policies across distributed server clusters.

## 🚀 Features
- **Strategy Pattern Architecture:** Decoupled routing algorithms enabling seamless runtime policy swapping.
- **Priority Queue Optimization:** Least Load algorithm implemented with a Min-Heap (`heapq`), optimizing lookup to $O(1)$ and state updates to $O(\log N)$.
- **Interactive UI Dashboard:** Built with Streamlit and Plotly for real-time workload tracking and load variance visualization.
- **Automated Testing Suite:** Thoroughly tested using `pytest`.

## 📊 Benchmark Summary
| Metric | Round Robin (Static) | Least Load (Dynamic Heap) | Impact |
| :--- | :--- | :--- | :--- |
| **Complexity** | $O(1)$ | $O(1)$ retrieval / $O(\log N)$ update | Optimal Scale |
| **Task Disparity** | Equal count | Load-balanced count | Prevents idle nodes |
| **Load Imbalance** | High | Minimized (~89% reduction) | Eliminates hotspots |

## 🛠️ Installation & Execution

1. **Clone repository:**
   ```bash
   git clone [https://github.com/PruthaMarne/Distributed-Resource-Optimizer.git](https://github.com/PruthaMarne/Distributed-Resource-Optimizer.git)
   cd distributed_resource_optimizer

2. **Create and activate a virtual environment**
python -m venv venv
# On Windows (PowerShell):
venv\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Run the application**
# On Streamlit
streamlit run app.py
# On CLI Benchmark (Terminal Output)
python main.py
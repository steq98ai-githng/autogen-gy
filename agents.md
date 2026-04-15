# AGENTS.md - JULES Self-Evolution Ecosystem (autogen-gy)

## 🏗 Project Vision
This repository is designed as an **Autonomous Software Evolution Factory**. By integrating Google Labs' **JULES** with iterative research frameworks, we aim to achieve "Continuous Intelligence." The system functions as a closed-loop laboratory where AI agents analyze codebase context, formulate hypotheses, implement changes, and verify results autonomously.

The core objective function is: **Minimize $val\_bpb$ (Validation Bits-Per-Byte) and maximize System CP Value (Cost-Performance) without compromising inference speed.**

---

## 📊 System Architecture & Infrastructure
The project leverages JULES as a cloud-based asynchronous execution engine. All agent activities follow the sandboxed workflow illustrated below:

<img width="1054" height="927" alt="image" src="https://github.com/user-attachments/assets/f1841106-11bf-4252-97e9-8fd798a62eb1" />

1.  **Context Loading**: JULES scans `AGENTS.md` and the entire repository (utilizing Gemini 3 Pro's 2M context window) to understand its operational boundaries.
2.  **VM Sandboxing**: All commands (`uv run`, tests, builds) are executed in isolated Google Cloud VMs to protect the local environment.
3.  **Autonomous Delivery**: Successful optimizations are delivered via GitHub Pull Requests (PRs) accompanied by detailed experiment logs and performance metrics.

---

## 🤖 Agent Roles & Responsibilities

| Role | Key Responsibility | Primary Assets |
| :--- | :--- | :--- |
| **Strategist (Teacher)** | **The Brain**. Translates high-level research (arXiv, web reports) into actionable logic within `program.md`. | `program.md`, `research/` |
| **Operator (Student)** | **The Hands**. Executes code modifications, refactors, and hyperparameter tuning within `train.py` based on strategic guidance. | `train.py` |
| **Critic (Evaluator)** | **The Gatekeeper**. Runs `prepare.py` to act as a neutral judge. Validates if the PR meets performance and safety criteria. | `prepare.py`, `tests/` |
| **Scout (Tooling)** | **The Facilitator**. Discovers and integrates new **MCP (Model Context Protocol)** servers to expand agent capabilities. | `mcp.json` |

---

## 🛡 Engineering Guardrails
To maintain system integrity, JULES must adhere to the following strict constraints:

1.  **The Three-File Contract**:
    * `prepare.py`: **IMMUTABLE**. Agents are strictly forbidden from modifying the evaluation logic or dataset preparation.
    * `train.py`: **MUTABLE**. The primary sandbox for agent experimentation.
    * `program.md`: **STRATEGIC**. Directional guidance authored by the human operator or the Strategist agent.
2.  **300-Second Budget**: Every experiment must complete its validation run within **300 seconds** to ensure high-frequency iteration.
3.  **Auto-Revert Protocol**: If a modification leads to an increase in $val\_bpb$ or causes a build failure, the agent must perform an immediate `git revert`.
4.  **Atomic Changes**: Keep PRs focused. Single-task changes (under 100 lines) are prioritized for reviewability and stability.

---

## 🧬 Self-Evolution Protocol
* **Step 1 (Ingestion)**: Monitor GitHub Issues for optimization requests or architectural bottlenecks.
* **Step 2 (Planning)**: Teacher agent updates `program.md` with the latest optimization strategy.
* **Step 3 (Execution)**: Student agent modifies `train.py` in a cloud VM and runs the 300s benchmark.
* **Step 4 (Validation)**: Evaluator agent checks the resulting bit-per-byte score.
* **Step 5 (Persistence)**: Successful strategies are logged in `.agent/skills` and merged via PR.

---

### 💡 Developer Notes
* **Triggering JULES**: When initiating tasks at `jules.google.com`, always include: *"Refer to AGENTS.md for system architecture and role constraints."*
* **MCP Integration**: Ensure your `mcp.json` is updated with relevant tools (e.g., Jira for task tracking or Chrome DevTools for UI testing) to provide the agents with more "hands."

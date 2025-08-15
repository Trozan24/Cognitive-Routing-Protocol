# Cognitive Routing Protocol (CRP)

[![Project Status: Prototype Complete](https://img.shields.io/badge/status-prototype_complete-brightgreen.svg)](https://github.com/Yudis-bit/Cognitive-Routing-Protocol)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This repository contains the complete architecture and functional prototype for the **Cognitive Routing Protocol (CRP)**, a Layer-0/Layer-1 enhancement protocol designed to fundamentally reshape the efficiency, resilience, and profitability of Decentralized Physical Infrastructure Networks (DePIN).

---

## Key Findings from the Prototype

The Python prototype in this repository has successfully validated the core hypothesis of CRP. A comparative analysis between a "Dumb Router" (using Dijkstra's algorithm) and a "Cognitive Router" (using Reinforcement Learning) demonstrated:

* **✅ Adaptive Routing:** The Cognitive Router successfully learned to **dynamically avoid a congested network link**, using it less than **0.1%** of the time, compared to the Dumb Router which was stuck in congestion nearly **40%** of the time.
* **🚀 Performance Gains:** By avoiding these bottlenecks, the Cognitive Router achieved **~22% lower average latency** for successful packet deliveries, proving its ability to optimize for overall network health.
* **📊 Full Analysis:** The complete comparative simulation can be run via the `simulations/run_cognitive_sim.py` script.

## Full Project Architecture

The protocol is designed with two primary components working in tandem:

1.  **Off-Chain AI Core (Python):**
    * A discrete-event simulation environment for modeling a DePIN.
    * A **Cognitive Node** agent equipped with a Reinforcement Learning model (Multi-Armed Bandit) to make intelligent, adaptive routing decisions.

2.  **On-Chain Trust Layer (Solidity):**
    * A `NodeRegistry` smart contract on an Ethereum-compatible blockchain to handle the economic and trust logic.
    * Its core functions include node registration, a staking mechanism for collateral, and an on-chain reputation system (`TrustScore`) to incentivize good behavior.

## Tech Stack

* **Simulation & AI Core**: Python 3.10+
* **Smart Contracts**: Solidity ^0.8.20
* **Contract Development Environment**: Hardhat
* **Blockchain Interaction**: Web3.py
* **Dependencies**: OpenZeppelin Contracts

## Project Structure (Monorepo)

This project uses a monorepo structure to cleanly separate the simulation logic from the smart contract code.

cognitive-routing-protocol/
├── contracts/          # Hardhat Project & Smart Contracts
│   ├── contracts/
│   │   ├── INodeRegistry.sol
│   │   └── NodeRegistry.sol
│   ├── scripts/
│   └── package.json
│
├── simulation/         # Python Prototype & Simulation
│   ├── crp/
│   └── simulations/
│
└── .gitignore          # Ignores files for both projects


## Getting Started

To run this project locally, you'll need to set up both the simulation and contract environments.

### 1. Running the Python Simulation

1.  **Navigate to the simulation folder:**
    ```bash
    cd simulation
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # Example for Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Run the comparative simulation:**
    This script will run the Dumb Router vs. the Cognitive Router and display the final performance analysis.
    ```bash
    python simulations/run_cognitive_sim.py
    ```

### 2. Working with the Smart Contracts

1.  **Navigate to the contracts folder:**
    ```bash
    cd contracts
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
3.  **Compile the contracts:**
    This command will check for errors and generate the necessary ABI files.
    ```bash
    npx hardhat compile
    ```
4.  **(Optional) Deploy to a testnet:**
    You can configure `hardhat.config.js` with your RPC URL and private key to deploy the contract.

## Completed Roadmap

* [x] **Phase 0: Architecture & Whitepaper** - Conceptual design and vision.
* [x] **Phase 1: Simulation Environment** - Modular testbed development in Python.
* [x] **Phase 2: "Dumb" Router (Baseline)** - Dijkstra's algorithm implementation for benchmarking.
* [x] **Phase 3: Cognitive Node (AI Core)** - AI agent implementation with a Multi-Armed Bandit model.
* [x] **Phase 4: Integration & Comparative Analysis** - Validation of CRP's performance benefits.
* [x] **Phase 5: On-Chain Component Design (Solidity)** - Smart contract architecture for trust and staking.

## Contributing

Contributions are welcome. Please fork the repository, create a dedicated feature branch for your work, and submit a pull request.

## License

This project is licensed under the MIT License.
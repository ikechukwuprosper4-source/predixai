# PredixMarket: Decentralized AI-Powered Prediction Platform 🏟️🚀

**PredixMarket** is a next-generation platform where users can predict real-world events and earn rewards based on their accuracy. Unlike traditional markets, PredixMarket uses **Autonomous AI Agents** to discover, curate, and resolve prediction events in real-time.

## 🌟 Key Features

1.  **AI-Generated Markets**: Our **Market Curator Agent** scans global news, social media (X/Twitter), and blockchain activity to automatically create high-interest prediction events.
2.  **Autonomous Resolution**: No centralized human "judges." Our **AI Oracle Agent** verifies the outcome of events using multiple trusted news sources and resolves markets automatically.
3.  **Predict & Earn**: A seamless user interface for placing "Yes" or "No" predictions. Your earnings are calculated based on market depth and timing.
4.  **Community-Driven**: Users can propose new markets and earn a "Creator Reward" when their markets gain traction.
5.  **Web3 Ready**: Integrated with Polygon (USDC) for instant payouts and transparent transactions.

## 🛠 Project Components

- **Frontend**: Streamlit-based "Marketplace" for users to browse, predict, and track earnings.
- **Backend (Agents)**: 
    - `CuratorAgent`: Discovers and creates markets.
    - `OracleAgent`: Resolves finished markets.
- **Engine**: A lightweight Constant Product Market Maker (CPMM) logic to determine Yes/No prices.

## 📦 Setup & Deployment

1.  **Clone and Install**
    ```bash
    git clone <repo-url>
    cd predixmarket
    pip install -r requirements.txt
    ```

2.  **Configure API Keys**
    - `GROQ_API_KEY`: Powering the AI Agents.
    - `TAVILY_API_KEY`: For real-time news search.
    - `POLYGON_PRIVATE_KEY`: For payouts and market creation.

3.  **Launch the Platform**
    ```bash
    streamlit run ui/app.py
    ```

4.  **Launch the AI Agent Backend**
    ```bash
    python main.py --mode worker
    ```

## 🛡 Disclaimer
This is an experimental platform. Predict responsibly.

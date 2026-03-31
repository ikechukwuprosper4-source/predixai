import streamlit as st
import pandas as pd
import os
import json
import time
from datetime import datetime
from predixmarket.core.engine import MarketEngine

# Configuration
st.set_page_config(page_title="PredixMarket: Predict & Earn 🏟️", layout="wide", page_icon="🏟️")

# Initialize Engine
engine = MarketEngine()

# Simulated Wallet (In production, this would be a real Web3 wallet)
if "wallet_balance" not in st.session_state:
    st.session_state.wallet_balance = 1000.0
if "predictions" not in st.session_state:
    st.session_state.predictions = []

# Sidebar Navigation
with st.sidebar:
    st.title("🏟️ PredixMarket")
    st.image("https://img.icons8.com/nolan/128/prediction.png", width=100)
    st.divider()
    st.metric("My Balance", f"${st.session_state.wallet_balance:.2f} USDC")
    st.divider()
    st.subheader("Your Profile")
    st.write("Mavitan CEO")
    st.caption("Pro Predictor 🎖️")
    st.divider()
    if st.button("🔌 Reconnect Wallet", use_container_width=True):
        st.success("Wallet connected via Polygon.")

# Main Dashboard
st.title("⛓️ Mavitan PredixMarket: Decentralized Predictions")
st.caption("AI-powered prediction platform where you earn for accuracy.")

# 1. Platform Tabs
tab_browse, tab_my, tab_create = st.tabs(["🔍 Browse Markets", "📈 My Predictions", "🤖 AI Market Creator"])

# Tab 1: Browse Markets
with tab_browse:
    st.header("Active Prediction Events")
    
    # Filter by Category
    category = st.selectbox("Category", ["All", "Politics", "Crypto", "Entertainment", "Sports"])
    
    # Load markets from Engine
    markets = engine.markets
    active_markets = [m for m in markets.values() if m["status"] == "OPEN"]
    
    if not active_markets:
        st.info("No active markets. Ask the AI Curator to generate some!")
    else:
        # Display as grid
        cols = st.columns(2)
        for i, m in enumerate(active_markets):
            with cols[i % 2]:
                with st.container(border=True):
                    st.subheader(f"{m['title']} (Closing: {m['end_date']})")
                    st.write(m['description'])
                    
                    prices = engine.get_price(m['id'])
                    
                    # Columns for Yes/No prices
                    p1, p2 = st.columns(2)
                    with p1:
                        st.metric("YES Price", f"${prices['yes']:.2f}", help="Current cost of a YES share.")
                    with p2:
                        st.metric("NO Price", f"${prices['no']:.2f}", delta_color="inverse")
                    
                    # Prediction Actions
                    bet_amount = st.number_input(f"Bet Amount (USDC) for {m['id']}", 10.0, step=10.0, key=f"amt_{m['id']}")
                    col_b1, col_b2 = st.columns(2)
                    
                    with col_b1:
                        if st.button(f"Predict YES on {m['id']}", type="primary", use_container_width=True):
                            if st.session_state.wallet_balance >= bet_amount:
                                engine.predict(m['id'], "YES", bet_amount, "user_1")
                                st.session_state.wallet_balance -= bet_amount
                                st.session_state.predictions.append({
                                    "market": m['title'],
                                    "side": "YES",
                                    "amount": bet_amount,
                                    "entry_price": prices['yes'],
                                    "time": datetime.now().strftime("%H:%M:%S")
                                })
                                st.success("Prediction Placed! 🚀")
                                st.rerun()
                            else:
                                st.error("Insufficient Balance.")
                                
                    with col_b2:
                        if st.button(f"Predict NO on {m['id']}", use_container_width=True):
                            if st.session_state.wallet_balance >= bet_amount:
                                engine.predict(m['id'], "NO", bet_amount, "user_1")
                                st.session_state.wallet_balance -= bet_amount
                                st.session_state.predictions.append({
                                    "market": m['title'],
                                    "side": "NO",
                                    "amount": bet_amount,
                                    "entry_price": prices['no'],
                                    "time": datetime.now().strftime("%H:%M:%S")
                                })
                                st.success("Prediction Placed! 🚀")
                                st.rerun()

# Tab 2: My Predictions
with tab_my:
    st.header("My Portfolio & Earnings")
    if not st.session_state.predictions:
        st.write("You haven't placed any predictions yet.")
    else:
        df_p = pd.DataFrame(st.session_state.predictions)
        st.table(df_p)
        
        # Simulated Earnings Chart
        st.subheader("Estimated Earnings Projection")
        st.line_chart([100, 110, 125, 140, 135, 150]) # Dummy data

# Tab 3: AI Market Curator (Admin)
with tab_create:
    st.header("🤖 Autonomous Market Curator")
    st.write("Our AI Agent scans global news and proposes new markets for users to earn from.")
    
    if st.button("🚀 Trigger AI Market Discovery", type="primary"):
        with st.status("AI Agent is scanning the news..."):
            st.write("Connecting to Groq (Llama-3)...")
            st.write("Analyzing current news for 'high-volatility events'...")
            time.sleep(2)
            st.write("Analyzing social sentiment on X/Twitter...")
            time.sleep(1)
            
            # Simulated AI Market Proposals
            new_market = {
                "title": "Will Bitcoin reach $100,000 by May 2026?",
                "category": "Crypto",
                "description": "BTC has been trending upwards. Will it break the legendary $100k barrier?",
                "end_date": "2026-05-31"
            }
            
            st.success("New Market Discovered!")
            st.json(new_market)
            
            if st.button("Confirm & Deploy Market"):
                mid = engine.create_market(new_market['title'], new_market['category'], new_market['description'], new_market['end_date'])
                st.success(f"Market Deploy Successful! (ID: {mid})")
                st.rerun()

# 4. Global Footer
st.divider()
st.caption("Mavitan PredixMarket © 2026. Built by elite AI engineers.")

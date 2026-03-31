import os
import json
from typing import Dict, List, Optional
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from loguru import logger
from datetime import datetime

class ProposedMarket(BaseModel):
    """Structured output for the AI Curator to suggest a new market."""
    title: str = Field(description="A catchy, concise title for the prediction event.")
    category: str = Field(description="Politics, Crypto, Entertainment, or Sports.")
    description: str = Field(description="A brief, clear description of the event.")
    end_date: str = Field(description="Resolution date in YYYY-MM-DD format.")
    reasoning: str = Field(description="Why this market is relevant now.")

class CuratorAgent:
    """
    AI Market Curator Agent responsible for scanning the news 
    and proposing high-interest prediction markets for users.
    """
    def __init__(self, model_name: str = "llama3-70b-8192"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.warning("GROQ_API_KEY missing. Curator will operate in SIMULATION mode.")
            self.llm = None
        else:
            self.llm = ChatGroq(model=model_name, api_key=self.api_key)
            
        self.search_tool = DuckDuckGoSearchRun()

    def discover_markets(self, topic: str = "world news and finance") -> List[ProposedMarket]:
        """
        Scans news for high-interest events and returns proposed markets.
        """
        logger.info(f"AI Curator scanning news for topic: {topic}")
        
        # Step 1: Perform Web Search (Free)
        query = f"breaking news and high-interest upcoming events in {topic}"
        try:
            news_data = self.search_tool.run(query)
        except Exception as e:
            logger.error(f"Search failed: {e}")
            news_data = "No news data found."

        # Step 2: Use LLM to propose a market
        if not self.llm:
            # Fallback for simulation
            return [ProposedMarket(
                title="Will Bitcoin reach $100k by 2026?",
                category="Crypto",
                description="Analysis of BTC trends suggests a potential breakout.",
                end_date="2026-12-31",
                reasoning="High-interest topic with high volatility."
            )]

        prompt = ChatPromptTemplate.from_template("""
        You are a visionary Prediction Market Curator. 
        Analyze the following news data and propose THREE high-interest prediction markets.
        
        News Data: {data}
        
        Criteria for a good market:
        1. It must be binary (YES or NO outcome).
        2. It must have a clear, verifiable resolution date.
        3. It must be interesting enough to attract 'Predict & Earn' users.
        
        Output format: Valid JSON as a list of ProposedMarket schemas.
        """)
        
        try:
            chain = prompt | self.llm.with_structured_output(List[ProposedMarket])
            results = chain.invoke({"data": news_data})
            return results
        except Exception as e:
            logger.error(f"AI Market Proposal failed: {e}")
            return []

    def resolve_market(self, market_title: str) -> str:
        """
        AI Oracle logic: Verify if an event has occurred (YES or NO).
        """
        logger.info(f"AI Oracle resolving market: {market_title}")
        query = f"Has this event occurred yet? {market_title}"
        news_verification = self.search_tool.run(query)
        
        # Simplistic LLM check (stub)
        return "YES" if "confirmed" in news_verification.lower() else "NO"

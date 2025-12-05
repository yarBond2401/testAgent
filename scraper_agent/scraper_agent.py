from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool


scraper_agent = Agent(
    name="scraper_agent",
    description="Company Research Agent that scrapes websites for company data, analyzes profitability and fundraising, and exports results to CSV",
    instructions="./instructions.md",
    files_folder="./files",
    tools_folder="./tools",
    tools=[WebSearchTool()],
    model="gpt-5.1",
    model_settings=ModelSettings(
    ),
)

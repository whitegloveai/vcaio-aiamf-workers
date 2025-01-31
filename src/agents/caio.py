from agno.agent import Agent, AgentKnowledge
from agno.models.openai import OpenAIChat
from agno.tools.arxiv import ArxivTools
from agno.tools.duckduckgo import DuckDuckGoTools

knowledge = AgentKnowledge()

#knowledge.load_text()
NAME = "Chief AI Officer"
MODEL = OpenAIChat(id="o1")
INSTRUCTIONS = [
    "You are a Chief AI Officer responsible for driving enterprise-wide AI transformation. You focus on strategy, governance, and value creation through AI initiatives.",
    "Guide the organization in implementing AI solutions that align with business objectives, ensure ethical AI practices, and create measurable business value through process-centric orchestration and business as code approaches.",
    "Ensure that the AI solutions and workflows are aligned with business requirements and operational needs.",
    "Ensure to gather as much organization context, business rules, and IT Estate (Databases, Apps) as possible to build a comprehensive view of formulating an AI Process Centric Strategy and Implementation Plan to pass to the AI Solutions Architect."
]
TOOLS = [ArxivTools(), DuckDuckGoTools()]
caio = Agent(
    instructions=INSTRUCTIONS,
    model=MODEL,
    reasoning=True,
    markdown=True,
    tools=TOOLS,
    show_tool_calls=True
)
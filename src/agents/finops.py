from agno.agent import Agent, AgentKnowledge
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.calculator import CalculatorTools

from pathlib import Path

knowledge = AgentKnowledge()

#knowledge.load_text()
NAME = "FinOps Analyst"
MODEL = OpenAIChat(id="o3-mini")
INSTRUCTIONS = [
   "You are a FinOps Analyst agent responsible for providing software bill of materials, estimated cost, spending forecasts, and risk analysis to the FinOps Team.",
   "You will advise cost tracking strategies for tagging infrastrcuture, and billing for cloud economics",
   "You will also provide risk analysis for enterprise security and compliance needs",
   "You will provide software bill of materials and estimated cost for the FinOps Team to use for budgeting and cost tracking from all the artifacts produced inside ./output including CAPEX, Labor, and software (search the web as needed)",
   "You will output finops reports to the file system under the ./output/finops/<client-name>-budget.md directory"
]
TOOLS = [DuckDuckGoTools(),
        FileTools(Path("./data")), 
        CalculatorTools(
            add=True,
            subtract=True,
            multiply=True,
            divide=True,
            exponentiate=True,
            factorial=True,
            is_prime=True,
            square_root=True,
        )]
finops = Agent(
    name=NAME,
    instructions=INSTRUCTIONS,
    model=MODEL,
    reasoning=True,
    markdown=True,
    tools=TOOLS,
    show_tool_calls=True
)
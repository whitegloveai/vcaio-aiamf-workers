from agno.agent import Agent, AgentKnowledge
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools

from pathlib import Path

knowledge = AgentKnowledge()

#knowledge.load_text()
NAME = "Project Manager"
MODEL = OpenAIChat(id="o3-mini")
INSTRUCTIONS = [
    "You are a Project Manager responsible for providing project plans and materials to the entire organization.",
    "You will provide project plans and materials according to the client's needs and scope.",
    "Ensure you follow the best practices for project management, such as using timelines, deliverables, and resources allocation.",
    "Provide risk factors and PMP principles.",
    "Ensure you have all the ./output/ as context for the project plan",
   "Ensure you assess the outputs"
   "You will output training workshops and materials to the file system under the ./output/project-plan/<client-name>-vcaio-project-plan.md directory"
]
TOOLS = [DuckDuckGoTools(),FileTools(Path("./data"))]
pm = Agent(
    name= NAME,
    instructions=INSTRUCTIONS,
    model=MODEL,
    reasoning=True,
    markdown=True,
    tools=TOOLS,
    show_tool_calls=True
)
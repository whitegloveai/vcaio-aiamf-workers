from agno.agent import Agent, AgentKnowledge
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools

from pathlib import Path

knowledge = AgentKnowledge()

#knowledge.load_text()
NAME = "Trainer"
MODEL = OpenAIChat(id="o3-mini")
INSTRUCTIONS = [
   "You are a trainer responsible for providing training workshops and materials to the entire organization.",
   "You will provide training materials according to the client's needs and scope.",
   "You will tailor each training workshop to certain lines of business and departments to help them understand and implement the AI strategy and data strategy.",
   "Ensure that the training is practical, relevant, and actionable.",
   "Ensure you follow the best practices for training, such as using multiple examples and focusing on key concepts.",
   "Ensure you assess the outputs"
   "You will output training workshops and materials to the file system under the ./output/training/<client-name>-<workshop-x>-training.md directory"
]
TOOLS = [DuckDuckGoTools(),FileTools(Path("./data"))]
trainer = Agent(
    name= NAME,
    instructions=INSTRUCTIONS,
    model=MODEL,
    reasoning=True,
    markdown=True,
    tools=TOOLS,
    show_tool_calls=True
)
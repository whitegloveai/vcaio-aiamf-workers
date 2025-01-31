from agno.agent import Agent
from agno.tools.file import FileTools

from src.agents.caio import caio
from src.agents.architect import architect
from src.client.context import ClientContext, initialize_context
from src.config import vcaio_ascii
from src.services.logging import setup_logger

import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
# Setup logger for this module
logger = setup_logger(__name__)

vcaio_team = Agent(
    name="VCAIO Team",
    team=[caio, architect],
    instructions=[
        "First, the Chief AI Officer will perform discovery of the client to develop the AI Strategy. Then alwasys transfer to the architect",
        "Architect will design the AI architecture and technical implementation plans based on the Chief AI Officer's strategy",
        f"Write each agents output to the file system under the ./output/<client-name>-<agent>-{datetime.now().strftime('%m-%d-%Y')}.md"
    ],
    tools=[FileTools(Path("./data"))],
    show_tool_calls=True
)

def run(context: ClientContext):
    """Run initial discovery phase with CAIO"""
    discovery_input = {
        "organization_context": context.config["organization"],
        "discovery_context": context.config["discovery_context"]
    }
    
    # Run CAIO discovery process
    try:
        return vcaio_team.run(
            f"Based on this organization context, develop an AI strategy and implementation roadmap: {json.dumps(discovery_input, indent=2)}"
        )
    except Exception as e:
        logger.error(f"Error during discovery: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info(vcaio_ascii)
    
    load_dotenv()
    
    # Initialize client context
    context = initialize_context()
    
    # Run discovery phase
    session = run(context)
    logger.info("View all the output files in the ./data/output directory to support your vCAIO engagement")

from agno.agent import Agent
from agno.tools.file import FileTools

from src.agents.caio import caio
from src.agents.architect import architect
from src.agents.pm import pm
from src.agents.trainer import trainer
from src.agents.finops import finops
from src.client.context import ClientContext, initialize_context
from src.config import BANNER
from src.services.logging import setup_logger

import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
# Setup logger for this module
logger = setup_logger(__name__)

vcaio_team = Agent(
    name="VCAIO Team",
    team=[caio, architect, finops, pm, trainer],
    instructions=[
        "First, the Chief AI Officer will perform discovery of the client to develop the AI Strategy. Then alwasys transfer to the architect",
        "Architect will design the AI architecture and technical implementation plans based on the Chief AI Officer's strategy, then transfer to the Project Manager",
        "Project Manager will ensure the technical feasibility of the AI solution and design a detailed project plan, then transfer to Trainer",
        "Trainer will devise workshops and training plans tailored to departments role based on AI strategy and employee enablement for adopting AI, then transfer to FinOps",
        "FinOps will create software bill of materials and projected costs with business objectives and all context inside ./",
        "Workflow of agents is caio->architect->trainer->pm->finops",
        "Each must produce their necessary artifact based on the information provided by the previous agent and ensure client context",
        f"Write each agents output to the file system under the ./output/<client-name>-<agent>-{datetime.now().strftime('%m-%d-%Y')}.md"
    ],
    tools=[FileTools(Path("./data"))],
    show_tool_calls=True
)

def run(context: ClientContext):
    """Run initial discovery phase with CAIO with comprehensive context validation"""
    logger.info("Initializing discovery phase with complete client context")
    
    # Validate required configuration sections
    required_sections = ["organization", "discovery_context", "data_sources", "it_estate", "compliance"]
    missing_sections = [section for section in required_sections if section not in context.config]
    if missing_sections:
        raise ValueError(f"Missing required configuration sections: {', '.join(missing_sections)}")
    
    # Prepare comprehensive discovery input with all available context
    discovery_input = {
        "organization_context": context.config["organization"],
        "discovery_context": {
            "business": context.config["discovery_context"]["business"],
            "compliance": context.config["discovery_context"]["compliance"],
            "data_sources": context.config["discovery_context"]["data_sources"],
            "it_estate": context.config["discovery_context"]["it_estate"]
        },
        "data_sources": {
            "external": context.config["data_sources"]["external"],
            "internal": context.config["data_sources"]["internal"]
        },
        "it_estate": {
            "applications": context.config["it_estate"]["applications"],
            "cloud_services": context.config["it_estate"]["cloud_services"],
            "databases": context.config["it_estate"]["databases"],
            "integration_points": context.config["it_estate"]["integration_points"]
        },
        "compliance": {
            "data_privacy": context.config["discovery_context"]["compliance"]["data_privacy"],
            "requirements": context.config["discovery_context"]["compliance"]["requirements"],
            "security_controls": context.config["discovery_context"]["compliance"]["security_controls"]
        }
    }
    
    # Log discovery context for debugging
    logger.debug(f"Starting discovery with context:\n" + 
                f"Business Goals: {discovery_input['discovery_context']['business']['strategic_goals']}\n" +
                f"Compliance Requirements: {discovery_input['compliance']['data_privacy']}\n" +
                f"Data Sources Count: {len(discovery_input['data_sources']['external']) + len(discovery_input['data_sources']['internal'])}")
    
    # Run CAIO discovery process with enhanced error handling
    try:
        logger.info("Initiating VCAIO team discovery process")
        return vcaio_team.run(
            f"Based on this comprehensive organization context, develop an AI strategy and implementation roadmap that addresses:\n"
            f"1. Business goals and pain points\n"
            f"2. Compliance and security requirements\n"
            f"3. Available data sources and IT infrastructure\n"
            f"Context: {json.dumps(discovery_input, indent=2)}"
        )
    except KeyError as ke:
        logger.error(f"Configuration error: Missing key {str(ke)}")
        raise
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during discovery: {str(e)}")
        raise

def main_execution_flow(config_path: str, verbose: bool = False, output_dir: str = "./data/output"):
    """Main execution flow with enhanced parameter handling"""
    
    logger.info(BANNER)
    load_dotenv()
    
    # Initialize context with provided parameters
    context = initialize_context(config_path=config_path)
    context.output_dir = Path(output_dir)
    
    # Run discovery phase
    session = run(context)
    
    logger.info(f"View all output files in {output_dir} to support your vCAIO engagement")
    return session
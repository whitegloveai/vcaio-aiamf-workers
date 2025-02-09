# Virtual Chief AI Officer (vCAIO) - WhiteGlove AI

An AI-powered solution architect and strategy consultant that helps organizations develop their AI transformation roadmap.

**TODO: research agent**

## Architecture

```mermaid
graph TD
    subgraph Agents
        CAIO[Chief AI Officer]
        ARCH[AI Solution Architect]
        PM[Project Manager]
        TM[Trainer Manager]
        FINOPS[FinOps]
    end

    subgraph Tools
        FT[File Tools]
        DC[Data Collection]
        WS[Web Search]
        RD[Arxiv Tools]
        CG[Calculator Tools]
    end

    subgraph Data
        IN[/Input Directory/]
        OUT[/Output Directory/]
        CFG[/Config Directory/]
    end

    CAIO -->|Discovery Phase| DC
    DC -->|Stores| IN
    CAIO -->|Generates Strategy| OUT
    ARCH -->|Reads Strategy| OUT
    ARCH -->|Technical Design| OUT
    FT -->|Manages| IN
    FT -->|Manages| OUT
    FT -->|Reads| CFG
    PM -->|Develops| OUT
    TM -->|Trains| OUT
    FINOPS -->|Reads| OUT
    FINOPS -->|Generates| OUT
```
## Prerequisites
- OpenAI API key[https://platform.openai.com/api-keys]
- Git [https://git-scm.com/]
- Python 3 [https://www.python.org/downloads/]
- uv [https://docs.astral.sh/uv/getting-started/installation/]

## Setup
**Clone Repo**:
```bash
git clone https://github.com/whitegloveai/vcaio-aiamf-workers.git
cd vcaio-aiamf-workers
```

**Install uv and setup venv** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

Setup `.env`:
```bash
cp .env.example .env # Input your OpenAI API key (we'll probably want to do local private agents in the event of security/legal concerns)
```

1. Create a client configuration in `src/config/client.yaml` with:
   - Organization details
   - Business context
   - Technical context:
     - Compliance requirements
     - Data sources
     - IT estate information
     - Current AI/ML initiatives

2. Place any supporting documents in `./data/input/`

3. Usage:
```bash
# Validate config
vcaio validate-config

# Run full workflow with default config
vcaio run

# Run with custom config and output directory
vcaio run --config ./src/config/custom-client.yaml --output-dir ./reports

# Show all available commands
vcaio --help

# Display version
vcaio --version

# List available AI agents
vcaio list-agents
```

4. Review outputs in `./data/output/`:
   - `organization-ai-bluprint-*.md`: AI Strategy Document
   - `/artifacts/organization-architect-*.md`: Technical Implementation Plan
   - `/project-plan/organization-pm-*.md`: Project Plan
   - `/finops/organization-finance-*.md`: Financial Plan
   - `/training/organization-trainer-*.md`: Trainings & Workshops

## Project Structure

```
.
├── src/
│   ├── agents/         # AI agent definitions
│   │   ├── caio.py     # Chief AI Officer agent
│   │   └── architect.py # Solution Architect agent
│   │   └── pm.py       # Project Manager agent
│   │   └── trainer.py  # Trainer agent
│   │   └── finops.py   # FinOps agent
│   ├── client/         # Client context and data management
│   ├── config/         # Configuration files
│   │   └── client.yaml # Client configuration template
│   ├── services/       # Shared services and utilities
│   ├── cli.py         # Command-line interface
│   ├── config.py      # Global configuration
│   └── core.py        # Core execution logic
├── data/
│   ├── input/         # Client input documents
│   └── output/        # Generated strategies and plans
├── pyproject.toml     # Project metadata and dependencies
├── .env.example       # Environment variables template
└── README.md         # Project documentation
```
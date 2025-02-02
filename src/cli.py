import click
from importlib import metadata
from .core import main_execution_flow
from .client.context import ClientContext

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(metadata.version("vcaio-agno"), "-v", "--version")
def cli():
    """Virtual Chief AI Officer (vCAIO) Command Line Interface
    
    Manage AI strategy development, technical implementation plans, organizational context, financial planning, employee enablement, and project planning.
    """
    pass

@cli.command()
@click.option("--config", 
              default="./src/config/client.yaml",
              type=click.Path(exists=True),
              help="Path to client configuration YAML file")
@click.option("--verbose", is_flag=True, help="Enable debug logging")
@click.option("--output-dir",
              default="./data/output",
              type=click.Path(),
              help="Directory for generated artifacts")
def run(config, verbose, output_dir):
    """Execute full vCAIO workflow"""
    click.secho("🚀 Starting Virtual Chief AI Officer...", fg="green")
    main_execution_flow(
        config_path=config,
        verbose=verbose,
        output_dir=output_dir
    )

@cli.command()
@click.argument("config", default="./src/config/client.yaml")
def validate_config(config):
    """Validate client configuration file"""
    try:
        ClientContext(config_path=config)
        click.secho("✅ Configuration is valid", fg="green")
    except Exception as e:
        click.secho(f"❌ Configuration error: {str(e)}", fg="red")
        raise click.Abort()

@cli.command()
def list_agents():
    """Display available AI agents"""
    click.echo("Available Agents:")
    click.echo("\n• Chief AI Officer (CAIO)")
    click.echo("  - Strategic discovery and AI roadmap development")
    click.echo("\n• AI Solution Architect")
    click.echo("  - Technical design and implementation planning")
    click.echo("\n• Project Manager")
    click.echo("  - Project plans and materials development")
    click.echo("\n• Trainer")
    click.echo("  - Provide trainings and workshops for clients line of business and departments based on tailored AI strategy")
    click.echo("\n• FinOps")
    click.echo("  - Financial operations, cloud economics strategy, budget, software bill of materials, and compliance monitoring")

if __name__ == "__main__":
    cli()
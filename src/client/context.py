import os
from pathlib import Path
import yaml

class ClientContext:
    def __init__(self, config_path: str = "./src/config/client.yaml"):
        self.config_path = Path(config_path)
        self.data_dir = Path("./data")
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        if not self.config_path.exists():
            print("No client configuration found. Let's create one.")
            return self._create_initial_config()
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Check if config is empty or has empty required fields
        if self._is_config_empty(config):
            print("Client configuration is empty. Let's fill it out.")
            return self._create_initial_config()
            
        return config
    
    def _is_config_empty(self, config: dict) -> bool:
        """Check if the configuration has empty required fields"""
        org = config.get('organization', {})
        return not all([
            org.get('name'),
            org.get('industry'),
            org.get('size'),
            org.get('location')
        ])
    
    def _create_initial_config(self) -> dict:
        """Create initial configuration by prompting user for input"""
        config = {
            'organization': {},
            'discovery_context': {
                'business': {'strategic_goals': [], 'pain_points': [], 'success_metrics': [], 'key_stakeholders': []},
                'it_estate': {'databases': [], 'applications': [], 'integration_points': [], 'cloud_services': []},
                'data_sources': {'internal': [], 'external': []},
                'compliance': {'requirements': [], 'data_privacy': [], 'security_controls': []}
            },
            'documents': {
                'input_directory': './data/input',
                'output_directory': './data/output',
                'supported_formats': ['.pdf', '.docx', '.txt', '.md', '.json', '.csv', '.xls', '.xls']
            }
        }
        
        # Get organization details
        print("\nPlease provide organization details:")
        config['organization']['name'] = input("Organization name: ").strip()
        config['organization']['industry'] = input("Industry: ").strip()
        config['organization']['size'] = input("Organization size (e.g., Small, Medium, Large): ").strip()
        config['organization']['location'] = input("Location: ").strip()
        
        # Get business context
        print("\nPlease provide business context (enter empty line to finish each section):")
        config['discovery_context']['business']['strategic_goals'] = self._get_list_input("Strategic goals")
        config['discovery_context']['business']['pain_points'] = self._get_list_input("Pain points")
        config['discovery_context']['business']['success_metrics'] = self._get_list_input("Success metrics")
        config['discovery_context']['business']['key_stakeholders'] = self._get_list_input("Key stakeholders")
        
        # Save the configuration
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        return config
    
    def _get_list_input(self, prompt: str) -> list:
        """Helper to get list input from user"""
        print(f"\nEnter {prompt} (press Enter twice to finish):")
        items = []
        last_input_empty = False
        
        while True:
            item = input("> ").strip()
            if not item:
                if last_input_empty:
                    break
                last_input_empty = True
            else:
                last_input_empty = False
                items.append(item)
        
        return items
    
    def setup_directories(self):
        """Ensure required directories exist"""
        for dir_name in ['input', 'output']:
            (self.data_dir / dir_name).mkdir(parents=True, exist_ok=True)

def initialize_context(config_path: str = "./src/config/client.yaml") -> ClientContext:
    import yaml
    # Load the YAML configuration
    with open(config_path, 'r') as file:
        client_config = yaml.safe_load(file)

    # If discovery_context exists, merge its keys into the top-level config
    if 'discovery_context' in client_config:
        dc = client_config['discovery_context']
        client_config['data_sources'] = dc.get('data_sources', {})
        client_config['it_estate'] = dc.get('it_estate', {})
        client_config['compliance'] = dc.get('compliance', {})
    else:
        # Ensure top-level required configuration sections exist
        client_config.setdefault('data_sources', {})
        client_config.setdefault('it_estate', {})
        client_config.setdefault('compliance', {})

    # Instantiate the ClientContext (assuming it's defined elsewhere in the module)
    context = ClientContext(config_path)
    # Assign the full configuration to context.config
    context.config = client_config
    # Also set additional attributes if needed
    context.data_sources = client_config.get("data_sources", {})
    context.it_estate = client_config.get("it_estate", {})
    context.compliance = client_config.get("compliance", {})
    
    # Setup directories and other required structure
    context.setup_directories()
    return context
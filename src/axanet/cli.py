"""
Command Line Interface for Axanet Client Manager
===============================================

This module provides a professional command-line interface for the Axanet
Client Manager application using the Click framework.

Features:
---------
- Interactive and non-interactive modes
- Subcommands for different operations
- Input validation and error handling
- Colored output and progress indicators
- Help documentation for all commands

Educational Notes for Students:
-------------------------------
1. Click framework provides professional CLI capabilities
2. Command groups organize related functionality
3. Input validation prevents errors and improves UX
4. Progress indicators provide feedback for long operations
5. Context management ensures proper resource cleanup
6. Error handling provides meaningful feedback to users

Design Patterns Used:
---------------------
- Command Pattern: Each CLI command encapsulates an operation
- Factory Pattern: Click decorators create command objects
- Strategy Pattern: Different output formats for different contexts
"""

import click
import logging
from typing import Optional
import sys
from pathlib import Path

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from axanet.services import ClientManager
from axanet.models import Client
from axanet.exceptions import ClientError, ClientNotFoundError, ClientExistsError, ValidationError
from axanet.config import get_config
from axanet.utils import setup_logging, get_user_confirmation, create_table_display


class AxanetCLI:
    """
    Main CLI application class.
    
    This class manages the CLI state and provides common functionality
    for all commands.
    
    Educational Notes:
        - CLI state management ensures consistent behavior
        - Centralized error handling improves user experience
        - Logging integration provides debugging capabilities
    """
    
    def __init__(self):
        """Initialize CLI application."""
        self.config = get_config()
        self.client_manager = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for CLI application."""
        setup_logging(
            log_file=self.config.logging.file_name,
            log_level=self.config.logging.level,
            console_output=self.config.debug
        )
        self.logger = logging.getLogger(__name__)
    
    def get_client_manager(self) -> ClientManager:
        """Get or create client manager instance."""
        if self.client_manager is None:
            try:
                self.client_manager = ClientManager()
            except Exception as e:
                click.echo(f"Error initializing client manager: {e}", err=True)
                sys.exit(1)
        return self.client_manager


# Global CLI instance
cli_app = AxanetCLI()


@click.group()
@click.version_option(version="1.0.0", prog_name="Axanet Client Manager")
@click.option('--debug', is_flag=True, help='Enable debug output')
def cli(debug):
    """
    Axanet Client Manager - Professional client data management system.
    
    This application helps manage client information for Axanet telecommunications
    company, providing CRUD operations for client records and service history.
    
    Examples:
    
        # Create a new client interactively
        axanet create
        
        # List all clients
        axanet list
        
        # Search for clients
        axanet search "Garcia"
        
        # Add service to existing client
        axanet update "Ana Garcia" "New web development project"
    """
    if debug:
        cli_app.config.debug = True
        cli_app._setup_logging()


@cli.command()
@click.option('--name', prompt='Client name', help='Full name of the client')
@click.option('--phone', prompt='Phone number', help='Client phone number')
@click.option('--email', prompt='Email address', help='Client email address')
@click.option('--service', prompt='First service description', help='Description of the first service')
def create(name: str, phone: str, email: str, service: str):
    """
    Create a new client with initial service.
    
    This command creates a new client record with the provided information
    and adds the first service to their record.
    
    Educational Note:
        The @click.option decorator with prompt=True creates interactive
        prompts for missing arguments, improving user experience.
    """
    try:
        client_manager = cli_app.get_client_manager()
        
        # Validate inputs
        if not name.strip():
            click.echo("Error: Client name cannot be empty", err=True)
            return
        
        # Create client
        with click.progressbar(length=1, label='Creating client') as bar:
            client = client_manager.create_client(name, phone, email, service)
            bar.update(1)
        
        click.echo(f"\n✓ Successfully created client: {client.name}")
        click.echo(f"  Client ID: {client.client_id}")
        click.echo(f"  File saved to: {client.normalized_name}.txt")
        
        cli_app.logger.info(f"CLI: Created client {client.name}")
        
    except ClientExistsError as e:
        click.echo(f"Error: {e}", err=True)
    except ValidationError as e:
        click.echo(f"Validation Error: {e}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        cli_app.logger.error(f"CLI create error: {e}")


@cli.command()
@click.option('--format', type=click.Choice(['table', 'detailed']), default='table',
              help='Output format for client list')
def list(format: str):
    """
    List all registered clients.
    
    This command displays all clients in the system with their basic information.
    Use different formats to control the level of detail shown.
    """
    try:
        client_manager = cli_app.get_client_manager()
        clients = client_manager.get_all_clients()
        
        if not clients:
            click.echo("No clients found in the system.")
            return
        
        click.echo(f"\nFound {len(clients)} client(s):\n")
        
        if format == 'table':
            # Display as formatted table
            headers = ['Name', 'Phone', 'Email', 'Services']
            rows = []
            
            for client in clients:
                rows.append([
                    client.name,
                    client.phone,
                    client.email,
                    str(len(client.services))
                ])
            
            table = create_table_display(headers, rows)
            click.echo(table)
            
        else:  # detailed format
            for i, client in enumerate(clients, 1):
                click.echo(f"{i}. {client.name}")
                click.echo(f"   ID: {client.client_id}")
                click.echo(f"   Phone: {client.phone}")
                click.echo(f"   Email: {client.email}")
                click.echo(f"   Registration: {client.registration_date.strftime('%Y-%m-%d')}")
                click.echo(f"   Services: {len(client.services)}")
                click.echo()
        
        cli_app.logger.info(f"CLI: Listed {len(clients)} clients")
        
    except Exception as e:
        click.echo(f"Error listing clients: {e}", err=True)
        cli_app.logger.error(f"CLI list error: {e}")


@cli.command()
@click.argument('name')
def show(name: str):
    """
    Show detailed information for a specific client.
    
    NAME: The name of the client to display
    
    This command displays all available information for a client,
    including their service history.
    """
    try:
        client_manager = cli_app.get_client_manager()
        client = client_manager.get_client(name)
        
        click.echo(f"\n📋 Client Details: {client.name}")
        click.echo("=" * 50)
        click.echo(f"Client ID: {client.client_id}")
        click.echo(f"Phone: {client.phone}")
        click.echo(f"Email: {client.email}")
        click.echo(f"Registration Date: {client.registration_date.strftime('%Y-%m-%d')}")
        click.echo(f"\n🔧 Services ({len(client.services)}):")
        
        if client.services:
            for i, service in enumerate(client.services, 1):
                date_str = service.date_requested.strftime('%Y-%m-%d')
                click.echo(f"  {i}. {service.description} ({date_str})")
        else:
            click.echo("  No services registered yet")
        
        cli_app.logger.info(f"CLI: Showed client {client.name}")
        
    except ClientNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        cli_app.logger.error(f"CLI show error: {e}")


@cli.command()
@click.argument('name')
@click.argument('service_description')
def update(name: str, service_description: str):
    """
    Add a new service to an existing client.
    
    NAME: The name of the client to update
    SERVICE_DESCRIPTION: Description of the new service
    
    This command adds a new service entry to the client's record
    with the current date.
    """
    try:
        client_manager = cli_app.get_client_manager()
        
        # Validate service description
        if not service_description.strip():
            click.echo("Error: Service description cannot be empty", err=True)
            return
        
        # Update client
        with click.progressbar(length=1, label='Adding service') as bar:
            client = client_manager.update_client(name, service_description)
            bar.update(1)
        
        click.echo(f"\n✓ Successfully added service to {client.name}")
        click.echo(f"  Service: {service_description}")
        click.echo(f"  Total services: {len(client.services)}")
        
        cli_app.logger.info(f"CLI: Updated client {client.name} with service")
        
    except ClientNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
    except ValidationError as e:
        click.echo(f"Validation Error: {e}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        cli_app.logger.error(f"CLI update error: {e}")


@cli.command()
@click.argument('name')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def delete(name: str, force: bool):
    """
    Delete a client and their file.
    
    NAME: The name of the client to delete
    
    This command permanently removes a client record and their data file.
    Use with caution as this operation cannot be undone.
    """
    try:
        client_manager = cli_app.get_client_manager()
        
        # Verify client exists and get details
        client = client_manager.get_client(name)
        
        click.echo(f"\n⚠️  About to delete client: {client.name}")
        click.echo(f"   Client ID: {client.client_id}")
        click.echo(f"   Services: {len(client.services)}")
        
        # Confirmation
        if not force:
            if not get_user_confirmation("Are you sure you want to delete this client?"):
                click.echo("Operation cancelled.")
                return
        
        # Delete client
        with click.progressbar(length=1, label='Deleting client') as bar:
            client_manager.delete_client(name)
            bar.update(1)
        
        click.echo(f"\n✓ Successfully deleted client: {name}")
        
        cli_app.logger.info(f"CLI: Deleted client {name}")
        
    except ClientNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        cli_app.logger.error(f"CLI delete error: {e}")


@cli.command()
@click.argument('query')
def search(query: str):
    """
    Search for clients by name, email, or phone.
    
    QUERY: Search term to look for in client records
    
    This command searches through all client records and displays
    matching results.
    """
    try:
        client_manager = cli_app.get_client_manager()
        
        if len(query.strip()) < 2:
            click.echo("Error: Search query must be at least 2 characters long", err=True)
            return
        
        clients = client_manager.search_clients(query)
        
        if not clients:
            click.echo(f"No clients found matching '{query}'")
            return
        
        click.echo(f"\nFound {len(clients)} client(s) matching '{query}':\n")
        
        for i, client in enumerate(clients, 1):
            click.echo(f"{i}. {client.name}")
            click.echo(f"   Phone: {client.phone}")
            click.echo(f"   Email: {client.email}")
            click.echo(f"   Services: {len(client.services)}")
            click.echo()
        
        cli_app.logger.info(f"CLI: Searched for '{query}', found {len(clients)} results")
        
    except Exception as e:
        click.echo(f"Error searching clients: {e}", err=True)
        cli_app.logger.error(f"CLI search error: {e}")


@cli.command()
def stats():
    """
    Display system statistics.
    
    This command shows various statistics about the client database
    including total clients, services, and usage patterns.
    """
    try:
        client_manager = cli_app.get_client_manager()
        statistics = client_manager.get_statistics()
        
        click.echo("\n📊 System Statistics")
        click.echo("=" * 30)
        click.echo(f"Total Clients: {statistics['total_clients']}")
        click.echo(f"Total Services: {statistics['total_services']}")
        click.echo(f"Avg Services/Client: {statistics['average_services_per_client']}")
        
        # Additional info
        config = get_config()
        data_dir = config.database.full_path
        click.echo(f"\nData Directory: {data_dir}")
        click.echo(f"Directory exists: {data_dir.exists()}")
        
        if data_dir.exists():
            file_count = len(list(data_dir.glob("*.txt")))
            click.echo(f"Files in directory: {file_count}")
        
        cli_app.logger.info("CLI: Displayed statistics")
        
    except Exception as e:
        click.echo(f"Error getting statistics: {e}", err=True)
        cli_app.logger.error(f"CLI stats error: {e}")


@cli.command()
def interactive():
    """
    Start interactive mode with menu-driven interface.
    
    This command provides a traditional menu-driven interface
    for users who prefer interactive operation.
    """
    click.echo("🏢 Axanet Client Manager - Interactive Mode")
    click.echo("=" * 50)
    
    client_manager = cli_app.get_client_manager()
    
    while True:
        try:
            click.echo("\nAvailable Operations:")
            click.echo("1. Create new client")
            click.echo("2. List all clients") 
            click.echo("3. Show client details")
            click.echo("4. Update client (add service)")
            click.echo("5. Delete client")
            click.echo("6. Search clients")
            click.echo("7. Show statistics")
            click.echo("8. Exit")
            
            choice = click.prompt("\nSelect an option", type=int)
            
            if choice == 1:
                name = click.prompt("Client name")
                phone = click.prompt("Phone number")
                email = click.prompt("Email address")
                service = click.prompt("First service description")
                
                try:
                    client = client_manager.create_client(name, phone, email, service)
                    click.echo(f"✓ Created client: {client.name}")
                except Exception as e:
                    click.echo(f"Error: {e}")
                    
            elif choice == 2:
                clients = client_manager.get_all_clients()
                if clients:
                    click.echo(f"\nClients ({len(clients)}):")
                    for i, client in enumerate(clients, 1):
                        click.echo(f"{i}. {client.name} - {len(client.services)} services")
                else:
                    click.echo("No clients found.")
                    
            elif choice == 3:
                name = click.prompt("Client name")
                try:
                    client = client_manager.get_client(name)
                    click.echo(f"\nClient: {client.name}")
                    click.echo(f"ID: {client.client_id}")
                    click.echo(f"Phone: {client.phone}")
                    click.echo(f"Email: {client.email}")
                    click.echo(f"Services: {len(client.services)}")
                except ClientNotFoundError:
                    click.echo("Client not found.")
                    
            elif choice == 4:
                name = click.prompt("Client name")
                service = click.prompt("New service description")
                try:
                    client = client_manager.update_client(name, service)
                    click.echo(f"✓ Added service to {client.name}")
                except ClientNotFoundError:
                    click.echo("Client not found.")
                except Exception as e:
                    click.echo(f"Error: {e}")
                    
            elif choice == 5:
                name = click.prompt("Client name to delete")
                try:
                    client = client_manager.get_client(name)
                    if get_user_confirmation(f"Delete {client.name}?"):
                        client_manager.delete_client(name)
                        click.echo(f"✓ Deleted client: {name}")
                    else:
                        click.echo("Operation cancelled.")
                except ClientNotFoundError:
                    click.echo("Client not found.")
                except Exception as e:
                    click.echo(f"Error: {e}")
                    
            elif choice == 6:
                query = click.prompt("Search query")
                clients = client_manager.search_clients(query)
                if clients:
                    click.echo(f"\nFound {len(clients)} matching clients:")
                    for client in clients:
                        click.echo(f"- {client.name}")
                else:
                    click.echo("No matching clients found.")
                    
            elif choice == 7:
                stats = client_manager.get_statistics()
                click.echo(f"\nTotal Clients: {stats['total_clients']}")
                click.echo(f"Total Services: {stats['total_services']}")
                click.echo(f"Average Services per Client: {stats['average_services_per_client']}")
                
            elif choice == 8:
                click.echo("Goodbye!")
                break
                
            else:
                click.echo("Invalid choice. Please select 1-8.")
                
        except (KeyboardInterrupt, EOFError):
            click.echo("\nGoodbye!")
            break
        except Exception as e:
            click.echo(f"Unexpected error: {e}")


if __name__ == '__main__':
    cli()
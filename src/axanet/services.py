"""
Client Management Services for Axanet Client Manager
===================================================

This module contains the business logic for managing clients, including
CRUD operations, file management, and data validation.

Classes:
--------
- ClientManager: Main service class for client operations
- FileManager: Handles file system operations

Educational Notes for Students:
-------------------------------
1. Service classes encapsulate business logic and provide a clean API
2. Separation of concerns: FileManager handles file ops, ClientManager handles business logic
3. Hash tables (dictionaries) provide O(1) lookup performance for client operations
4. Error handling ensures data integrity and provides meaningful feedback
5. Logging provides visibility into application behavior for debugging and monitoring

Design Patterns Used:
---------------------
- Service Pattern: ClientManager provides high-level business operations
- Repository Pattern: FileManager abstracts data persistence
- Factory Pattern: Methods that create and return Client instances
- Observer Pattern: Logging observes and records all operations
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional
import os

from .models import Client
from .exceptions import ClientError, ClientNotFoundError, ClientExistsError, FileOperationError
from .config import get_config, get_data_directory, get_client_file_path


class FileManager:
    """
    Handles file system operations for client data.
    
    This class abstracts all file system interactions, providing a clean
    interface for reading, writing, and managing client files.
    
    Educational Notes:
        - Abstraction layer separates file operations from business logic
        - Error handling converts system errors to domain-specific exceptions
        - Path management ensures cross-platform compatibility
        - Atomic operations prevent data corruption
    """
    
    def __init__(self):
        """Initialize file manager with configuration."""
        self.config = get_config()
        self.logger = logging.getLogger(__name__)
        self._ensure_data_directory()
    
    def _ensure_data_directory(self) -> None:
        """Ensure the data directory exists."""
        try:
            data_dir = get_data_directory()
            data_dir.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Data directory ensured: {data_dir}")
        except OSError as e:
            raise FileOperationError("create", str(get_data_directory()), e)
    
    def read_client_file(self, normalized_name: str) -> str:
        """
        Read client data from file.
        
        Args:
            normalized_name (str): Normalized client name
            
        Returns:
            str: File content
            
        Raises:
            FileOperationError: If file read fails
            ClientNotFoundError: If client file doesn't exist
        """
        file_path = get_client_file_path(normalized_name)
        
        if not file_path.exists():
            raise ClientNotFoundError(normalized_name)
        
        try:
            content = file_path.read_text(encoding=self.config.database.encoding)
            self.logger.debug(f"Read client file: {file_path}")
            return content
        except OSError as e:
            raise FileOperationError("read", str(file_path), e)
    
    def write_client_file(self, normalized_name: str, content: str) -> None:
        """
        Write client data to file.
        
        Args:
            normalized_name (str): Normalized client name
            content (str): Content to write
            
        Raises:
            FileOperationError: If file write fails
        """
        file_path = get_client_file_path(normalized_name)
        
        try:
            file_path.write_text(content, encoding=self.config.database.encoding)
            self.logger.debug(f"Wrote client file: {file_path}")
        except OSError as e:
            raise FileOperationError("write", str(file_path), e)
    
    def delete_client_file(self, normalized_name: str) -> None:
        """
        Delete client file.
        
        Args:
            normalized_name (str): Normalized client name
            
        Raises:
            FileOperationError: If file delete fails
            ClientNotFoundError: If client file doesn't exist
        """
        file_path = get_client_file_path(normalized_name)
        
        if not file_path.exists():
            raise ClientNotFoundError(normalized_name)
        
        try:
            file_path.unlink()
            self.logger.debug(f"Deleted client file: {file_path}")
        except OSError as e:
            raise FileOperationError("delete", str(file_path), e)
    
    def list_client_files(self) -> List[str]:
        """
        List all client files in the data directory.
        
        Returns:
            List[str]: List of normalized client names
            
        Raises:
            FileOperationError: If directory listing fails
        """
        try:
            data_dir = get_data_directory()
            file_extension = self.config.database.file_extension
            
            client_files = []
            for file_path in data_dir.glob(f"*{file_extension}"):
                if file_path.is_file():
                    # Remove extension to get normalized name
                    normalized_name = file_path.stem
                    client_files.append(normalized_name)
            
            self.logger.debug(f"Listed {len(client_files)} client files")
            return sorted(client_files)
        
        except OSError as e:
            raise FileOperationError("list", str(get_data_directory()), e)
    
    def file_exists(self, normalized_name: str) -> bool:
        """
        Check if client file exists.
        
        Args:
            normalized_name (str): Normalized client name
            
        Returns:
            bool: True if file exists, False otherwise
        """
        file_path = get_client_file_path(normalized_name)
        return file_path.exists()


class ClientManager:
    """
    Main service class for managing Axanet clients.
    
    This class provides high-level operations for creating, reading, updating,
    and deleting client records. It uses a hash table (dictionary) for fast
    in-memory lookups and delegates file operations to FileManager.
    
    Educational Notes:
        - Hash table provides O(1) average case lookup performance
        - In-memory cache reduces file system access for better performance
        - Business logic validation ensures data integrity
        - Comprehensive logging provides audit trail and debugging information
        - Error handling provides specific, actionable error messages
    
    Attributes:
        _clients_cache (Dict[str, Client]): In-memory cache of loaded clients
        _file_manager (FileManager): Handles file system operations
    """
    
    def __init__(self):
        """Initialize client manager."""
        self._clients_cache: Dict[str, Client] = {}
        self._file_manager = FileManager()
        self.logger = logging.getLogger(__name__)
        
        # Load existing clients into cache
        self._load_all_clients()
        
        self.logger.info(f"ClientManager initialized with {len(self._clients_cache)} clients")
    
    def _load_all_clients(self) -> None:
        """
        Load all existing clients into memory cache.
        
        Educational Note:
            Loading all clients at startup provides fast access but uses more memory.
            This is suitable for small to medium datasets. For larger datasets,
            you might implement lazy loading or pagination.
        """
        try:
            client_files = self._file_manager.list_client_files()
            
            for normalized_name in client_files:
                try:
                    content = self._file_manager.read_client_file(normalized_name)
                    client = Client.from_file_content(content)
                    self._clients_cache[normalized_name] = client
                except Exception as e:
                    self.logger.warning(f"Failed to load client {normalized_name}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Failed to load clients: {e}")
    
    def create_client(self, name: str, phone: str, email: str, first_service: str) -> Client:
        """
        Create a new client with initial service.
        
        Args:
            name (str): Client full name
            phone (str): Phone number
            email (str): Email address
            first_service (str): Description of first service
            
        Returns:
            Client: Created client instance
            
        Raises:
            ClientExistsError: If client already exists
            ValidationError: If client data is invalid
            FileOperationError: If file operations fail
            
        Educational Note:
            This method demonstrates transaction-like behavior: validate first,
            then perform all operations. If any step fails, no partial state is left.
        """
        # Create client instance and validate
        client = Client(name=name, phone=phone, email=email)
        client.validate()
        
        # Add first service
        client.add_service(first_service)
        
        # Check if client already exists
        normalized_name = client.normalized_name
        if normalized_name in self._clients_cache:
            raise ClientExistsError(normalized_name)
        
        # Check if file exists (in case cache is out of sync)
        if self._file_manager.file_exists(normalized_name):
            raise ClientExistsError(normalized_name)
        
        # Save to file
        content = client.to_file_format()
        self._file_manager.write_client_file(normalized_name, content)
        
        # Add to cache
        self._clients_cache[normalized_name] = client
        
        self.logger.info(f"Created client: {name} ({client.client_id})")
        return client
    
    def get_client(self, name: str) -> Client:
        """
        Get client by name.
        
        Args:
            name (str): Client name (original or normalized)
            
        Returns:
            Client: Client instance
            
        Raises:
            ClientNotFoundError: If client doesn't exist
        """
        # Normalize the name for lookup
        normalized_name = Client(name=name, phone="", email="").normalized_name
        
        if normalized_name not in self._clients_cache:
            raise ClientNotFoundError(name)
        
        client = self._clients_cache[normalized_name]
        self.logger.debug(f"Retrieved client: {name}")
        return client
    
    def get_all_clients(self) -> List[Client]:
        """
        Get all clients.
        
        Returns:
            List[Client]: List of all clients
            
        Educational Note:
            Returns a copy of the clients list to prevent external modification
            of the internal cache. This is a defensive programming practice.
        """
        clients = list(self._clients_cache.values())
        clients.sort(key=lambda c: c.name)  # Sort by name for consistent ordering
        
        self.logger.debug(f"Retrieved {len(clients)} clients")
        return clients
    
    def update_client(self, name: str, new_service: str) -> Client:
        """
        Add a new service to an existing client.
        
        Args:
            name (str): Client name
            new_service (str): Description of new service
            
        Returns:
            Client: Updated client instance
            
        Raises:
            ClientNotFoundError: If client doesn't exist
            ValidationError: If service description is invalid
            FileOperationError: If file operations fail
        """
        # Get client from cache
        client = self.get_client(name)
        
        # Add new service (this validates the service description)
        client.add_service(new_service)
        
        # Save updated client to file
        normalized_name = client.normalized_name
        content = client.to_file_format()
        self._file_manager.write_client_file(normalized_name, content)
        
        self.logger.info(f"Updated client {name} with new service: {new_service}")
        return client
    
    def delete_client(self, name: str) -> bool:
        """
        Delete a client.
        
        Args:
            name (str): Client name
            
        Returns:
            bool: True if client was deleted
            
        Raises:
            ClientNotFoundError: If client doesn't exist
            FileOperationError: If file operations fail
        """
        # Get client to ensure it exists
        client = self.get_client(name)
        normalized_name = client.normalized_name
        
        # Delete file
        self._file_manager.delete_client_file(normalized_name)
        
        # Remove from cache
        del self._clients_cache[normalized_name]
        
        self.logger.info(f"Deleted client: {name} ({client.client_id})")
        return True
    
    def client_exists(self, name: str) -> bool:
        """
        Check if a client exists.
        
        Args:
            name (str): Client name
            
        Returns:
            bool: True if client exists
        """
        normalized_name = Client(name=name, phone="", email="").normalized_name
        return normalized_name in self._clients_cache
    
    def get_client_count(self) -> int:
        """
        Get total number of clients.
        
        Returns:
            int: Number of clients
        """
        return len(self._clients_cache)
    
    def search_clients(self, query: str) -> List[Client]:
        """
        Search clients by name, email, or phone.
        
        Args:
            query (str): Search query
            
        Returns:
            List[Client]: Matching clients
            
        Educational Note:
            This demonstrates basic search functionality. In a production
            system, you might implement more sophisticated search with
            indexing, fuzzy matching, or full-text search capabilities.
        """
        query = query.lower().strip()
        matching_clients = []
        
        for client in self._clients_cache.values():
            # Search in name, email, and phone
            if (query in client.name.lower() or 
                query in client.email.lower() or 
                query in client.phone):
                matching_clients.append(client)
        
        # Sort by name for consistent results
        matching_clients.sort(key=lambda c: c.name)
        
        self.logger.debug(f"Search for '{query}' found {len(matching_clients)} clients")
        return matching_clients
    
    def refresh_cache(self) -> None:
        """
        Refresh the in-memory cache from disk.
        
        Educational Note:
            This method is useful for scenarios where external processes
            might modify the data files, or for debugging cache-related issues.
        """
        self._clients_cache.clear()
        self._load_all_clients()
        self.logger.info(f"Cache refreshed with {len(self._clients_cache)} clients")
    
    def get_statistics(self) -> Dict[str, int | float]:
        """
        Get usage statistics.
        
        Returns:
            Dict[str, int | float]: Statistics about clients and services
        """
        total_clients = len(self._clients_cache)
        total_services = sum(len(client.services) for client in self._clients_cache.values())
        
        return {
            "total_clients": total_clients,
            "total_services": total_services,
            "average_services_per_client": round(total_services / total_clients, 2) if total_clients > 0 else 0
        }
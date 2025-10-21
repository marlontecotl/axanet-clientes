# -*- coding: utf-8 -*-
"""
Axanet Client Manager
----------------------
Console-based application to manage client data for the company Axanet.

This script allows users to create, view, update, and delete client information,
storing each client's data in a dedicated plain text file.

Features:
- Client information stored in plain text files.
- In-memory dictionary (hash table) for fast client lookup.
- Error handling with clear feedback to users.
- Modular, scalable structure.
- Input validation.

Author: Axanet Development Team
Reviewed by: Senior Software Developer
"""

from os import path, makedirs, listdir, remove  # For file and directory operations
from datetime import datetime  # For generating timestamps and registration dates
from re import sub  # For regular expressions used in name normalization
from logging import basicConfig, INFO, info, error, warning, critical # For logging application activity
from typing import Optional  # Optional typing for clarity

# Configure logging
basicConfig(
    filename="axanet_client_manager.log",  # Log file name
    level=INFO,  # Minimum logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Timestamp format
)
BASE_DIRECTORY = "axanet_clients_data"  # Directory where client files will be stored
client_files_map = {}  # Dictionary that maps normalized client names to their file paths
def normalize_name(client_name: str) -> str:
    """Normalizes the client name to lowercase with underscores.
    Args:
        client_name (str): Raw name input.
    Returns:
        str: Normalized name.
    """
    return sub(r"\s+", "_", client_name.strip().lower())
def generate_client_id(client_name: str) -> str:
    """Generates a unique client ID using initials and timestamp.
    Args:
        client_name (str): Full client name.
    Returns:
        str: Generated client ID.
    """
    initials = "".join([word[0].upper() for word in client_name.strip().split()])
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{initials}_{timestamp}"

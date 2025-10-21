# -*- coding: utf-8 -*-  # Encoding declaration for UTF-8 character support
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
- Input validation and confirmation prompts for destructive actions.

Author: Axanet Development Team
Reviewed by: Senior Software Developer
"""

from os import path, makedirs, listdir, remove  # For file and directory operations
from datetime import datetime  # For generating timestamps and registration dates
from re import sub  # For regular expressions used in name normalization
from logging import (
    basicConfig,
    INFO,
    info,
    error,
    warning,
    critical,
)  # For logging application activity
from typing import Optional  # Optional typing for clarity

# Configure logging
basicConfig(
    filename="axanet_client_manager.log",  # Log file name
    level=INFO,  # Minimum logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Timestamp format
)

BASE_DIRECTORY = "axanet_clients_data"  # Directory where client files will be stored
client_files_map = (
    {}
)  # Dictionary that maps normalized client names to their file paths


def normalize_name(client_name):
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


def ensure_base_directory():
    """Ensures the base directory exists or creates it.

    Raises:
        SystemExit: If directory creation fails.
    """
    try:
        if not path.exists(BASE_DIRECTORY):
            makedirs(BASE_DIRECTORY)
            info("Created base directory: %s", BASE_DIRECTORY)
    except OSError as e:
        error("Failed to create base directory: %s", e)
        print(f"[ERROR] Failed to create base directory: {e}")
        exit(1)


def load_clients():
    """Loads existing client files from disk into memory.

    Populates client_files_map with current clients.

    Raises:
        Exception: If reading directory fails.
    """
    client_files_map.clear()
    try:
        for file in listdir(BASE_DIRECTORY):
            if file.endswith(".txt"):
                normalized_name = file[:-4]
                client_files_map[normalized_name] = path.join(BASE_DIRECTORY, file)
        info("Loaded %d clients", len(client_files_map))
    except Exception as e:
        error("Failed to load client files: %s", e)
        print(f"[ERROR] Failed to load client files: {e}")


def create_client():
    """Creates a new client, stores data in a file, and logs the action.

    Raises:
        Exception: If writing the client file fails.
    """
    try:
        name = input("Client name: ")
        normalized_name = normalize_name(name)

        if normalized_name in client_files_map:
            print("\n[!] Error: Client already exists.\n")
            warning("Attempted to create existing client: %s", name)
            return

        phone = input("Phone number: ")
        email = input("Email address: ")
        first_service = input("First service description: ")
        registration_date = datetime.now().strftime("%Y-%m-%d")
        client_id = generate_client_id(name)

        file_path = path.join(BASE_DIRECTORY, f"{normalized_name}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"Name: {name}\n")
            file.write(f"Client_ID: {client_id}\n")
            file.write(f"Phone: {phone}\n")
            file.write(f"Email: {email}\n")
            file.write(f"RegistrationDate: {registration_date}\n")
            file.write("Services:\n")
            file.write(f"- {first_service} ({registration_date})\n")

        client_files_map[normalized_name] = file_path
        print(f"\n[✓] Client '{name}' successfully created.\n")
        info("Created client: %s", name)

    except Exception as e:
        error("Failed to create client: %s", e)
        print(f"[ERROR] Failed to create client: {e}")


def view_client():
    """Displays a specific client or lists all registered clients.

    Raises:
        Exception: If file operations fail.
    """
    try:
        option = input("Search by name (1) or list all clients (2)? ")

        if option == "1":
            name = input("Client name: ")
            normalized_name = normalize_name(name)
            file_path = client_files_map.get(normalized_name)

            if not file_path or not path.exists(file_path):
                print("\n[!] Client not found.\n")
                warning("Client not found for view: %s", name)
                return

            print("\n--- Client Details ---")
            with open(file_path, "r", encoding="utf-8") as file:
                print(file.read())
            info("Viewed client: %s", name)

        elif option == "2":
            if not client_files_map:
                print("\n[!] No clients registered.\n")
                return

            print("\nRegistered Clients:")
            for name in client_files_map:
                print(f"- {name.replace('_', ' ').title()}")
            info("Listed all clients")
        else:
            print("\n[!] Invalid option.\n")

    except Exception as e:
        error("Failed to retrieve client(s): %s", e)
        print(f"[ERROR] Failed to retrieve client(s): {e}")


def update_client():
    """Appends a new service record to a client file.

    Raises:
        Exception: If the file update fails.
    """
    try:
        name = input("Client name to update: ")
        normalized_name = normalize_name(name)
        file_path = client_files_map.get(normalized_name)

        if not file_path or not path.exists(file_path):
            print("\n[!] Client not found.\n")
            warning("Client not found for update: %s", name)
            return

        new_service = input("Enter new service description: ")
        current_date = datetime.now().strftime("%Y-%m-%d")

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"- {new_service} ({current_date})\n")

        print(f"\n[✓] Service added to client '{name}'.\n")
        info("Updated client '%s' with new service", name)

    except Exception as e:
        error("Failed to update client: %s", e)
        print(f"[ERROR] Failed to update client: {e}")


def delete_client():
    """Deletes a client file upon confirmation.

    Raises:
        Exception: If deletion fails.
    """
    try:
        name = input("Client name to delete: ")
        normalized_name = normalize_name(name)
        file_path = client_files_map.get(normalized_name)

        if not file_path or not path.exists(file_path):
            print("\n[!] Client not found.\n")
            warning("Client not found for deletion: %s", name)
            return

        confirmation = (
            input(f"Are you sure you want to delete '{name}'? (y/n): ").strip().lower()
        )
        if confirmation == "y":
            remove(file_path)
            client_files_map.pop(normalized_name)
            print(f"\n[✓] Client '{name}' successfully deleted.\n")
            info("Deleted client: %s", name)
        else:
            print("\n[-] Operation cancelled.\n")
            info("Deletion cancelled for client: %s", name)

    except Exception as e:
        error("Failed to delete client: %s", e)
        print(f"[ERROR] Failed to delete client: {e}")


def display_menu():
    """Displays the main menu with available actions."""
    print(
        """
===== Axanet Client Management Console =====
1. Create new client
2. View client information
3. Update existing client
4. Delete client
5. Exit
"""
    )


def main():
    """Main function that handles user input and routes to operations.

    Handles keyboard interrupts and logs unexpected errors.
    """
    try:
        ensure_base_directory()
        load_clients()

        while True:
            display_menu()
            option = input("Select an option: ")

            if option == "1":
                create_client()
            elif option == "2":
                view_client()
            elif option == "3":
                update_client()
            elif option == "4":
                delete_client()
            elif option == "5":
                print("\nThank you for using the Axanet Client Manager. Goodbye!\n")
                info("Application exited by user")
                break
            else:
                print("\n[!] Invalid option. Please try again.\n")

    except KeyboardInterrupt:
        print("\n[!] Program interrupted by user.\n")
        warning("Program interrupted by user")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        critical("Unexpected error occurred: %s", e)


if __name__ == "__main__":
    main()
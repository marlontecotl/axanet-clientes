"""
Custom Exception Classes for Axanet Client Manager
=================================================

This module defines custom exception classes used throughout the Axanet Client Manager
application. These exceptions provide specific error handling for different scenarios
that can occur during client management operations.

Classes:
--------
- ClientError: Base exception for all client-related errors
- ClientNotFoundError: Raised when a client cannot be found
- ClientExistsError: Raised when trying to create a client that already exists
- ValidationError: Raised when client data validation fails
- FileOperationError: Raised when file operations fail

Educational Notes for Students:
-------------------------------
1. Custom exceptions provide more specific error handling than generic exceptions
2. Inheritance hierarchy allows for catching broader or more specific error types
3. Exception messages should be descriptive to help with debugging
4. Always include context information in exception messages

Example Usage:
--------------
    try:
        client_manager.get_client("nonexistent_client")
    except ClientNotFoundError as e:
        print(f"Client not found: {e}")
    except ClientError as e:
        print(f"General client error: {e}")
"""


class ClientError(Exception):
    """
    Base exception class for all client-related errors.
    
    This is the parent class for all custom exceptions in the Axanet Client Manager.
    It allows for catching any client-related error with a single except clause.
    
    Args:
        message (str): Error message describing what went wrong
        client_name (str, optional): Name of the client involved in the error
    """
    
    def __init__(self, message: str, client_name: str):
        super().__init__(message)
        self.message = message
        self.client_name = client_name
    
    def __str__(self) -> str:
        if self.client_name:
            return f"{self.message} (Client: {self.client_name})"
        return self.message


class ClientNotFoundError(ClientError):
    """
    Exception raised when a client cannot be found.
    
    This exception is raised when attempting to access, modify, or delete
    a client that doesn't exist in the system.
    
    Example:
        raise ClientNotFoundError("Client not found", "juan_perez")
    """
    
    def __init__(self, client_name: str):
        message = f"Client '{client_name}' not found in the system"
        super().__init__(message, client_name)


class ClientExistsError(ClientError):
    """
    Exception raised when trying to create a client that already exists.
    
    This prevents duplicate client records from being created.
    
    Example:
        raise ClientExistsError("ana_garcia")
    """
    
    def __init__(self, client_name: str):
        message = f"Client '{client_name}' already exists in the system"
        super().__init__(message, client_name)


class ValidationError(ClientError):
    """
    Exception raised when client data validation fails.
    
    This exception is raised when client data doesn't meet the required
    format or business rules (e.g., invalid email, missing required fields).
    
    Args:
        field (str): The field that failed validation
        value (str): The value that failed validation
        reason (str): Why the validation failed
    """
    
    def __init__(self, field: str, value: str, reason: str):
        message = f"Validation failed for field '{field}': {reason} (Value: {value})"
        super().__init__(message)
        self.field = field
        self.value = value
        self.reason = reason


class FileOperationError(ClientError):
    """
    Exception raised when file operations fail.
    
    This exception is raised when there are issues with file system operations
    such as reading, writing, or deleting client files.
    
    Args:
        operation (str): The file operation that failed (read, write, delete)
        file_path (str): Path to the file involved in the error
        original_error (Exception, optional): The original system exception
    """
    
    def __init__(self, operation: str, file_path: str, original_error: Exception):
        message = f"File {operation} operation failed for: {file_path}"
        if original_error:
            message += f" (Reason: {str(original_error)})"
        
        super().__init__(message)
        self.operation = operation
        self.file_path = file_path
        self.original_error = original_error
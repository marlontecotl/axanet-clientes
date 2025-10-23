"""
Utility Functions for Axanet Client Manager
===========================================

This module contains utility functions and helper classes used throughout
the Axanet Client Manager application.

Functions:
----------
- setup_logging: Configure application logging
- validate_email: Email validation utility
- format_phone: Phone number formatting utility
- sanitize_filename: Make strings safe for filenames
- get_user_confirmation: CLI confirmation prompts

Educational Notes for Students:
-------------------------------
1. Utility functions promote code reuse and maintainability
2. Input validation prevents security issues and data corruption
3. Consistent formatting improves user experience
4. Logging setup centralizes debugging and monitoring capabilities
5. Helper functions abstract common operations

Design Patterns Used:
---------------------
- Utility Pattern: Static functions for common operations
- Strategy Pattern: Different formatting strategies for different data types
"""

import logging
import logging.handlers
import re
import sys
from pathlib import Path
from typing import Optional, Union


def setup_logging(
    log_file: Optional[str] = None,
    log_level: str = "INFO",
    max_file_size_mb: int = 10,
    backup_count: int = 5,
    console_output: bool = True
) -> None:
    """
    Configure application logging with file rotation and console output.
    
    Args:
        log_file (str, optional): Path to log file
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        max_file_size_mb (int): Maximum size of log file in MB before rotation
        backup_count (int): Number of backup log files to keep
        console_output (bool): Whether to output logs to console
        
    Educational Note:
        Proper logging setup is crucial for production applications.
        This function demonstrates:
        - Multiple log handlers (file + console)
        - Log rotation to prevent disk space issues
        - Configurable log levels for different environments
        - Formatted output for better readability
    """
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # Add file handler if log file is specified
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=max_file_size_mb * 1024 * 1024,  # Convert MB to bytes
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
        
    Educational Note:
        Email validation is more complex than it appears. This function
        provides basic validation suitable for most use cases. For
        production systems, consider using dedicated email validation
        libraries or services.
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(pattern, email.strip()))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if phone is valid, False otherwise
        
    Educational Note:
        Phone number validation varies significantly by country and region.
        This function provides basic validation for common formats.
        Production systems should use specialized libraries like phonenumbers.
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove common formatting characters
    clean_phone = re.sub(r'[^\d]', '', phone.strip())
    
    # Check if it contains only digits and has reasonable length
    return len(clean_phone) >= 10 and len(clean_phone) <= 15


def format_phone(phone: str) -> str:
    """
    Format phone number for consistent display.
    
    Args:
        phone (str): Raw phone number
        
    Returns:
        str: Formatted phone number
        
    Educational Note:
        Consistent formatting improves user experience and data quality.
        This function demonstrates string manipulation and regex usage.
    """
    if not phone:
        return phone
    
    # Remove all non-digit characters
    digits_only = re.sub(r'[^\d]', '', phone.strip())
    
    # Format based on length (assuming US format for 10+ digits)
    if len(digits_only) == 10:
        return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
    elif len(digits_only) == 11 and digits_only[0] == '1':
        return f"+1 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:]}"
    else:
        # Return original if it doesn't match common patterns
        return phone


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """
    Make a string safe for use as a filename.
    
    Args:
        filename (str): Original filename
        replacement (str): Character to replace invalid characters with
        
    Returns:
        str: Safe filename
        
    Educational Note:
        Filename sanitization prevents security issues and ensures
        cross-platform compatibility. Different operating systems
        have different restrictions on valid filename characters.
    """
    if not filename:
        return "unnamed"
    
    # Replace invalid filename characters
    # Invalid chars: < > : " | ? * \ /
    invalid_chars = r'[<>:"|?*\\/]'
    safe_filename = re.sub(invalid_chars, replacement, filename.strip())
    
    # Replace multiple consecutive replacement chars with single
    safe_filename = re.sub(f'{re.escape(replacement)}+', replacement, safe_filename)
    
    # Remove leading/trailing replacement chars and whitespace
    safe_filename = safe_filename.strip(f' {replacement}')
    
    # Ensure filename is not empty
    if not safe_filename:
        return "unnamed"
    
    # Limit length to prevent filesystem issues
    max_length = 200
    if len(safe_filename) > max_length:
        safe_filename = safe_filename[:max_length].rstrip(f' {replacement}')
    
    return safe_filename


def get_user_confirmation(message: str, default: bool = False) -> bool:
    """
    Get yes/no confirmation from user.
    
    Args:
        message (str): Confirmation message
        default (bool): Default value if user just presses Enter
        
    Returns:
        bool: True for yes, False for no
        
    Educational Note:
        User confirmation prevents accidental destructive operations.
        This function demonstrates input validation and default value handling.
    """
    default_text = "[Y/n]" if default else "[y/N]"
    prompt = f"{message} {default_text}: "
    
    while True:
        try:
            response = input(prompt).strip().lower()
            
            if not response:
                return default
            
            if response in ('y', 'yes', 'true', '1'):
                return True
            elif response in ('n', 'no', 'false', '0'):
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
                
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            return False


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to specified length with suffix.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length including suffix
        suffix (str): Suffix to add to truncated text
        
    Returns:
        str: Truncated text
        
    Educational Note:
        Text truncation is useful for display formatting and preventing
        layout issues in CLI applications or reports.
    """
    if not text or len(text) <= max_length:
        return text
    
    truncate_length = max_length - len(suffix)
    if truncate_length <= 0:
        return suffix[:max_length]
    
    return text[:truncate_length] + suffix


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
        
    Educational Note:
        Human-readable formatting improves user experience.
        This function demonstrates unit conversion and string formatting.
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    # Format with appropriate decimal places
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"


def validate_name(name: str) -> tuple[bool, str]:
    """
    Validate client name.
    
    Args:
        name (str): Name to validate
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
        
    Educational Note:
        Returning tuples allows functions to provide both boolean results
        and additional context (like error messages) in a single call.
    """
    if not name or not isinstance(name, str):
        return False, "Name cannot be empty"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name) > 100:
        return False, "Name cannot be longer than 100 characters"
    
    # Check for invalid characters (basic validation)
    if re.search(r'[<>:"|?*\\/]', name):
        return False, "Name contains invalid characters"
    
    return True, ""


def create_table_display(
    headers: list[str], 
    rows: list[list[str]], 
    max_width: int = 80
) -> str:
    """
    Create a formatted table for CLI display.
    
    Args:
        headers (list[str]): Column headers
        rows (list[list[str]]): Table rows
        max_width (int): Maximum total table width
        
    Returns:
        str: Formatted table string
        
    Educational Note:
        Formatted tables improve readability of CLI output.
        This function demonstrates string manipulation, padding,
        and layout calculations.
    """
    if not headers or not rows:
        return ""
    
    # Calculate column widths
    num_cols = len(headers)
    available_width = max_width - (num_cols - 1) * 3  # Account for separators
    col_width = available_width // num_cols
    
    # Ensure minimum column width
    col_width = max(col_width, 10)
    
    # Build table
    lines = []
    
    # Header
    header_line = " | ".join(h[:col_width].ljust(col_width) for h in headers)
    lines.append(header_line)
    
    # Separator
    separator = "-" * len(header_line)
    lines.append(separator)
    
    # Rows
    for row in rows:
        # Ensure row has same number of columns as headers
        padded_row = row + [""] * (num_cols - len(row))
        row_line = " | ".join(str(cell)[:col_width].ljust(col_width) 
                             for cell in padded_row[:num_cols])
        lines.append(row_line)
    
    return "\n".join(lines)
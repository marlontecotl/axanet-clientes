"""
Data Models for Axanet Client Manager
=====================================

This module contains the data models used in the Axanet Client Manager application.
The models define the structure and behavior of client data, including validation
and serialization methods.

Classes:
--------
- Client: Represents a client with their information and services
- Service: Represents a service requested by a client

Educational Notes for Students:
-------------------------------
1. Data classes provide a clean way to define data structures
2. Type hints improve code readability and enable better IDE support
3. Validation methods ensure data integrity
4. Serialization methods allow for easy data persistence
5. The __str__ and __repr__ methods provide meaningful string representations

Design Patterns Used:
---------------------
- Data Transfer Object (DTO): Client class encapsulates related data
- Factory Pattern: Class methods act as alternative constructors
- Validation Pattern: Separate methods for validating different aspects of data
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any
from re import match
import uuid

from .exceptions import ValidationError


@dataclass
class Service:
    """
    Represents a service requested by a client.
    
    This class encapsulates service information including description
    and the date when the service was requested.
    
    Attributes:
        description (str): Description of the service
        date_requested (datetime): When the service was requested
    
    Educational Note:
        Using dataclasses reduces boilerplate code and automatically
        generates __init__, __repr__, and other methods.
    """
    description: str
    date_requested: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f"- {self.description} ({self.date_requested.strftime('%Y-%m-%d')})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert service to dictionary for serialization."""
        return {
            "description": self.description,
            "date_requested": self.date_requested.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Service':
        """Create Service instance from dictionary."""
        return cls(
            description=data["description"],
            date_requested=datetime.fromisoformat(data["date_requested"])
        )


@dataclass
class Client:
    """
    Represents a client in the Axanet system.
    
    This class encapsulates all client information including personal details,
    contact information, and service history. It provides methods for validation,
    serialization, and business operations.
    
    Attributes:
        name (str): Full name of the client
        phone (str): Phone number
        email (str): Email address
        services (List[Service]): List of services requested by the client
        client_id (str): Unique identifier for the client
        registration_date (datetime): When the client was registered
    
    Educational Notes:
        - The client_id is automatically generated using UUID and timestamp
        - Services are stored as a list of Service objects
        - Validation ensures data integrity before saving
        - The normalized_name property creates filesystem-safe filenames
    """
    name: str
    phone: str
    email: str
    services: List[Service] = field(default_factory=list)
    client_id: str = field(default="")
    registration_date: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Called after dataclass initialization to set computed fields."""
        if not self.client_id:
            self.client_id = self._generate_client_id()
    
    def _generate_client_id(self) -> str:
        """
        Generate a unique client ID using initials and timestamp.
        
        Returns:
            str: Generated client ID in format "AB_20241022143045"
            
        Educational Note:
            This method combines business logic (initials) with technical
            requirements (uniqueness via timestamp) to create meaningful IDs.
        """
        # Extract initials from client name
        words = self.name.strip().split()
        initials = "".join([word[0].upper() for word in words if word])
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        return f"{initials}_{timestamp}"
    
    @property
    def normalized_name(self) -> str:
        """
        Get filesystem-safe version of client name.
        
        Returns:
            str: Normalized name suitable for filenames
            
        Educational Note:
            This property converts spaces to underscores and makes lowercase
            to ensure consistent file naming across different operating systems.
        """
        import re
        return re.sub(r"\s+", "_", self.name.strip().lower())
    
    def add_service(self, description: str) -> None:
        """
        Add a new service to the client's service history.
        
        Args:
            description (str): Description of the new service
            
        Raises:
            ValidationError: If description is empty or invalid
        """
        if not description or not description.strip():
            raise ValidationError("service_description", description, "Service description cannot be empty")
        
        service = Service(description=description.strip())
        self.services.append(service)
    
    def validate(self) -> None:
        """
        Validate all client data.
        
        Raises:
            ValidationError: If any validation rule fails
            
        Educational Note:
            Centralized validation ensures data integrity and provides
            clear error messages for debugging and user feedback.
        """
        self._validate_name()
        self._validate_phone()
        self._validate_email()
    
    def _validate_name(self) -> None:
        """Validate client name."""
        if not self.name or not self.name.strip():
            raise ValidationError("name", self.name, "Name cannot be empty")
        
        if len(self.name.strip()) < 2:
            raise ValidationError("name", self.name, "Name must be at least 2 characters long")
    
    def _validate_phone(self) -> None:
        """Validate phone number."""
        if not self.phone or not self.phone.strip():
            raise ValidationError("phone", self.phone, "Phone number cannot be empty")
        
        # Remove common phone number formatting
        clean_phone = self.phone.strip().replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        
        if not clean_phone.isdigit():
            raise ValidationError("phone", self.phone, "Phone number must contain only digits")
        
        if len(clean_phone) < 10:
            raise ValidationError("phone", self.phone, "Phone number must be at least 10 digits long")
    
    def _validate_email(self) -> None:
        """Validate email address."""
        if not self.email or not self.email.strip():
            raise ValidationError("email", self.email, "Email cannot be empty")
        
        # Basic email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not match(email_pattern, self.email.strip()):
            raise ValidationError("email", self.email, "Email format is invalid")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert client to dictionary for serialization.
        
        Returns:
            Dict[str, Any]: Client data as dictionary
            
        Educational Note:
            Serialization to dictionary allows for easy conversion to JSON,
            YAML, or other data formats for storage or API communication.
        """
        return {
            "name": self.name,
            "client_id": self.client_id,
            "phone": self.phone,
            "email": self.email,
            "registration_date": self.registration_date.isoformat(),
            "services": [service.to_dict() for service in self.services]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Client':
        """
        Create Client instance from dictionary.
        
        Args:
            data (Dict[str, Any]): Client data as dictionary
            
        Returns:
            Client: New client instance
            
        Educational Note:
            Factory methods like this provide alternative ways to create
            objects and are useful for deserialization from stored data.
        """
        client = cls(
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            client_id=data["client_id"],
            registration_date=datetime.fromisoformat(data["registration_date"])
        )
        
        # Load services
        for service_data in data.get("services", []):
            service = Service.from_dict(service_data)
            client.services.append(service)
        
        return client
    
    def to_file_format(self) -> str:
        """
        Convert client data to file format for storage.
        
        Returns:
            str: Client data formatted for text file storage
            
        Educational Note:
            This method creates a human-readable text format that matches
            the requirements specification. It's designed to be both
            machine-parseable and human-readable.
        """
        lines = [
            f"Name: {self.name}",
            f"Client_ID: {self.client_id}",
            f"Phone: {self.phone}",
            f"Email: {self.email}",
            f"RegistrationDate: {self.registration_date.strftime('%Y-%m-%d')}",
            "Services:"
        ]
        
        # Add services
        if self.services:
            for service in self.services:
                lines.append(str(service))
        else:
            lines.append("- No services registered yet")
        
        return "\n".join(lines)
    
    @classmethod
    def from_file_content(cls, content: str) -> 'Client':
        """
        Create Client instance from file content.
        
        Args:
            content (str): Content from client text file
            
        Returns:
            Client: New client instance
            
        Raises:
            ValidationError: If file format is invalid
            
        Educational Note:
            This parser reads the text file format and reconstructs the
            Client object. It demonstrates text parsing and error handling.
        """
        lines = content.strip().split('\n')
        client_data = {}
        services = []
        
        # Parse basic client information
        in_services_section = False
        
        for line in lines:
            line = line.strip()
            
            if line == "Services:":
                in_services_section = True
                continue
            
            if in_services_section:
                if line.startswith("- ") and " (" in line and line.endswith(")"):
                    # Parse service line: "- Service description (2024-10-22)"
                    service_text = line[2:]  # Remove "- "
                    
                    # Find the date in parentheses
                    last_paren = service_text.rfind("(")
                    if last_paren != -1:
                        description = service_text[:last_paren].strip()
                        date_str = service_text[last_paren+1:-1].strip()
                        
                        try:
                            service_date = datetime.strptime(date_str, "%Y-%m-%d")
                            service = Service(description=description, date_requested=service_date)
                            services.append(service)
                        except ValueError:
                            # Skip invalid date formats
                            continue
                continue
            
            # Parse key-value pairs
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                
                if key == "Name":
                    client_data["name"] = value
                elif key == "Client_ID":
                    client_data["client_id"] = value
                elif key == "Phone":
                    client_data["phone"] = value
                elif key == "Email":
                    client_data["email"] = value
                elif key == "RegistrationDate":
                    try:
                        client_data["registration_date"] = datetime.strptime(value, "%Y-%m-%d")
                    except ValueError:
                        client_data["registration_date"] = datetime.now()
        
        # Validate required fields
        required_fields = ["name", "phone", "email"]
        for field in required_fields:
            if field not in client_data:
                raise ValidationError(field, "", f"Required field '{field}' not found in file")
        
        # Create client instance
        client = cls(
            name=client_data["name"],
            phone=client_data["phone"],
            email=client_data["email"],
            client_id=client_data.get("client_id", ""),
            registration_date=client_data.get("registration_date", datetime.now())
        )
        
        # Add services
        client.services = services
        
        return client
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        service_count = len(self.services)
        return f"Client: {self.name} ({self.client_id}) - {service_count} service(s)"
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"Client(name='{self.name}', client_id='{self.client_id}', "
                f"phone='{self.phone}', email='{self.email}', "
                f"services={len(self.services)})")
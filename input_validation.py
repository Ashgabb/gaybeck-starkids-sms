"""
Data Validation and Input Sanitization
Provides validation decorators and utilities for CRUD operations
Version: 1.0.0
"""

import re
import logging
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class InputValidator:
    """Validate user inputs for various data types"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError(f"Invalid email format: {email}")
        return email
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number (10+ digits)"""
        phone_digits = re.sub(r'\D', '', str(phone))
        if len(phone_digits) < 10:
            raise ValidationError(f"Phone number too short: {phone}")
        return phone
    
    @staticmethod
    def validate_date(date_str, format='%Y-%m-%d'):
        """Validate date format"""
        try:
            return datetime.strptime(str(date_str), format)
        except ValueError:
            raise ValidationError(f"Invalid date format: {date_str}. Expected {format}")
    
    @staticmethod
    def validate_string(value, min_length=1, max_length=255, field_name="String"):
        """Validate string length"""
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        if len(value) < min_length:
            raise ValidationError(f"{field_name} too short (min: {min_length})")
        
        if len(value) > max_length:
            raise ValidationError(f"{field_name} too long (max: {max_length})")
        
        return value.strip()
    
    @staticmethod
    def validate_number(value, min_val=None, max_val=None, field_name="Number"):
        """Validate numeric value"""
        try:
            num = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be a number")
        
        if min_val is not None and num < min_val:
            raise ValidationError(f"{field_name} below minimum ({min_val})")
        
        if max_val is not None and num > max_val:
            raise ValidationError(f"{field_name} exceeds maximum ({max_val})")
        
        return num
    
    @staticmethod
    def validate_choice(value, choices, field_name="Field"):
        """Validate value is in allowed choices"""
        if value not in choices:
            raise ValidationError(f"{field_name} must be one of: {', '.join(choices)}")
        return value


class StudentValidator:
    """Validation rules for student data"""
    
    @staticmethod
    def validate_student_data(data):
        """
        Validate complete student record
        
        Args:
            data: Dictionary with student fields
            
        Returns:
            Validated and sanitized data
        """
        validator = InputValidator()
        errors = []
        
        # Validate required fields
        required_fields = ['name', 'student_id', 'date_of_birth', 'gender']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            raise ValidationError("; ".join(errors))
        
        # Validate individual fields
        try:
            data['name'] = validator.validate_string(data['name'], min_length=2, max_length=100, field_name="Name")
            data['student_id'] = validator.validate_string(data['student_id'], min_length=1, max_length=50, field_name="Student ID")
            validator.validate_date(data['date_of_birth'])
            validator.validate_choice(data['gender'], ['M', 'F', 'Other'], "Gender")
            
            # Optional fields
            if 'phone' in data and data['phone']:
                data['phone'] = validator.validate_phone(data['phone'])
            
            if 'parent_email' in data and data['parent_email']:
                data['parent_email'] = validator.validate_email(data['parent_email'])
            
            if 'bus_fee' in data and data['bus_fee']:
                data['bus_fee'] = validator.validate_number(data['bus_fee'], min_val=0)
            
            if 'monthly_fee' in data and data['monthly_fee']:
                data['monthly_fee'] = validator.validate_number(data['monthly_fee'], min_val=0)
            
        except ValidationError as e:
            raise ValidationError(f"Student validation failed: {str(e)}")
        
        return data


class TeacherValidator:
    """Validation rules for teacher data"""
    
    @staticmethod
    def validate_teacher_data(data):
        """Validate complete teacher record"""
        validator = InputValidator()
        errors = []
        
        # Validate required fields
        required_fields = ['name', 'hire_date', 'starting_salary']
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            raise ValidationError("; ".join(errors))
        
        try:
            data['name'] = validator.validate_string(data['name'], min_length=2, max_length=100, field_name="Name")
            validator.validate_date(data['hire_date'])
            data['starting_salary'] = validator.validate_number(data['starting_salary'], min_val=0)
            
            if 'phone' in data and data['phone']:
                data['phone'] = validator.validate_phone(data['phone'])
            
            if 'email' in data and data['email']:
                data['email'] = validator.validate_email(data['email'])
            
        except ValidationError as e:
            raise ValidationError(f"Teacher validation failed: {str(e)}")
        
        return data


class FinancialValidator:
    """Validation rules for financial transactions"""
    
    @staticmethod
    def validate_transaction_data(data):
        """Validate financial transaction record"""
        validator = InputValidator()
        errors = []
        
        required_fields = ['transaction_date', 'amount', 'transaction_type', 'category_id']
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            raise ValidationError("; ".join(errors))
        
        try:
            validator.validate_date(data['transaction_date'])
            data['amount'] = validator.validate_number(data['amount'], min_val=0.01, field_name="Amount")
            validator.validate_choice(data['transaction_type'], ['income', 'expense'], "Transaction Type")
            
        except ValidationError as e:
            raise ValidationError(f"Transaction validation failed: {str(e)}")
        
        return data


def validate_crud_input(validator_func):
    """
    Decorator for CRUD operations to validate inputs
    Usage: @validate_crud_input(StudentValidator.validate_student_data)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, data, *args, **kwargs):
            try:
                validated_data = validator_func(data)
                logger.debug(f"Input validation passed for {func.__name__}")
                return func(self, validated_data, *args, **kwargs)
            except ValidationError as e:
                logger.error(f"Input validation failed in {func.__name__}: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
                raise
        
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test validators
    validator = InputValidator()
    
    try:
        print("Testing validators...")
        
        # Valid email
        email = validator.validate_email("test@example.com")
        print(f"✓ Valid email: {email}")
        
        # Valid phone
        phone = validator.validate_phone("0244123456")
        print(f"✓ Valid phone: {phone}")
        
        # Valid string
        name = validator.validate_string("John Doe", min_length=2, max_length=100, field_name="Name")
        print(f"✓ Valid name: {name}")
        
        # Test student validation
        student_data = {
            'name': 'Jane Smith',
            'student_id': 'ST001',
            'date_of_birth': '2010-05-15',
            'gender': 'F',
            'phone': '0244123456',
            'parent_email': 'parent@example.com'
        }
        validated = StudentValidator.validate_student_data(student_data)
        print(f"✓ Valid student data: {validated['name']}")
        
    except ValidationError as e:
        print(f"✗ Validation error: {e}")

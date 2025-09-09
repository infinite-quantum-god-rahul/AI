import logging
from typing import Any, Dict
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)

class ErrorHandler:
    def __init__(self):
        self.error_messages = {
            'file_too_large': 'File size exceeds maximum allowed limit',
            'invalid_file_type': 'Invalid file type. Please upload PDF or DOCX files only',
            'file_processing_error': 'Error processing uploaded file',
            'resume_analysis_error': 'Error analyzing resume content',
            'job_matching_error': 'Error finding job matches',
            'database_error': 'Database operation failed',
            'authentication_error': 'Authentication failed',
            'authorization_error': 'Access denied',
            'validation_error': 'Invalid input data',
            'rate_limit_exceeded': 'Rate limit exceeded. Please try again later',
            'service_unavailable': 'Service temporarily unavailable',
            'internal_error': 'Internal server error'
        }

    def handle_error(self, error: Exception) -> str:
        """Handle and format error messages"""
        try:
            error_type = type(error).__name__
            error_message = str(error)
            
            # Log the full error for debugging
            logger.error(f"Error occurred: {error_type} - {error_message}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Return user-friendly error message
            if 'file' in error_message.lower():
                if 'size' in error_message.lower():
                    return self.error_messages['file_too_large']
                elif 'type' in error_message.lower() or 'format' in error_message.lower():
                    return self.error_messages['invalid_file_type']
                else:
                    return self.error_messages['file_processing_error']
            
            elif 'resume' in error_message.lower() or 'analysis' in error_message.lower():
                return self.error_messages['resume_analysis_error']
            
            elif 'job' in error_message.lower() or 'match' in error_message.lower():
                return self.error_messages['job_matching_error']
            
            elif 'database' in error_message.lower() or 'sql' in error_message.lower():
                return self.error_messages['database_error']
            
            elif 'auth' in error_message.lower() or 'login' in error_message.lower():
                return self.error_messages['authentication_error']
            
            elif 'permission' in error_message.lower() or 'access' in error_message.lower():
                return self.error_messages['authorization_error']
            
            elif 'validation' in error_message.lower() or 'invalid' in error_message.lower():
                return self.error_messages['validation_error']
            
            else:
                return self.error_messages['internal_error']
                
        except Exception as e:
            logger.error(f"Error in error handler: {str(e)}")
            return self.error_messages['internal_error']

    def create_error_response(self, error: Exception, request_id: str = None) -> Dict[str, Any]:
        """Create structured error response"""
        return {
            'error': type(error).__name__,
            'detail': self.handle_error(error),
            'timestamp': datetime.utcnow().isoformat(),
            'request_id': request_id
        }

    def log_error(self, error: Exception, context: str = None):
        """Log error with context"""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'timestamp': datetime.utcnow().isoformat(),
            'traceback': traceback.format_exc()
        }
        
        logger.error(f"Error logged: {error_info}")

    def validate_input(self, data: Any, required_fields: list) -> bool:
        """Validate input data"""
        try:
            if not data:
                return False
            
            if isinstance(data, dict):
                for field in required_fields:
                    if field not in data or not data[field]:
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Input validation error: {str(e)}")
            return False

    def sanitize_error_message(self, message: str) -> str:
        """Sanitize error message for user display"""
        # Remove sensitive information
        sensitive_patterns = [
            r'password',
            r'token',
            r'key',
            r'secret',
            r'credential'
        ]
        
        import re
        for pattern in sensitive_patterns:
            message = re.sub(pattern, '[REDACTED]', message, flags=re.IGNORECASE)
        
        return message

class BookingValidationError(Exception):
    """Base exception for all booking validation errors"""

    pass


class InvalidParametersError(BookingValidationError):
    """Raised when required parameters are missing or invalid"""

    pass


class InvalidDateError(BookingValidationError):
    """Raised when dates are invalid"""

    pass


class InvalidPaxConfigurationError(BookingValidationError):
    """Raised when passenger configuration is invalid"""

    pass

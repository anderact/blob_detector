def validate_parameter(value, min_value, max_value):
    return max(min_value, min(value, max_value))
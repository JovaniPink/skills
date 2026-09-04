"""Small JSON Schema subset used by the standard-library-only catalog validators."""

from __future__ import annotations

import re
from datetime import date
from urllib.parse import urlparse


def _is_type(value: object, expected: str) -> bool:
    checks = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
        "null": lambda item: item is None,
    }
    return expected in checks and checks[expected](value)


def _format_is_valid(value: str, format_name: str) -> bool:
    if format_name == "date":
        try:
            return date.fromisoformat(value).isoformat() == value
        except ValueError:
            return False
    if format_name == "uri":
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    return True


def validate_instance(instance: object, schema: object, path: str = "$") -> list[str]:
    """Validate the schema keywords used by this repository."""

    if not isinstance(schema, dict):
        return [f"{path}: schema must be an object"]
    errors: list[str] = []

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema:
        allowed = schema["enum"]
        if not isinstance(allowed, list) or instance not in allowed:
            errors.append(f"{path}: must be one of {allowed!r}")

    expected_type = schema.get("type")
    if isinstance(expected_type, str) and not _is_type(instance, expected_type):
        errors.append(f"{path}: expected {expected_type}, found {type(instance).__name__}")
        return errors

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            return errors + [f"{path}: schema properties must be an object"]
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in instance:
                    errors.append(f"{path}: missing required property {key!r}")
        minimum = schema.get("minProperties")
        if isinstance(minimum, int) and len(instance) < minimum:
            errors.append(f"{path}: requires at least {minimum} properties")
        maximum = schema.get("maxProperties")
        if isinstance(maximum, int) and len(instance) > maximum:
            errors.append(f"{path}: permits at most {maximum} properties")
        for key, value in instance.items():
            child_path = f"{path}.{key}"
            if key in properties:
                errors.extend(validate_instance(value, properties[key], child_path))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{child_path}: additional property is not allowed")

    if isinstance(instance, list):
        minimum = schema.get("minItems")
        if isinstance(minimum, int) and len(instance) < minimum:
            errors.append(f"{path}: requires at least {minimum} items")
        maximum = schema.get("maxItems")
        if isinstance(maximum, int) and len(instance) > maximum:
            errors.append(f"{path}: permits at most {maximum} items")
        if schema.get("uniqueItems") is True:
            for index, value in enumerate(instance):
                if value in instance[:index]:
                    errors.append(f"{path}[{index}]: duplicate item is not allowed")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, value in enumerate(instance):
                errors.extend(validate_instance(value, item_schema, f"{path}[{index}]"))

    if isinstance(instance, str):
        minimum = schema.get("minLength")
        if isinstance(minimum, int) and len(instance) < minimum:
            errors.append(f"{path}: requires at least {minimum} characters")
        maximum = schema.get("maxLength")
        if isinstance(maximum, int) and len(instance) > maximum:
            errors.append(f"{path}: permits at most {maximum} characters")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, instance) is None:
            errors.append(f"{path}: does not match required pattern {pattern!r}")
        format_name = schema.get("format")
        if isinstance(format_name, str) and not _format_is_valid(instance, format_name):
            errors.append(f"{path}: is not a valid {format_name}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        minimum = schema.get("minimum")
        if isinstance(minimum, (int, float)) and instance < minimum:
            errors.append(f"{path}: must be at least {minimum}")
        maximum = schema.get("maximum")
        if isinstance(maximum, (int, float)) and instance > maximum:
            errors.append(f"{path}: must be at most {maximum}")

    return errors

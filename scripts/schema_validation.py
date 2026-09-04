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
        "number": lambda item: (
            isinstance(item, (int, float)) and not isinstance(item, bool)
        ),
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


def _resolve_local_reference(
    schema: dict[str, object], root_schema: dict[str, object], path: str
) -> tuple[dict[str, object] | None, list[str]]:
    reference = schema.get("$ref")
    if reference is None:
        return schema, []
    if not isinstance(reference, str) or not reference.startswith("#/"):
        return None, [f"{path}: unsupported schema reference {reference!r}"]
    target: object = root_schema
    for raw_part in reference.removeprefix("#/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(target, dict) or part not in target:
            return None, [f"{path}: unresolved schema reference {reference!r}"]
        target = target[part]
    if not isinstance(target, dict):
        return None, [
            f"{path}: schema reference {reference!r} must resolve to an object"
        ]
    return target, []


def _validate_instance(
    instance: object, schema: object, path: str, root_schema: dict[str, object]
) -> list[str]:
    """Validate the supported JSON Schema subset against one instance value."""

    if not isinstance(schema, dict):
        return [f"{path}: schema must be an object"]
    schema, reference_errors = _resolve_local_reference(schema, root_schema, path)
    if schema is None:
        return reference_errors
    errors: list[str] = []

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema:
        allowed = schema["enum"]
        if not isinstance(allowed, list) or instance not in allowed:
            errors.append(f"{path}: must be one of {allowed!r}")

    expected_type = schema.get("type")
    allowed_types = [expected_type] if isinstance(expected_type, str) else expected_type
    if allowed_types is not None:
        if not isinstance(allowed_types, list) or not all(
            isinstance(item, str) for item in allowed_types
        ):
            return errors + [
                f"{path}: schema type must be a string or array of strings"
            ]
        if not any(_is_type(instance, item) for item in allowed_types):
            expected = (
                allowed_types[0]
                if len(allowed_types) == 1
                else f"one of {allowed_types!r}"
            )
            errors.append(
                f"{path}: expected {expected}, found {type(instance).__name__}"
            )
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
                errors.extend(
                    _validate_instance(value, properties[key], child_path, root_schema)
                )
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
                errors.extend(
                    _validate_instance(
                        value, item_schema, f"{path}[{index}]", root_schema
                    )
                )

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


def validate_instance(instance: object, schema: object, path: str = "$") -> list[str]:
    """Validate the schema keywords used by this repository."""

    if not isinstance(schema, dict):
        return [f"{path}: schema must be an object"]
    return _validate_instance(instance, schema, path, schema)

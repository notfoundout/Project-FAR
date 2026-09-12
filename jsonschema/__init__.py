"""Constrained local jsonschema-compatible validator used when PyPI is unavailable."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable

__version__ = "4.22.0"

@dataclass(frozen=True)
class ValidationError(Exception):
    message: str
    path: tuple[Any, ...] = ()
    schema_path: tuple[Any, ...] = ()
    def __str__(self) -> str: return self.message

class Draft202012Validator:
    def __init__(self, schema: dict[str, Any]):
        self.schema = schema
    @classmethod
    def check_schema(cls, schema: dict[str, Any]) -> None:
        if not isinstance(schema, dict):
            raise ValidationError("schema must be an object")
    def iter_errors(self, instance: Any) -> Iterable[ValidationError]:
        yield from _validate(instance, self.schema, self.schema, (), ())

def _resolve(ref: str, root: dict[str, Any]) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValidationError(f"unsupported ref: {ref}")
    cur: Any = root
    for part in ref[2:].split('/'):
        cur = cur[part]
    return cur

def _type_ok(instance: Any, typ: Any) -> bool:
    if isinstance(typ, list):
        return any(_type_ok(instance, member) for member in typ)
    return {
        "object": isinstance(instance, dict),
        "array": isinstance(instance, list),
        "string": isinstance(instance, str),
        "integer": isinstance(instance, int) and not isinstance(instance, bool),
        "number": isinstance(instance, (int, float)) and not isinstance(instance, bool),
        "null": instance is None,
        "boolean": isinstance(instance, bool),
    }.get(typ, True)

def _unique(values: list[Any]) -> bool:
    return all(not any(value == prior for prior in values[:index]) for index, value in enumerate(values))

def _validate(instance: Any, schema: dict[str, Any], root: dict[str, Any], path: tuple[Any,...], spath: tuple[Any,...]):
    if "$ref" in schema:
        yield from _validate(instance, _resolve(schema["$ref"], root), root, path, spath+("$ref",)); return
    if "allOf" in schema:
        for i, sub in enumerate(schema["allOf"]): yield from _validate(instance, sub, root, path, spath+("allOf",i))
    if "oneOf" in schema:
        matches=[]; errors=[]
        for i, sub in enumerate(schema["oneOf"]):
            errs=list(_validate(instance, sub, root, path, spath+("oneOf",i)))
            if not errs: matches.append(i)
            errors.extend(errs)
        if len(matches)!=1:
            yield ValidationError("value must match exactly one allowed schema", path, spath+("oneOf",)); return
    if "const" in schema and instance != schema["const"]:
        yield ValidationError(f"expected constant {schema['const']!r}", path, spath+("const",))
    if "enum" in schema and instance not in schema["enum"]:
        yield ValidationError(f"value {instance!r} is not in enum", path, spath+("enum",))
    typ=schema.get("type")
    if typ and not _type_ok(instance, typ):
        yield ValidationError(f"expected type {typ}", path, spath+("type",)); return
    if isinstance(instance, str):
        import re
        if schema.get("minLength") is not None and len(instance)<schema["minLength"]: yield ValidationError("string is shorter than minLength", path, spath+("minLength",))
        if schema.get("maxLength") is not None and len(instance)>schema["maxLength"]: yield ValidationError("string is longer than maxLength", path, spath+("maxLength",))
        # JSON Schema `pattern` succeeds when the regular expression matches
        # anywhere in the instance; it is not an implicit full-string match.
        if schema.get("pattern") and not re.search(schema["pattern"], instance): yield ValidationError("string does not match pattern", path, spath+("pattern",))
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if schema.get("minimum") is not None and instance < schema["minimum"]: yield ValidationError("number is below minimum", path, spath+("minimum",))
        if schema.get("maximum") is not None and instance > schema["maximum"]: yield ValidationError("number is above maximum", path, spath+("maximum",))
        if schema.get("exclusiveMinimum") is not None and instance <= schema["exclusiveMinimum"]: yield ValidationError("number is not above exclusiveMinimum", path, spath+("exclusiveMinimum",))
        if schema.get("exclusiveMaximum") is not None and instance >= schema["exclusiveMaximum"]: yield ValidationError("number is not below exclusiveMaximum", path, spath+("exclusiveMaximum",))
    if isinstance(instance, list):
        if schema.get("minItems") is not None and len(instance)<schema["minItems"]: yield ValidationError("array has fewer items than minItems", path, spath+("minItems",))
        if schema.get("maxItems") is not None and len(instance)>schema["maxItems"]: yield ValidationError("array has more items than maxItems", path, spath+("maxItems",))
        if schema.get("uniqueItems") is True and not _unique(instance): yield ValidationError("array items are not unique", path, spath+("uniqueItems",))
        item_schema=schema.get("items")
        if item_schema:
            for i, item in enumerate(instance): yield from _validate(item, item_schema, root, path+(i,), spath+("items",))
    if isinstance(instance, dict) or "properties" in schema:
        if not isinstance(instance, dict): return
        if schema.get("minProperties") is not None and len(instance)<schema["minProperties"]: yield ValidationError("object has fewer properties than minProperties", path, spath+("minProperties",))
        if schema.get("maxProperties") is not None and len(instance)>schema["maxProperties"]: yield ValidationError("object has more properties than maxProperties", path, spath+("maxProperties",))
        for req in schema.get("required", []):
            if req not in instance: yield ValidationError(f"required property {req!r} is missing", path, spath+("required",))
        props=schema.get("properties", {})
        additional=schema.get("additionalProperties", True)
        for k in instance:
            if k in props:
                continue
            if additional is False:
                yield ValidationError(f"additional property {k!r} is not allowed", path+(k,), spath+("additionalProperties",))
            elif isinstance(additional, dict):
                yield from _validate(instance[k], additional, root, path+(k,), spath+("additionalProperties",))
        for k, sub in props.items():
            if k in instance: yield from _validate(instance[k], sub, root, path+(k,), spath+("properties",k))

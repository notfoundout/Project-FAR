"""Constrained local jsonschema-compatible validator used when PyPI is unavailable.

This is not upstream ``jsonschema``. It implements the Draft 2020-12 keywords listed in
``SUPPORTED_KEYWORDS`` and fails closed on any other keyword: a schema that uses an
unimplemented keyword raises ``ValidationError`` when a validator is constructed, instead of
silently ignoring the constraint. ``format`` is an annotation, as in upstream without a format
checker. ``pattern`` uses ECMA-262 semantics for ``$`` and ``.`` as JSON Schema requires.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import re
from typing import Any, Iterable

__version__ = "4.22.0+far.local"

#: Draft 2020-12 assertion and applicator keywords this validator enforces.
SUPPORTED_KEYWORDS = frozenset({
    "$ref", "allOf", "anyOf", "oneOf", "not", "if", "then", "else",
    "type", "const", "enum",
    "minLength", "maxLength", "pattern",
    "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum",
    "minItems", "maxItems", "uniqueItems", "items", "contains", "minContains", "maxContains",
    "minProperties", "maxProperties", "required", "properties", "additionalProperties", "propertyNames",
})
#: Keywords with no validation semantics (identifiers, annotations, definitions containers).
ANNOTATION_KEYWORDS = frozenset({
    "$schema", "$id", "$defs", "definitions", "$comment", "title", "description",
    "default", "examples", "format", "readOnly", "writeOnly", "deprecated",
})
_TYPES = frozenset({"object", "array", "string", "integer", "number", "null", "boolean"})
_SUBSCHEMA = ("not", "if", "then", "else", "items", "contains", "additionalProperties", "propertyNames")
_SUBSCHEMA_LISTS = ("allOf", "anyOf", "oneOf")
_SUBSCHEMA_MAPS = ("properties", "$defs", "definitions")

@dataclass(frozen=True)
class ValidationError(Exception):
    message: str
    path: tuple[Any, ...] = ()
    schema_path: tuple[Any, ...] = ()
    def __str__(self) -> str: return self.message

class Draft202012Validator:
    def __init__(self, schema: dict[str, Any]):
        self.check_schema(schema)
        self.schema = schema
    @classmethod
    def check_schema(cls, schema: dict[str, Any]) -> None:
        if not isinstance(schema, dict):
            raise ValidationError("schema must be an object")
        problems = sorted(set(_schema_problems(schema, schema, ())))
        if problems:
            raise ValidationError("unsupported or invalid schema: " + "; ".join(problems))
    def iter_errors(self, instance: Any) -> Iterable[ValidationError]:
        yield from _validate(instance, self.schema, self.schema, (), ())

def _schema_problems(schema: Any, root: dict[str, Any], spath: tuple[Any, ...]) -> Iterable[str]:
    where = "/".join(str(part) for part in spath) or "<root>"
    if isinstance(schema, bool):
        return
    if not isinstance(schema, dict):
        yield f"{where}: subschema must be an object or boolean"
        return
    for key, value in schema.items():
        if key not in SUPPORTED_KEYWORDS and key not in ANNOTATION_KEYWORDS:
            yield f"{where}: unsupported keyword {key!r}"
        elif key == "$ref":
            if not isinstance(value, str) or not value.startswith("#/"):
                yield f"{where}: unsupported non-local $ref {value!r}"
            else:
                try:
                    _resolve(value, root)
                except (KeyError, TypeError, ValidationError):
                    yield f"{where}: unresolvable $ref {value!r}"
        elif key == "type":
            members = value if isinstance(value, list) else [value]
            for member in members:
                if member not in _TYPES:
                    yield f"{where}: unknown type {member!r}"
        elif key == "pattern":
            try:
                re.compile(_ecma_pattern(value))
            except (re.error, TypeError) as exc:
                yield f"{where}: invalid pattern {value!r}: {exc}"
        elif key in _SUBSCHEMA:
            yield from _schema_problems(value, root, spath + (key,))
        elif key in _SUBSCHEMA_LISTS:
            if not isinstance(value, list) or not value:
                yield f"{where}: {key} must be a non-empty array"
            else:
                for i, sub in enumerate(value): yield from _schema_problems(sub, root, spath + (key, i))
        elif key in _SUBSCHEMA_MAPS:
            if not isinstance(value, dict):
                yield f"{where}: {key} must be an object"
            else:
                for name, sub in value.items(): yield from _schema_problems(sub, root, spath + (key, name))

def _ecma_pattern(pattern: str) -> str:
    """Translate ECMA-262 ``$`` (end of input only) and ``.`` (no line terminators) to ``re``.

    Python's ``$`` also matches before a trailing newline and its ``.`` matches ``\\r``,
    U+2028 and U+2029, so an unmodified ``re.search`` accepts strings ECMA-262 rejects.
    """
    out: list[str] = []
    in_class = False
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == "\\" and i + 1 < len(pattern):
            out.append(pattern[i:i + 2]); i += 2; continue
        if in_class:
            if char == "]": in_class = False
            out.append(char)
        elif char == "[":
            # ECMA-262 `[]`/`[^]` have no Python equivalent; `re` rejects them, so the schema
            # check fails closed instead of silently translating them.
            in_class = True; out.append(char)
        elif char == "$":
            out.append(r"\Z")
        elif char == ".":
            out.append("[^\\n\\r\\u2028\\u2029]")
        else:
            out.append(char)
        i += 1
    return "".join(out)

def _resolve(ref: str, root: dict[str, Any]) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValidationError(f"unsupported ref: {ref}")
    cur: Any = root
    for part in ref[2:].split('/'):
        cur = cur[part.replace("~1", "/").replace("~0", "~")]
    return cur

def _type_ok(instance: Any, typ: Any) -> bool:
    if isinstance(typ, list):
        return any(_type_ok(instance, member) for member in typ)
    if typ == "integer":
        if isinstance(instance, bool):
            return False
        if isinstance(instance, int):
            return True
        return isinstance(instance, float) and math.isfinite(instance) and instance.is_integer()
    return {
        "object": isinstance(instance, dict),
        "array": isinstance(instance, list),
        "string": isinstance(instance, str),
        "number": isinstance(instance, (int, float)) and not isinstance(instance, bool),
        "null": instance is None,
        "boolean": isinstance(instance, bool),
    }[typ]

def _json_equal(left: Any, right: Any) -> bool:
    """Compare JSON values without Python's bool/int equality collapse."""
    if isinstance(left, bool) or isinstance(right, bool):
        return isinstance(left, bool) and isinstance(right, bool) and left is right
    if left is None or right is None:
        return left is None and right is None
    left_number = isinstance(left, (int, float)) and not isinstance(left, bool)
    right_number = isinstance(right, (int, float)) and not isinstance(right, bool)
    if left_number or right_number:
        return left_number and right_number and left == right
    if isinstance(left, str) or isinstance(right, str):
        return isinstance(left, str) and isinstance(right, str) and left == right
    if isinstance(left, list) or isinstance(right, list):
        return (
            isinstance(left, list)
            and isinstance(right, list)
            and len(left) == len(right)
            and all(_json_equal(a, b) for a, b in zip(left, right))
        )
    if isinstance(left, dict) or isinstance(right, dict):
        return (
            isinstance(left, dict)
            and isinstance(right, dict)
            and set(left) == set(right)
            and all(_json_equal(left[key], right[key]) for key in left)
        )
    return False

def _unique(values: list[Any]) -> bool:
    return all(
        not any(_json_equal(value, prior) for prior in values[:index])
        for index, value in enumerate(values)
    )

def _valid(instance: Any, schema: Any, root: dict[str, Any], path: tuple[Any, ...], spath: tuple[Any, ...]) -> bool:
    return next(iter(_validate(instance, schema, root, path, spath)), None) is None

def _validate(instance: Any, schema: Any, root: dict[str, Any], path: tuple[Any,...], spath: tuple[Any,...]):
    if schema is True:
        return
    if schema is False:
        yield ValidationError("false schema does not allow any value", path, spath); return
    if "$ref" in schema:
        # Draft 2020-12 evaluates keywords adjacent to $ref as well as the referenced schema.
        yield from _validate(instance, _resolve(schema["$ref"], root), root, path, spath+("$ref",))
    if "allOf" in schema:
        for i, sub in enumerate(schema["allOf"]): yield from _validate(instance, sub, root, path, spath+("allOf",i))
    if "anyOf" in schema:
        if not any(_valid(instance, sub, root, path, spath+("anyOf",i)) for i, sub in enumerate(schema["anyOf"])):
            yield ValidationError("value must match at least one allowed schema", path, spath+("anyOf",))
    if "oneOf" in schema:
        matches=[]; errors=[]
        for i, sub in enumerate(schema["oneOf"]):
            errs=list(_validate(instance, sub, root, path, spath+("oneOf",i)))
            if not errs: matches.append(i)
            errors.extend(errs)
        if len(matches)!=1:
            yield ValidationError("value must match exactly one allowed schema", path, spath+("oneOf",)); return
    if "not" in schema and _valid(instance, schema["not"], root, path, spath+("not",)):
        yield ValidationError("value must not match the disallowed schema", path, spath+("not",))
    if "if" in schema:
        if _valid(instance, schema["if"], root, path, spath+("if",)):
            if "then" in schema: yield from _validate(instance, schema["then"], root, path, spath+("then",))
        elif "else" in schema:
            yield from _validate(instance, schema["else"], root, path, spath+("else",))
    if "const" in schema and not _json_equal(instance, schema["const"]):
        yield ValidationError(f"expected constant {schema['const']!r}", path, spath+("const",))
    if "enum" in schema and not any(_json_equal(instance, item) for item in schema["enum"]):
        yield ValidationError(f"value {instance!r} is not in enum", path, spath+("enum",))
    typ=schema.get("type")
    if typ and not _type_ok(instance, typ):
        yield ValidationError(f"expected type {typ}", path, spath+("type",)); return
    if isinstance(instance, str):
        if schema.get("minLength") is not None and len(instance)<schema["minLength"]: yield ValidationError("string is shorter than minLength", path, spath+("minLength",))
        if schema.get("maxLength") is not None and len(instance)>schema["maxLength"]: yield ValidationError("string is longer than maxLength", path, spath+("maxLength",))
        # JSON Schema `pattern` succeeds when the regular expression matches
        # anywhere in the instance; it is not an implicit full-string match.
        if schema.get("pattern") and not re.search(_ecma_pattern(schema["pattern"]), instance): yield ValidationError("string does not match pattern", path, spath+("pattern",))
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
        if item_schema is not None:
            for i, item in enumerate(instance): yield from _validate(item, item_schema, root, path+(i,), spath+("items",))
        if "contains" in schema:
            matched = sum(1 for i, item in enumerate(instance) if _valid(item, schema["contains"], root, path+(i,), spath+("contains",)))
            low = schema.get("minContains", 1); high = schema.get("maxContains")
            if matched < low: yield ValidationError("array does not contain enough matching items", path, spath+("contains",))
            if high is not None and matched > high: yield ValidationError("array contains too many matching items", path, spath+("maxContains",))
    if isinstance(instance, dict) or "properties" in schema:
        if not isinstance(instance, dict): return
        if schema.get("minProperties") is not None and len(instance)<schema["minProperties"]: yield ValidationError("object has fewer properties than minProperties", path, spath+("minProperties",))
        if schema.get("maxProperties") is not None and len(instance)>schema["maxProperties"]: yield ValidationError("object has more properties than maxProperties", path, spath+("maxProperties",))
        for req in schema.get("required", []):
            if req not in instance: yield ValidationError(f"required property {req!r} is missing", path, spath+("required",))
        if "propertyNames" in schema:
            for k in instance: yield from _validate(k, schema["propertyNames"], root, path+(k,), spath+("propertyNames",))
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

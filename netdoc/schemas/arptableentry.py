"""Schema validation for ArpTableEntry."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from jsonschema import validate, FormatChecker

from dcim.models import Interface as Interface_model

from netdoc.models import ArpTableEntry
from netdoc import utils


def get_schema():
    """Return the JSON schema to validate ArpTableEntry data."""
    return {
        "type": "object",
        "properties": {
            "interface_id": {
                "type": "integer",
                "enum": list(
                    Interface_model.objects.all().values_list("id", flat=True)
                ),
            },
            "ip_address": {
                "type": "string",
            },
            "mac_address": {
                "type": "string",
            },
        },
    }


def get_schema_create():
    """Return the JSON schema to validate new ArpTableEntry objects."""
    schema = get_schema()
    schema["required"] = [
        "interface_id",
        "ip_address",
        "mac_address",
    ]
    return schema


def create(**kwargs):
    """Create an ArpTableEntry."""
    kwargs = utils.delete_empty_keys(kwargs)
    validate(kwargs, get_schema_create(), format_checker=FormatChecker())
    obj = utils.object_create(ArpTableEntry, **kwargs)
    return obj


def get(interface_id, ip_address, mac_address, discovered=True):
    """Return an ArpTableEntry."""
    obj = utils.object_get_or_none(
        ArpTableEntry,
        interface_id=interface_id,
        ip_address=ip_address,
        mac_address=mac_address,
    )
    if obj and discovered:
        # Update updated_at
        obj.save()
    return obj


def get_list(**kwargs):
    """Get a list of ArpTableEntry objects."""
    validate(kwargs, get_schema(), format_checker=FormatChecker())
    result = utils.object_list(ArpTableEntry, **kwargs)
    return result

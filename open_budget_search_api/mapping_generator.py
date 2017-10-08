from copy import copy


class MappingGenerator(object):

    def __init__(self, base=None):
        if base is None:
            base = {}
        self._mapping = base
        self._search_fields = []

    @classmethod
    def _convert_date_format(cls, fmt):
        if fmt is not None and fmt.startswith('fmt:'):
            fmt = fmt[4:]
            fmt = fmt.replace('%d', 'dd')
            fmt = fmt.replace('%m', 'MM')
            fmt = fmt.replace('%y', 'yy')
            fmt = fmt.replace('%Y', 'yyyy')
            fmt = fmt.replace('%H', 'HH')
            fmt = fmt.replace('%M', 'mm')
            fmt = fmt.replace('%S', 'ss')
            fmt = fmt.replace('%f', 'SSS')
            assert '%' not in fmt
            return fmt
        else:
            return 'strict_date_optional_time'

    @classmethod
    def _convert_field(cls, field, search_fields, prefix):
        schema_type = field['type']
        if schema_type == 'array':
            field = copy(field)
            field['type'] = field['es:itemType']
            return cls._convert_field(field, search_fields, prefix)
        enabled = field.get('es:index', True)
        subschema = {'fields': []}
        if enabled and schema_type == 'object':
            subschema = field['es:schema']
        converted_type, prop = {
            "integer": ("long",
                        {"ignore_malformed": True,
                         "index": False}),
            "number": ("scaled_float",
                       {"scaling_factor": 100,
                        "ignore_malformed": True,
                        "index": False}),
            "string": ("text", {}),
            "boolean": ("boolean", {}),
            "date": ("date",
                     {"ignore_malformed": True,
                      "format": cls._convert_date_format(field.get('format'))}),
            "datetime": ("date",
                         {"ignore_malformed": True,
                          "format": cls._convert_date_format(field.get('format'))}),
            "object": (None,
                       {"properties":
                           cls._update_properties({}, subschema, search_fields, prefix + field['name'] + '.')
                           if enabled else {},
                        "enabled": enabled,
                        "dynamic": False})
        }[schema_type]
        if converted_type is not None:
            prop['type'] = converted_type
        if converted_type == 'text':
            search_field = prefix + field['name']
            if 'es:title' in field:
                search_field += '^10'
            search_fields.append(search_field)
        return field['name'], prop

    @classmethod
    def _update_properties(cls, properties, schema, search_fields, prefix=''):
        fields = schema['fields']
        properties.update(dict(cls._convert_field(f, search_fields, prefix) for f in fields))
        return properties

    def generate_from_schema(self, schema):
        properties = {}
        self._search_fields = []
        self._mapping['properties'] = properties
        self._update_properties(properties, schema, self._search_fields)

    def get_mapping(self):
        return self._mapping

    def get_search_fields(self):
        return self._search_fields

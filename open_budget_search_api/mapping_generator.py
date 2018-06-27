from copy import copy


class MappingGenerator(object):

    def __init__(self):
        self._search_fields = []

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
        converted_type, _ = {
            "integer": ("long",{}),
            "number": ("scaled_float",{}),
            "string": ("text", {}),
            "boolean": ("boolean", {}),
            "date": ("date",{}),
            "datetime": ("date",{}),
            "object": (None,
                       {"properties":
                           cls._update_properties(subschema, search_fields, prefix + field['name'] + '.')
                           if enabled else {}})
        }[schema_type]
        if converted_type == 'text':
            if field['name'] not in ('doc_id',):
                search_field = prefix + field['name']
                to_add = [search_field]
                if 'es:title' in field or 'es:hebrew' in field:
                    to_add.append(search_field+'.hebrew^10')
                search_fields.extend(to_add)

    @classmethod
    def _update_properties(cls, schema, search_fields, prefix=''):
        fields = schema['fields']
        for f in fields:
            cls._convert_field(f, search_fields, prefix)

    def generate_from_schema(self, schema):
        self._search_fields = []
        self._update_properties(schema, self._search_fields)

    def get_search_fields(self):
        return self._search_fields

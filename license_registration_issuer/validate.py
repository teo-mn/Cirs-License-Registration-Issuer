from jsonschema import validators, Draft7Validator, ValidationError


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for _property, sub_schema in properties.items():
            if "default" in sub_schema:
                instance.setdefault(_property, sub_schema["default"])
                if _property in instance and instance[_property] is None:
                    instance[_property] = sub_schema["default"]

        for error in validate_properties(
                validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


def parse_error_message(e: ValidationError):
    msg = '[' + '.'.join(map(str, e.absolute_path)) + '] ' + e.message
    # msg = e.message
    if 'error_msg' in e.schema:
        msg = e.schema['error_msg']
    if e.validator == 'required':
        for x in e.validator_value:
            if '\'' + x + '\'' in e.message and 'properties' in e.schema \
                    and x in e.schema['properties'] and 'error_msg' in e.schema['properties'][x]:
                msg = e.schema['properties'][x]['error_msg']
    return msg


CustomValidator = extend_with_default(Draft7Validator)

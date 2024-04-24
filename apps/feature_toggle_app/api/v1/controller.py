from .db_controller import get_toggle_list_with_filters_db, create_feature_toggle_db, bulk_update_toggle_state_db, bulk_update_toggle_environment_db, get_toggle_detail_db

def get_feature_toggle_list(filters):
    filters.update({"is_deleted": False})
    result = get_toggle_list_with_filters_db(filters)
    return result


def get_feature_toggle_detail_by_identifier(identifier):
    result = get_toggle_detail_db(identifier)
    return result


def create_feature_toggle(data):
    result = create_feature_toggle_db(data)
    return result


def bulk_update_toggle_state(toggle_ids, state, metadata):
    if not toggle_ids:
        return False
    # Prepare updates
    update_fields = {'state': state}

    # Add additional metadata fields to update if they exist
    if 'updated_by' in metadata:
        update_fields['updated_by'] = metadata['updated_by']

    if 'notes' in metadata:
        update_fields['notes'] = metadata['notes']

    updated_count = bulk_update_toggle_state_db(toggle_ids, update_fields)

    return {'updated_count': updated_count}


def bulk_update_toggle_environment(toggle_ids, environment, metadata):
    if not toggle_ids:
        return False
    # Prepare updates
    update_fields = {'environment': environment}

    # Add additional metadata fields to update if they exist
    if 'updated_by' in metadata:
        update_fields['updated_by'] = metadata['updated_by']

    if 'notes' in metadata:
        update_fields['notes'] = metadata['notes']

    updated_count = bulk_update_toggle_environment_db(toggle_ids, update_fields)

    return {'updated_count': updated_count}

from .db_controller import get_toggle_list_with_filters_db, create_feature_toggle_db


def get_feature_toggle_list(filters):
    result = get_toggle_list_with_filters_db(filters)
    return result

def create_feature_toggle(post_data):
    result = create_feature_toggle_db(post_data)
    return result
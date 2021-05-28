from constants.general_constants import Classification
from constants.db_constants import Tables
from services.db_utilities import retrieve_table_mapping
from fuzzy_match import match


def categorize_vendors(vendor_ids):
    """
    Determines closest vendor name in database and returns its category_id

    :param vendor_ids: list of vendor ids to categorize
    :return: dictionary mapping vendor name to category id
    """
    # Get mapping between vendor name and vendor id
    vendors_name_id_mapping = retrieve_table_mapping(Tables.VENDORS, "vendorName", "vendorId")
    vendors_id_name_mapping = {v: k for k, v in vendors_name_id_mapping.items()}

    # Get mapping between vendor id and category id
    vendor_id_category_mapping = retrieve_table_mapping(Tables.VENDOR_CATEGORIES, "vendorId", "categoryId")

    # Vendor names to categorize
    names_to_categorize = [vendors_id_name_mapping[v_id] for v_id in vendor_ids]

    # List of vendor names
    name_list = vendors_name_id_mapping.keys()
    vendor_id_category_id_dict = {}
    for search_name in names_to_categorize:
        if search_name not in vendor_id_category_id_dict:
            # Default category id is -1
            category_id = -1

            # Extract existing vendor name with lowest levenshtein distance, using minimum threshold
            best_match = match.extractOne(search_name, name_list, "levenshtein", Classification.MIN_DISTANCE)
            if best_match is not None:
                match_id = vendors_name_id_mapping[best_match[0]]
                category_id = vendor_id_category_mapping.get(match_id, -1)

            # Add vendor id + category id combination to dictionary
            vendor_id = vendors_name_id_mapping[search_name]
            vendor_id_category_id_dict[vendor_id] = category_id
    return vendor_id_category_id_dict

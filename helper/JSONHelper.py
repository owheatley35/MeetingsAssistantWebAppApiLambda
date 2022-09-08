from typing import List


def convert_custom_object_list_to_dict(input_list: List[any]) -> List[dict]:
    """
    Converts a list of any custom object into a dictionary, ready for conversion to json
    :param input_list: List of any object
    :return: List of dictionary of the objects
    """
    new_list = []

    for item in input_list:
        new_list.append(item.__dict__)

    return new_list


def convert_custom_object_to_dict(input_object: any) -> dict:
    """
    Converts any object to its dictionary form
    :param input_object: any object to be converted to a dictionary
    :return: dictionary of object
    """
    return input_object.__dict__

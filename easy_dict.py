def get_data_from(nested_dictionary, simple_key):
    curr_dict = nested_dictionary
    for key in simple_key:
        curr_dict = curr_dict[key]
    return curr_dict


# example usage
if __name__ == "__main__":
    my_dict = {'oi': [{'opa': 3}]}
    get_3 = ['oi', 0]
    print(get_data_from(my_dict, get_3))

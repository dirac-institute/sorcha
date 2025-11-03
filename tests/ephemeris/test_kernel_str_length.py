# This file tests if the function _split_kernel_path_str() returns the right string
from sorcha.utilities.generate_meta_kernel import _split_kernel_path_str

def test_kernel_str_length():

    # Each list in the tuple is a test containing the input, expected output and split value for the function, respectively
    test_strings = (["this is a test string", "this is a test +' 'string", 15],
                    ["this is another test string which is slightly larger", "this is another+' ' test string wh+' 'ich is slightly+' ' larger", 15], 
                    ["small string","small string", 79],
                    ["split will be the length of this string to see what happens", "split will be the length of this string to see what happens+' '", 59])
    print(test_strings[0])
    for test_data in test_strings:
        print(test_data[0])
        output = _split_kernel_path_str(test_data[0], split = test_data[2])
        assert output == test_data[1]

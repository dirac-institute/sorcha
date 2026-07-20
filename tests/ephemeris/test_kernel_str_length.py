# This file tests if the function _split_kernel_path_str() returns the right string
import os
import spiceypy
from sorcha.utilities.generate_meta_kernel import _split_kernel_path_str

def test_kernel_str_length():

    # Each list in the tuple is a test containing the input, expected output and split value for the function, respectively
    test_strings = (
        ["this is a test string", "this is a test +',\n'string", 15],
        [
            "this is another test string which is slightly larger",
            "this is another+',\n' test string wh+',\n'ich is slightly+',\n' larger",
            15,
        ],
        ["small string", "small string", 79],
        [
            "split will be the length of this string to see what happens",
            "split will be the length of this string to see what happens+',\n'",
            59,
        ],
    )
    for test_data in test_strings:
        output = _split_kernel_path_str(test_data[0], split=test_data[2])
        assert output == test_data[1]



def test_meta_kernel_loads_under_long_path(tmp_path):
    # A cache path long enough to trip the SPICE 80-char string limit.
    deep = tmp_path
    while len(str(deep)) < 160:
        deep = deep / "12345678"
    deep.mkdir(parents=True, exist_ok=True)

    # A tiny kernel we can check actually loaded.
    (deep / "tiny.tls").write_text("\\begindata\nDELTET/DELTA_T_A = 99.5\n\\begintext\n")

    mk = deep / "meta_kernel.txt"
    mk.write_text(
        "\\begindata\n\n"
        f"PATH_VALUES = ('{_split_kernel_path_str(str(deep))}')\n\n"
        "PATH_SYMBOLS = ('A')\n\n"
        "KERNELS_TO_LOAD = ( '$A/tiny.tls' )\n\n"
        "\\begintext\n"
    )

    spiceypy.kclear()
    try:
        spiceypy.furnsh(str(mk))  # would raise TYPEMISMATCH before the fix
        assert spiceypy.gdpool("DELTET/DELTA_T_A", 0, 1)[0] == 99.5
    finally:
        spiceypy.kclear()

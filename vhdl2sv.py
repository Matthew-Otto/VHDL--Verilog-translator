# This will convert many common VHDL patterns to their SystemVerilog equivalents

import os
import re

regex_list = [ # (re.compile(r"", re.IGNORECASE), ""),
    (re.compile(r"--", re.IGNORECASE), "//"),  # comments
    (re.compile(r"\(([0-9]+)\)", re.IGNORECASE), "[\g<1>]"),  # (2) to [2]
    (re.compile(r"([^\s]*\s+)<=", re.IGNORECASE), "assign \g<1>="),  # "var <= val" to "assign var = val"

    # Operators
    (re.compile(r"([^\w])or([^\w])", re.IGNORECASE), "\g<1>|\g<2>"),
    (re.compile(r"([^\w])xor([^\w])", re.IGNORECASE), "\g<1>^\g<2>"),
    (re.compile(r"([^\w])and([^\w])", re.IGNORECASE), "\g<1>&\g<2>"),
    (re.compile(r"([^\w])not([^\w])", re.IGNORECASE), "\g<1>~\g<2>"),
    
    # "var : in std_logic_vector(PARAM-1 downto 0);" to "input logic [PARAM-1:0] var,"
    (re.compile(r"([^\s]+)\s+:\s+in\s+std_logic_vector\(([^\s]+)\s*downto\s*(\d)\);", re.IGNORECASE), "input  logic [\g<2>:\g<3>] \g<1>,"),
    (re.compile(r"([^\s]+)\s+:\s+in\s+std_logic_vector\(([^\s]+)\s*downto\s*(\d)\)+;", re.IGNORECASE), "input  logic [\g<2>:\g<3>] \g<1>);"),
    # "var : in std_logic;" to "input  logic var,"
    (re.compile(r"([^\s]+)\s+:\s+in\s+std_logic;", re.IGNORECASE), "input  logic \g<1>,"),
    (re.compile(r"([^\s]+)\s+:\s+in\s+std_logic\);", re.IGNORECASE), "input  logic \g<1>);"),
    
    # "var : out std_logic_vector(PARAM-1 downto 0);" to "output logic [PARAM-1:0] var,"
    (re.compile(r"([^\s]+)\s+:\s+out\s+std_logic_vector\(([^\s]+)\s*downto\s*(\d)\);", re.IGNORECASE), "output logic [\g<2>:\g<3>] \g<1>,"),
    (re.compile(r"([^\s]+)\s+:\s+out\s+std_logic_vector\(([^\s]+)\s*downto\s*(\d)\)+;", re.IGNORECASE), "output logic [\g<2>:\g<3>] \g<1>);"),
    # "var : out std_logic;" to "output logic var,"
    (re.compile(r"([^\s]+)\s+:\s+out\s+std_logic;", re.IGNORECASE), "output logic \g<1>,"),
    (re.compile(r"([^\s]+)\s+:\s+out\s+std_logic\);", re.IGNORECASE), "output logic \g<1>);"),
    
    # "signal var : std_logic_vector(PARAM-1 downto 0)" to "logic [PARAM-1:0] var"
    (re.compile(r"signal\s([^\s]+)\s+:\s+std_logic_vector\(([^\s]+)\s*downto\s*(\d).*;", re.IGNORECASE), "logic [\g<2>:\g<3>] \g<1>;"),
    # "signal var : std_logic" to "logic var"
    (re.compile(r"signal\s([^\s]+)\s+:\s+std_logic", re.IGNORECASE), "logic \g<1>"),
]


def main():
    dir = r"./VHDL/div_rtl"
    for filename in os.listdir(dir):
        if not filename.endswith(".vhd"):
            continue

        # make a copy of .vhd file to .sv
        oldpath = os.path.join(dir, filename)
        new_filename = filename.replace(".vhd", ".sv")
        newpath = os.path.join(dir, new_filename)
        
        with open(oldpath, "r") as file:
            file_contents = file.readlines()

        with open(newpath, "w") as file:
            for (regex, replace) in regex_list:
                file_contents = [regex.sub(replace, line) for line in file_contents]
            file.writelines(file_contents)



if __name__ == "__main__":
    main()
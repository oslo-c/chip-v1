help_message ="""
o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o
|                                     Chip: A command line interface for querying ChatGPT                                       |
o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o
|       <interactive mode>    Type 'chip' and ask away, as if you were having a conversation. Active when you see 'Chip>'       |
|                                                                                                                               |
| Options:                                                                                                                      |
|   -h, --help            show this help message and exit                                                                       |
|   -v, --verbosity       Use this flag to set the max tokens for the response. One character/space = One token.                |
|                                                                                                                               |
| Input Options:                                                                                                                |
|   -q , --quick          Submit question directly, surrounded by quotes. Ex: $ chip -f 'your query here'                       |
|   -if , --input-file    Use the content of a file as input. Combine with -q flag to add query related to input file.          |
|                                                                                                                               |
| Output Options:                                                                                                               |
|   -of , --output-file   Export query result to named file. Ex: $ Chip -q 'What is the capital of Denmark?' -of response.txt   |
o~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~o
"""

def get_help():
    return help_message


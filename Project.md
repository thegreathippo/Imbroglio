#Project Architecture
##Data-Side
###im_parser.py
This module is responsible for supplying the Parser class, which -- when instanced with a dictionary -- provides a Parser instance which will (when supplied with the entity uid and a string) translate infix expressions into functions. These function-formulas effectively allow components to behave as if they had property decorators.
###im_reader.py
This module provides a simple way to translate human-readable files into dictionaries of values.

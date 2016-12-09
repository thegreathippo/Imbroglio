"""
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""
import collections

R = "RIGHT"
L = "LEFT"
RIGHT = R
LEFT = L

def add(val1, val2):
	return val1 + val2

def subtract(val1, val2):
	return val1 - val2

def divide(val1, val2):
	answer = val1 / val2
	if int(answer) == answer:
		return int(answer)
	return answer

def multiply(val1, val2):
	return val1 * val2

def exponent(val1, val2):
	return val1 ** val2

def _max(val1, val2):
	return max(val1, val2)

def _min(val1, val2):
        return min(val1, val2)

Operator = collections.namedtuple("Operator", ["function", "precedence",
                                               "associativity"])
Function = collections.namedtuple("Function", ["function"]) 

operators = {
	"+" : Operator(add, 2, L),
	"-" : Operator(subtract, 2, L),
	"/" : Operator(divide, 3, L),
	"*" : Operator(multiply, 3, L),
	"^" : Operator(exponent, 4, R)
	}
		
functions = {
	"max" : Function(_max),
	"min" : Function(_min)
	}

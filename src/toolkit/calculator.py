from toolkit.errors import InvalidSymbolError


def tokenizator(expression: str) -> list[str]:
    """Splits the expression string into a list of tokens: numbers and operators"""
    tokens=[]
    current_number=""
    for character in expression:
        if character==" ":
            if current_number:
                tokens.append(current_number)
                current_number=""
        elif character in "0123456789" or character==".":
            current_number+=character
        elif character in "+-*/":
            if current_number:
                tokens.append(current_number)
                current_number=""
            tokens.append(character)
        else:
            raise InvalidSymbolError(f"Недопустимый символ:{character}")
    if current_number: 
        tokens.append(current_number)
    return tokens
        
def parse_strings(strings):
    for string in strings:

        # Try to parse as float or int
        try:
            var = float(string)
            if var.is_integer():
                yield int(var)
            else:
                yield var
        except ValueError:
            pass

        # Try to parse as boolean
        if string.lower() == 'true':
            yield True
        if string.lower() == 'false':
            yield False

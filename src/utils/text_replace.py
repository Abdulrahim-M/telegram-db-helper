import re

def replace_data(text, data):
    fields = ["name", "index", "unid", "email", "phone", "address"]
    replacement = dict(zip(fields, data))

    def replace_var(match):
        var_name = match.group(1)
        return replacement.get(var_name, "UNKNOWN")

    return re.sub(r"\$(.*?)\$", replace_var, text)
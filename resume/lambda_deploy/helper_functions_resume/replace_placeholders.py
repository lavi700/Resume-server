def replace_placeholders(string, replacements):
    """
    Replaces placeholders in the HTML template with their corresponding values.

    :param html: The HTML template as a string.
    :param replacements: A dictionary where keys are placeholders (without curly braces)
                         and values are the values to replace them with.
    :return: The HTML string with placeholders replaced.
    """
    for placeholder, value in replacements.items():
        placeholder_tag = f"%%{placeholder}%%"  # Using %% as a delimiter for placeholders
        string = string.replace(placeholder_tag, value)
    return string

# replacements should be like:
replacements = {
    "order_number": "123",
    "order_date": "1/1/2020",
}
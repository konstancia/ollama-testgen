def extract_description_text(description):
    """
    Converts Atlassian Document Format (ADF) to plain text.
    """
    if not description:
        return ""

    text_blocks = []

    for block in description.get("content", []):
        for content in block.get("content", []):
            if "text" in content:
                text_blocks.append(content["text"])

    return "\n".join(text_blocks)

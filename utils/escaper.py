import re


def html_esc(html_str: str) -> str:
    html_str.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
    return html_str


def html_tag_filter(html: str) -> str:
    reg = r"(<\/?([a-z0-9]+).*?>)"

    supported_tags = [
        "b",
        "strong",
        "i",
        "em",
        "u",
        "ins",
        "s",
        "strike",
        "del",
        "tg-spoiler",
        "span",
        "a",
        "code",
        "pre",
    ]

    tags = re.findall(reg, html)

    for tag, tagname in tags:
        if tagname not in supported_tags:
            html = html.replace(tag, "")

    return html

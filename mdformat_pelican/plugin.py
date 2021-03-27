from typing import List, Optional, Tuple

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdformat.renderer import MDRenderer


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""


def replace_pelican_placeholdlers(original_url) -> str:
    new_url = original_url
    for placeholder in (
        "author",
        "category",
        "index",
        "tag",
        "filename",
        "static",
        "attach",
    ):
        new_url = new_url.replace("%7B" + placeholder + "%7D", "{" + placeholder + "}")
        new_url = new_url.replace("%7C" + placeholder + "%7C", "{" + placeholder + "}")
    return new_url


def render_token(
    renderer: MDRenderer,
    tokens: List[Token],
    index: int,
    options: dict,
    env: dict,
) -> Optional[Tuple[str, int]]:
    """Convert token(s) to a string, or return None if no render method available.

    :returns: (text, index) where index is of the final "consumed" token
    """
    token = tokens[index]
    if token.type == "link_open":
        token.attrSet("href", replace_pelican_placeholdlers(token.attrGet("href")))
        return None
    elif token.type == "image":
        token.attrSet("src", replace_pelican_placeholdlers(token.attrGet("src")))
        return None
    return None

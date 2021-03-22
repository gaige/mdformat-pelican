from typing import List, Optional, Tuple

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdformat.renderer import MARKERS, MDRenderer
from mdit_py_plugins.footnote import footnote_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""


def replace_pelican_placeholdlers(uri_key, attr_list):
    new_attrs = []
    for a in attr_list:
        if a[0] == uri_key:
            new_url = a[1]
            for placeholder in ('author', 'category', 'index', 'tag', 'filename', 'static', 'attach'):
                new_url = new_url.replace("%7B" + placeholder + "%7D", '{' + placeholder + '}')
            new_attrs += [[uri_key, new_url]]
        else:
            new_attrs += [a]
    return new_attrs

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
    if token.type == 'link_open':
        token.attrs = replace_pelican_placeholdlers('href', token.attrs)
        return None
    elif token.type == 'image':
        token.attrs = replace_pelican_placeholdlers('src', token.attrs)
        return None
    return None

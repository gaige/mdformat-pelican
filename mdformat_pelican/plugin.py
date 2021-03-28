from typing import List, Optional, Tuple

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from markdown_it.token import Token
from mdformat.renderer import MDRenderer

# from mdformat.renderer import LOGGER, MDRenderer


def update_mdit(mdit: MarkdownIt) -> None:
    """
    Skip pairs before the first empty line
    """

    frontMatter = make_front_matter_rule()
    mdit.block.ruler.before(
        "table",
        "front_matter",
        frontMatter,
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )


def make_front_matter_rule():
    def frontMatter(state: StateBlock, start_line: int, end_line: int, silent: bool):
        # grab initial data if it's : separated
        if start_line != 0:
            return False

        # Since start is found, we can report success here in validation mode
        # if silent:
        #    return True

        # Search for the end of the block
        next_line = start_line
        start_content = 0
        meta = {}

        while True:
            next_line += 1
            if next_line >= end_line:
                # unclosed block should be autoclosed by end of document.
                return False

            start = state.bMarks[next_line]
            maximum = state.eMarks[next_line]

            if start == maximum:
                # empty line is terminator
                break

            key_value = state.src[start:maximum].split(":", 1)
            if len(key_value) != 2:
                # Error here, we have no k/v separator
                return False
            meta[key_value[0].lower()] = key_value[1]
        old_parent = state.parentType
        old_line_max = state.lineMax
        state.parentType = "container"

        # this will prevent lazy continuations from ever going past our end marker
        state.lineMax = next_line

        token = state.push("pelican_frontmatter", "", 0)
        # token.hidden = True
        token.content = state.src[state.bMarks[start_content] : state.eMarks[next_line]]
        token.block = True
        token.meta = meta

        state.parentType = old_parent
        state.lineMax = old_line_max
        state.line = next_line
        token.map = [start_line, state.line]

        # consider taking the content into a dictionary and checking for Title: .+\n

        return True

    return frontMatter


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
    if token.type == "pelican_frontmatter":
        # if 'title' not in token.meta:
        #    LOGGER.warning("Required title missing from front matter")
        return token.content + "\n", index
    elif token.type == "link_open":
        token.attrSet("href", replace_pelican_placeholdlers(token.attrGet("href")))
        return None
    elif token.type == "image":
        token.attrSet("src", replace_pelican_placeholdlers(token.attrGet("src")))
        return None
    return None

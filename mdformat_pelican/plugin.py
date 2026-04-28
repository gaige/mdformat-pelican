from typing import Any, Mapping

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from mdformat import renderer
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess, Render


def update_mdit(mdit: MarkdownIt) -> None:
    """
    Skip pairs before the first empty line
    """

    front_matter = make_front_matter_rule()
    mdit.block.ruler.before(
        "table",
        "front_matter",
        front_matter,
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )


def make_front_matter_rule():
    def front_matter(state: StateBlock, start_line: int, end_line: int, silent: bool):
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

    return front_matter


def _pelican_frontmatter_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return node.content.rstrip()


# Precompute the pelican placeholders to avoid doing it on every render.
# Supports both the standard curly braces and the deprecated pipe characters as delimiters:
# - %7B -> {
# - %7D -> }
# - %7C -> |
PLACEHOLDERS: [str, str] = {
    start + keyword + end: "{" + keyword + "}"
    for keyword in (
        "author",
        "category",
        "index",
        "tag",
        "filename",
        "static",
        "attach",
    )
    for start, end in (("%7B", "%7D"), ("%7C", "%7C"))
}


def replace_pelican_placeholdlers(original_url: str) -> str:
    new_url = original_url
    for placeholder, replacement in PLACEHOLDERS.items():
        new_url = new_url.replace(placeholder, replacement)
    return new_url


def _pelican_image_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    node.attrs["src"] = replace_pelican_placeholdlers(node.attrs["src"])
    return renderer.DEFAULT_RENDERERS.get("image")(node, context)


# Replace Pelican placeholders in already-rendered link output, after the link
# renderer has produced the final `[text](url)` string. Using a postprocessor
# instead of overriding the link renderer avoids conflicts with other plugins
# that also register a link renderer (e.g. mdformat-recover-urls), since
# postprocessors are collaborative while only the first registered renderer
# wins.
def _pelican_link_postprocessor(
    text: str,
    node: RenderTreeNode,
    context: Any,
) -> str:
    return replace_pelican_placeholdlers(text)


RENDERERS: Mapping[str, Render] = {
    "pelican_frontmatter": _pelican_frontmatter_renderer,
    "image": _pelican_image_renderer,
}

POSTPROCESSORS: Mapping[str, Postprocess] = {
    "link": _pelican_link_postprocessor,
}

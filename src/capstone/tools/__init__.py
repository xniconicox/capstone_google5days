# src/capstone/tools/__init__.py

from .stac_search import (
    search_satellite_scenes,
    SEARCH_STAC_SCENES_TOOL_SPEC,
)


# LLM に渡すための「ツール仕様」一覧（読み取り専用のメタデータ）
TOOL_SPECS = [
    SEARCH_STAC_SCENES_TOOL_SPEC,
]


# 実行時に使う「ツール関数」のレジストリ
TOOL_REGISTRY = {
    "search_stac_scenes": search_satellite_scenes,
}


def get_tool_specs():
    """
    Return the list of tool specifications to expose to the agent.

    この関数を経由しておくと、将来フィルタや変換を挟むときにも楽です。
    """
    return TOOL_SPECS


def get_tool_callable(name: str):
    """
    Look up a tool callable by its name.

    Unknown names should be treated as configuration errors.
    """
    try:
        return TOOL_REGISTRY[name]
    except KeyError as exc:
        raise KeyError(f"Unknown tool name: {name}") from exc

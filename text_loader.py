import os
import time
import folder_paths

# UX用の疑似項目
NO_FILES_ITEM = "(no text files found)"
INVALID_ITEM = "(invalid selection)"

# 対応拡張子（.yml追加）
TEXT_EXTENSIONS = (".txt", ".md", ".json", ".yaml", ".yml")

# 大量ファイルでUIが固まるのを防ぐ安全上限（必要なら増減）
MAX_FILES_PER_DIR = 5000

# INPUT_TYPES呼び出しが頻繁なので、軽いキャッシュ（秒）
CACHE_TTL_SECONDS = 5.0
_scan_cache = {
    "ts": 0.0,
    "files": None,
}


def _is_allowed_text_file(filename: str) -> bool:
    return filename.lower().endswith(TEXT_EXTENSIONS)


def _scan_text_files():
    now = time.time()
    cached_files = _scan_cache.get("files")
    if cached_files is not None and (now - _scan_cache.get("ts", 0.0)) < CACHE_TTL_SECONDS:
        return cached_files

    files = []

    input_dir = folder_paths.get_input_directory()
    output_dir = folder_paths.get_output_directory()

    # input/output をスキャン。prefix付きで選択肢にする
    for base_dir, prefix in [(input_dir, "input"), (output_dir, "output")]:
        count = 0
        for root, _, filenames in os.walk(base_dir):
            for filename in filenames:
                if not _is_allowed_text_file(filename):
                    continue

                # root -> base_dir の相対パスにして prefix を付けて保持
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, base_dir).replace("\\", "/")
                files.append(f"{prefix}/{rel_path}")

                count += 1
                if count >= MAX_FILES_PER_DIR:
                    # 上限到達したら打ち切り（必要なら上限を調整）
                    break
            if count >= MAX_FILES_PER_DIR:
                break

    files = sorted(set(files))
    if not files:
        files = [NO_FILES_ITEM]

    _scan_cache["ts"] = now
    _scan_cache["files"] = files
    return files


def _resolve_and_validate_path(file_value: str) -> str:
    """
    file_value: "input/xxx.txt" or "output/yyy.md"
    戻り値: 読み取り対象の安全な絶対パス（base_dir配下であることを保証）
    """
    # 疑似項目は拒否
    if file_value in (NO_FILES_ITEM, INVALID_ITEM) or not file_value:
        raise ValueError("No valid file selected")

    parts = file_value.split("/", 1)
    if len(parts) != 2:
        raise ValueError("Invalid file format")

    source, rel_path = parts[0], parts[1]

    if source == "input":
        base_dir = folder_paths.get_input_directory()
    elif source == "output":
        base_dir = folder_paths.get_output_directory()
    else:
        raise ValueError(f"Invalid source prefix: {source}")

    # 絶対パスや空、ドライブレター/UNCっぽい入力を拒否
    if not rel_path or os.path.isabs(rel_path):
        raise ValueError("Invalid relative path")

    # 正規化して base_dir からの脱出を防ぐ
    base_dir_abs = os.path.abspath(base_dir)
    target_abs = os.path.abspath(os.path.join(base_dir_abs, rel_path))

    # commonpathで「base_dir配下」であることを保証
    if os.path.commonpath([base_dir_abs, target_abs]) != base_dir_abs:
        raise ValueError("Path traversal detected")

    if not os.path.exists(target_abs):
        raise FileNotFoundError(f"File not found: {target_abs}")

    return target_abs


class TextFileLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # ComfyUIのドロップダウン
                "file": (_scan_text_files(),),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "load_text"
    CATEGORY = "utils"

    def load_text(self, file):
        try:
            target_path = _resolve_and_validate_path(file)
            # テキストがUTF-8以外でも極力落ちないように errors="replace"
            with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                return (f.read(),)
        except Exception as e:
            # ここは運用方針次第で raise にしてもOK。
            # 文字列返却だと下流で気づきにくい場合がある。
            return (f"Error loading file: {e}",)
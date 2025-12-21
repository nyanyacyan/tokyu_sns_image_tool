# installer/src/main.py

from __future__ import annotations

from flow.base.logger import Logger
from flow.base.chatgpt import generate_recommend_comment


def main() -> None:
    """Issue #17 動作確認用の簡易テストエントリポイント（同期）"""

    logger = Logger()

    # テスト用の特徴リスト（4つ）
    features = ["南向きの明るいリビング", "収納豊富", "駅近", "オートロック付き"]

    comment = generate_recommend_comment(
        features=features,
        min_len=10,
        max_len=3,
        max_retries=1,
        model=None,      # api_requests.py 側のデフォルトを使うなら None のままでOK
        logger=logger,   # 既存ロガーを使う
    )

    print("=== 最終コメント ===")
    print(comment)


if __name__ == "__main__":
    main()
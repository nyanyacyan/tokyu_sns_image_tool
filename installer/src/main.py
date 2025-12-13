# installer/src/main.py

from __future__ import annotations

import asyncio

from flow.base.logger import Logger
from flow.const.const_prompt import ChatGptPrompt
from flow.base.api_requests import call_openai_chat
from flow.base.logger import Logger

def dummy_llm(prompt: str) -> str:
    """テスト用: プロンプトを受け取って、固定のコメントを返すだけ（現在は未使用）"""
    # 本番ではここで OpenAI API などを呼び出す想定
    return (
        "南向きの明るいリビングと、たっぷり収納できるクローゼットが魅力のお部屋です。"
        "駅からも近くて通勤やお出かけにも便利ですよ。"
    )


async def generate_recommend_comment(
    logger: Logger,
    llm_func,
    label: str,
    min_len: int,
    max_len: int,
    features: list[str],
) -> str:
    """ChatGptPrompt.recommend を使って紹介文を生成し、文字数チェック＋ログ出力する（LLM 部分は async）"""

    # ① Enum からプロンプトひな型（テンプレート文字列）を取り出す
    template = ChatGptPrompt.recommend.value

    # ② 特徴を4つぶん用意（足りなければ空文字で埋める）
    items = (features + ["", "", "", ""])[:4]

    # ③ .format(...) で {minLen}, {maxLen}, {item0}〜{item3} を埋める
    prompt = template.format(
        minLen=min_len,
        maxLen=max_len,
        item0=items[0],
        item1=items[1],
        item2=items[2],
        item3=items[3],
    )

    # 送信プロンプトをログに残す
    logger.info_log(f"[{label}] 送信プロンプト:\n{prompt}")

    # ④ 実際に LLM（ここでは llm_func = OpenAI 呼び出し）を呼ぶ
    text = await call_openai_chat(
        prompt,
        max_tokens=512,
        temperature=0.7,
    )
    length = len(text)

    # 生成結果をログ
    logger.info_log(f"[{label}] 生成コメント({length}文字): {text}")

    # ⑤ 文字数チェックしてログ
    in_range = (min_len <= length <= max_len)
    if not in_range:
        logger.info_log(
            f"[{label}] 文字数範囲外: {length} 文字 (想定 {min_len}〜{max_len})"
        )
    else:
        logger.info_log(f"[{label}] 文字数OK: {length}文字")

    return text


async def main() -> None:
    """Issue #17 動作確認用の簡易テストエントリポイント"""

    logger = Logger()

    # テスト用の特徴リスト
    features = ["南向きの明るいリビング", "収納豊富", "駅近", "オートロック付き"]

    # OpenAI API を叩く関数を llm_func として渡す
    async def llm_func(prompt: str) -> str:
        # max_tokens や temperature はテスト用に控えめに設定
        return await call_openai_chat(
            logger=logger,
            prompt=prompt,
            max_tokens=512,
            temperature=0.7,
        )

    comment = await generate_recommend_comment(
        logger=logger,
        llm_func=llm_func,
        label="recommend_test",
        min_len=50,
        max_len=120,
        features=features,
    )

    print("=== 最終コメント ===")
    print(comment)


if __name__ == "__main__":
    asyncio.run(main())
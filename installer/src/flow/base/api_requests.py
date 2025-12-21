# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# installer/src/flow/base/api_requests.py

# 標準モジュールimport
import os # 標準ライブラリのOSモジュール
from openai import OpenAI # openaiライブリからOpneAIクラスを取り込む

# 自作モジュールimport
from flow.base.logger import Logger
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

logger = Logger()

# **********************************************************************************

# ------------------------------------------------------------------------------
# 関数定義

def call_openai_chat(
    prompt: str,
    model: str = "gpt-5-mini-2025-08-07",  # ←ここでChatGPTのモデルを指定
) -> str:
    """Responses API を使って OpenAI へリクエストし、
       生成されたテキストを返す同期関数"""
    
    api_key = os.environ.get("OPENAI_API_KEY") # 辞書のように扱えるオブジェクト、os.environを呼び出して、OS内の「OPEN_API_KEY」の環境変数を、辞書型のキー・値として取得
    if not api_key: # 変数api_keyがFalseの場合の処理
        logger.error_log("[call_openai_chat] OPENAI_API_KEY が設定されていません")
        raise RuntimeError("OPENAI_API_KEY is not set") # 例外クラスのRuntimeErrorで「OPEN＿API_KEY is not set」でエラーを返す

    # OpenAIクライアントを生成
    client = OpenAI(api_key=api_key) # OpneAIクラスをインスタンス化
    
    try:
        # OpneAIにアクセスするResponses API を、responseオブジェクトのcreateメソッドを呼び出して、使用するモデルとプロンプトを渡す
        response = client.responses.create(
            model=model,
            input=prompt,
        )
        
        # responseオブジェクトのoutput_textオブジェクト に生成済みの返答がまとめて入る
        text = response.output_text
        
        logger.info_log(f"[call_openai_chat] レスポンス取得成功 ({len(text)} 文字)")
        return text

    except Exception as e:
        logger.error_log(f"[call_openai_chat] API リクエスト失敗: {e}")
        raise

    # ------------------------------------------------------------------------------
    # 関数定義


    # ------------------------------------------------------------------------------

# **********************************************************************************

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# installer/src/flow/base/api_requests.py

# 標準モジュールimport
from __future__ import annotations # __future__モジュールから、型ヒントを文字列として扱い、後で処理するannotaitionsという将来仕様を有効化し、クラス同士の参照序列に縛られないコード設計の柔軟性を向上

import os # 標準ライブラリのOSモジュール
from typing import Any, Dict #typingモジュールから、任意の型を表すAnyと、キーと値を表す辞書型を表すDictをインポート

#import httpx # 非同期でhttpリクエストを送るための外部ライブラリ
from openai import OpenAI

# 自作モジュールimport
from flow.base.logger import Logger
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

logger = Logger()


def call_openai_chat(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.7,
    model: str = "gpt-5.2",  # 新しいモデル名にも変更できます
) -> str:
    """Responses API を使って OpenAI へリクエストし、
       生成されたテキストを返す同期関数"""
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error_log("[call_openai_chat] OPENAI_API_KEY が設定されていません")
        raise RuntimeError("OPENAI_API_KEY is not set")

    # OpenAIクライアントを生成
    client = OpenAI(api_key=api_key)
    
    try:
        # Responses API を呼び出す
        response = client.responses.create(
            model=model,
            input=prompt,
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        
        # output_text に生成済みの返答がまとめて入る
        text = response.output_text
        
        logger.info_log(f"[call_openai_chat] レスポンス取得成功 ({len(text)} 文字)")
        return text

    except Exception as e:
        logger.error_log(f"[call_openai_chat] API リクエスト失敗: {e}")
        raise
#OPENAI_API_URL = "https://api.openai.com/v1/chat/completions" # ChatGPTにアクセスするURL
#OPENAI_MODEL = "gpt-4.1-mini" # 使用するChatGPTのモデルを指定

#async def call_openai_chat(prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
    """単一のユーザープロンプト(文字列)を OpenAI の chat/completions に送り、帰ってきた本文(content)だけを返す共通関数。
    　　※ここでは「どういう物件か」「どんなテンプレを使うか」は知らない。ただ「渡された prompt を投げて、結果のテキストだけを返す」役割に専念。
    """
    #api_key = os.environ.get("OPENAI_API_KEY") # 各OSの環境変数を取り扱う辞書型のオブジェクトのenvironで、getメソッドを呼び出して、各OSの辞書型環境変数のキーである、OPENAI_API_KEYに対する値を取得して、代入
    
    #if not api_key: # api_keyに何も無い場合の処理
        #logger.error_log(f"[call_openai_chat] OPENAI_API_KEY が環境変数に設定されていません")
        # ここでは例外を投げて、上位でキャッチさせる設計にしておく
        #raise RuntimeError("OPENAI_API_KEY is not set") # raiseにてRuntimeErrorクラスを用いて、引数で渡したOPENAI_API_KEY is not setというメッセージ付きの例外オブジェクトを発生させて、例外処理とする
    
    # APIキーとjson送信データ形式をしてして、headersに代入 
    #headers = {
        #"Authorization": f"Bearer {api_key}",
        #"Content-Type": "application/json",
    #}
    
 # model：GPTモデル　messages：会話履歴　max_token：テキストの最大トークン量　temperature：文章のランダム性    
    #payload: Dict[str, Any] = {
        #"model": OPENAI_MODEL,
        #"messages": [
            #{"role": "user", "content": prompt},
        #],
        #"max_tokens": max_tokens,
        #"temperature": temperature,
    #}

    #logger.debug_log(
        #f"[call_openai_chat] リクエスト送信: model={OPENAI_MODEL}, "
        #f"max_tokens={max_tokens}, temperature={temperature}"
    #)

    #try:
        #async with httpx.AsyncClient(timeout=30.0) as client: # 非同期のhttp通信を行うためのクライアントを生成し、30秒でタイムアウト。async　withで通信終了後に自動で接続を閉じる
            #resp = await client.post( # OPENAI API　に対してhttp postリクエストを送信
                #OPENAI_API_URL, # awaitによってリクエストが返ってくるまで一旦処理を中断し、レスポンスが返ったら処理を再開
                #headers=headers, # headersには認証情報、jsonには送信したいプロンプトや設定情報が含まれている
                #json=payload
            #)
            
    #except httpx.ReadError as e: # httpxがAPIからレスポンスを読み取れなかった場合の処理
        #logger.error_log(f"[call_openai_chat] リクエストエラー: {e}")
        #raise
    
    #if resp.status_code != 200: # APIのhttpステータスコードが成功である200以外の時の処理
        #logger.error_log(
            #f"[call_openai_chat] ステータスコード異常: {resp.status_code}, body={resp.text}"
        #)
        #raise RuntimeError(f"OpenAI API error: {resp.status_code}") # 例外処理として、ステータスコード付きのエラーメッセージを返す
        
    #data = resp.json() # openAI APIからのhttp レスポンスである、json形式の文字列を、jsonメソッドを使用してpythonが読み込めるように辞書型に変換
    
    #try:
        #content = data["choices"][0]["message"]["content"] #　OpenAI APIのレスポンス(json)は階層構造になっているため、choicesリストの0番目、最初の要素の中のmessagesオブジェクトのcontentにて生成文を抜き出して、変数へ代入
        
    #except (KeyError,IndexError) as e: # 辞書に存在しないキーを指定した際、またはリストの範囲外を指定した際の処理
        #logger.error_log(f"[call_openai_chat] レスポンス解析エラー: {e}, body={data}")
        #raise
        
    #logger.info_log(f"[call_openai_chat] レスポンス取得成功（文字数: {len(content)})")
    #return content
    
# **********************************************************************************
# class定義


    # ------------------------------------------------------------------------------
    # 関数定義


    # ------------------------------------------------------------------------------
    # 関数定義


    # ------------------------------------------------------------------------------

# **********************************************************************************

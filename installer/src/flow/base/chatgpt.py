# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# inataller/src/flow/base/chatgpt.py

# import
# 標準モジュール
from __future__ import annotations
from typing import Callable, List, Optional

# 自作モジュール
from flow.base.logger import Logger
from flow.base.api_requests import call_openai_chat # api_requests.pyからcall_openai_chatメソッドをインポート
from flow.const.const_prompt import ChatGptPrompt # const_prompt.pyからChatGptPromptクラスをインポート

# **********************************************************************************

# ------------------------------------------------------------------------------
# 関数定義
def _ensure_4_items(features: List[str]) -> List[str]:
    """featuresを必ず4要素に整形して返す。
    
    - 4未満: 足りない分を""（空文字）で埋める
    - 4超過: 先頭4つに切り詰める
    """
    if features is None: # 引数で渡された変数featuresの値が何も無い場合の処理
        features = [] # 変数featuresにからのリストを代入
        
    # 先頭4つまでに切り詰め
    f = list(features)[:4] # 組み込み関数listで、引数で渡されたfeaturesの値を、スライスで先頭0番目から4番目の手前までを取り出した、新しいlistオブジェクトを返す
    
    # 4個になるまで空文字で埋める
    while len(f) < 4: # lenメソッドの引数へ、変数fを渡して、変数fの要素が4以下の場合の処理
        f.append("") # リストの要素を追加する、appendメソッドを呼び出し引数へ空文字「""」を渡して、変数fのリストへ空文字を追加
    
    return f

# ------------------------------------------------------------------------------
# 関数定義
def _build_recommend_prompt(min_len: int, max_len: int, features: List[str]) -> str:
    """recommend テンプレートに値を差し込んで、送信プロンプト文字列を作る。"""
    f = _ensure_4_items(features) # 引数で渡された変数featuresの値を、4つの要素のリスト型に変換する_ensure_4_itemsメソッドを呼び出して、変数fに代入
    template = ChatGptPrompt.recommend.value # ChatGptPromptクラスの列挙型で定義したデータの名前recmmendと、格納されているプロンプト文章を呼び出すvalue属性を用いて、プロンプト文章を変数templateへ代入
    return template.format( # 引数で指定した文字列を、メソッド前の文字列へ埋め込む、formatメソッドを呼び出して、変数template内の、min_len、max_len、item0、item1、item2、item3へ、それぞれ引数で渡された値と、変数fの中に格納された0〜3番目リスト要素を、文字列を埋め込んで返す
        minLen=min_len,
        maxLen=max_len,
        item0=f[0],
        item1=f[1],
        item2=f[2],
        item3=f[3],
    )
    
# ------------------------------------------------------------------------------
# 関数定義
def _build_fixed_prompt(char_limit: int, before_text: str) -> str:
    """fixedPrompt テンプレートに値を差し込んで、再生成プロンプト文字列を作る。"""
    template = ChatGptPrompt.fixedPrompt.value # ChatGptPromptクラスの列挙型で定義したデータの名前fixedPromptと、格納されているプロンプト文章を呼び出すvalue属性を用いて、プロンプト文章を変数templateへ代入
    return template.format( # 引数で指定した文字列を、メソッド前の文字列へ埋め込む、formatメソッドを呼び出して、変数template内のcharLimitとbeforePromptへ、それぞれ引数で渡された値を埋め込んで返す
        charLimit=char_limit,
        beforePrompt=before_text,
    )
    
# ------------------------------------------------------------------------------
# 関数定義
def _in_range(text: str, min_len: int, max_len: int) -> bool:
    """文字列が min_len~max_len に入っていれば True。"""
    length = len(text) # 組み込み関数lenを用いて、引数で渡されたtextの文字列の数を数えて、変数lengthへ代入
    return min_len <= length <= max_len # textの要素数が、変数min_len以上、変数max_len以下である場合は,Trueを返して、それ以外はFalseを返す

# ------------------------------------------------------------------------------
# 関数定義
def generate_recommend_comment(
    features: List[str],
    min_len: int = 50,
    max_len: int = 120,
    max_retries: int = 1,
    model: Optional[str] = None,
    logger: Optional[Logger] = None,
    llm_func: Optional[Callable[[str], str]] = None, # 引数にstr1つ受け取り、戻り値としてstrを返す引数llm_funcにNoneを代入
) -> str:

    """
    物件紹介コメントを生成する（同期処理）
    1) ChatGptPrompt.recommend で生成
    2) 文字数が範囲外なら ChatGptPrompt.fixedPrompt で再生成（max_retries 回まで）
    3) 最終テキストを返す（条件に入らなくても返す）
    """
    if logger is None: # 変数loggerに何も無い場合は、Loggerクラスをインスタンス化
        logger = Logger()
        
    # LLM呼び出し関数（テスト用に差し替え可能）
    def _default_llm(prompt: str) -> str:
        
        if model: # 引数で渡された変数modelがTrueの場合
            return call_openai_chat(prompt=prompt, model=model) # openaiにリクエストするcall_openai_chatメソッドを呼び出して、引数で渡された変数promptと変数modelの値を渡す
        
        return call_openai_chat(prompt=prompt) # 変数modelがTrue以外の場合、call_openai_chatメソッドを呼び出してpromptの値を渡す
    
    llm = llm_func or _default_llm # 引数で渡されたllm_funcまたは、_default_llmメソッドがTrueの場合、Trueの値を変数llmへ代入する
    
    # 1) recmmend で初回生成
    prompt = _build_recommend_prompt( # プロンプト文章を作成する_build_recommend_promptメソッドを呼び出して、変数prmptへ代入
            min_len=min_len,
            max_len=max_len,
            features=features,
        )
    
    logger.info_log(f"[recommend_test] 送信プロンプト: \n\n{prompt}\n")
    
    text = (llm(prompt) or "").strip() # 変数llmに格納されている、call_openai_chatメソッドの引数へ、変数promptの値を渡して返された値、または空文字を、stripメソッドで、先頭・末尾のから文字、改行文字列を除去した文字列を取得して、変数textへ代入
    
    logger.info_log(f"[recommend_test] 生成コメント({len(text)}文字: {text})")
    
    if _in_range(text, min_len=min_len, max_len=max_len): # _in_rangeメソッドを呼び出した結果、Trueの場合の処理
        logger.info_log(f"[recommend_test] 文字数OK: {len(text)}文字")
        return text
    
    # _in_rangeメソッドを呼び出した結果、True以外の場合の処理     
    logger.info_log(
        f"[recommend_test] 文字数NG: {len(text)}文字 (許容範囲{min_len}~{max_len})"
    )
    
    # 2) 再生成（固定プロンプト）
    for retry in range(max_retries): # 組み込み関数rangeの引数、変数max_retriesで渡された値である1を、繰り返し処理として1回指定し、渡された値1を、変数retryへ代入
        fix_prompt = _build_fixed_prompt(char_limit=max_len, before_text=text) # プロンプト再生成メソッド_build_fixed_promptを呼び出して、結果を変数fix_promptへ代入
        logger.info_log(
            f"[recommend_test] 文字数オーバーのため再生成します "
            f"(retry={retry + 1}/{max_retries})\n\n{fix_prompt}\n"
        )
        text = (llm(fix_prompt) or "").strip() # stripメソッドで、変数llmとpromptまたは空文字の末尾の空白文字を除去した文字列を取得して、変数textへ代入
        logger.info_log(f"[recommend_test] 生成コメント({len(text)}文字): {text}") 
        
        if _in_range(text, min_len=min_len, max_len=max_len): # _in_rangeメソッドを呼び出した結果、Trueの場合の処理
            logger.info_log(f"[recommend_test] 文字数OK: {len(text)}文字")   
            return text
        
        # _in_rangeメソッドを呼び出した結果、True以外の場合の処理 
        logger.info_log(
            f"[recommend_test] 文字数NG: {len(text)}文字 (許容範囲{min_len}~{max_len})"
        )
    # 再生成しても文字数が条件を満たさなかった場合の処理 
    logger.info_log(f"[recommend_test] 再生生後も文字数条件を満たしませんでした。最終結果を返します。")
    return text
    # ------------------------------------------------------------------------------
    # 関数定義
    # ------------------------------------------------------------------------------
    # 関数定義
    # ------------------------------------------------------------------------------
    # 関数定義
    # ------------------------------------------------------------------------------
    # 関数定義
    # ------------------------------------------------------------------------------
    # 関数定義
    # ------------------------------------------------------------------------------
    # 関数定義
    # ------------------------------------------------------------------------------
    # 関数定義
    
    
    # ------------------------------------------------------------------------------


# **********************************************************************************

#logger.py
import logging             # ログ出力用の標準ライブラリ
import os                  # ファイル・フォルダ操作用の標準ライブラリ
from datetime import datetime  # 日時操作用の標準ライブラリ
import sys                 # システム関連の標準ライブラリ（エラー出力用）

# ログをファイル＆ターミナル両方に出力するクラス
class Logger:
    def __init__(self):
        log_folder_name = "log"                                # ログを保存するフォルダ名
        os.makedirs(log_folder_name, exist_ok=True)            # フォルダがなければ自動作成（既にあってもOK）
        now = datetime.now()                                   # 現在時刻を取得
        self.time_str = now.strftime("%H:%M:%S")               # 時:分:秒だけの文字列
        now_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")       # ファイル名用の日付・時刻文字列
        file_name = f"{now_time_str}.log"                      # 例: "2025-06-20_08-00-00.log"
        file_path = os.path.join(log_folder_name, file_name)   # フォルダとファイル名を結合

        # ログの出力設定（ファイル名、ログレベル、フォーマットなど）
        logging.basicConfig(
            filename=file_path,                                # ログの出力ファイル
            level=logging.DEBUG,                                # INFOレベル以上をすべて記録
            format='%(asctime)s - %(levelname)s - %(message)s' # 日時・レベル・内容
        )

    # メッセージの先頭にインスタンス生成時の時刻をつけて返す
    def message_and_time(self, message: str) -> str:
        return f"{self.time_str} - {message}"                  # 例: "08:00:00 - 任意のメッセージ"

    # DEBUGレベルのログを出力（ファイル＆ターミナル）
    def debug_log(self, message):
        logging.debug(self.message_and_time(message))          # ファイル出力
        print(self.message_and_time(message))                  # ターミナルにも出力

    # INFOレベルのログを出力（ファイル＆ターミナル）
    def info_log(self, message):
        logging.info(self.message_and_time(message))           # ファイル出力
        print(self.message_and_time(message))                  # ターミナルにも出力

    # WARNINGレベルのログを出力（ファイル＆ターミナル）
    def warning_log(self, message):
        logging.warning(self.message_and_time(message))        # ファイル出力
        print(self.message_and_time(message))                  # ターミナルにも出力

    # ERRORレベルのログを出力（ファイル＆ターミナル・エラー用ストリーム）
    def error_log(self, message):
        logging.error(self.message_and_time(message))          # ファイル出力
        print(self.message_and_time(message), file=sys.stderr) # エラー用ターミナル出力

    # CRITICALレベルのログを出力（ファイル＆ターミナル・エラー用ストリーム）
    def critical_log(self, message):
        logging.critical(self.message_and_time(message))       # ファイル出力
        print(self.message_and_time(message), file=sys.stderr) # エラー用ターミナル出力

    # ChatGPTが生成した紹介文のログを出力
    def log_generated_comment(self, label: str, text: str, min_len: int, max_len: int) -> bool:
        """ ChatGPT が生成した紹介文について、'文字数''指定範囲内かどうか''本文そのもの'をログに出しつつ、範囲内なら True ,そうでなければ False を返す"""
        length = len(text) # 引数で渡されたtextの要素の個数を、変数lengthへ代入
        
        # 文字数と判定結果をログに残す
        in_range = (min_len <= length <= max_len) # 連鎖比較にて、min_lenが、length以下かつ、lengthがmax_len以下である場合、変数in_rangeへTrueを返す
        self.info_log(
            f"[log_generated_comment] ラベル={label}, 文字数={length}, " 
            f"許容範囲=({min_len}〜{max_len}), 範囲内か={in_range}"
            
            )
        
        # 実際の本文もログに残す
        self.info_log(f"[log_generated_comment] 生成された紹介文: {text}")
        
        return in_range
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
            level=logging.DEBUG,                               # DEBUGレベル以上をすべて記録
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

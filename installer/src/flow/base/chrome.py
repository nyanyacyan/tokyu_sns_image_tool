# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# chrome.py
# import
from selenium import webdriver  # Chromeを自動操作するためのライブラリ
from selenium.webdriver.chrome.options import Options  # Chrome起動時の設定をするためのクラス
from selenium.webdriver.remote.webdriver import WebDriver  # WebDriverの型ヒント用
import logging  # ログ（記録）を出力するための標準ライブラリ

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# このファイル専用のログ出力機能を準備
logger = logging.getLogger(__name__)

# **********************************************************************************
# class定義
class Chrome:
    @staticmethod  # インスタンス化せず、クラス名.メソッド名で直接呼べるようにする
    
    # ------------------------------------------------------------------------------
    # 関数定義
    def get_driver(url: str) -> WebDriver:

    # ------------------------------------------------------------------------------

        try:
            # Chromeの起動オプションを設定（ここでは画面サイズを1200×800ピクセルに指定）
            options = Options()
            options.add_argument("--window-size=1200,800")

            # Chromeブラウザを実際に起動する（この1行でウィンドウが開く！）
            driver = webdriver.Chrome(options=options)

            # 操作用のリモコン（WebDriverオブジェクト）を呼び出し元へ返す
            return driver

        except Exception as e:  # もしエラーが起きた場合
            # エラー内容と詳しい情報をログに記録（あとからトラブル解決しやすくする）
            logger.error(f"Chrome起動エラー: {e}", exc_info=True)
            # エラーをそのまま呼び出し元へ伝えて、プログラムを止める
            raise


    # ------------------------------------------------------------------------------

# **********************************************************************************

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# chrome.py
# import
from selenium import webdriver  # 「selenium」というライブラリの「webdriver」というブラウザを自動操作する大枠の基本モジュールを取り込む
from selenium.webdriver.chrome.options import Options  # 「selenium.webdriver.chrome.options」というモジュールから「Options」というChrome起動時の設定をするためのクラスを取り込む
from selenium.webdriver.remote.webdriver import WebDriver  # 「selenium.webdriver.emote.webdriver」というモジュールから「WebDriver」というブラウザを自動操作するクラスを取り込む
from logger import Logger  # logger.pyからLoggerクラスを取り込む


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

logger = Logger() # Loggerクラスをインスタンス化して、変数loggerに代入してchrome.pyで使用   

# **********************************************************************************

# class定義
class Chrome:
    # ------------------------------------------------------------------------------
    
    # 関数定義
    @staticmethod  # selfを使わずインスタンス化しないで、クラス名.メソッド名で直接呼べるようにする
    def get_options() -> Options: # この関数はOptionsクラスのメソッドを使用
        options = Options() # Optionsクラスをインスタンス化して、変数optionsへ代入
        options.add_argument("--window-size=1200,800") # Optionsクラスの"add_argument"という、Chromeの起動オプションを指定するメソッドを使用して、ウィンドウサイズを指定
        options.binary_location = "/this/path/does/not/exist/chrome"
        return options # optionsの結果を関数の外でも使えるように返す
        
    # ------------------------------------------------------------------------------     
    
    # 関数定義
    @staticmethod # selfを使わずインスタンス化しないで、クラス名.メソッド名で直接呼べるようにする
    def get_driver(url: str) -> WebDriver: # この関数はWebDriverクラスのメソッドを使用して、関数の引数には変数urlに文字列を受け取る

        try: # 以下のコード内でエラーが発生した場合、exceptで定義された処理が実行される
            options = Chrome.get_options() # Chromeクラスの関数get_optionsを呼び出して、変数optionsに代入
            driver = webdriver.Chrome(options=options) # webdriverというモジュールの中にある、Chromeクラスをインスタンス化して、上記の変数optionsを、chromeクラスのコンストラクタ内のoptionsに代入した結果を、変数driverへ代入
            if url: # 変数urlが空で無ければ以下が実行される
                driver.get(url) # 変数driverに代入されている、Chromeクラスのオブジェクトである、getメソッドの引数へurlという文字列を渡す
            return driver # driverの結果を関数の外でも使えるように返す

        except Exception as e: # try内でエラーが発生した場合、変数eにエラー内容が入る。Exceptionを略して"e"とする。
            logger.error_log(f"Chrome起動エラー: {e}") # getLogger関数から呼び出されたLoggerクラス内のerror_logメソッドを呼び出して、引数へ文字列"Chrome起動エラー:Exception"と、変数eに代入されたエラー内容の文字列を渡す
            raise # 処理を停止して、この関数を呼び出したもとへエラー内容を伝える

    # ------------------------------------------------------------------------------

# **********************************************************************************

if __name__ == "__main__":
    import time
    drv = None  # 例外時に finally で参照しても安全にする
    try:
        drv = Chrome.get_driver("https://example.com")
        logger.info_log("Chrome 起動テスト OK（3秒後に終了）")
        time.sleep(3)
    except Exception as e:
        logger.error_log(f"自己テスト失敗: {type(e).__name__}: {e}")
        raise
    finally:
        if drv:
            try:
                drv.quit()
            except Exception:
                pass

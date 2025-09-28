# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# chrome.py
# import
from selenium import webdriver  # 「selenium」というライブラリの「webdriver」というブラウザを自動操作する大枠の基本モジュールを取り込む
from selenium.webdriver.chrome.options import Options  # 「selenium.webdriver.chrome.options」というモジュールから「Options」というChrome起動時の設定をするためのクラスを取り込む
from selenium.webdriver.remote.webdriver import WebDriver  # 「selenium.webdriver.emote.webdriver」というモジュールから「WebDriver」というブラウザを自動操作するクラスを取り込む
from logger import Logger  # logger.pyからLoggerクラスを取り込む


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# **********************************************************************************

# class定義
class Chrome:
    # ------------------------------------------------------------------------------
    
    # 関数定義
    def get_options(self) -> Options: # この関数はOptionsクラスのメソッドを使用
        options = Options() # Optionsクラスをインスタンス化して、変数optionsへ代入
        options.add_argument("--window-size=1200,800") # Optionsクラスの"add_argument"という、Chromeの起動オプションを指定するメソッドを使用して、ウィンドウサイズを指定
        return options # optionsの結果を関数の外でも使えるように返す
        
    # ------------------------------------------------------------------------------     
    
    # 関数定義
    def get_driver(self) -> WebDriver: # WebDriverクラスを使用
        logger = Logger() # Loggerクラスをインスタンス化して、変数loggerに代入  

        try: # 以下のコード内でエラーが発生した場合、exceptで定義された処理が実行される
            options = self.get_options() # Chromeクラスの関数get_optionsを呼び出して、変数optionsに代入
            logger.info_log(f"Chrome起動開始") # 起動開始のログを残す
            driver = webdriver.Chrome(options=options) # webdriverというモジュールの中にある、Chromeクラスをインスタンス化して、上記の変数optionsを、chromeクラスのコンストラクタ内のoptionsに代入した結果を、変数driverへ代入
            logger.info_log(f"Chrome起動成功") # 起動成功のログを残す
            return driver # driverの結果を関数の外でも使えるように返す

        except Exception as e: # try内でエラーが発生した場合、変数eにエラー内容が入る。Exceptionを略して"e"とする。
            logger.error_log(f"Chrome起動エラー: {e}") # getLogger関数から呼び出されたLoggerクラス内のerror_logメソッドを呼び出して、引数へ文字列"Chrome起動エラー:Exception"と、変数eに代入されたエラー内容の文字列を渡す
            raise # 処理を停止して、この関数を呼び出したもとへエラー内容を伝える

    # ------------------------------------------------------------------------------
    
    # 関数定義
    def open_site(self,url:str) -> WebDriver: # WebDriverクラスを使用
        logger = Logger() # Loggerクラスをインスタンス化して、変数loggerに代入
        
        driver = self.get_driver() # 1.driverを起動する
        logger.info_log(f"URLアクセス開始:{url}")
        try:
            driver.get(url) # 2.URLにアクセスする
            logger.info_log(f"URLアクセス成功:{url}")
            return driver # 3.driverを返す
        
        except Exception as e:
            logger.error_log(f"URLアクセス失敗:{url}")
            raise
        
# **********************************************************************************

if __name__ == "__main__":
    chrome = Chrome()
    url = "https://www.yahoo.co.jp"
    chrome.open_site(url)

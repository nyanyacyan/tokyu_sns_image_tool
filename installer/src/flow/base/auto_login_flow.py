# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# auto_login_flow.py

# 標準モジュールimport
from selenium.common.exceptions import TimeoutException # 「selenium.common.exceptions」というモジュールから、「TimeoutException」という操作や処理が設定時間内に完了されなかった場合に通知するクラス
from selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラス
from selenium.webdriver.support.ui import WebDriverWait # 「selenium.webdriver.support.ui」というモジュールから取り込んだ「WebDriberWait」という待機オブジェクト作るクラス
from selenium.webdriver.support import expected_conditions as EC # 「selenium.webdriver.support」というモジュールから取り込んだ「expected_conditions」という「どんな条件を満たすまで待つか」という待機オブジェクトを作るモジュールを略して「EC」としている
from pathlib import Path # 「pathlib」というファイルやフォルダのpathを扱うモジュールから、pathを取り扱う「Path」というクラスを取り組む
from selenium.webdriver.remote.webelement import WebElement # 「slenium.webdriver.remote.webelement」というモジュールから取り込んだ「WebElment」という、ブラウザ上の要素を操作するクラス
import json,time,random # 「json」、「time」、「random」という標準ライブラリのモジュールを取り込む

# 自作モジュールimport
from flow.base.logger import Logger  # logger.pyからLoggerクラスを取り込む


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# **********************************************************************************

# class定義
class Auto_Login_Flow:
# ------------------------------------------------------------------------------
    
    # 関数定義
    def __init__(self):
        
        base_dir = Path(__file__).resolve().parents[3] # auto_login_flow.pyから3階層上のディレクトリを取得
        self.config_path = base_dir / "config" / "config.json" # jsonファイルのパスを組み立てて、変数confi_pathへ代入
        self.user_id, self.user_pass, self.login_url, self.loggedin_url, self.logged_in_css = self.load_config()# config.jsonからID,パスワード、URLなどを読み込み、各変数へ代入
        self.logger = Logger()
# ------------------------------------------------------------------------------
    
    # 関数定義
    def wait_random(self,a: float = 0.6, b: float = 5.0): # ランダムに待機する関数　初期設定で、第一引数aへ不動小数点0.6から第二引数bへ浮動小数点5.0の間をランダムで待機する
        time.sleep(random.uniform(a, b)) # 「time」というモジュール内の処理を一時停止する「sleep」という関数の引数へ、randomというモジュールのa〜bの範囲の中からランダムな浮動小数点を返す

# ------------------------------------------------------------------------------
    
    # 関数定義    
    def find_element(self,driver,by,value,timeout=10) -> WebElement:
        """指定した要素を探して返す"""
        
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by,value))) # WebDriverWaitをインスタンス化　Chromeブラウザで、指定の属性が出現するまで最大10秒待機
            el = driver.find_element(by,value,) # 引数driverから、webdriver.Chromeクラスを貰い、そこからfind_elementメソッドを呼び出して、byとvalueに渡された引数を渡して、属性を探す
            self.logger.info_log(f"[find_element]要素を取得成功: by={by},value={value}") # 要素取得成功のログ
            
        except TimeoutException as e: # 時間内に要素が見つからなかった時の処理
            self.logger.error_log(f"[find_element]要素が見つかりません: by={by},value={value},timeout={timeout},url={driver.current_url}") # 要素取得失敗のログ
        
            raise
        
        return el
# ------------------------------------------------------------------------------    

    # 関数定義    
    def input_text(self,el: WebElement,text) -> None:
        """指定した要素を探し出して文字を入力する"""
        
        try:
            el.clear() # webdriver.chromeクラスのclearというメソッドを呼び出して、文字列を消去する
            el.send_keys(text) # find_elementメソッド内のdriver.find_elementメソッドで、戻り値がWebElementのオブジェクトが返ってきて、そのWebElementオブジェクトに属しているsend_keysメソッドを呼び出して、文字を送る。
            self.logger.info_log(f"[input_text]入力成功:text={text}") # 要素取得成功のログ
        
        except Exception as e:
            self.logger.error_log(f"[input_text]入力失敗:text={text},error={e}") # 要素取得失敗のログ
            
            raise
# ------------------------------------------------------------------------------
    
    def click_element(self,el: WebElement,timeout=10) -> None:
        """指定した要素をクリックする（待機+ログ+例外処理付き）"""
        
        try:
            WebDriverWait(el.parent, timeout).until(EC.element_to_be_clickable((el)))# WebDriverWaitをインスタンス化　Chromeブラウザで、指定の属性が出現するまで最大10秒待機
            el.click() # find_elementメソッド内のdriver.find_elementメソッドで、戻り値がWebElementのオブジェクトが返ってきて、そのWebElementオブジェクトに属しているclickメソッドを呼び出してクリックする。
            
            self.logger.info_log(f"[click_element]クリック成功") # 要素取得成功のログ
        
        except Exception as e:
            self.logger.error_log(f"[click_element]クリック失敗:error={e}") # 要素取得失敗のログ
            raise
# ------------------------------------------------------------------------------    
    # 関数定義
    def open_new_tab(self,driver,url: str):
        """ブラウザから新しいタブを開く"""
        d = driver
        d.switch_to.new_window("tab") # タブを開くメソッド
        d.get(url) # タブのURLを渡して立ち上げる
        
# ------------------------------------------------------------------------------    
    # 関数定義
    def is_logged_in(self,driver,timeout=12) -> bool:
        """URL一致でログイン済みとみなす"""

        if driver.current_url.startswith(self.loggedin_url): # 現在のURLとjsonファイルで設定したURLが一致しているか判定
            self.logger.info_log(f"ログイン後のURL一致を確認。ログイン済と判断。") # 要素取得成功のログ
            return True
            
        if not self.logged_in_css: # jsonファイルで指定した要素を設定していない場合は、ここで終了
            return False
            
        try:
            WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR,self.logged_in_css))) # jsonファイルで指定した要素が出現するまで最大12秒待機
            self.logger.info_log(f"ログイン後の要素一致を確認。ブラウザは開いたまま残します。") # 要素取得成功のログ
            return True
        
        except TimeoutException:
            self.logger.info_log(f"要素が見つからず、ログイン未完了") # 要素取得失敗のログ
            return False
# ------------------------------------------------------------------------------  
    # 関数定義      
    def load_config(self) -> tuple[str,str,str,str,str]:
        """jsonファイルの読み込み"""
        
        with open(self.config_path, encoding="utf-8") as f: # コンストラクタで設定したjsonファイルのパスにアクセスして開く
            cfg = json.load(f)["TOKYU_JYUTAKU_LEASE"] # "TOKYU_JYUTAKU_LEASE"のファイルを読み込む
            
        return cfg["ID"], cfg["PASS"], cfg["URL"], cfg["LOGINED_URL"], cfg["LOGGED_IN_CSS"]  # 各jsonファイル設定値を読み込み
    
# ------------------------------------------------------------------------------
    # 関数定義
    def checkbox_reset(self,el: WebElement) -> None:
        """チェックボックスのリセット"""
        
        if el.is_selected():
            el.click()
            self.logger.info_log(f"チェックボックスをリセット（OFF）しました")
            
        else:
            self.logger.info_log(f"チェックボックスは既にOFFです")


# **********************************************************************************


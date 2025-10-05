# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# installer/src/flow/scraper_flow.py
# import

from flow.base.chrome import Chrome # chrome.pyからChromeクラスを取り込む
from selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラス
from selenium.webdriver.support.ui import WebDriverWait # 「selenium.webdriver.support.ui」というモジュールから取り込んだ「WebDriberWait」という待機オブジェクト作るクラス
from selenium.webdriver.support import expected_conditions as EC # 「selenium.webdriver.support」というモジュールから取り込んだ「expected_conditions」という「どんな条件を満たすまで待つか」という待機オブジェクトを作るモジュールを略して「EC」としている
from pathlib import Path
import json,time,random

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# **********************************************************************************

def wait_random(a: float = 0.6, b: float = 1.4):
        time.sleep(random.uniform(a, b))
        
# class定義
class LoginAutomator:
    
    # ------------------------------------------------------------------------------
    
    # 関数定義
    def __init__(self): # ファイルパスの設定
        base_dir = Path(__file__).resolve().parents[2] # scraper_flow.pyから2階層上のディレクトリを取得
        self.config_path = base_dir / "config" / "config.json" # config.jsonの場所を指定

        # config.jsonからID,パスワード、URLなどを読み込み、各変数へ代入
        self.user_id, self.user_pass, self.login_url, self.loggedin_url, self.logged_in_css = self.load_config()
        
        # Chromeクラスのopen_siteメソッドを呼び出してインスタンス化
        self.driver = None   
    # ------------------------------------------------------------------------------
    
    # 関数定義
    def ensure_logged_in(self): # ログイン済みなら新タブで開く。未ログインならログインして開くメソッド
                
        if self.driver is None:
            self.driver = Chrome().open_site(self.login_url)
        d = self.driver
        wait_random() # ランダム時間で待機
        
        if self.is_logged_in(): # is_logged_inメソッドを呼び出して、ログイン状態をチェック
            self.open_new_tab(self.loggedin_url) # open_new_tabメソッドを呼び出して、ログイン後のブラウザの新しいタブを開く
            return  
        d.get(self.login_url) # ログイン後のURLでは無かった場合、ここから始まり、jsonファイルのログインURLにアクセスして開く
        wait_random() # ランダム時間で待機

        WebDriverWait(d, 10).until(EC.presence_of_element_located((By.ID, "txtLoginId"))) # WebDriverWaitをインスタンス化　Chromeブラウザで、id=txtLoginIdという属性が出現するまで最大10秒待機
        id_el = d.find_element(By.ID, "txtLoginId") # webdriver.chromeクラスの、find_elementというメソッドを呼び出して、id=txtLoginIdという属性を探した結果を変数id_elへ代入
        pw_el = d.find_element(By.ID, "txtLoginPass") # webdriver.chromeクラスの、find_elementというメソッドを呼び出して、id=txtLoginPassという属性を探した結果を変数id_elへ代入
        
        id_el.clear() # webdriver.chromeクラスのclearというメソッドを呼び出して、id_elで探したtxtLoginIdの文字列を消去する
        wait_random() # ランダム時間で待機
        id_el.send_keys(self.user_id) # webdriver.chromeクラスのsend.keysというメソッドを呼び出して、id_elで探したtxtLoginIdへ、jsonファイルのuser_idの値を打ち込む
        
        pw_el.clear() # webdriver.chromeクラスのclearというメソッドを呼び出して、id_pwで探したtxtLoginPassの文字列を消去する
        pw_el.send_keys(self.user_pass) # webdriver.chromeクラスのsend.keysというメソッドを呼び出して、id_pwで探したtxtLoginpassへ、jsonファイルのuser_passの値を打ち込む
        wait_random() # ランダム時間で待機

        # （任意）チェックボックスにレ点
        try:
            ui = d.find_element(By.CSS_SELECTOR, ".jqTransformCheckboxWrapper a.jqTransformCheckbox")
            if "jqTransformChecked" not in ui.get_attribute("class"):
                ui.click()
                wait_random()
        except Exception:
            pass  # 無ければ無視

        # ログインボタン → URLが変わるまで待機
        d.find_element(By.CSS_SELECTOR, "#login-btn a").click()
        WebDriverWait(d, 12).until(lambda x: x.current_url != self.login_url)
        wait_random()

        # 最終確認
        if self.is_logged_in():
            print("ログイン成功：ブラウザは開いたまま残します。")
        else:
            print("ログイン後URLが想定と異なります。現在URL：", d.current_url)
    # ------------------------------------------------------------------------------

    # 関数定義
    def load_config(self):
        with open(self.config_path, encoding="utf-8") as f:
            cfg = json.load(f)["TOKYU_JYUTAKU_LEASE"]
        # ログイン後画面に必ずある要素（任意指定。無ければ空文字でOK）
        self.logged_in_css = cfg.get("LOGGED_IN_CSS", "")
        return cfg["ID"], cfg["PASS"], cfg["URL"], cfg["LOGINED_URL"], cfg["LOGGED_IN_CSS"],
    # ------------------------------------------------------------------------------
    
    # 関数定義
    def is_logged_in(self):
        """URL一致でログイン済みとみなす"""
        d = self.driver

        if d.current_url.startswith(self.loggedin_url):
            return True
        
        if self.logged_in_css:
            elements = d.find_elements(By.CSS_SELECTOR,self.logged_in_css)
            if elements:
                return True
        
        return False
    # ------------------------------------------------------------------------------

    # 関数定義
    def open_new_tab(self, url: str):
        d = self.driver
        d.switch_to.new_window("tab")
        d.get(url)
        wait_random()
        
    # **********************************************************************************
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# installer/src/flow/scraper_flow.py

# 標準モジュールimport
from selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラスfrom selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラスfrom selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラスfrom selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラスfrom selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラスfrom selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラス

# 自作モジュールimport
from flow.base.chrome import Chrome # chrome.pyからChromeクラスを取り込む
from flow.base.auto_login_flow import Auto_Login_Flow # auto_login_flow.pyからAuto_Login_Flowクラスを取り込む

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# **********************************************************************************

# class定義
class LoginAutomator: # 「ログインオートメーター」というログインを自動で行うクラス
    
    # ------------------------------------------------------------------------------
    
    # 関数定義
    def __init__(self):
    
        # 初期設定
        self.autologin = Auto_Login_Flow()
        
        self.user_id, self.user_pass, self.login_url, self.loggedin_url, self.logged_in_css = self.autologin.load_config() 
        
        self.chrome_driver = Chrome().open_site(self.login_url)
        
    # ------------------------------------------------------------------------------
    
    # 関数定義
    def ensure_logged_in(self):

        self.autologin.wait_random() # ランダム時間で待機
        
        # ログイン状態チェック
        if self.autologin.is_logged_in(self.chrome_driver): # is_logged_inメソッドを呼び出して、ログイン状態をチェック
            self.autologin.open_new_tab(self.chrome_driver,self.loggedin_url) # ログイン状態であったら、open_new_tabメソッドを呼び出して、ログイン後のブラウザの新しいタブを開く 
        
        else:
        # IDとPW欄を探す
            self.autologin.find_element(self.chrome_driver, By.ID, "txtLoginId") # webdriver.chromeクラスの、find_elementというメソッドを呼び出して、id=txtLoginIdという属性を探す
            self.autologin.wait_random() # ランダム時間で待機
            self.autologin.find_element(self.chrome_driver, By.ID, "txtLoginPass") # webdriver.chromeクラスの、find_elementというメソッドを呼び出して、id=txtLoginPassという属性を探す
        
        # IDとPW入力
            self.autologin.input_text(self.chrome_driver, By.ID, "txtLoginId",self.user_id) # Auto_Login_Flowクラスのinput_textメソッドを呼び出して、"txtLoginId"の要素へjsonファイルIDを入力
            self.autologin.wait_random() # ランダム時間で待機
            self.autologin.input_text(self.chrome_driver, By.ID, "txtLoginPass",self.user_pass) # Auto_Login_Flowクラスのinput_textメソッドを呼び出して、"txtLoginPass"の要素へjsonファイルPWを入力

        # チェックボックスにレ点クリック
            try:
                self.autologin.find_element(self.chrome_driver, By.CSS_SELECTOR, ".jqTransformCheckboxWrapper a.jqTransformCheckbox") # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、チェックボックスの要素を探す
                self.autologin.wait_random() # ランダム時間で待機
                self.autologin.click_element(self.chrome_driver, By.CSS_SELECTOR, ".jqTransformCheckboxWrapper a.jqTransformCheckbox") # Auto_Login_Flowクラスのclick_elementメソッドを呼び出して、チェックボックスにレ点を入れる

            except Exception:
                pass  # 無ければ無視

        # ログインボタンクリック
            self.autologin.click_element(self.chrome_driver, By.CSS_SELECTOR, "#login-btn a") # Auto_Login_Flowクラスのclick_elementメソッドを呼び出して、ログインボタンをクリック
            self.autologin.wait_random() # ランダム時間で待機

        # 最終確認
            if self.autologin.is_logged_in(self.chrome_driver):
                return
            
            else:
                return
    # ------------------------------------------------------------------------------

    # 関数定義
    
    # ------------------------------------------------------------------------------
    
    # 関数定義
    
    # ------------------------------------------------------------------------------

    # 関数定義
    
        
    # **********************************************************************************
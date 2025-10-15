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
            id_el = self.autologin.find_element(self.chrome_driver, By.ID, "txtLoginId") # webdriver.chromeクラスの、find_elementというメソッドを呼び出して、id=txtLoginIdという属性を探す
            pw_el = self.autologin.find_element(self.chrome_driver, By.ID, "txtLoginPass") # webdriver.chromeクラスの、find_elementというメソッドを呼び出して、id=txtLoginPassという属性を探す
        
        # IDとPW入力
            self.autologin.input_text(id_el,self.user_id) # Auto_Login_Flowクラスのinput_textメソッドを呼び出して、"txtLoginId"の要素へjsonファイルIDを入力
            self.autologin.wait_random() # ランダム時間で待機
            self.autologin.input_text(pw_el,self.user_pass) # Auto_Login_Flowクラスのinput_textメソッドを呼び出して、"txtLoginPass"の要素へjsonファイルPWを入力

        # チェックボックスを探してレ点クリック
            try:
                cb_el = self.autologin.find_element(self.chrome_driver, By.CSS_SELECTOR, ".jqTransformCheckboxWrapper a.jqTransformCheckbox") # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、チェックボックスの要素を探す
                self.autologin.wait_random() # ランダム時間で待機
                self.autologin.click_element(cb_el) # Auto_Login_Flowクラスのclick_elementメソッドを呼び出して、チェックボックスにレ点を入れる

            except Exception:
                pass  # 無ければ無視

        # ログインボタンを探してクリック
            lg_el = self.autologin.find_element(self.chrome_driver, By.CSS_SELECTOR, "#login-btn a") # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、ログインボタンの要素を探し、戻り値であるWebElementをlg_idへ渡す
            self.autologin.wait_random() # ランダム時間で待機
            self.autologin.click_element(lg_el) # Auto_Login_Flowクラスのclick_elementメソッドを呼び出し、lg_elに渡されたWebElmentを渡して、ログインボタンをクリック
            

        # ログイン後のチェック
            if self.autologin.is_logged_in(self.chrome_driver):
                pass
            
            else:
                return
            
        # エリア選択、転載可レ点,検索の要素を探す
            self.autologin.wait_random() # ランダム時間で待機
            
            cb_ar_el = self.autologin.find_element(self.chrome_driver,By.CSS_SELECTOR,".jqTransformCheckboxWrapper a.jqTransformCheckbox") # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、チェックボックスの要素を探し、戻り値を渡す
            cb_te_el = self.autologin.find_element(self.chrome_driver,By.CSS_SELECTOR,"#chkKoukoku2") # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、チェックボックスの要素を探し、戻り値を渡す
            cb_ke_el = self.autologin.find_element(self.chrome_driver,By.CSS_SELECTOR,"span.searchdtlara img[src*='btn_area_route_search_out.gif']") # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、チェックボックスの要素を探し、戻り値を渡す
        
        # エリア選択をリセットしてクリック
            self.autologin.wait_random() # ランダム時間で待機
            self.autologin.checkbox_reset(cb_ar_el) # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、WebElmentの戻り値を渡して、チェックボックスをリセットする
            self.autologin.click_element(cb_ar_el) # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、WebElmentの戻り値を渡して、チェックボックスをクリックする
            
        # 転載可をリセットしてレ点クリック    
            self.autologin.wait_random() # ランダム時間で待機
            self.autologin.checkbox_reset(cb_te_el) # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、WebElmentの戻り値を渡して、チェックボックスをリセットする
            self.autologin.click_element(cb_te_el) # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、WebElmentの戻り値を渡して、チェックボックスをクリックする
            
        # 検索をクリック    
            self.autologin.wait_random() # ランダム時間で待機
            self.autologin.click_element(cb_ke_el) # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、WebElmentの戻り値を渡して、チェックボックスをクリックする
    # ------------------------------------------------------------------------------

    # 関数定義
    
    # ------------------------------------------------------------------------------
    
    # 関数定義
    
    # ------------------------------------------------------------------------------

    # 関数定義
    
        
    # **********************************************************************************
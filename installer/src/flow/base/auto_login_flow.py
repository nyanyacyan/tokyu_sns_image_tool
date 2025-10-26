# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# auto_login_flow.py

# 標準モジュールimport
from selenium.common.exceptions import TimeoutException # 「selenium.common.exceptions」というモジュールから、「TimeoutException」という操作や処理が設定時間内に完了されなかった場合に通知するクラス
from selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラス
from selenium.webdriver.support.ui import WebDriverWait # 「selenium.webdriver.support.ui」というモジュールから取り込んだ「WebDriberWait」という待機オブジェクト作るクラス
from selenium.webdriver.support import expected_conditions as EC # 「selenium.webdriver.support」というモジュールから取り込んだ「expected_conditions」という「どんな条件を満たすまで待つか」という待機オブジェクトを作るモジュールを略して「EC」としている
from pathlib import Path # 「pathlib」というファイルやフォルダのpathを扱うモジュールから、pathを取り扱う「Path」というクラスを取り組む
from selenium.webdriver.remote.webelement import WebElement # 「slenium.webdriver.remote.webelement」というモジュールから取り込んだ「WebElment」という、ブラウザ上の要素を操作するクラス
from urllib.parse import urljoin,quote,urlparse # 「urllib.parse」というURLを扱うモジュールから、「urljoin」と「quote」という関数を取り込む
from contextlib import contextmanager # 「contextlib」という標準ライブラリのモジュールから、「contextmanager」というデコレーター関数を取り込む
from typing import Optional,Iterable,List # 「typing」という標準ライブラリのモジュールから、「Optional」、「Iterable」、「List」という型ヒントを取り込む
import json,time,random,re,pickle # 「json」、「time」、「random」、「re」、「pickle」という標準ライブラリのモジュールを取り込む

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
            return el
            
        except TimeoutException as e: # 時間内に要素が見つからなかった時の処理
            self.logger.error_log(f"[find_element]要素が見つかりません: by={by},value={value},timeout={timeout},url={driver.current_url}") # 要素取得失敗のログ
        
            raise
        
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
            WebDriverWait(el.parent, timeout).until(EC.element_to_be_clickable(el))# WebDriverWaitをインスタンス化　Chromeブラウザで、指定の属性が出現するまで最大10秒待機
            el.click() # find_elementメソッド内のdriver.find_elementメソッドで、戻り値がWebElementのオブジェクトが返ってきて、そのWebElementオブジェクトに属しているclickメソッドを呼び出してクリックする。
            
            self.logger.info_log(f"[click_element]クリック成功") # 要素取得成功のログ
        
        except Exception as e:
            self.logger.error_log(f"[click_element]クリック失敗:error={e}") # 要素取得失敗のログ
            raise
# ------------------------------------------------------------------------------    
    # 関数定義
    def open_new_tab(self,driver,url: str) -> None:
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
        
        if el.is_selected(): # WebElementオブジェクトに属しているis_selectedメソッドを呼び出して、チェックボックスにレ点が入っているか判定
            el.click() # レ点が入っていたら、WebElementオブジェクトに属しているclickメソッドを呼び出して、チェックボックスをクリックしてレ点を外す
            self.logger.info_log(f"チェックボックスをリセット（OFF）しました") # チェックボックスをOFFにしたログ
            
        else:
            self.logger.info_log(f"チェックボックスは既にOFFです") # チェックボックスがOFFのログ 

# ------------------------------------------------------------------------------
    # 関数定義
    def swich_to_iframe(self,driver,by,value,timeout=15) -> None: 
        """指定iframeが利用可能になるまで待ち、そこへ切り替える"""
        try:
            iframe_el = self.find_element(driver,by,value) # Auto_Login_Flowクラスのfind_elementメソッドを呼び出して、iframe要素を探し、戻り値であるWebElementをiframe_elへ渡す
            driver.switch_to.frame(iframe_el) # webdriver.Chromeクラスのswitch_to.frameメソッドを呼び出して、引数へ渡されたiframe_elを渡して、iframe内へ移動する
            self.logger.info_log(f"[iframe] iframe内に切り替え完了") # 要素取得成功のログ
            
        except TimeoutException:
            self.logger.error_log(f"[iframe] iframeが見つかりません: by={by}, value={value}") # 要素取得失敗のログ
            raise
# ------------------------------------------------------------------------------
    # 関数定義
    def switch_to_default(self,driver) -> None:
        """iframeから親ページに戻る"""
        driver.switch_to.default_content() # webdriver.Chromeクラスのswitch_to.default_contentメソッドを呼び出して、親ページへ戻る
        self.logger.info_log(f"[irame] 親ページに戻りました") # 要素取得成功のログ
    
# ------------------------------------------------------------------------------
    # 関数定義
    def find_elements(self,driver,by,value,timeout=10) -> list[WebElement]:
        """指定した要素群を探して返す"""
        
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((by,value))) # WebDriverWaitをインスタンス化　Chromeブラウザで、指定の属性が出現するまで最大10秒待機
            els = driver.find_elements(by,value,) # 引数driverから、webdriver.Chromeクラスを貰い、そこからfind_elementsメソッドを呼び出して、byとvalueに渡された引数を渡して、属性を探す
            self.logger.info_log(f"[find_elements]要素を{len(els)}件取得成功: by={by},value={value}") # 要素取得成功のログ
            return els
            
        except TimeoutException : # 時間内に要素が見つからなかった時の処理
            self.logger.error_log(f"[find_elements]要素群が見つかりません: by={by},value={value},timeout={timeout},url={driver.current_url}") # 要素取得失敗のログ
        
            return[]
# ------------------------------------------------------------------------------
    # 関数定義
    def get_onclick(self,el:WebElement) -> str:
        """要素のonclick属性を取得して返す"""
        
        try:
            onclick_val = el.get_attribute("onclick") # WebElementモジュールの「get_attribute」メソッドを呼び出して、引数で指定したhtmlの要素である「onclick」が持つ値を抜き出す
            
            if onclick_val:
                self.logger.info_log(f"[get_onclick] onclick取得成功:{onclick_val}") # 取得成功のログ
            else:
                self.logger.info_log(f"[get_onclick] onclickが空文字またはNoneでした") # 何も取得出来ない時のログ
                
            return onclick_val
            
        except Exception as e:
            self.logger.error_log(f"[onclick] 取得失敗: {e}") # 取得失敗のログ
            
            return ""
    
# ------------------------------------------------------------------
    # 関数定義
    def parse_window_open_first_arg(self,onclick: str) -> Optional[str]:
        """onclick属性のwindow.openの第一引数を抽出して返す"""
        
        if not onclick:
            self.logger.info_log(f"[parse_window_open_first_arg] 引数onclickが空のためスキップ") # onclickが何もなかったときのログ
            return None
        
        m = re.search(r"window\.open\s*\((.*)\)\s*;?\s*$",onclick.strip()) # 正規表現の「re」という文字列を検索する標準モジュールのsearchメソッドを呼び出し、第一引数へ「検索したい文字列パターン」、第二引数へ「検索対象の文字列」を渡して、widow・・の文字列を探す。stripメソッドは文字列の先頭と末尾から空白や指定した文字を取り除く
        
        if not m:
            self.logger.error_log(f"[parse_window_open_first_arg] window.openが見つかりません: {onclick}") # 指定した文字列が見つからない場合のログ
            return None
        
        inside = m.group(1) # reモジュールで検索を実行した結果として返される「Match」オブジェクトのgroupメソッドを呼び出し、（）で指定した引数部分を取得して、onclickの値を取得する。
        
        depth = 0
        quote_ch = None
        arg_chars = []
        
        for ch in inside:
            if quote_ch:
                arg_chars.append(ch)
                if ch == quote_ch:
                    quote_ch = None
                continue
            
            if ch in ("'",'"'):
                quote_ch = ch
                arg_chars.append(ch)
                continue
            
            if ch == "(":
                depth += 1
                arg_chars.append(ch)
                continue
                
            if ch == ")":
                depth -= 1
                arg_chars.append(ch)
                continue
                
            if ch == "," and depth == 0:
                break
            
            arg_chars.append(ch)
            
        first_arg = "".join(arg_chars).strip()
        
        if first_arg and first_arg[0] in ("'",'"'):
            q = first_arg[0]
            
            if not first_arg.rstrip().endswith(q):
                self.logger.error_log(f"[parse_window_open_first_arg] 末尾クォート欠落を検知。補完します")
                first_arg = first_arg + q
            
            if first_arg:
                self.logger.info_log(f"[parse_window_open_first_arg] 第一引数抽出成功: {first_arg}")
            else:
                self.logger.info_log(f"[parse_window_open_first_arg] 第一引数を抽出できませんでした")
                    
        return first_arg or None    

# ------------------------------------------------------------------------------
    # 関数定義
    def evaluate_js_concat(self,expr: str) -> Optional[str]:
        """JavaScriptの文字列連結式を評価して返す"""
        if not expr:
            self.logger.info_log(f"[evaluate_js_concat] expが空のためNoneを返します")
            return None
        
        s = expr.strip()
        if len(s) >= 2 and s[0] in ("'",'"') and s[-1] == s[0]:
            plain = s[1:-1]
            self.logger.info_log(f"[evaluate_js_concat] シンプル文字列として解釈:{plain}")
            return plain

        tokens = []
        buf = ""
        depth = 0
        quote_ch = None
        
        for ch in s:
            if quote_ch:
                buf += ch
                if ch == quote_ch:
                    quote_ch = None
                continue
            
            if ch in ("'",'"'):
                quote_ch = ch
                buf += ch
                continue
            
            if ch == "(":
                depth += 1
                buf += ch
                continue
            
            if ch == ")":
                depth -= 1
                buf += ch
                continue
            
            if ch == "+" and depth == 0:
                if buf.strip():
                    tokens.append(buf.strip())
                buf = ""
                continue
                
            buf += ch
        
        if buf.strip():
            tokens.append(buf.strip())
        
        parts: list[str] = []
        for t in tokens:
            
            if len(t) >= 2 and t[0] in ("'",'"') and t[-1] == t[0]:
                val = t[1:-1]
                parts.append(val)
                self.logger.info_log(f"[evaluate_js_concat] 文字列トークン:{[val]}")
                continue
            
            m2 = re.match(r"encodeURI\s*\(\s*(['\"])(.*?)\1\s*\)",t)
            if m2:
                original = m2.group(2)
                encoded = quote(original,safe="~()*!.'")
                parts.append(encoded)
                self.logger.info_log(f"[evaluate_js_concat] encodeURIトークン: 元={original}, エンコード後={encoded}")
                continue
                    
            self.logger.error_log(f"[evaluate_js_concat] 評価できないトークンがあります: {t}")
            parts.append(t)
            
        result = "".join(parts)
        self.logger.info_log(f"[evaluate_js_concat] 連結結果: {result}")
        return result

# ------------------------------------------------------------------------------
    # 関数定義
    def to_absolute_url(self,path_or_url: str,driver) -> Optional[str]:
        """相対URLを絶対URLに変換して返す"""
        if not path_or_url:
            self.logger.info_log(f"[to_absolute_url] 空のURLが渡されました")
            return ""
        
        if re.match(r"^https?://",path_or_url):
            self.logger.info_log(f"[to_absolute_url] 既に絶対URLです: {path_or_url}")
            return path_or_url
        
        base =  "https://map.cyber-estate.jp/mediation/main/" 
        abs_url =  urljoin(base,path_or_url)
        
        self.logger.info_log(f"[to_absolute_url] 相対URLを絶対URLに変換: base={base} + path={path_or_url} -> {abs_url}")
        return abs_url
    
# ------------------------------------------------------------------------------
    # 関数定義
    def simplify_detail_url(self,expr: str) -> str:
        """詳細URLを簡略化して返す"""
        m = re.match(r"""^['"]([^'"]*?&hid=)['"]\s*\+\s*encodeURI\(\s*['"]([^'"]+)['"]\s*\)\s*\+\s*['"]([^'"]+)['"]\s*$""",expr.strip())
        
        if m:
            prefix = m.group(1)
            hid_val = m.group(2)
            suffix = m.group(3)
            hid_enc = quote(hid_val,safe="~()*!.'")
            result = prefix + hid_enc + suffix
            self.logger.info_log(f"[simplyfy_detail_url] 特殊パターンで整形: {result}")
            return result
        
        self.logger.info_log(f"[simplify_detail_url] 通常パターンで整形")
        return self.evaluate_js_concat(expr)
#**********************************************************************************


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# auto_login_flow.py

# 標準モジュールimport
from selenium.common.exceptions import TimeoutException, NoSuchElementException # 「selenium.common.exceptions」というモジュールから、「TimeoutException」という操作や処理が設定時間内に完了されなかった場合に通知するクラス
from selenium.webdriver.common.by import By # 「selenium.webdriver.common.by」というモジュールから取り込んだ「By」という、どの方法でhtmlの要素を探すかを指定するクラス
from selenium.webdriver.support.ui import WebDriverWait # 「selenium.webdriver.support.ui」というモジュールから取り込んだ「WebDriberWait」という待機オブジェクト作るクラス
from selenium.webdriver.support import expected_conditions as EC # 「selenium.webdriver.support」というモジュールから取り込んだ「expected_conditions」という「どんな条件を満たすまで待つか」という待機オブジェクトを作るモジュールを略して「EC」としている
from pathlib import Path # 「pathlib」というファイルやフォルダのpathを扱うモジュールから、pathを取り扱う「Path」というクラスを取り組む
from selenium.webdriver.remote.webelement import WebElement # 「slenium.webdriver.remote.webelement」というモジュールから取り込んだ「WebElment」という、ブラウザ上の要素を操作するクラス
from urllib.parse import urljoin,quote,urlparse # 「urllib.parse」というURLを扱うモジュールから、「urljoin」と「quote」という関数を取り込む
from contextlib import contextmanager # 「contextlib」という標準ライブラリのモジュールから、「contextmanager」というデコレーター関数を取り込む
from typing import Optional,Iterable,List,Dict # 「typing」という標準ライブラリのモジュールから、「Optional」、「Iterable」、「List」、「Dict」という型ヒントを取り込む
from datetime import datetime
import json, time, random, re, pickle, base64,os #「json」、「time」、「random」、「re」、「pickle」、「base64」、「os」という標準ライブラリのモジュールを取り込む

# 自作モジュールimport
from flow.base.logger import Logger  # logger.pyからLoggerクラスを取り込む
from flow.base.path import get_pickle_file_dir,get_today_pickle_path
from .chrome import Chrome # chrome.pyからChromeクラスを取り込む

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
    
# ------------------------------------------------------------------------------
    # 関数定義
    def get_detail_links(self,driver) -> list[WebElement]:
        """一覧から『詳細』ボタンのa要素を全て取得"""
        return self.find_elements(driver,By.XPATH,"//a[contains(@onclick,'window.open')][.//img[@alt='詳細']]")


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
        
        depth = 0 # カッコの深さを変数depthにて数える
        quote_ch = None # 'や"に出会ったら文字列の先頭として変数quote_chにて捉える
        arg_chars = [] # 抜き出した第一引数の文字を変数arg_charsに1文字ずつ貯める
        
        for ch in inside: # リスト変数insideから1文字ずつを取り出して、変数chへ代入して、以下のいずれかのif文処理を行う
            
            if quote_ch: # 変数quote_chがTrueの時の処理。’や”があった場合の次の文字列、つまりaとかbの通常の文字列の処理
                arg_chars.append(ch) # appendという初期から備わっている、リスト型メソッドを用いて引数chで受け取った1文字を、リストarg_charsへ順番に追加していく
                if ch == quote_ch: # 変数chと変数quote_chが一致した場合の処理。つまり最初に’や”が補足され、その次に’や”を補足した場合の処理
                    quote_ch = None # 変数quote_chにNoneを代入して、この処理をスキップ
                continue
            
            if ch in ("'",'"'): # 変数chに"'",'"'がある場合の処理
                quote_ch = ch # 変数quote_chへ、変数chの値、つまり’や”を代入する
                arg_chars.append(ch) # appendという初期から備わっている、リスト型メソッドを用いて引数chで受け取った1文字を、リストarg_charsへ順番に追加していく
                continue
            
            if ch == "(": # 変数chと「（　」の文字列が一致した場合の処理
                depth += 1 # 変数depthへ1を足して代入
                arg_chars.append(ch) # appendという初期から備わっている、リスト型メソッドを用いて引数chで受け取った1文字を、リストarg_charsへ順番に追加していく
                continue
                
            if ch == ")": # 変数chと「　）」の文字列が一致した場合の処理
                depth -= 1 # 変数depthへ1を引いて代入
                arg_chars.append(ch) # appendという初期から備わっている、リスト型メソッドを用いて引数chで受け取った1文字を、リストarg_charsへ順番に追加していく
                continue
                
            if ch == "," and depth == 0: # 変数chが「,」と一致した場合、と変数depthが0で一致した場合、文字列が終わったと判断して、for文処理を抜け出す。
                break
            
            arg_chars.append(ch) # appendという初期から備わっている、リスト型メソッドを用いて引数chで受け取った1文字を、リストarg_charsへ順番に追加していく
            
        first_arg = "".join(arg_chars).strip() # ""という空文字を区切りとして、変数arg_chars内の1文字ずつを、joinという初期から備わっている文字型メソッドを用いて結合し、同じく初期から備わっている文字型メソッドのstiripを引数なしで指定することで、文字列前後の空白・改行・空白文字を削除して、変数first_argに代入する。
                    
        if first_arg and first_arg[0] in ("'",'"'): # 変数first_argがTrueかつ、［0］で指定した、変数first_argの一文字目が、「’」か「”」である場合は、以下の処理を行う。
            q = first_arg[0] # 変数first_argの一文字目を、変数qに代入する。
            
            if not first_arg.rstrip().endswith(q): # 変数first_argの末尾を空白を削除する「rtstrip」というメソッドと、引数で変数qにて渡された値が、変数first_argの文字列の最後にあるかをチェックする「endswith」というメソッドを使用して、それが否定されてTrueだった場合、次の処理が行われる。つまり末尾に「”か’」が無ければ処理が行われる。
                self.logger.error_log(f"[parse_window_open_first_arg] 末尾クォート欠落を検知。補完します") # 抽出した文字列の末尾に「”か’」が無かったときのログ
                first_arg = first_arg + q # 変数first_argに変数qを足して、変数first_argへ代入する。
            
            if first_arg: # 変数first_argの末尾に「”か’」がある場合、次の処理が行われる。
                self.logger.info_log(f"[parse_window_open_first_arg] 第一引数抽出成功: {first_arg}") # 抽出した文字列の末尾に「”か’」が有ったときのログ
                
            else: # 上記いづれの条件を満たさなかった場合、次の処理が行われる。
                self.logger.info_log(f"[parse_window_open_first_arg] 第一引数を抽出できませんでした") # 文字列の抽出に失敗したときのログ
                    
        return first_arg or None # 変数first_argに値があれば、それを返し、ない場合はNoneを返す

# ------------------------------------------------------------------------------
    # 関数定義
    def to_absolute_url(self,path_or_url: str,driver) -> Optional[str]:
        """相対URLを絶対URLに変換して返す"""
        
        if not path_or_url: # 渡された引数path_or_urlがTrueではない時、以下の処理を行う。
            self.logger.info_log(f"[to_absolute_url] 空のURLが渡されました") # 空のURLが渡されたときのログ
            return ""
        
        if re.match(r"^https?://",path_or_url): # 正規表現reモジュールのmatchメソッドで、第一引数で指定された文字列と、第二引数で指定された変数に格納されている文字列が一致した場合、以下の処理を行う。
            self.logger.info_log(f"[to_absolute_url] 既に絶対URLです: {path_or_url}") # 絶対URLが渡されたときのログ
            return path_or_url
        
        base =  "https://map.cyber-estate.jp/mediation/main/"  # 結合するURLを変数baseへ代入する
        abs_url =  urljoin(base,path_or_url) # urljoinメソッドを使用して、変数baseと変数path_or_urlを結合して、変数abs_urlへ代入する
        
        self.logger.info_log(f"[to_absolute_url] 相対URLを絶対URLに変換: base={base} + path={path_or_url} -> {abs_url}") # URL結合成功時のログ
        return abs_url
    
# ------------------------------------------------------------------------------
    # 関数定義
    def simplify_detail_url(self,expr: str) -> str:
        """詳細URLを簡略化して返す"""
        
        m = re.match(r"""^['"]([^'"]*?&hid=)['"]\s*\+\s*encodeURI\(\s*['"]([^'"]+)['"]\s*\)\s*\+\s*['"]([^'"]+)['"]\s*$""",expr.strip()) # 正規表現reモジュールのmatchメソッドを使用して、変数exprの文字列の前後をstripメソッドで空白を削除した文字列が、matchメソッドの第一引数で指定した文字列と適合するか調べ、適合した場合、その値を変数mに代入する。
        
        if m:
            prefix = m.group(1) # reモジュールで検索を実行した結果として返される「Match」オブジェクトのgroupメソッドを呼び出し、（）で指定した引数部分の文字列を取得して、変数prefixへ代入する
            hid_val = m.group(2) # reモジュールで検索を実行した結果として返される「Match」オブジェクトのgroupメソッドを呼び出し、（）で指定した引数部分の文字列を取得して、変数hid_valへ代入する
            suffix = m.group(3) # reモジュールで検索を実行した結果として返される「Match」オブジェクトのgroupメソッドを呼び出し、（）で指定した引数部分の文字列を取得して、変数suffixへ代入する
            hid_enc = quote(hid_val,safe="~()*!.'") # 取得した文字列をURLとして使えるように、変換するメソッドである「quote」を用いて、第一引数へ変換する文字列をしていして、第二引数へエンコードしない文字列をしていし、変数hid_encに代入する
            result = prefix + hid_enc + suffix # 変数prefix、hid_enc、suffixをそれぞれ足して、変数resultへ代入する
            self.logger.info_log(f"[simplyfy_detail_url] 特殊パターンで整形: {result}") # 文字列の結合に成功したときのログ
            return result
        self.logger.info_log(f"[simplyfy_detail_url] パターンに該当せず、そのまま返します: {expr}")
        return expr

        
# ------------------------------------------------------------------------------
    # 関数定義
    def clean_text(self,text:str) -> str:
        """改行や余分なスペースをまとめて、前後空白を取る"""
        original = text # clean_textメソッドの引数textに渡された文字列を、変数originalへ代入する。
        cleaned = re.sub(r"\s+"," ",text).strip() # 正規表現reモジュールのsubメソッドを使用して、第一引数で指定した空白文字列を探して、第二引数で指定した半角文字を、第三引数で指定した文字列内を検索して置き換えて、stripメソッドを用いて文字の前後の空白を削除し、変数originalへ代入する。
    
        if original != cleaned:# 変数originalと変数cleanedが一致しない場合、以下の処理を行う。
            self.logger.info_log(f"[clean_text] 正規化を実施: before={repr(original)}, after={repr(cleaned)}") # 成功したときのログ
        
        else:
            self.logger.info_log(f"[clean_text] 変更無し: {repr(original)}") # 失敗したときのログ
        
        return cleaned
# ------------------------------------------------------------------------------
    # 関数定義
    def sanitize_title(self,title:str) -> str:
        """ファイル名などに使えない記号を安全な文字に変える"""
        original = title # sanitize_titleメソッドの引数titleに渡された文字列を、変数originalへ代入する。
        sanitized = re.sub(r'[\\/:*?"<>|]',"_",title) # 正規表現reモジュールのsubメソッドを使用して、第一引数で指定した空白文字列を探して、第二引数で指定した文字列を、第三引数で指定した文字列内を検索して置き換えて、変数sanitizeへ代入する。
        
        if original != sanitized: # 変数originalと変数sanitizedが一致しない場合、以下の処理を行う。
            self.logger.info_log(f"[sanitize_title] 禁止文字を置換: before={repr(original)},after={repr(sanitized)}") # 成功したときのログ
        
        else:
            self.logger.info_log(f"[sanitize_title] 変更無し: {repr(original)}") # 失敗したときのログ
            
        return sanitized
    
# ------------------------------------------------------------------------------
    # 関数定義
    def extract_room_info_from_row(self,row:WebElement) -> WebElement:
        """一つの部屋行から物件名・専有面積・階を取り出して返す"""
        try:
            tds = row.find_elements(By.TAG_NAME,"td") # extract_room_info_from_rowメソッドの引数で渡された、webelmentのfind_elementsメソッドを呼び出して、ByクラスのTAG_NAMEメソッドにて”td”タグを探した結果を、変数tdsへ代入する。
            
            if len(tds) < 6: # 変数tdsに格納されたtdタグの個数が6個未満の場合、以下の処理を行う。
                self.logger.error_log(f"extract_room_info_from_row 想定列数未満のためスキップ:len(tds)={len(tds)}") # 失敗したときのログ
                return None
            
            prop_span = row.find_element(By.XPATH,"ancestor::table[contains(@class,'bkn_list_block')][1]""//li[contains(@class,'clsListBkn')]/span") # 変数rowに返されたwebelmentメソッドの引数で、XPATHで物件ブロックの文字列を探して、その結果を変数prop_spanへ代入する。
            property_name = self.clean_text(prop_span.text) # clean_textメソッドで、変数prop_span内の指定文字列を半角スペースへ変換して、変数property_nameへ代入する。
            
            area_text = self.clean_text(tds[4].text) # 変数tbsに格納されている5列目のリストの文字列である専有面積の文字列の余分な改行や空白を整理して、変数area_textに代入する。
            floor_raw = tds[5].text.splitlines()[0] # 変数tbsに格納されている6列目のリスト文字列である階の文字列を、改行ごとに分割するメソッドであるsplitlinesで、2分割して、1行目だけを取り出して、変数floor_rawに代入する。
            floor_text = self.clean_text(floor_raw) # 変数floor_rawに格納されている文字列の余分な改行や空白をclean_textメソッドで整理して、変数floor_textに代入する。
            
            self.logger.info_log(f"[extract_room_info_from_row] 取得成功: "f"物件名={property_name}, 専有面積={area_text}, 階={floor_text}") #　成功したときのログ 
            
            return property_name,area_text,floor_text
        
        except Exception as e:
            self.logger.error_log(f"[extract_room_info_from_row] 取得失敗: {e}") # 失敗したときのログ
            return None
        
# ------------------------------------------------------------------------------
    # 関数定義
    def make_title(self,property_name:str, area:str, floor:str) -> str:
        """物件名・専有面積・階から辞書用タイトルを作る"""
        
        title = f"物件名{property_name}_専有面積{area}_階{floor}" # extract_room_info_from_rowメソッドで取り出した物件名、専有面積、階をつなげて変数titleへ代入する。
        title = self.sanitize_title(title) # ファイル名に使用できない文字列を変換して、再度変数titleへ代入する。
        return title
    
# ------------------------------------------------------------------------------
    # 関数定義
    def create_property_dict(self,driver) -> Dict[str,str]:
        """一覧テーブルからタイトル（物件名_専有面積_階）ｰ>詳細URLの辞書を作成して返す"""
        d: Dict[str,str] = {} # 変数dへ空の辞書を代入する
        detail_links = self.find_elements(driver,By.XPATH,"//a[contains(@onclick,'window.open')][.//img[@alt='詳細']]") # 一覧ページにある全ての詳細のボタンがある周辺の要素を取り出して、変数dtail_linksへ代入する。
    
    
        for a in detail_links: # 変数dtail_linksに格納された、一覧表示から取得した詳細ボタンの情報を繰り返し処理をする
            try:
                oc = self.get_onclick(a) # 詳細ボタンの要素を取り出す。
                first = self.parse_window_open_first_arg(oc) # onclick属性のwindow.openの第一引数、つまり物件URLを抽出して返す
                if not first: # 物件URLがない場合の処理
                    self.logger.error_log("[create_property_dict] onclick解析に失敗。スキップ") # 失敗したときのログ
                    continue
                
                rel = self.simplify_detail_url(first)or first # 詳細URLを簡略化して返す、またはsimplify_detail_urlメソッドが空の場合は、変数firstを変数relに代入する。
                url = self.to_absolute_url(rel,driver) # 相対URLを絶対URLに変換して返して、変数urlに代入する
                if not url: # 絶対URLがない場合の処理
                    self.logger.error_log(f"[create_property_dict] URL生成に失敗。スキップ") # 失敗したときのログ
                    continue
                
                row = a.find_element(By.XPATH,"./ancestor::tr[contains(@class,'clsTrData')][1]") # 詳細ボタン（aタグ）から見て、一番近い「tr.clsTrData」の行を、すなわち物件名・専有面積・階の情報の文字列を取得する。
                info = self.extract_room_info_from_row(row) # 変数rowに代入された一つの部屋行から物件名・専有面積・階を取り出して返す
                if not info: # 物件名・専有面積・階の情報がない場合の処理
                    continue 
                property_name,area_text,floor_text = info # 先の変数へ、変数infoに格納されている、物件名・専有面積・階の数値を代入する。
            
                title = self.make_title(property_name,area_text,floor_text) # 物件名・専有面積・階から辞書用タイトルを作る
                title = self.ensure_unique_title(d,title) #辞書のタイトルが重ならないようにする 
                
                d[title] = url # titleを辞書のキー、urlを辞書の値として、変数dへ辞書データを登録する。
            
            except Exception as e:
                self.logger.error_log(f"[create_propery_dict] 行処理中にエラー: {e}") # 失敗したときのログ
                continue
        
        return d 

# ------------------------------------------------------------------------------
    # 関数定義
    def ensure_unique_title(self, d:Dict[str,str], title:str) -> str:
        """辞書の中でtitleが重複しないように、末尾に_2、_3....をつけて返す"""
        
        original = title 
        suffix = 2 # 変数suffixへ2を代入する
        while title in d: # 変数titleの値の中に、変数dの値が含まれていた場合、すなわち辞書タイトルが被っていた場合の繰り返し処理
            title = f"{original}_{suffix}" # 辞書タイトルのあとに数値を追加
            suffix += 1 # 被るたびに1カウントして増やしていく
            
        return title
# ------------------------------------------------------------------------------
    # 関数定義
    def save_titles_pickle(self, data: dict | list) -> dict | list: # 「｜」はorを意味する
        """タイトル辞書（またはリスト）をpickleとして保存する"""
        
        try:
            pkl_path = get_today_pickle_path() # pathファイルの、今日の日付を使ったpickleファイルのパスを返すメソッドを呼び出し
            
            with open(pkl_path, "wb") as f: # ファイル操作の組み込み関数である、open関数の第一引数に指定のファイルの値が格納されている「pkl_path」を渡し、第二引数へ操作モードを書き込み用にバイナリモードでオープンする「wb」を渡して、open（）が返すファイルオブジェクトをfという変数名とする
                pickle.dump(data, f) # pickleモジュールの、ファイルにデータを書き込むdump関数の第一引数へ、引数dataで受け取った辞書データ、またはリストデータを第二引数で指定したpickleファイルへ書き込みを行う
                
                self.logger.info_log(f"[save_titles_pickle] 保存成功: {pkl_path}") # pickleファイルへの保存が成功したときのログ
                
                self.cleanup_old_pickles() # 古いpklファイルを削除する
                
                return pkl_path
            
        except Exception as e:
            self.logger.error_log(f"[save_titles_pickle] 保存失敗: {e}") # pickleファイルへの保存に失敗したときのログ
            return None

# ------------------------------------------------------------------------------
    # 関数定義
    def get_latest_pickle_file(self) -> Optional[Path]:
        """最新のpklを探す"""
        
        pdir = get_pickle_file_dir() # ログを保存するディレクトリのパスを返して、ディレクトリがなければ自動作成する関数を呼び出し 
        files = list(pdir.glob("*.pkl")) # list関数で、ログを保存するパスが格納されている、変数pdir内で、「.pkl」のファイルを取得して、リスト化する
        
        if not files: # pklファイルが無い場合の処理
            self.logger.info_log("[get_latest_pickle_file] pickleなし→None返す") # pklファイルがない場合のログ
            return None
        
        latest = max(files, key=lambda p:p.stem) # リスト内の最大値を求めるmax関数の第一引数へ、pklのファイルパスが格納されている変数filesを渡し、第二引数へラムダ演算子で定義した、p.stemで拡張子を除いたファイル名、つまり日付の数値である引数pを、変数keyに代入して渡し、最新の日付を求める
        self.logger.info_log(f"[get_latest_pickle_file] 最新: {latest}") # 最新の日付pklファイルが有った場合のログ
        return latest
    
# ------------------------------------------------------------------------------
    # 関数定義
    def load_latest_titles_or_empty(self) -> dict | list:
        """最新のpickleを読み込む"""
        
        path = self.get_latest_pickle_file() # 最新のpklファイルを探すメソッドを呼び出す
        
        if not path: # 最新のpklファイルではない場合の処理
            return{} # 空の辞書を返す
        
        try:
            with open(path, "rb") as f: # ファイル操作の組み込み関数である、open関数の第一引数に指定のファイルの値が格納されている「path」を渡し、第二引数へ操作モードを読み込み用にバイナリモードでオープンする「rb」を渡して、open（）が返すファイルオブジェクトをfという変数名とする
                data = pickle.load(f) # pickleモジュールのファイルの読み込みを行うload関数で、第一引数へ最新のpklファイルが格納されている変数fを渡す
                
            self.logger.info_log(f"[load_latest_titles_or_empty] 読み込み成功: {path}") # 最新のpklファイル読み込み成功時のログ
            return data
        
        except Exception as e: # ファイル破損などのエラーでも止まらず、からの辞書を返して処理を続行させる
            self.logger.error_log(f"[load_latest_titles_or_empty] 読み込み失敗: {e}") # 最新のpklファイル読み込み失敗時のログ
            return {}
# ------------------------------------------------------------------------------
    # 関数定義
    def cleanup_old_pickles(self) -> None:
        """古いpickleを削除する"""
        pdir = get_pickle_file_dir() # ログを保存するディレクトリのパスを返して、ディレクトリがなければ自動作成する関数を呼び出し
        files = sorted(pdir.glob("*.pkl"), key=lambda p: p.stem) # sorted関数にてpklファイルを日付順の昇順にリストを並べ替えて、変数filesに代入
        
        if len(files) <= 1: # len関数で変数files内のリスト数を数えて、1以下の場合の処理
            self.logger.info_log(f"[cleanup_old_pickles] 削除対象なし") # 古いpklファイルが無い場合のログ
            return
        
        old_files = files[:-1] # 変数files内の日付の古いファイルパス名の順番から、最新の一つ手前までのファイルパス名を、変数old_fileへ代入
        
        for f in old_files: # 変数old_file内のファイルパスを繰り返し、変数fへ代入して処理
            try:
                f.unlink() # osモジュールのファイルパスを削除する関数を使用
                self.logger.info_log(f"[cleanup_old_pickles] 削除: {f}") # ファイル削除成功時のログ
            except Exception as e:
                self.logger.error_log(f"[clean_old_pickles] 削除失敗: {e}") # ファイル削除失敗時のログ
                
        
# ------------------------------------------------------------------------------
    # 関数定義
    def filter_new_titles(self,current_dict: dict[str,str], prev_data: dict | list) -> dict[str,str]:
        """前回までに保存されていたタイトルを除外して、今回「新たに見つかったタイトル」だけの辞書を返す"""
        
        if isinstance(prev_data,dict): # 指定した辞書データが格納されたprev_dataが、指定したdict型である場合、Trueを返したときの処理
            prev_titles = set(prev_data.keys()) # 組み込み関数のsetメソッドを呼び出して、第一引数で渡された辞書データが格納されてるprev_dataの、キーを１つずつ返し、それらを並び順の無い集合体に変換し、変数prev_titlesへ代入する
            
        elif isinstance(prev_data,list): # 指定した辞書データが格納されたprev_dataが、指定したlist型である場合、Trueを返したときの処理
            prev_titles = set(prev_data) # 組み込み関数のsetメソッドを呼び出して、引数で渡されたリストデータが格納されているprev_dataを、並び順のない集合体に変換し、変数prev_titlesへ代入する
            
        else:
            prev_titles = set() # それ以外は、空のセットを変数prev_titlesへ代入する
            
        total_now = len(current_dict) # 組み込み関数であるリストの要素の個数を調べるlen関数を使用して、引数のcurrent_dictに格納されている辞書データの要素を数えて、変数total_nowへ代入する
        new_dict: dict[str,str] = {} # 変数new_dictへ空の辞書データを代入する
            
        for title,url in current_dict.items(): # 変数current_dictに格納されているキーと値のペアを、タプルで1つずつ返し、変数titleとurlへそれぞれ繰り返し代入し、次の処理を行う
            if title in prev_titles: # 変数titleに格納されているキーが、変数prev_titlesに格納されている集合体の中に含まれている場合、次の処理を行う
                continue
            
            new_dict[title] = url # 変数urlに含まれている辞書データの値を、辞書型の変数new_dictに格納されている、キーである変数titleを指定して、値を変更する
            
        
        already_count = total_now - len(new_dict) # 引数current_dictに格納されている辞書データの要素数が格納されている、変数total_nowから、辞書型である変数new_dictに格納されている要素数を引いた値を、変数already_countへ代入する
        new_count = len(new_dict) # 辞書型である変数new_dictに格納されている要素数を、変数new_countへ代入する
        
        self.logger.info_log(f"[filter_new_titles] 今回取得: {total_now}件 /" f"既存: {already_count}件 / 新規:{new_count}件") # ログ出力
        
        return new_dict
# ------------------------------------------------------------------------------
    # 関数定義
    def make_empty_property_dict(self,title: str) -> dict:
        """1件の物件情報を入れるための「空の辞書テンプレ」を作って返す"""
        
        # 変数dへ以下の情報を格納する辞書データの雛形を作成
        d = {
            "title": title,
            "line": "",
            "station": "",
            "walk": "",
            
            "layout": "",
            "area": "",
            "price": 0,
            "maintenance_fee": 0,
            "deposit": 0.0,
            "key_money": 0.0,
            
            "features": [],
            "preferences": [],
            
            "exterior_image": "",
            "layout_image_path": "",
            
            "interior_1": "",
            "interior_2": "",
            "interior_3": "",
            "interior_4": "",
            "interior_5": "",
            
            "comment_b": "",
            "comment_c": "",
            "comment_d": "",
            
            "saved_files": [],
        } 
        
        self.logger.info_log(f"[make_empty_property_dict] テンプレ作成: title={title}")
            
        return d
# ------------------------------------------------------------------------------
    # 関数定義
    def add_line_station_walk(self,driver, data: dict) -> dict:
        """詳細ページの「交通/所在地」セルから、line（路線名）、station（駅名）、walk（徒歩情報）を取得して、引数dataの辞書に追加して返す"""
        
        
        try: # detail_pickupテーブルの中から『交通/所在地』という見出しセルを探し、その1つ下の行の1列目のセルの情報を取得
            cell = driver.find_element( 
                By.XPATH,
                (
                    "//table[@id='detail_pickup']"
                    "//td[contains(@class,'tbl_tit_detail')"
                    "and contains(.,'交通') and contains(.,'所在地')]"
                    "/parent::tr"
                    "/following-sibling::tr[1]"
                    "/td[1]"                           
                )
            )
            
        except NoSuchElementException: # 指定した要素が見つからないときの処理 
            self.logger.error_log(f"[add_line_station_walk] 交通/所在地セルが見つかりません")
            data["line"] = "" # 辞書データの"line"を空文字にする
            data["station"] = "" # 辞書データの"station"を空文字にする
            data["walk"] = "" # 辞書データの"walk"を空文字にする
            return data
        
        except Exception as e: # それ以外の例外処理で、要素が見つからないときと同様に該当辞書データを空文字にする
            self.logger.error_log(f"[add_line_station_walk] 要素取得中にエラー:{e}")
            data["line"] = ""
            data["station"] = ""
            data["walk"] = ""
            return data
        
        raw_text = cell.text.strip() # XPATHで取得した要素を格納した変数cellの先頭と末尾の空白を取り除いて、変数raw_textへ代入
        if not raw_text: # 変数raw_textが空の場合の処理で、要素が見つからないときと同様に、該当辞書データを空文字にする
            self.logger.info_log("[add_line_station_walk] 交通/所在地セルが空のため、空文字で保存")
            data["line"] = ""
            data["station"] = ""
            data["walk"] = ""
            return data
            
        first_line = raw_text.splitlines()[0] # XPATHで取得した要素をsptitlinesメソッドで改行しないで、1つの文字列にして、変数first_lineへ代入
        first_line = self.clean_text(first_line) # 自作のclean_textメソッドを使用して、文字列の前後の空白と改行をなくして、もう一度変数first_lineへ代入
        
        if "／" in first_line: # もし変数first_lineの中に全角のスラッシュが合った場合の処理
            left,walk = first_line.split("／", 1) # splitメソッドで全角スラッシュを区切り文字として、１回だけ変数first_lineの文字列を分割取得して、前半を変数left、後半を変数walkへ代入
            walk = self.clean_text(walk) # 全角スラッシュが含まれている文字列が格納された、変数walkの全角スラッシュを半角スラッシュに置き換えて、変数walkへ代入
        else: # それ以外の処理
            left = first_line # 変数first_lineを変数leftへ代入
            walk = "" # 変数walkへから文字を代入
            
            
        tokens = left.split() # 変数leftの文字列を、区切り文字無しの、分割回数0回でリストを取得し、変数tokensへ代入
        
        if len(tokens) >= 2: # 組み込み関数のlen（）で、変数tokensのリスト要素が2以上の場合の処理
            station = tokens[-1] # 変数tokensのリスト最後尾のリスト以外を、変数stationへ代入
            line_name = " ".join(tokens[:-1]) # 組み込み関数のjoinを用いて、変数tokensの最後尾のリスト以外のリスト全てを半角スペースと結合させて、変数line_nameへ代入
        else: # それ以外の処理
            line_name = left # 変数leftの値を、変数line_nameへ代入
            station = "" # 変数stationへ空文字を代入
            
        if station and not station.endswith("駅"): # もし変数stationの文字列の末尾が"駅"ではない場合の処理
            station = station + "駅" # 変数文字列の末尾に"駅"を足して、変数stationへ代入
            
        data["line"] = line_name # 辞書データのlineへ、変数line_nameの値を代入
        data["station"] = station # 辞書データのstationへ、変数stationの値を代入
        data["walk"] = walk # 辞書データのwalkへ、変数walkの値を代入
        
        self.logger.info_log(f"[add_line_station_walk] 取得成功: line={line_name},station={station},walk={walk}")
        
        return data
# ------------------------------------------------------------------------------
    # 関数定義
    def scrape_detail_pages_line_station_walk(self,driver,title_url_dict: Dict[str,str]) -> Dict[str,dict]:
        """タイトル　->　詳細URLの辞書を受け取り、各詳細ページを新しいタブで開いてline/station/walk/price/maintenance_fee/deposit/key_moneyを埋めたproperty_dictを返す"""
        
        results: Dict[str,dict] = {} # 変数resultsへからの辞書を代入
        original_handle = driver.current_window_handle # ｗebDriverメソッドにある、現在開いているタブの識別子（ID）を格納しているcurrent_window_handle変数、つまり詳細ページを開くまえの一覧ページのタブの識別子を変数original_hadleへ代入
        
        for title, url in title_url_dict.items(): # 辞書名title_url_dictから、ディクショナリメソッドであるitemsを用いて、キーと値をそれぞれ、変数titleとurlへ繰り返し代入処理
            self.logger.info_log(f"[scrape_detail_pages_line_station_walk] 詳細ページ処理開始: title={title},url={url}")
            
            prop = self.make_empty_property_dict(title) # 自作メソッドである空の辞書を作成する、make_empty_property_dictメソッドへ、引数へ繰り返し処理で代入された変数titileの値を渡して、辞書を作成し、その結果を変数propへ代入
        
            try:
                self.open_new_tab(driver,url) # 自作メソッドであるopen_new_tabの引数へ、渡された引数driverとurlの値を渡して、Chromeブラウザで詳細URLを開く
                self.wait_random()
            
                self.switch_to_default(driver) # 自作メソッドで新しいタブ内でのフレーム状態を初期化して、スクレイピングできるようにする
            
                prop = self.add_line_station_walk(driver,prop) # 自作メソッドであるadd_line_station_walkの引数へ、Chromeドライバーと繰り返し処理で代入された、変数titleが含まれた辞書データのpropを渡して、最寄り駅と徒歩時間を追加した辞書データを作成
                prop = self.add_deposit_and_key_money(driver,prop) #自作メソッドで詳細ページから、辞書データへ敷金と礼金の情報を辞書データへ追加 
                prop = self.add_layout_and_area(driver,prop) # 自作メソッドで詳細ページから、間取と専有面積の情報を辞書データへ追加
                prop = self.add_features_and_preferences(driver,prop) # 自作メソッドで詳細ページから、設備とこだわり情報を辞書データへ追加
                prop = self.add_exterior_and_layout_images(driver,prop) # 自作メソッドで詳細ページから、外観画像URL+間取り画像キャプチャを取得して辞書データへ追加
                prop = self.add_interior_images_and_comments(driver,prop) # 自作メソッドで詳細ページから、スライダー（#detail_pic）から interior_1〜5 を埋め、あわせて comment_b〜d を生成して辞書データへ追加
            
                self.logger.info_log(
                    f"[scrape_detail_pages_line_station_walk] 取得結果: "
                    f"line={prop['line']}, station={prop['station']},walk={prop['walk']}, " 
                    f"price={prop['price']}, maintenance_fee={prop['maintenance_fee']}, "
                    f"deposit={prop['deposit']}, key_money={prop['key_money']}, "
                    f"layout={prop['layout']}, area={prop['area']}, "
                    f"features={prop['features']}, preferences={prop['preferences']}"
                    f"exterior_image={prop['exterior_image']}, "
                    f"layout_image_path={prop['layout_image_path']}, "
                    
                )

                results[title] = prop # 変数propに格納された辞書データを、辞書resultsのキーである、変数titleに格納する
        
            except Exception as e:
                self.logger.error_log(f"[scrape_detail_pages_line_station_walk] "f"タイトル={title} の処理中にエラー: {e}")
            
            finally: # 例外処理の有無にかかわらず、必ず以下を処理
            
                try:
                    driver.close() # 詳細ページを開く際に立ち上がった新しいタブを閉じる
                except Exception as e:
                    pass
            
                try:
                    driver.switch_to.window(original_handle) # sleniumが操作対象とするブラウザの識別子を、一覧ページの識別子に渡して、そこを操作対象とする
            
                except Exception:
                    pass
            
        return results
                
# ------------------------------------------------------------------------------
    # 関数定義
    def extract_int_from_text(self,text: str) -> int:
        """文字列から数字だけ抜き出してintに変換（無ければ0）"""
        
        if text is None: # 引数textで受け取った値が、何も無い場合の処理
            return 0 # 変数textへ0を返す
        
        digits = re.sub(r"[^\d]","",text) # 正規表現の文字列を指定した文字列へ置換する、subメソッドを呼び出して、変数text内の文字列を、第一引数で指定した[^\d]、つまり数字以外の文字列を、第二引数で指定した空文字へ、置換して変数digitsへ代入
        
        if digits: # 変数digitsが真の場合
            val = int(digits) # 変数digitsの値を整数に置換し、変数valへ代入
            self.logger.info_log(f"[extract_int_from_text] 数値抽出成功: text={repr(text)}, val={val}")
            return val
        
        else:
            self.logger.info_log(f"[extract_int_from_text] 数値が見つからず0として扱います: text={repr(text)}")
            return 0        
# ------------------------------------------------------------------------------
    # 関数定義    
    def add_price_and_maintenance_fee(self,driver,data: dict) -> dict:
        """詳細ページの「賃料/管理費等」セルから、price（賃料）とmaintenance（管理費）を取得してdataに追加して返す"""
        
        try: # XPATHで該当のhtml要素を検索して、値の結果を変数cellへ代入
            cell = driver.find_element(
                By.XPATH,
                (
                    "//table[@id='detail_pickup']"
                    "//span[@id='detail_price']/parent::td"
                )
            ) 
        except Exception as e: # 要素が見つからなかった場合、辞書データのpriceとmaintenanceへ、0を代入して返す
            self.logger.error_log(f"[add_price_and_maintenance_fee] 賃料セルが見つかりません: {e}")
            data["price"] = 0
            data["maintenance_fee"] = 0
            return data
            
        raw_text = cell.text.strip() # XPATHで取得した値である文字列から、WebElementプロパティであるtextを用いて、有効な文字列だけを取得し、前後の空白を取り除いて、変数raw_textへ代入
        
        if not raw_text: # 変数raw_textが真でない場合、辞書データのpriceとmaintenanceへ、0を代入して返す
            self.logger.info_log(f"[add_price_and_maintenance_fee] 賃料セルが空のため0で保存します")
            data["price"] = 0
            data["maintenance_fee"] = 0
            return data
        
        lines = raw_text.splitlines() # 変数raw_text内の行で分割した、各行の文字列をリストで取得して、変数linesへ代入　例187,000円 管理費　5,0000円という2行の文字列を、lines　=["187,000円"、"管理費　5,000円"]とリスト化する
        
        price_line = lines[0] if len(lines) >= 1 else "" # 変数lines内のリストが1以上の場合、変数linesの1つ目を変数price_lineへ、それ以外の場合、空文字を変数price_lineへ代入する
        maint_line = lines[1] if len(lines) >= 2 else "" # 変数lines内のリストが2以上の場合、変数linesの2つ目を変数maint_lineへ、それ以外の場合、空文字を変数maint_lineへ代入する
        
        price_val = self.extract_int_from_text(price_line) # 自作メソッドのextract_int_from_textで、引数で渡された文字列から数字を整数にして、変数price_valへ代入
        maint_val = self.extract_int_from_text(maint_line) # 自作メソッドのextract_int_from_textで、引数で渡された文字列から数字を整数にして、変数price_valへ代入
        
        data["price"] = price_val # 変数price_valの値を辞書データのpriceへ代入
        data["maintenance_fee"] = maint_val # 変数maint_valの値を辞書データのmaintenance_feeへ代入
        
        self.logger.info_log(f"[add_price_and_maintenance_fee] 取得成功: price={price_val}, maintenance_fee={maint_val}")
        return data
        
# ------------------------------------------------------------------------------
    # 関数定義 
    def extract_float_months(self,text: str) -> float:
        """1ヶ月、1.5ヶ月、‐、なし、などの文字列からfloat値（月数）を抽出して返す。見つからなければ0.0とする。"""
        
        t = text.strip() # 引数textから渡された値である文字列の前後の空白を取り除いて、変数tへ代入
        
        if not t or t in("-","ー"): # 変数tが空文字または、変数tが、「‐」、「ー」である場合、0.0を返す
            self.logger.info_log(f"[extract_float_months] '-'判定のため0.0扱い: text={repr(text)}")
            return 0.0
        
        m = re.search(r"(\d+(?:\.\d+)?)", t) # 正規表現のsearchメソッドを呼び出して、変数tに格納されている文字列から、第一引数で指定した整数、または小数を変数mへ代入
        
        if not m: # 変数mがfalseの場合、0.0を返す
            self.logger.info_log(f"[extract_float_months] 数値が見つからず0.0扱い: text={repr(text)}")
            return 0.0
        
        val = float(m.group(1)) # マッチオブジェクトである、groupメソッドで、変数ｍの第一引数で指定した、整数または小数を取り出して、浮動小数点に変換して、変数valへ代入
        self.logger.info_log(f"[extract_float_months] 数値抽出成功: text={repr(text)}, val={val}")
        return val
# ------------------------------------------------------------------------------
    # 関数定義
    def add_deposit_and_key_money(self,driver,data: dict) -> dict:
        """詳細ページの「敷金（保証金）/礼金」セルから、deposit（敷金）とkey_money（礼金）を取得してdataに追加して返す"""
        
        try: # XPATHで該当のhtml要素を検索して、値の結果を変数cellへ代入
            cell = driver.find_element(
                By.XPATH,
                (
                    "//table[@id='detail_pickup']"
                    "//td[contains(@class,'tbl_tit_detail')and contains(.,'敷金')]"
                    "/parent::tr"
                    "/following-sibling::tr[1]"
                    "/td[3]"
                )
            )
        
        except Exception as e: # 例外処理の場合、辞書データのdepositとkey_moneyに0.0を代入
            self.logger.error_log(f"[add_deposit_and_key_money] 敷金/礼金セルが見つかりません: {e}")
            data["deposit"] = 0.0
            data["key_money"] = 0.0
            return data
        
        raw_text = cell.text.strip() # XPATHで取得した値である文字列から、WebElementプロパティであるtextを用いて、有効な文字列だけを取得し、前後の空白を取り除いて、変数raw_textへ代入
        
        if not raw_text: # 変数raw_textが空文字の場合、辞書データのdepositとkey_moneyに0.0を代入
            self.logger.info_log(f"[add_deposit_and_key_money] 敷金/礼金セルが空のため0.0で保存します")
            data["deposit"] = 0.0
            data["key_money"] = 0.0
            return data
        
        lines = raw_text.splitlines() # 変数raw_text内の行で分割した、各行の文字列をリストで取得して、変数linesへ代入
        deposit_line = self.clean_text(lines[0]) if len(lines) >= 1 else "" # 変数linesに格納されているリストの個数が1以上の場合、自作メソッドであるclean_textで、変数linesの1番目の値の余分な空白を埋めて、変数deposit_lineへ代入、それ以外の場合、空文字を代入
        key_line = self.clean_text(lines[1]) if len(lines) >= 2 else "" # 変数linesに格納されているリストの個数が2以上の場合、自作メソッドであるclean_textで、変数linesの2番目の値の余分な空白を埋めて、変数deposit_lineへ代入、それ以外の場合、空文字を代入
        
        deposit_val = self.extract_float_months(deposit_line) # 自作メソッドであるextract_float_monthsで、変数deposit_lineに格納された値を浮動小数点に変換して、変数deposit_valへ代入
        key_val = self.extract_float_months(key_line) # 自作メソッドであるextract_float_monthsで、変数key_lineに格納された値を浮動小数点の整数に変換して、変数key_valへ代入
        
        data["deposit"] = deposit_val # 辞書データdepositへ、変数deposit_valの値を代入
        data["key_money"] = key_val # 辞書データkey_moneyへ、変数key_valの値を代入
        
        self.logger.info_log(f"[add_deposit_and_key_money] 取得成功: deposit={deposit_val},key_money={key_val}")
        return data          
# ------------------------------------------------------------------------------
    # 関数定義
    def add_layout_and_area(self,driver, data: dict) -> dict:
        """詳細ページの「間取/専有面積」セルからlayout（間取り）とarea（専有面積）を取得してdataに追加して返す"""
        
        try: # XPATHで該当のhtml要素を検索して、値の結果を変数cellへ代入
            cell = driver.find_element(
                By.XPATH,
                (
                    "//table[@id='detail_pickup']"
                    "//td[contains(@class,'tbl_tit_detail') and contains(.,'間取')]"
                    "/parent::tr"
                    "/following-sibling::tr[1]"
                    "/td[4]"
                )
            )
        
        except Exception as e: # 例外処理の場合、辞書データのlayoutとareaに0.0を代入
            self.logger.error_log(f"[add_layout_and_area] 間取/専有面積セルが見つかりません: {e}")
            data["layout"] = ""
            data["area"] = ""
            return data
            
        raw_text = cell.text.strip() # XPATHで取得した値である文字列から、WebElementプロパティであるtextを用いて、有効な文字列だけを取得し、前後の空白を取り除いて、変数raw_textへ代入
        
        if not raw_text: # 変数raw_textが空文字の場合、辞書データのlayoutとareaに0.0を代入
            self.logger.info_log(f"[add_layout_and_area] 間取/専有面積セルが空のため空文字で保存します")
            data["layout"] = ""
            data["area"] = ""
            return data
            
        lines = raw_text.splitlines() # 変数raw_text内の行で分割した、各行の文字列をリストで取得して、変数linesへ代入
        layout_line = self.clean_text(lines[0]) if len(lines) >= 1 else "" # 変数linesに格納されているリストの個数が1以上の場合、自作メソッドであるclean_textで、変数linesの1番目の値の余分な空白を埋めて、変数layout_lineへ代入、それ以外の場合、空文字を代入
        area_line   = self.clean_text(lines[1]) if len(lines) >= 2 else "" # 変数linesに格納されているリストの個数が2以上の場合、自作メソッドであるclean_textで、変数linesの2番目の値の余分な空白を埋めて、変数area_lineへ代入、それ以外の場合、空文字を代入
        
        data["layout"] = layout_line # 辞書データlayoutへ、変数layout_lineの値を代入
        data["area"]   = area_line # 辞書データareaへ、変数area_lineの値を代入
        
        self.logger.info_log(f"[add_layout_and_area] 取得成功: layout={layout_line}, area={area_line}")
        return data       
# ------------------------------------------------------------------------------
    # 関数定義           
    def extract_list_from_equipment_table(self, table_el:WebElement, label: str) -> list[str]:
        """<table class="equipment">内の<td>から’'・ステムキッチン'のようなテキストをリスト化して返す"""
        
        items: list[str] = [] # 文字列型のリストを格納する変数itemsへ、空のリストを代入
        
        try: # 第一引数で渡されたWebElementのfind_elementsメソッドを呼び出して、渡された値の中の複数のtdタグを探して、変数tdsへ代入
            tds = table_el.find_elements(By.XPATH, ".//td")
            
        except Exception as e: # 例外処理
            self.logger.error_log(f"[extract_list_from_equipment_table] {label}用td取得失敗: {e}")
            return items
        
        for td in tds: # 変数tdsに格納された複数のtdタグを、変数tdへ繰り返し代入して処理
            raw = td.text or "" # WebElementプロパティであるtextを使用して、XPATHで取得したtdタグの文字列を変数rawへ代入、または、何も無い場合は空文字を代入
            text = self.clean_text(raw) # 自作メソッドclean_textを呼び出して、変数rawの文字列の余分な余白を埋めて、変数textへ代入
            
            if not text or text == "-": # 変数textが空文字である場合、または変数textが半角ハイフンと一致した場合、処理を続行
                continue
            
            if text.startswith("・"): # 先頭文字列が引数で指定した文字列と一致した場合にTrueを返すstartswithメソッドを呼び出して、変数textの先頭が「・」であった場合の処理
                text = text.lstrip("・").strip() # 引数で指定した、先頭の文字列を除去するlstripメソッドを呼び出して、変数textの「・」を取り除き、stiripメソッドで前後の空白を取り除き、変数textへ代入
                
            if not text: # 変数textが空文字である場合、処理を続行
                continue
            
            items.append(text) # リストへ要素を追加するappendメソッドを呼び出して、変数textに格納されているtdから取得した文字列を、文字列型のリストを格納するitemsへ代入
            
        self.logger.info_log(f"[extract_list_from_equipment_table] {label} {len(items)}件取得: {items}")
        return items
# ------------------------------------------------------------------------------
    # 関数定義   
    def add_features_and_preferences(self,driver, data: dict) -> dict:
        """詳細ページの「設備」「こだわり内容」テーブルからfeatures/preferencesを取得してdataに追加して返す"""
        
        features: list[str] = [] # 文字列型のリストを格納する変数featuresへ、空のリストを代入
        
        try: # XPATHで該当のhtml要素を検索して、値の結果を変数equip_tableへ代入
            equip_table = driver.find_element(
                By.XPATH,
                (
                    "//td[@class='tbl_tit' and normalize-space()='設備']"
                    "/following-sibling::td[1]"
                    "//table[contains(@class,'equipment')]"
                )
            )
            
            features = self.extract_list_from_equipment_table(equip_table, "features") # 自作メソッドであるtdタグの情報を整理するメソッドを呼び出して、第一引数でXPATHで取得した文字列を渡して整理し、その結果を変数featuresへ代入
            
        except NoSuchElementException: # tdタグ要素が見つからない場合の処理
            self.logger.error_log(f"[add_features_and_preferences] 設備テーブルが見つかりません")
            
        except Exception as e: # 例外処理
            self.logger.error_log(f"[add_features_add_preferences] 設備取得中にエラー: {e}")
            
        
        preferences: list[str] = [] # 文字列型のリストを格納する変数preferencesへ、空のリストを代入
        
        try: # XPATHで該当のhtml要素を検索して、値の結果を変数equip_tableへ代入
            pref_table = driver.find_element(
                By.XPATH,
                (
                    "//td[@class='tbl_tit' and normalize-space()='こだわり内容']"
                    "/following-sibling::td[1]"
                    "//table[contains(@class,'equipment')]"
                )
            )
            
            preferences = self.extract_list_from_equipment_table(pref_table, "preferences") # 自作メソッドであるtdタグの情報を整理するメソッドを呼び出して、第一引数でXPATHで取得した文字列を渡して整理し、その結果を変数preferencesへ代入
            
        except NoSuchElementException: # tdタグ要素が見つからない場合の処理
            self.logger.info_log(f"[add_features_and_preferences] こだわり内容テーブルが見つかりません（空として処理）")
            
        except Exception as e: # 例外処理
            self.logger.error_log(f"[add_features_and_preferences] こだわり内容取得中にエラー: {e}")
            
        data["features"] = features # 変数featuresに格納されたリストを、辞書データのfeaturesへ代入
        data["preferences"] = preferences # 変数preferencesに格納されたリストを、辞書データのpreferencesへ代入
            
        self.logger.info_log(f"[add_features_and_preferences] 取得結果: "f"features={features}, preferences={preferences}")
            
        return data
            
# ------------------------------------------------------------------------------
    # 関数定義  
    def add_exterior_and_layout_images(self, driver, data: dict) -> dict:
        """外観画像URL+間取り画像キャプチャを取得してdataに追加する"""
        
        exterior_url = "" # 変数exterior_urlへ空文字を代入
        
        try:
            exterior_img = driver.find_element(By.CSS_SELECTOR, "#detail_pic ul li img") # detail_picというIDを持つ、要素内にある＜ul＞＜li＞＜img＞と一致するWebElement要素を取得して、変数exterior_imgへ代入
            src = exterior_img.get_attribute("src") or "" # WebElementオプションのgeet_attributeを使用して引数で指定した「src」を、変数exterior_imgに格納されている要素から、指定したオブジェクトから該当する要素である相対URLを、変数srcへ代入、または何も無い場合は、空文字を代入する
            
            if src: # 変数srcがTrueの場合の処理
                exterior_url = self.to_absolute_url(src,driver) # 自作メソッドである相対URLを絶対URLへ変換するto_absolute_urlを使用して、変数exterior_urlへ代入
            
        except Exception as e: # 例外処理
            self.logger.error_log(f"[add_exterior_and_layout_images] 外観画像取得に失敗（空文字として処理）: {e}")
        
        data["exterior_image"] = exterior_url #　格納されたURLを辞書データへ渡す
        
        data = self.capture_layout_image(driver,data) # 自作メソッドである間取画像をPNG保存するメソッドを呼び出して、取得したURLを渡して、画像を保存して返す
        
        self.logger.info_log(
            f"[add_exterior_and_layout_images] 取得結果: "
            f"exterior_image={data['exterior_image']}, "
            f"layout_image_path={data['layout_image_path']}"
        )    
        
        return data                 
# ------------------------------------------------------------------------------
    # 関数定義  
    def capture_layout_image(self,driver, data: dict) -> dict:
        """間取キャンバス（<canvas id="cvsMdrImage">）をPNGで保存し、layout_image_pathとsaved_filesに反映する。失敗時は何も変更せずにそのまま返す。"""
        
        title = data.get("title", "layout") # getメソッドを呼び出して、辞書データ内から引数で指定した、titleキーを取得して、なかった場合はlayoutキーを変数titleに代入

        try:
            wait = WebDriverWait(driver, 10) # 最大10秒間待機
            canvas = wait.until(EC.visibility_of_element_located((By.ID, "cvsMdrImage"))) # cvsMdrImageというID属性要素がページ内に見つかり、かつ画面上に表示するまで、最大10秒待機して、その要素を変数canvasへ代入
            
        except TimeoutException: # 10秒以上経過して、要素が表示されなかった場合の処理
            self.logger.info_log("[capture_layout_image] キャンバスが表示されずタイムアウト: layout_image_pathは空のまま")
            return data
        
        except Exception as e: # 例外処理
            self.logger.error_log(f"[capture_layout_image] キャンバス待機中にエラー: {e}")
            return data

        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", canvas) # WebDriverメソッドのexecute_scriptを呼び出して、第二引数で渡された要素を、第一引数で指定した、第二引数の要素をJavaScriptコードであるscrollIntoViewで、画面上部に移動させる
            
        except Exception as e: # 例外処理
            self.logger.info_log(f"[capture_layout_image] scrollIntoViewでエラー（無視して続行）: {e}")

        base_dir = Path(__file__).resolve().parents[3] # pathlib.Pathオブジェクトのparentsで、現在のファイルディレクトリから4つ上へ、resolveメソッドで絶対パスへ変換したファイルパスを変数base_dirへ代入
        layout_dir = base_dir / "data" / "pickle" / "layout" # 変数base_dirにファイルパスへ、左記のパスを追加して、変数layout_dirへ代入
        layout_dir.mkdir(parents=True, exist_ok=True) # OSモジュールのmkdirメソッドを呼び出して、変数parentsとexist_okへTrueを代入したディレクトリを作成

        today = datetime.now().strftime("%Y%m%d") # 現在の日時を取得し、strftimeメソッドで年月日形式に変換し、変数todayに代入
        safe_title = self.sanitize_title(title) # 自作メソッドで、引数で渡された変数title内の、ファイル名に使用できない文字列を、使用可能に変換し、変数safe_titleへ代入
        filename = f"{safe_title}_{today}.png" # 変数safe_titleとtodayの文字列を.pngで結合して、変数falenameへ代入
        abs_path = layout_dir / filename # 変数layout_dirの文字列へfilenameを/を加えて追加し、変数abs_pathへ代入し絶対パスを作成し代入
        rel_path = Path("installer") / "data" / "pickle" / "layout" / filename # 相対パスを作成して代入

        try:
            canvas.screenshot(str(abs_path)) # webDriverモジュールのscreenshotメソッドを呼び出して、strメソッドで渡された変数abs_pathを文字列に変換し、その引数で渡された要素を探してスクリーンショットをする
            self.logger.info_log(f"[capture_layout_image] 要素スクショで取得: abs={abs_path}, rel={rel_path}")
            
        except Exception as e: # 例外処理
            self.logger.info_log(f"[capture_layout_image] 要素スクショ失敗、toDataURLフォールバックを試行: {e}")
            
            try:
                data_url = driver.execute_script( # 画像データのJavaScriptを取得
                    """
                    const canvas = document.getElementById('cvsMdrImage');
                    if (!canvas) { return null; }
                    try { return canvas.toDataURL('image/png'); }
                    catch(e) { return 'ERROR:' + e.message; }
                    """
                )

                if not data_url or not isinstance(data_url, str): # 変数data_urlが何も無い場合、または指定したオブジェクトが指定したクラスのインスタンスである時にTrueを返す、isinstanceメソッドを呼び出して、変数data_urlが文字列では無かった場合の処理
                    self.logger.info_log("[capture_layout_image] toDataURLがnull / 不正な値を返却")
                    return data

                if data_url.startswith("ERROR:"): # 引数で指定した文字列が、先頭に含まれていた場合Trueを返すメソッドstartswithメソッドを呼び出し、変数deta_urlの先頭が、「ERROR」だった場合の処理
                    self.logger.info_log(f"[capture_layout_image] toDataURLでエラー: {data_url}")
                    return data

                if not data_url.startswith("data:image/png;base64,"): # 変数deta_urlの先頭文字が、data・・・と一致しなかった場合の処理
                    self.logger.info_log(f"[capture_layout_image] 想定外のdataURL形式: {data_url[:50]}...")
                    return data

                base64_data = data_url.split(",", 1)[1] # 変数data_urlの文字列を、分割して取得するsplitメソッドを呼び出して、第一引数で指定した「,」で区切り、1回で分割した値を、リストの1番目から、変数base64_dataへ代入
                png_bytes = base64.b64decode(base64_data) # 文字列やバイナリデータを、ASCII文字に変換された文字列を、もとのバイナリデータに戻すb64decodeメソッド呼び出して、引数で渡されたbase64_dataのASCII文字の値を、変数png_bytesへ代入

                with open(abs_path,"wb") as f: # ファイルを開くopenメソッドを呼び出して、変数abs_pathに格納されているファイルパスを、書き込み用バイナリモードデータで開き、最後にファイルを閉じる
                    f.write(png_bytes) # 変数abs_pathに格納されているファイルパスへ、引数png_bytesで渡されたバイナリデータを、書き込む

                self.logger.info_log(f"[capture_layout_image] toDataURL フォールバックで取得: abs={abs_path}, rel={rel_path}")

            except Exception as e2: # 例外処理
                self.logger.error_log(f"[capture_layout_image] toDataURL フォールバックも失敗: {e2}")
                return data

        data["layout_image_path"] = str(rel_path) # 相対パスが格納されている変数rel_pathを文字列に置換し、辞書データへ代入
        saved = data.get("saved_files", []) # saved_filesというキーの値を取り出して、変数savedへ代入、存在しない場合は空のリストを返す
        saved.append(str(rel_path)) # 間取り画像の相対パスを文字列にして、変数savedのリストへ追加
        data["saved_files"] = saved # 変数savedのリストを辞書データへ追加

        return data
# ------------------------------------------------------------------------------
    # 関数定義
    def add_interior_images_and_comments(self, driver, data: dict) -> dict:
        """スライダー（#detail_pic）から interior_1〜5 を埋め、あわせて comment_b〜d を生成して data に追加する。"""
        try:
            # スライダー内の全画像を取得（メインスライダー優先、無ければサムネイル側）
            img_elements = driver.find_elements(By.CSS_SELECTOR, "#detail_pic ul li img") # detail_picというIDを持つ、要素内にある＜ul＞＜li＞＜img＞と一致するWebElement要素を取得して、変数img_elementへ代入
            
            if not img_elements: # 変数img_elementsが何も無い場合
                img_elements = driver.find_elements(By.CSS_SELECTOR, "#pic_control ul li img") # detail_picというIDを持つ、要素内にある＜ul＞＜li＞＜img＞と一致するWebElement要素を取得して、変数exterior_imgへ代入

            urls: list[str] = [] # 変数urlsへ空のリストを代入

            for el in img_elements: # 変数img_elementsに格納されている要素を繰り返し、変数elへ代入して処理を繰り返す
                src = el.get_attribute("src")or"" # src属性の値を取得して、変数srcへ代入、または空文字を代入
                if not src: # srcが何も無い場合の処理
                    continue
                
                abs_url = self.to_absolute_url(src,driver) # srcから取得した値を自作メソッドのto__absolute_urlで、絶対パスへ変換して、変数abs_urlへ代入
                if abs_url not in urls: # 変数abs_urlに格納されている絶対パスが、変数urlsであるリストの中にない場合の処理
                    urls.append(abs_url) # 変数urlsのリストへ、abs_urlの値を追加
                    
            # まず/room/を含むURLだけを「内観画像」とみなして抽出    
            interior_urls = [u for u in urls if"/room/" in u] # リスト内包表記を用いて、変数uの中に「/room/」がある場合、変数urlsの中にあるリスト内の要素を、変数uに取り出して、変数uを新しいリストとして、変数interior_urlsへ代入
            
            # /room/が一つもない物件では、外観画像URLを除外した残りを内観候補とするフォールバック
            if not interior_urls: # 変数interior_urlsが何も無い場合の処理
                exterior = data.get("exterior_image","") # 辞書データであるdataから、キーであるexterior_imageの値を取得して、変数exeriorへ代入
                interior_urls = [u for u in urls if u != exterior] # リスト内包表記を用いて、変数uとexteriorが一致しない場合、変数urlsの中にあるリスト内の要素を、変数uに取り出して、変数uを新しいリストとして、変数interior_urlsへ代入
            
            # interior_1〜5を埋める    
            for i in range(5): # 変数iに0〜4を代入しながら処理を繰り返す
                key = f"interior_{i+1}" # interior_1〜5という文字列を、変数keyへ代入
                data[key] = interior_urls[i] if i < len(interior_urls) else"" # 変数interior_urlsの現在の数が、変数interior_urlsのリスト数以下の場合、辞書データのキーでkeyへ代入、それ以外は空文字を代入する

            # ログ用まとめ
            summary_items: list[str] = [] # 変数summary_itemsへ、空のリストを代入
            for i in range(5): # 変数iに0〜4を代入しながら処理を繰り返す
                key = f"interior_{i+1}" # interior_1〜5という文字列を、変数keyへ代入
                summary_items.append(f"{key}={data[key]}") # 変数summar_itemsのリストへ、キーと値の文字列ペアを追加
                
            self.logger.info_log(f"[add_interior_images_and_comments] 内観画像取得:"+",".join(summary_items) )
            

        # ---- 簡易コメント生成（ここは既存のまま）----
            layout = data.get("layout", "") # 辞書データのキー、layoutの値を取得して、変数layoutに代入
            area = data.get("area", "") # 辞書データのキー、areaの値を取得して、変数areaに代入
            line = data.get("line", "") # 辞書データのキー、lineの値を取得して、変数lineに代入
            station = data.get("station", "") # 辞書データのキー、stationの値を取得して、変数stationに代入
            walk = data.get("walk", "") # 辞書データのキー、walkの値を取得して、変数walkに代入

            data["comment_b"] = f"{layout}の間取りで、{area}の広さが魅力です。" # 取得した辞書データで合体した文字列を辞書データのcomment_bへ代入
            data["comment_c"] = f"{line}{station}から{walk}の立地で、通勤・通学にも便利です。" # 取得した辞書データで合体した文字列を辞書データのcomment_cへ代入
            data["comment_d"] = "収納や設備も充実しており、快適な暮らしが期待できます。" # 取得した辞書データで合体した文字列を辞書データのcomment_dへ代入

        except Exception as e:
            self.logger.error_log(f"[add_interior_images_and_comments] 内観画像・コメント取得でエラー: {e}")

        return data
# ------------------------------------------------------------------------------
    # 関数定義
    def cleanup_saved_files(self, property_dict: dict) -> None:
        """proprtty_dict［'save_files'］に登録された画像ファイルを削除する"""
        
        saved_files = property_dict.get("saved_files", []) # 辞書データのキーであるsaved_filesの値を取得して、存在しない場合は空リストを、変数saved_filesへ代入
        
        if not saved_files: # 変数saved_filesになにもない場合の処理
            self.logger.info_log(f"[cleanup_saved_files] 削除対象ファイルなし")
            return
        
        for file_path in saved_files: # 変数saved_filesに格納されている値を繰り返し、変数file_pathへ代入
            
            try:
                p = Path(file_path) # 変数file_pathの文字列をPathコンストラクタで、オブジェクト化して削除を簡単に実行できるようにする
                if p.exists(): # 変数pにパスが存在する場合の処理
                    p.unlink() # パスを削除
                    
                    self.logger.info_log(f"[cleanup_saved_files] 削除成功: {file_path}")
                else :
                    self.logger.info_log(f"[cleanup_saved_files] 存在しないためスキップ: {file_path}")
            
            except Exception as e:
                self.logger.error_log(f"[cleanup_saved_files] 削除失敗: {file_path}, error={e}")           
# ------------------------------------------------------------------------------
    # 関数定義           
    
    
#**********************************************************************************

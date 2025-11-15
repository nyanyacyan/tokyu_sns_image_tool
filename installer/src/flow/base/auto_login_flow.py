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
from typing import Optional,Iterable,List,Dict # 「typing」という標準ライブラリのモジュールから、「Optional」、「Iterable」、「List」、「Dict」という型ヒントを取り込む
import json,time,random,re,pickle # 「json」、「time」、「random」、「re」、「pickle」という標準ライブラリのモジュールを取り込む

# 自作モジュールimport
from flow.base.logger import Logger  # logger.pyからLoggerクラスを取り込む
from flow.base.path import get_pickle_file_dir,get_today_pickle_path

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
        return self.find_element(driver,By.XPATH,"//a[contains(@onclick,'window.open')][.//img[@alt='詳細']]")


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
            self.logger.info_log(f"[sanitize_title] 禁止文字を置換: before={repr(original)},after{repr(sanitized)}") # 成功したときのログ
        
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
        d: Dict[str,str] = {} # 変数dへからの辞書を代入する
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
    def save_titles_pickle(self, data: dict | list): # 「｜」はorを意味する
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
    def get_latest_pickle_file(self):
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
    def load_latest_titles_or_empty(self):
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
    def cleanup_old_pickles(self):
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
    
# ------------------------------------------------------------------------------
    # 関数定義
        
# ------------------------------------------------------------------------------
    # 関数定義
    
# ------------------------------------------------------------------------------
    # 関数定義           
#**********************************************************************************

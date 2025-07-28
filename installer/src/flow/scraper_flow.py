from selenium import webdriver # webブラウザの自動操作
from selenium.webdriver.common.by import By # ページ内の要素を指定
from selenium.webdriver.chrome.options import Options # ブラウザの起動オプションを設定
from selenium.webdriver.support.ui import WebDriverWait # ページ内の要素表示や読み込みを待つ
from selenium.webdriver.support import expected_conditions as EC # 「特定の要素が出現したら進める」等の待機条件を使う
from selenium.common.exceptions import TimeoutException # ページ表示や要素出現が時間内に終わらなかった場合のエラー取扱
import json # jsonファイルからデータ読み込み
from pathlib import Path # ファイルパスの操作

def get_login_info():# configファイルからIDとPWとURLを取得
    config_path = Path(__file__).parents[2]/ "config" / "config.json" # 相対パスでjsonファイルパスを指定
    
    # jsonファイルを開いて、各設定値を戻り値として取得
    with open(config_path,encoding="utf-8") as f: 
        config = json.load(f)
        lease_conf = config["TOKYU_JYUTAKU_LEASE"]
    return lease_conf["ID"], lease_conf["PASS"], lease_conf["URL"], lease_conf["LOGINED_URL"]

def open_login_page(): # 自動ログイン
    user_id, user_pass, url, logined_url = get_login_info() # 取得したjsonファイルの値を変数へ代入
    options = Options() # Chromeブラウザの設定をインスタンス化
    options.add_argument("--window-size=1200,800") # ウィンドウサイズを指定
    driver = webdriver.Chrome(options=options) # Chrome自動起動の設定条件を上記内容で渡す

    try:
        driver.get(url) #　指定のURLを開く
        
        if driver.current_url == logined_url:
            print("すでにログイン済であるため、再ログインをスキップ")
            input("画面を確認したらEnterで終了")
            driver.quit()
            return
            
        # 入力欄が現れるまで最大10秒待機して、”txtloginId”というhtml要素を探す判定条件
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID,"txtLoginId"))
        )

        # 各要素を探して、ID/PW自動入力
        driver.find_element(By.ID,"txtLoginId").send_keys(user_id)
        driver.find_element(By.ID,"txtLoginPass").send_keys(user_pass)

        # ログインボタン自動クリック
        driver.find_element(By.CSS_SELECTOR,"#login-btn a").click()

        # ログイン後の判定条件
        try:
            # ログイン後のURLへ変化するまで最大10秒待機して、ログイン後のURLと一致するか判定する
            WebDriverWait(driver, 10).until(lambda d: d.current_url != url)
            if driver.current_url == logined_url:
                print("ログイン成功！")
            else:
                print("ログイン失敗 or 予期せぬ画面です")
                print("現在のURL:", driver.current_url)
        except TimeoutException:
            print("ログイン後の画面遷移がタイムアウトしました（URLが変わりませんでした）")
            print("現在のURL:", driver.current_url)

    except Exception as e:
        print("想定外のエラーが発生:", e)
    finally:
        input("画面を確認したらEnterで終了…")
        driver.quit()



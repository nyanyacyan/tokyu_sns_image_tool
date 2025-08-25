# installer/src/flow/scraper_flow.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import time, random
from pathlib import Path

# 既存の Chrome 起動ユーティリティ
from flow.base.chrome import Chrome


# =========================
# 設定の読み込み（ID / PASS / ログインURL / ログイン後URL）
# =========================
def load_login_config():
    """config.json からログイン情報とURLを取得"""
    cfg_path = Path(__file__).parents[2] / "config" / "config.json"
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)["TOKYU_JYUTAKU_LEASE"]
    return cfg["ID"], cfg["PASS"], cfg["URL"], cfg["LOGINED_URL"]


# =========================
# ユーティリティ
# =========================
def wait_for_random_time(min_sec=1, max_sec=3):
    """人間らしさのためにランダムスリープ"""
    time.sleep(random.uniform(min_sec, max_sec))

def scroll_element_to_center(driver, el):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

def wait_for_page_ready(driver, timeout=20):
    """document.readyState == 'complete' になるまで待機"""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    wait_for_random_time()


# =========================
# ログイン関連
# =========================
def check_login_status(driver: webdriver.Chrome, loggedin_url: str) -> bool:
    """現在URLがログイン後URLと一致しているか確認"""
    return driver.current_url == loggedin_url

def perform_login(driver: webdriver.Chrome, user_id: str, user_pass: str,
                  login_url: str, loggedin_url: str) -> None:
    """ログイン処理を実行"""
    if check_login_status(driver, loggedin_url):
        print("（スキップ）すでにログイン済み")
        return

    driver.get(login_url)
    wait_for_random_time()

    # 入力欄が出るまで待機
    try:
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.ID, "txtLoginId"))
        )
        wait_for_random_time()
    except TimeoutException:
        raise RuntimeError("ログインページの読み込みが遅い/ID欄が見つかりません")

    # ID / PASS 入力
    id_el = driver.find_element(By.ID, "txtLoginId")
    pw_el = driver.find_element(By.ID, "txtLoginPass")
    id_el.clear(); id_el.send_keys(user_id)
    wait_for_random_time()
    pw_el.clear(); pw_el.send_keys(user_pass)
    wait_for_random_time()

    # 「次回入力省略」チェック（jqTransform の見た目UIをクリック）
    try:
        ui = driver.find_element(
            By.CSS_SELECTOR, ".jqTransformCheckboxWrapper a.jqTransformCheckbox"
        )
        if "jqTransformChecked" not in ui.get_attribute("class"):
            ui.click()
            wait_for_random_time()
    except Exception:
        # 無くても続行
        pass

    # ログインボタン押下（クリック可能を待つ）
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-btn a"))
    )
    wait_for_random_time()
    driver.find_element(By.CSS_SELECTOR, "#login-btn a").click()

    # URL変化待ち
    try:
        WebDriverWait(driver, 12).until(lambda d: d.current_url != login_url)
        wait_for_random_time()
    except TimeoutException:
        raise RuntimeError("ログイン後の画面遷移がタイムアウトしました")

    if check_login_status(driver, loggedin_url):
        print("ログイン成功")
    else:
        print("ログイン後URLが想定と異なります。現在URL:", driver.current_url)

def login_if_needed(driver: webdriver.Chrome, user_id: str, user_pass: str,
                    login_url: str, loggedin_url: str) -> None:
    """ログイン状態を確認し、切れていたらログインする"""
    if not check_login_status(driver, loggedin_url):
        perform_login(driver, user_id, user_pass, login_url, loggedin_url)


# =========================
# クリック可能要素の探索（CSS/XPath対応 & iframe対応）
# =========================
def wait_for_clickable_element(driver, locators, timeout=12):
    """
    locators: [("css", "span.searchdtlara img"), ("xpath", "//span[contains(@class,'searchdtlara')]//img"), ...]
    のような (by_kind, query) のリスト。順に試してクリック可能まで待つ。
    """
    last_err = None
    for by_kind, query in locators:
        by = By.CSS_SELECTOR if by_kind.lower() == "css" else By.XPATH
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, query))
            )
            wait_for_random_time()
            return el, (by_kind, query)
        except Exception as e:
            last_err = e
    raise TimeoutException(f"どのロケータでもクリック可能になりませんでした: {locators}") from last_err

def search_element_in_iframes(driver, locators, timeout=12):
    """親 → すべての iframe を順に探索（CSS/XPath対応）"""
    driver.switch_to.default_content()
    try:
        el, matched = wait_for_clickable_element(driver, locators, timeout=4)
        return el, matched, None
    except TimeoutException:
        pass

    frames = driver.find_elements(By.CSS_SELECTOR, "iframe, frame")
    for idx, fr in enumerate(frames):
        try:
            driver.switch_to.frame(fr)
            el, matched = wait_for_clickable_element(driver, locators, timeout=4)
            return el, matched, idx
        except Exception:
            driver.switch_to.default_content()
            continue

    driver.switch_to.default_content()
    raise TimeoutException("親/全iframe内で検索ボタンを見つけられませんでした。")


# =========================
# チェックボックス操作
# =========================
def _set_checkbox_all_area(driver: webdriver.Chrome, checked: bool) -> None:
    """「全エリア選択」チェックを設定"""
    WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.area_route_check"))
    )
    wait_for_random_time()

    ui_sel = "li.area_route_check span.clsAllCheck .jqTransformCheckboxWrapper a.jqTransformCheckbox"
    ui = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ui_sel)))
    scroll_element_to_center(driver, ui)
    wait_for_random_time()

    is_on = "jqTransformChecked" in ui.get_attribute("class")
    if is_on != checked:
        ui.click()
        wait_for_random_time()
        WebDriverWait(driver, 6).until(
            lambda d: ("jqTransformChecked" in ui.get_attribute("class")) == checked
        )
        wait_for_random_time()

def _set_checkbox_republish_allowed(driver: webdriver.Chrome, checked: bool) -> None:
    """「転載可」チェックを設定（input#chkKoukoku2 を直接操作）"""
    el = WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#chkKoukoku2"))
    )
    wait_for_random_time()
    scroll_element_to_center(driver, el)
    wait_for_random_time()

    result = driver.execute_script("""
        const el = arguments[0], want = arguments[1];
        el.removeAttribute('disabled');
        el.checked = !!want;
        el.dispatchEvent(new Event('change', {bubbles:true}));
        return el.checked === !!want;
    """, el, checked)

    if result is not True:
        raise RuntimeError("『転載可』のチェック状態が反映されませんでした。")


# =========================
# 検索処理
# =========================
def click_search_button_and_wait_results(driver):
    """検索ボタンをクリックして、結果一覧が表示されるまで待機"""
    SEARCH_BTN_LOCATORS = [
        ("css", "span.searchdtlara img[style*='cursor']"),
        ("css", "span.searchdtlara img"),
        ("xpath", "//span[contains(@class,'searchdtlara')]//img"),
        # 既存の候補も残しておく（画面のバリエーションに備える）
        ("css", "#btnSearch a"),
        ("css", "a#btnSearch"),
        ("css", ".btn-search a"),
    ]
    RESULTS_SELECTORS = ["#result-list", ".result-table", "#searchResult"]

    wait_for_page_ready(driver, timeout=20)

    # ボタン探索（親→iframe）
    try:
        btn, matched, iframe_idx = search_element_in_iframes(driver, SEARCH_BTN_LOCATORS, timeout=12)
    except TimeoutException:
        print("[DEBUG] current_url:", driver.current_url)
        print("[DEBUG] title:", driver.title)
        raise

    # クリック（通常→JSの順でフォールバック）
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        wait_for_random_time()
        btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", btn)

    print("検索ボタンをクリック（locator: %s %s, iframe: %s）" % (matched[0], matched[1], iframe_idx))

    # 結果待機（いずれかのルートが出現）
    for sel in RESULTS_SELECTORS:
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, sel))
            )
            wait_for_random_time()
            print("検索結果の一覧を確認（selector: %s）" % sel)
            return
        except TimeoutException:
            continue

    print("検索結果の根要素が見つかりませんでした: %s" % RESULTS_SELECTORS)
    raise TimeoutException(f"検索結果の根要素が見つかりませんでした: {RESULTS_SELECTORS}")


def apply_search_filters_and_execute(driver: webdriver.Chrome) -> None:
    """フィルターを設定して検索を実行"""
    # 事前に OFF でリセット
    _set_checkbox_all_area(driver, checked=False)
    _set_checkbox_republish_allowed(driver, checked=False)

    # 希望通り ON にする
    _set_checkbox_all_area(driver, checked=True)
    _set_checkbox_republish_allowed(driver, checked=True)

    # 検索 → 結果待機
    click_search_button_and_wait_results(driver)


# =========================
# メイン実行フロー
# =========================
def run_property_search_flow():
    """
    全体フロー：
      1) Chrome起動
      2) ログイン状態確認 → 必要ならログイン
      3) 「全エリア選択」「転載可」をチェック
      4) 検索ボタン押下 → 結果一覧の表示を待機
    """
    user_id, user_pass, login_url, loggedin_url = load_login_config()
    driver = Chrome.get_driver(login_url)   # 既存のユーティリティ仕様に合わせる（URL必須なら渡す）

    try:
        login_if_needed(driver, user_id, user_pass, login_url, loggedin_url)
        apply_search_filters_and_execute(driver)
    except Exception as e:
        print("想定外エラー:", e)
        raise
    finally:
        driver.quit()
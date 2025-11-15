# 標準モジュールimport
from pathlib import Path # pathlibという標準ライブラリを使って、パスを作成
from datetime import datetime # 標準ライブラリのdatetimeモジュールのdateimeモジュール

# 自作モジュールimport
from flow.base.logger import Logger

logger = Logger()


# ------------------------------------------------------------------------------
    # 関数定義
def get_log_dir():
    """
    ログを保存するディレクトリのパスを返す関数
    ディレクトリがなければ自動作成
    """
    log_dir = Path(__file__).parents[3] / "data" / "output" / "logs" # 相対ファイルを作成
    log_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    return log_dir
# ------------------------------------------------------------------------------
    # 関数定義
def get_pickle_file_dir():
    """
    pickleファイルの保存場所のパスを返す関数
    ディレクトリがなければ自動作成
    """
    pickle_dir = Path(__file__).parents[3] / "data" / "pickle" # 相対ファイルを作成
    pickle_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    logger.info_log(f"[get_pickle_dir] ディレクトリ確認済: {pickle_dir}")
    #pickle_file = pickle_dir / "data.pkl" # 保存するファイル名
    return pickle_dir 

# ------------------------------------------------------------------------------
    # 関数定義   
def get_template_dir():
    """
    テンプレ画像（A.png, B.pngなど）が保存されているディレクトリのパスを返す関数
    ディレクトリがなければ自動作成
    """
    template_dir = Path(__file__).parents[3] / "data" / "input" / "template" # 相対ファイルを作成
    template_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    return template_dir
# ------------------------------------------------------------------------------
    # 関数定義
def get_output_image_dir():
    """
    作成した画像（テンプレA〜Dの出力物）を保存するディレクトリのパスを返す関数
    ディレクトリがなければ自動作成
    """
    image_dir = Path(__file__).parents[3] / "data" / "output" / "images" # 相対ファイルを作成
    image_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    return image_dir
# ------------------------------------------------------------------------------
    # 関数定義
def get_font_dir():
    """
    フォントファイルを保存しておくディレクトリのパスを返す（なければ作成）
    例：installer/data/input/fonts/
    """
    font_dir = Path(__file__).parents[3] / "data" / "input" / "fonts" # 相対ファイルを作成
    font_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    return font_dir
# ------------------------------------------------------------------------------
    # 関数定義
def get_today_pickle_path():
    """今日の日付を使ったpickleファイルのパスを返す"""
    today_str = datetime.now().strftime("%Y%m%d") # 現在日時を取得するdatetime.nowメソッドで、現在日時を取得し、strftimeメソッドで「西暦・月・日」の表示へ変換させ、変数today_strへ代入
    pickle_dir = get_pickle_file_dir() # ログを保存するディレクトリのパスを返して、ディレクトリがなければ自動作成する関数を呼び出し
    pickle_file = pickle_dir / f"{today_str}.pkl" # 変数pickle_dirに格納されているファイルパスの後に、変数pickle_dirに格納されている日付を組み合わせ、拡張子を.pklとして、変数pickl_fileへ代入
    logger.info_log(f"[get_today_pickle_path] 生成: {pickle_file}") # 日付が入ったpklファイル作成が成功したときのログ
    return pickle_file
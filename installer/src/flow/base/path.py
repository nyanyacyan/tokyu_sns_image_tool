# pathlibという標準ライブラリを使って、パスを作成
from pathlib import Path

def get_log_dir():
    """
    ログを保存するディレクトリのパスを返す関数
    ディレクトリがなければ自動作成
    """
    log_dir = Path(__file__).parent.parent.parent.parent / "data" / "output" / "logs" # 相対ファイルを作成
    log_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    return log_dir

def get_pickle_file_dir():
    """
    pickleファイルの保存場所のパスを返す関数
    ディレクトリがなければ自動作成
    """
    pickle_dir = Path(__file__).parent.parent.parent.parent / "data" / "pickle" # 相対ファイルを作成
    pickle_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    pickle_file = pickle_dir / "data.pkl" # 保存するファイル名
    return pickle_file 
    
def get_template_dir():
    """
    テンプレ画像（A.png, B.pngなど）が保存されているディレクトリのパスを返す関数
    ディレクトリがなければ自動作成
    """
    template_dir = Path(__file__).parent.parent.parent.parent / "data" / "input" / "template" # 相対ファイルを作成
    template_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    return template_dir

def get_output_image_dir():
    """
    作成した画像（テンプレA〜Dの出力物）を保存するディレクトリのパスを返す関数
    ディレクトリがなければ自動作成
    """
    image_dir = Path(__file__).parent.parent.parent.parent / "data" / "output" / "images" # 相対ファイルを作成
    image_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    return image_dir

def get_font_dir():
    """
    フォントファイルを保存しておくディレクトリのパスを返す（なければ作成）
    例：installer/data/input/fonts/
    """
    font_dir = Path(__file__).parent.parent.parent.parent / "data" / "input" / "fonts" # 相対ファイルを作成
    font_dir.mkdir(parents=True, exist_ok=True) # ディレクトリが無い場合に自動で作成
    return font_dir

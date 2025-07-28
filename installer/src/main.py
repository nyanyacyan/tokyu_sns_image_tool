# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# main.py
# import
from flow.base.chrome import Chrome
from flow.base.path import get_log_dir
from flow.base.path import get_pickle_file_dir
from flow.base.path import get_template_dir
from flow.base.path import get_output_image_dir
from flow.scraper_flow import get_login_info
from flow.scraper_flow import open_login_page


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# **********************************************************************************
# class定義


# ------------------------------------------------------------------------------
# 関数定義
#def main():
    #url = "https://www.google.com"  # 必ず開きたいURLを指定
    #driver = Chrome.get_driver(url)
    #driver.get(url)
    #input("Chromeブラウザが指定URLで起動していればEnterを押してください…")
    #driver.quit()

def main():
    #log_dir = get_log_dir()
    #pickle_dir = get_pickle_file_dir()
    #template_dir = get_template_dir()
    #image_dir = get_output_image_dir()
    #print("ログディレクトリ：",log_dir)
    #print("ピクルファイルのパス:",pickle_dir)
    #print("テンプレ画像ディレクトリ:",template_dir)
    #print("出力した画像のパス:",image_dir)
    login_info = get_login_info()
    open_login = open_login_page()
    

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()


# ------------------------------------------------------------------------------

# **********************************************************************************

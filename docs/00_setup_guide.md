# 00_setup_guide.md
## セットアップ手順（開発者向け）

このドキュメントは、新しくプロジェクトに参加する開発者が環境構築をスムーズに進めるための手順書です。

<br>


## 前提条件

- OS: macOS / Windows / Linux
- Git / GitHub アカウントが設定済み
- Python 3.10.7 インストール済み
- 任意（仮想環境を使う場合）: `venv` または `pyenv`
- 任意（GUI操作用）: SourceTreeインストール済み


<br>



## 推奨エディタ：Visual Studio Code（VS Code）

- Python拡張機能（`ms-python.python`）をインストールしてください。
- `.vscode/launch.json` が含まれている場合、デバッグ設定も自動で有効になります。


<br>


## セットアップ手順

### １．**対象のリポジトリをクローンする**

#### 🔹 クローン手順（SourceTree）
```bash
1. SourceTreeを起動

2. 上部メニューの「リモート」タブをクリック

3. 表示されたリストから、対象のGitHubリポジトリを探す

4. クローンしたいリポジトリの横にある「クローン」ボタンをクリック

5. 「クローン先のフォルダ（保存場所）」を選択
  ※ 例：`~/Projects/your-repo`

6. 「クローン」ボタンを押して完了！
```
---

### ⚠️ 注意

- **対象のリポジトリが表示されない場合**は、以下を確認してください：
    - GitHubアカウントとの連携が正しくできているか
    - リポジトリが**プライベート**の場合、アクセス権があるか

- 上記を確認しても表示されない場合は、**PM（プロジェクト管理者）に確認**してください。

    ※リポジトリのURLを直接もらうことで、手動でのクローンも可能です。



<br>

---


### 2. **Pythonのバージョンを確認する**
Python 3.10.7 であることを確認してください。
``` python
python --version

# もしくは
python3 --version
```
「Python 3.10.7」の出力があることを確認



<br>

---

### 3. 仮想環境を作成・有効化する（推奨）
他のライブラリなどに依存しないため仮想環境を構築
```bash
python -m venv .venv
source .venv/bin/activate  # Windows の場合は .venv\Scripts\activate
```
- .venv という名前で統一します（VSCodeで自動認識されやすいため）
- ターミナル上の部分に(venv)と頭についているのかを確認
※(venv) が表示されていない場合は、仮想環境がまだ有効化されていません。

<br>


---

### **4. インタープリタ確認**
プロジェクト内で仮想環境（.venv）を正しく使うために、VSCodeで**Pythonの実行環境（インタープリタ）**が `.venv` に設定されているかを確認してください。

#### 手順

1. VSCodeでプロジェクトフォルダを開く

2. 画面右下に表示されている Python のバージョン表示
（例：`Python 3.10.7 64-bit`）をクリック

3. インタープリタ選択画面が表示されるので、一覧の中から `.venv` がついている項目を選択（例：`.venv/bin/python`）

4. 再度右下を確認し、 `.venv` が表示されていればOK

#### 補足

- `.venv` を選ばず、システムPython（例：`/usr/bin/python3`）になっていると、仮想環境が使われません。
- 表示されない場合は、仮想環境が作成されていない、または VSCode が再起動を必要としている可能性があります。

<br>


---

### 5. **依存ライブラリのインストール**

```bash
pip install -r requirements.txt
```

※ installer/requirements.txt 等、サブディレクトリにある場合もあります。

ライブラリがしっかり反映しているのかを確認
```bash
pip list
```


<br>





## ✅ 実行前チェックリスト

- [ ] Githubのcloneよりファイルを生成している
- [ ] 仮想環境を有効化している
- [ ] 依存ライブラリをrequirements.txtよりインストール済み
- [ ] APIキーなどの設定済み
- [ ] 入力ファイル（例：`data/input/*.csv`）が存在している



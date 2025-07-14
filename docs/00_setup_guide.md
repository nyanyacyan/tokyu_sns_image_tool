# 00_setup_guide.md
## セットアップ手順（開発者向け）

このドキュメントは、新しくプロジェクトに参加する開発者が環境構築をスムーズに進めるための手順書です。

---

## 前提条件

- OS: macOS / Windows / Linux
- Git / GitHub アカウントが設定済み
- Python 3.10.7 インストール済み
- 任意（仮想環境を使う場合）: `venv` または `pyenv`
- 任意（GUI操作用）: SourceTreeインストール済み

---

## 推奨エディタ：Visual Studio Code（VS Code）

- Python拡張機能（`ms-python.python`）をインストールしてください。
- `.vscode/launch.json` が含まれている場合、デバッグ設定も自動で有効になります。

---

## デバッグ方法（ステップ実行）

ステップデバッグにより、変数の中身や処理の流れを追いながらバグを特定できます。
ブレークポイントを設定して、対象の範囲などを絞りながら確認してください。

### 手順（VS Code）

1. `main.py` または任意の `.py` ファイルを開く
2. ブレークポイントをクリックで設置（左端の赤丸）
3. 左側の「実行とデバッグ」アイコン ▶ を選択
4. 「Python ファイル」を選択し `F5` で実行
5. 変数の中身や呼び出しスタックを確認しながらステップ実行
    - `F10`：次のステップへ進む
    - `F11`：関数内へステップイン

---

## Codeセットアップ手順

1. **このリポジトリをクローンする**

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
```

またはSourceTree の「クローン」機能を使用して取得してください。


### 2. 仮想環境を作成・有効化する（推奨）

```bash
python -m venv .venv
source .venv/bin/activate  # Windows の場合は .venv\Scripts\activate
```


### 3. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

※ installer/requirements.txt 等、サブディレクトリにある場合もあります。詳細は requirements_notes.md を参照してください。




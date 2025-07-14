# 02_requirements_notes.md
## Python依存ライブラリ管理に関する補足

このドキュメントでは、当プロジェクトで使用する Python ライブラリの管理方法と、複数の `requirements.txt` の役割について説明します。

---

## 📦 ライブラリインストールの基本

通常は以下のコマンドで依存関係を一括でインストールできます。

```bash
pip install -r requirements.txt
```

---

## 複数の requirements.txt の構成

当プロジェクトでは、用途に応じて2つの requirements.txt を管理しています。

- requirements.txt :
開発者・利用者共通で必要な最低限のライブラリを記載

- installer/requirements.txt :
クライアントへの納品用に使用

---

## インストール手順の例（両方対応）

### 仮想環境を有効化
```bash
source .venv/bin/activate  # Windowsの場合は .venv\Scripts\activate
```

### 依存ライブラリをインストール
```bash
pip install -r requirements.txt #または pip install -r installer/requirements.txt
```

---

## ライブラリ追加時のルール
- 必要最低限のライブラリのみ記載してください。

---

## 補足：VS Code の自動補完が効かない場合
- .vscode/settings.json にて python.pythonPath が仮想環境を指しているか

---

## pip install 時にエラーが出る場合の対処
- Could not find a version that satisfies the requirement
pipのバージョンを更新する pip install --upgrade pip

- PermissionError
仮想環境を使っていない可能性。venvを作成してください。

- ssl.SSLError や proxy 系エラー
社内ネットワーク制限の可能性あり。プロキシ設定を確認してください。

---

## 補足：requirementsファイルの場所
```text
project_root/
├── requirements.txt                # 共通ライブラリ
├── installer/
│   └── requirements.txt           # 実行系専用ライブラリ
```

---


## 補足：パッケージの更新や追加が発生した場合

```bash
# 変更内容を freeze で確認（仮想環境内で実施）
pip freeze > requirements.txt
# installerディレクトリ内も同様に
cd installer
pip freeze > requirements.txt
```



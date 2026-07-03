# Regression Result Visualizer

[![CI](https://github.com/kiyomoto0801/Regression-Result-Visualizer/actions/workflows/ci.yml/badge.svg)](https://github.com/kiyomoto0801/Regression-Result-Visualizer/actions/workflows/ci.yml)

Regression Result Visualizerは、CSVまたはExcel形式の回帰分析結果から、見やすい回帰結果表と係数プロットを自動作成するPythonツールです。

論文、レポート、研究発表、プレゼンテーションで使用する図表を、簡単なコマンドでPNG・PDF形式に出力できます。

## 主な機能

- CSV・Excelファイルの読み込み
- 回帰係数への有意性記号の自動付与
- 回帰結果表の画像作成
- 95％信頼区間付き係数プロットの作成
- PNG・PDF形式での出力
- 小数点以下の桁数の変更
- 表とグラフのタイトル変更
- 入力データの列や数値の自動検証

有意性記号は、次の基準で付与されます。

| 記号 | p値 |
|---|---:|
| `***` | 0.01未満 |
| `**` | 0.05未満 |
| `*` | 0.10未満 |

## 必要な環境

- Python 3.10以上
- pip

## インストール方法

リポジトリを取得します。

```bash
git clone https://github.com/kiyomoto0801/Regression-Result-Visualizer.git
cd Regression-Result-Visualizer
```

パッケージをインストールします。

```bash
pip install -e .
```

テストやコード品質チェックも実行する場合は、開発用の依存関係を含めてインストールします。

```bash
pip install -e ".[dev]"
```

## 入力データ

入力ファイルには、次の4列が必要です。

| 列名 | 内容 |
|---|---|
| `variable` | 変数名 |
| `coefficient` | 回帰係数 |
| `std_error` | 標準誤差 |
| `p_value` | p値 |

CSVファイルの例です。

```csv
variable,coefficient,std_error,p_value
L.credit,0.669,0.108,0.000
Health,-3.881,4.219,0.360
Remittance,-0.120,0.055,0.041
Health x Remittance,0.085,0.032,0.009
Income,0.421,0.180,0.027
```

サンプルファイルは、次の場所にあります。

```text
examples/sample_results.csv
```

## 最も簡単な使い方

次のコマンドを実行します。

```bash
rrv examples/sample_results.csv
```

実行後、`outputs`フォルダに次の4ファイルが作成されます。

```text
outputs/
├── regression_table.png
├── regression_table.pdf
├── coefficient_plot.png
└── coefficient_plot.pdf
```

## オプション

### 出力先を変更する

```bash
rrv examples/sample_results.csv --outdir results
```

### PNGだけを作成する

```bash
rrv examples/sample_results.csv --format png
```

### PDFだけを作成する

```bash
rrv examples/sample_results.csv --format pdf
```

### 小数点以下の桁数を変更する

```bash
rrv examples/sample_results.csv --digits 2
```

### タイトルを変更する

```bash
rrv examples/sample_results.csv \
  --table-title "Health and Financial Development" \
  --plot-title "Estimated Coefficients"
```

### 使用できるオプションを確認する

```bash
rrv --help
```

## Excelファイルの使用

CSVだけでなく、`.xlsx`形式のExcelファイルも使用できます。

```bash
rrv regression_results.xlsx
```

Excelファイルにも、CSVと同じ4列が必要です。

```text
variable
coefficient
std_error
p_value
```

## 開発環境の設定

開発用の依存関係をインストールします。

```bash
pip install -e ".[dev]"
```

プロジェクトの主な構成は次のとおりです。

```text
Regression-Result-Visualizer/
├── examples/
│   └── sample_results.csv
├── src/
│   └── regression_result_visualizer/
│       ├── __init__.py
│       ├── cli.py
│       ├── formatter.py
│       └── plotter.py
├── tests/
│   ├── test_formatter.py
│   └── test_plotter.py
├── pyproject.toml
└── README.md
```

## テスト

すべての単体テストを実行します。

```bash
pytest -v
```

コード品質を確認します。

```bash
ruff check src tests
```

GitHub Actionsでも、pushおよびpull requestのたびにテストとコード品質チェックが自動実行されます。

## ライセンス

このソフトウェアはMIT Licenseのもとで公開されています。
# 初回設定
- anacondaをinstallしてcondaコマンドを使えるように
- conda環境を読み込む
```bash
$ conda env create –-file condaenv.yaml --name homfa-converter
```
- activate
```bash
$ conda activate homfa-converter
```

## 実行例
- 通常
```bash
$ python3 -m converter "p & F(\!p & Fp)" 
```

- reverse
```bash
$  python3 -m converter "p & F(\!p & Fp)" reverse 
```

- Testの実行
```bash
$ python3 -m unittest
```

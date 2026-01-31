# ComfyUI テキストファイルローダー（カスタムノード）
[English](./README.md) / [日本語](./README-ja.md)

ComfyUI の input / output ディレクトリ内にあるテキスト系ファイルをスキャンし、ドロップダウンから1つ選んで、その内容を STRING として返す ComfyUI カスタムノードです。

## 想定ユースケース
* プロンプトや設定を外部ファイルとして管理し、ワークフローに読み込む 
* 複数のテキスト断片（プロンプトのバリエーション、JSON、YAML、メモなど）を素早く切り替える 

## 特長
* input / output の両ディレクトリを再帰的にスキャンし、対象ファイルを検索 
* 対応拡張子: .txt, .md, .json, .yaml, .yml 

## ノード詳細
* 表示名: Text File Loader 
* クラス名: TextFileLoader 
* カテゴリ: utils 
* 出力: STRING（ファイル内容） 

## インストール手順
1. ComfyUI をインストールします。
2. このリポジトリを ComfyUI の custom_nodes ディレクトリにクローンします。

```
git clone https://github.com/utsunolon/comfyui-text-file-loader
```

3. ComfyUI を再起動します。

## 使い方
1. ComfyUI/input または ComfyUI/output 配下にテキストファイルを置きます（例）。
   * ComfyUI/input/prompts/base.txt 
   * ComfyUI/output/notes/run.md 
2. Text File Loader ノードで、ドロップダウンから対象ファイルを選択します。
3. STRING 出力を、テキスト入力を受け付ける任意のノードに接続します。

## ライセンス
Apache License 2.0（LICENSE を参照）

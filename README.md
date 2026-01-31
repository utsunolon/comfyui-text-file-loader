# ComfyUI Text File Loader (Custom Node)

[English](./README.md) / [日本語](./README-ja.md)

A ComfyUI custom node that scans text-like files inside ComfyUI’s input and output directories, lets you pick one from a dropdown, and returns its contents as a STRING.

## Use cases
- Keep prompts/configs as external files and load them into workflows
- Quickly switch between multiple text snippets (prompt variants, JSON, YAML, notes)

## Features
- Recursively scans both input and output directories for eligible files
- Supported extensions: .txt, .md, .json, .yaml, .yml

## Node details
- Display name: Text File Loader
- Class name: TextFileLoader
- Category: utils
- Output: STRING (file content)

## Installation
1. Install ComfyUI.
2. Clone this repository into your ComfyUI custom_nodes directory:

```
git clone https://github.com/utsunolon/comfyui-text-file-loader
```

3. Restart ComfyUI.


## How to use
1. Place a text file under ComfyUI/input or ComfyUI/output, for example:
   - ComfyUI/input/prompts/base.txt
   - ComfyUI/output/notes/run.md

2. In the Text File Loader node, select the file from the dropdown.
3. Connect the STRING output into any node that accepts text input.


## License
Apache License 2.0 (see LICENSE)

<h1 align="center"><b>Document Information Extraction</b></h1>

## Table of Contents
- [Quick Start](#quick-start)
- [Introduction](#introduction)
- [Usage](#usage)
    - [Clone the Github Repo](#clone-the-github-repo)
    - [Install requirements](#install-requirements)
    - [Run Gradio](#run-gradio-app)
- [References](#references)



## Quick Start
### Video Demo
<p align="center"> 
  <img src="demo/demo.gif" alt="Sample signal" width="70%" height="10%">
</p>

## Introduction

## Usage
### Clone the Github Repo
```bash
git clone https://github.com/TaiQuach123/DocumentImageInformationExtraction.git
```
### Install requirements
```bash
pip install requirements.txt
```
### Run Gradio
It will take a while for the OCR model (Surya) to load. In the Gradio Demo App, you will have 3 options to choose:

``Use OCR``: Whether to use Surya OCR or not. The result from Surya OCR will be used. In order to use the 2 options below, you need to tick this.

``Visualize``: Whether to visualize the result (draw bounding boxes) or not. 


``Use LATIN Prompt``: Whether to use LATIN Prompt technique or not.


```bash
python app.py
```
## References

[1] https://github.com/WenjinW/LATIN-Prompt

[2] https://github.com/VikParuchuri/surya


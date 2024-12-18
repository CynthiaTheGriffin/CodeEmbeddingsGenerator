# Topological Data Analysis on Source Code Embeddings

## Introduction

This repository includes code that retrieves Java code from GitHub repositories, then data engineers the code into numerical representations of the code, or code embeddings. GitHubFileGetter.py obtains the download URLs of files in a specified repository (or subdirectory in the repository), and CodeEmbeddingsGenerator.py generates a new directory with the code embedding representations. RunAll.py simplifies the use of each file into two Python functions, which can be run with a single line of code. 

The result should create a new "data" folder containing the code embeddings. This new folder would be structured similarly to the original GitHub repository, with embeddings stored in folders named after the Java files from which they're derived.

This is intended to facilitate topological data analysis by automating the process of data engineering code embeddings of a selected GitHub repository through a seemless process.


## Setup

### Install Packages

Go into your terminal and run the following commands:

```
pip install torch
```
```
pip install tree-sitter-java
```
```
pip install tree-sitter
```

### Get UniXcoder

Download unixcoder.py from its [official site](https://github.com/microsoft/CodeBERT/tree/master/UniXcoder), then move it into the same directory as CodeEmbeddingsGenerator.py.


### Get GitHub Access Token

The provided code requires a GitHub access token to function. To obtain one, create a GitHub account, then follow the [official guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) to generate a fine-grained personal access token.


## Instructions

1. Complete the setup described above, and have your access token ready.

2. Generate code embeddings at the GitHub repository of your choice. 
- Please refer to the [RunAll.ipynb](RunAll.ipynb) notebook to run the code. 
- We have included our [downloads.json](https://github.com/CynthiaTheGriffin/CodeEmbeddingsGenerator/blob/main/download_urls.json) and [sample dataset](https://github.com/CynthiaTheGriffin/CodeEmbeddingsGenerator/tree/main/data/src/java/org/apache/ivy/tools/analyser), which should both match with the result of running the code in the notebook.

3. Perform topological data analysis using the newly generated code embeddings in the data folder. This is where the rest of the magic happens! However, explaining this step is far beyond the scope of this repository, but we have found some helpful links for any newcomers who want to have a go:
- Tutorial by Katherine Benjamin: [https://www.youtube.com/watch?v=8qXOdF1_nm8](https://www.youtube.com/watch?v=8qXOdF1_nm8)
- Tutorial by Elizabeth Munch: [https://www.youtube.com/watch?v=SbsvM4Gcbl0](https://www.youtube.com/watch?v=SbsvM4Gcbl0)


## Documentation

### RunAll.py

```get_download_urls(token:str, user:str, repo:str, sub_dir:str)```

Gets the download URLs of all Java files in the specified GitHub repository. Performs functions in GitHubFileGetter.py, and creates download_urls.json.

Arguments:
- user: Owner of target repository
- repo: Repository name
- sub_dir: Target subdirectory from within repository
- token: GitHub access token

```generate_embeddings(sub_dir:str)```

Generate code embeddings for all Java files given by the download URLs. Performs functions in CodeEmbeddingsGenerator.py, and creates a new "data" folder containing the code embeddings.

Argument:
- sub_dir: Target subdirectory from within the repository


### GitHubFileGetter.py

```get_github_files(self, user:str, repo:str, sub_dir:str = '', extensions:list[str]|None = None) -> dict:```

Gets the GitHub download URLs of every file in a specified repository.

Arguments:
- user: The repository owner's GitHub username.
- repo: The name of the repository.
- sub_dir: If a non-empty string, gets all files within the specified sub-directory.
- extension: If not None, gets all files that have one of the specified file extensions.


### CodeEmbeddingsGenerator.py

```generate_code_embeddings(file_url:str, sub_dir:str, model:UniXcoder, device:str = None) -> None```

Uses the pre-trained model to generate code embeddings from the given source code. Gives embeddings for whole classes, whole methods, and tokens, and stores them in a JSON file with relevant data. The data saved in a data folder, and put in a directory that mimics that of the original directory location of the source file.

Arguments:
- file_url: Download URL of a source file.
- sub_dir: The subdirectory of the Github repository from which source code is taken.
- model: UniXcoder transformer model.
- device: PyTorch device.

```embed_all_files(files:dict, sub_dir:str) -> None```

Generates Java code embeddings with the UniXcoder model for every given source code file. It is assumed that all the files are located in the same Github repository and subdirectory.

Arguments:
- files: Download URLs of the Java source code, with uniquely identifying IDs as the keys.
- sub_dir: The specific subdirectory to focus on. If it is an empty string, have no subdirectory to focus on, and organize everything from the master branch.


---

```Disclaimer: All writing and code in this repository was made entirely by Cynthia Xiong.```

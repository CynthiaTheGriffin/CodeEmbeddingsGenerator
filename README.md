# Topological Data Analysis on Source Code Embeddings

## Overview

This repository includes code that retrieves Java code from GitHub repositories, then data engineers the code into numerical representations of the code, or code embeddings. GitHubFileGetter.py obtains the download URLs of files in a specified repository (or subdirectory in the repository), and CodeEmbeddingsGenerator.py generates a new directory with the code embedding representations. RunAll.py simplifies the use of each file into two Python functions, which can be run with a single line of code. 

The result should create a new data folder containing the code embeddings. This new folder would be structured similarly to the original GitHub repository, with embeddings stored in folders named after the Java files from which they're derived.


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


## Instructions

Step 1: Complete the setup described above.

Step 2: Generate code embeddings at the GitHub repository of your choice. Please refer to [RunAll.ipynb](RunAll.ipynb) to run the code.

Step 3: Perform topological data analysis. 

This is where the rest of the magic happens! However, explaining this step is far beyond the scope of this repository, but we have found some helpful links for any newcomers who want to have a go:
- Tutorial by Katherine Benjamin: [https://www.youtube.com/watch?v=8qXOdF1_nm8](https://www.youtube.com/watch?v=8qXOdF1_nm8)
- Tutorial by Elizabeth Munch: [https://www.youtube.com/watch?v=SbsvM4Gcbl0](https://www.youtube.com/watch?v=SbsvM4Gcbl0)


## Data Engineering

CodeEmbeddingsGenerator.py reads Java code files, then uses the code to generate code embeddings through a systematic method:

1. Extract code fragments using the [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) parser at three levels: classes, methods, and tokens. The classes are the largest code fragments, which contains the smaller method code fragments, which contains the even smaller token code fragments.
2. Input the code fragments into the [UniXcoder](https://github.com/microsoft/CodeBERT/tree/master/UniXcoder) neural network model for AI code generation, which outputs code fragment embedding representations. Each embedding includes 768 values.
3. Save each embedding as a JSON file in a data folder, along with some other relevant data.
    - Includes the class/method name if it is a class/method embedding, or the token itself if it is a token embedding.
    - Includes the string indices for parsing out the code fragment being represented.

Here is an example data engineering pipeline, where the source code is taken from the official [Apache Ivy](https://github.com/apache/ant-ivy/tree/master) GitHub repository:
![Diagram of data engineering pipeline](img/data_engineering_pipeline.png)

Furthermore, the directory in the data folder is structured similarly to the structure of the source repository. JSON files that were created from a certain Java file would be stored in a folder named after that same Java file, which is stored in a location that mimics that of its source. JSON files are also named after the classes or methods they are in, including those that are nested. The idea is to simplify the process of separating embeddings by granularity and directory locations for ease of analysis.

Here are some example JSON filenames that were generated from [Ivy.java](https://github.com/apache/ant-ivy/blob/master/src/java/org/apache/ivy/Ivy.java) (from Apache Ivy):

| Filename | Meaning |
|-|-|
| c.Ivy.json | Class embedding of Ivy class |
| c.Ivy_m.AssertBound.json | Method embedding of AssertBound method found in Ivy class |
| c.Ivy_m.AssertBound_token.json | Token embedding of a token found in AssertBound method and Ivy class |
| c.Ivy_m.AssertBound_token(0).json | Token embedding of a different token found in AssertBound method and Ivy class |
| c.Ivy_m.AssertBound_token(1).json | Token embedding of yet another token found in AssertBound method and Ivy class |
| c.Ivy_m.bind.json | Method embedding of bind method found in Ivy class |
| c.Ivy_m.bind_m.transferProgress.json | Method embedding of transferProgress method found in bind method and Ivy class |
| c.Ivy_m.deliver.json | Method embedding of deliver method found in Ivy class |
| c.Ivy_m.deliver(0).json | Method embedding of a different deliver method found in Ivy class |

## Documentation

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


## References

[1] Batista, N., Sousa, G., Brandão, M., Silva, A., & Moro, M. (2018). Tie strength metrics to rank pairs of developers from github. Journal of Information and Data Management, 9(1), 69. https://doi.org/10.5753/jidm.2018.1637 

---

```Disclaimer: All writing and code in this repository was made entirely by Cynthia Xiong.```

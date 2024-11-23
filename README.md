# Topological Data Analysis on Source Code Embeddings

## Overview

Topological data analysis (TDA) is an emerging approach for analyzing complex datasets by extracting shape-based features and structural insights. While TDA has been applied to various domains, its use in studying source code is a relatively new and developing area. Still, it shows promise for providing new insights into code structure, quality, and evolution. Although source code repositories contain vast amounts of complex, high-dimensional data that can be challenging to analyze using traditional methods, TDA offers a unique perspective by focusing on the topological and geometric properties of data, which can reveal hidden structures and patterns.

This repository includes code that can facilitate TDA on Java source code from GitHub repositories by data engineering embedding representations of the source code. GitHubFileGetter.py obtains the download URLs of files in a specified repository (or subdirectory in the repository), and CodeEmbeddingsGenerator.py generates a new directory with the code embedding representations. This new directory would be structured similarly to the original repository to make separating embeddings by types and directory locations easier during analyses.

Suppose we want to analyze some Java files in the official Apache Ivy codebase.

Step 1: Obtain the download URLs of the Java files in the repository.
```
import json
from GitHubFileGetter import GitHubFileGetter

# Get the download URLs of all Java files in the ivy subdirectory of the ant-ivy GitHub repository
user = "apache" # Owner of target repository
repo = "ant-ivy" # Repository name
sub_dir = "ivy" # Target subdirectory from within repository
extensions = ["java"] # Specifies to take only .java files

token = "" # Fine-grained GitHub access token
file_getter = GitHubFileGetter(token)
java_files = file_getter.get_github_files(user, repo, sub_dir, extensions)

# Save URLs in a JSON file
with open(download_urls.json) as f:
  json.dump(java_files, f)
```

Step 2: Generate code embeddings for all files in the repository.
```
import json
from CodeEmbeddingsGenerator import generate_code_embeddings, embed_all_files

java_files = json.load(open("download_urls.json"))
sub_dir = "ivy"

# Generate code embeddings for a single Java file
url = java_files['0'] # Ivy.java download URL
model = UniXcoder("microsoft/unixcoder-base")
generate_code_embeddings(url, sub_dir, model)

# Generate code embeddings for all the Java files in the ivy subdirectory
embed_all_files(java_files, sub_dir)
```

Step 3: Perform topological data analysis. 

Explaining this step is far beyond the scope of this repository, we have found some helpful links for those who want to get started:

Tutorial by Katherine Benjamin: [https://www.youtube.com/watch?v=8qXOdF1_nm8](https://www.youtube.com/watch?v=8qXOdF1_nm8)
Tutorial by Elizabeth Munch: [https://www.youtube.com/watch?v=SbsvM4Gcbl0](https://www.youtube.com/watch?v=SbsvM4Gcbl0)


## Data Engineering

GenerateCodeEmbeddings.py reads Java source code files, then uses the code to generate code embeddings through a systematic method:

1. Extract code fragments using the [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) parser at three levels of granularity: classes, methods, and tokens.
2. Input the code fragments into the [UniXcoder](https://github.com/microsoft/CodeBERT/tree/master/UniXcoder) transformer neural network model, which outputs code fragment embeddings.
3. Save each embedding as a JSON file in a data folder, along with some relevant metadata.
  - Includes the class/method name if it is a class/method embedding, or the token itself if it is a token embedding.
  - Includes the string indices for parsing out the code fragment being represented.

Furthermore, the directory in the data folder is structured similarly to the structure of the source repository. JSON files that were created from a certain Java file would be stored in a folder named after that same Java file, which is stored in a location that mimics that of its source. JSON files are also named after the classes or methods they are in, including those that are nested. The idea is to simplify the process of separating embeddings by granularity and directory locations for ease of analysis.


## Documentation

### GitHubFileGetter.py

```get_github_files(self, user:str, repo:str, sub_dir:str = '', extensions:list[str]|None = None) -> dict:```

Gets the GitHub download URLs of every file in a specified repository.

Args:
- user: The repository owner's GitHub username.
- repo: The name of the repository.
- sub_dir: If a non-empty string, gets all files within the specified sub-directory.
- extension: If not None, gets all files that have one of the specified file extensions.


### CodeEmbeddingsGenerator.py

```generate_code_embeddings(file_url:str, sub_dir:str, model:UniXcoder, device:str = None) -> None```

Uses the pre-trained model to generate code embeddings from the given source code. Gives embeddings for whole classes, whole methods, and tokens, and stores them in a JSON file with relevant data. The data saved in a data folder, and put in a directory that mimics that of the original directory location of the source file.

Args:
- file_url: Download URL of a source file.
- sub_dir: The subdirectory of the Github repository from which source code is taken.
- model: UniXcoder transformer model.
- device: PyTorch device.

```embed_all_files(files:dict, sub_dir:str) -> None```

Generates Java code embeddings with the UniXcoder model for every given source code file. It is assumed that all the files are located in the same Github repository and subdirectory.

Args:
- files: Download URLs of the Java source code, with uniquely identifying IDs as the keys.
- sub_dir: The specific subdirectory to focus on. If it is an empty string, have no subdirectory to focus on, and organize everything from the master branch.

# Topological Data Analysis on Source Code Embeddings

Topological data analysis (TDA) is an emerging approach for analyzing complex datasets by extracting shape-based features and structural insights. While TDA has been applied to various domains, its use in studying source code is a relatively new and developing area. Still, it shows promise for providing new insights into code structure, quality, and evolution. Although source code repositories contain vast amounts of complex, high-dimensional data that can be challenging to analyze using traditional methods, TDA offers a unique perspective by focusing on the topological and geometric properties of data, which can reveal hidden structures and patterns.

This repository includes code that can facilitate TDA on source code from GitHub repositories by data engineering embedding representations of the source code. GitHubFileGetter.py obtains the download URLs of files in a specified repository (or subdirectory in the repository), and CodeEmbeddingsGenerator.py generates a new directory with the code embedding representations. This new directory would be structured similarly to the original repository to make separating embeddings by types and directory locations easier during analyses.

Suppose we want to analyze some Java files in the official Apache Ivy codebase.

Step 1: Obtain the download URLs of the Java files in the repository.
```
from GitHubFileGetter import GitHubFileGetter

# Get the download URLs of all Java files in the ivy subdirectory of the ant-ivy GitHub repository
user = "apache" # Owner of target repository
repo = "ant-ivy" # Repository name
sub_dir = "ivy" # Target subdirectory from within repository
extensions = ["java"] # Specifies to take only .java files

token = "" # Fine-grained GitHub access token
file_getter = GitHubFileGetter(token)
file_getter.get_github_files(user, repo, sub_dir, extensions)

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

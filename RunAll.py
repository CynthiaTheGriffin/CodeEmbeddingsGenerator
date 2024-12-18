import json
from GitHubFileGetter import GitHubFileGetter
from unixcoder import UniXcoder
from CodeEmbeddingsGenerator import embed_all_files


def get_download_urls(token:str, user:str, repo:str, sub_dir:str):
    '''
    Get the download URLs of all Java files in the specified GitHub repository.

    Args:
        user: Owner of target repository
        repo: Repository name
        sub_dir: Target subdirectory from within repository
        token: GitHub access token
    '''
    extensions = ["java"] # Specifies to take only .java files

    file_getter = GitHubFileGetter(token)
    java_files = file_getter.get_github_files(user, repo, sub_dir, extensions)

    # Save URLs in a JSON file
    with open("download_urls.json", "w") as f:
        json.dump(java_files, f)
    return


def generate_embeddings(sub_dir:str):
    '''
    Generate code embeddings for all Java files given by the download URLs.

    Args:
        sub_dir: Target subdirectory from within the repository
    '''
    java_files = json.load(open("download_urls.json"))

    # Generate code embeddings for all the Java files in the ivy subdirectory
    embed_all_files(java_files, sub_dir)
    return

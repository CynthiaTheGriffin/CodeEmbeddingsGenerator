from github import Github, Auth


class GitHubFileGetter:
    
    def __init__(self, token:str) -> None:
        self.auth = Auth.Token(token)
        return
    

    def __traverse_github(self, urls:list, dir:str) -> None:
        '''
        Recursively runs through a GitHub repository to collect download URLs from the files.

        Args:
            urls: A list to add URLs to.
            dir: Current directory.
        '''
        for content in self.__repo.get_contents(dir):
            if len(content.name.split('.')) > 1: # Base case: Content is file
                if self.__extensions != None:
                    # Only include if filename has a specified extension
                    if content.name.split('.')[-1] in self.__extensions:
                        urls.append(content.download_url)
                else:
                    urls.append(content.download_url)
            else: # Recursive case: Content is folder
                self.__traverse_github(self, urls, content.path)
        return
    

    def get_github_files(self, user:str, repo:str, sub_dir:str = '', extensions:list[str]|None = None):
        '''
        Gets the GitHub download URLs of every file in a specified repository.

        Args:
            user: The repository owner's GitHub username.
            repo: The name of the repository.
            sub_dir: If a non-empty string, gets all files within the specified sub-directory.
            extension: If not None, gets all files that have one of the specified file extensions.
        '''
        g = Github(auth=self.auth)
        # self.__repo = g.get_repo(full_name_or_id = user + '/' + repo)
        self.__repo = g.get_repo(full_name_or_id = 'apache/ant-ivy')
        self.__extensions = extensions

        urls = []
        self.__traverse_github(urls, sub_dir)
        return urls
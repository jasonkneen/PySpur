import logging
from pydantic import BaseModel, Field  # type: ignore
from ...base import BaseNode, BaseNodeConfig, BaseNodeInput, BaseNodeOutput
from phi.tools.github import GithubTools
from typing import Dict


class GitHubGetRepositoryNodeConfig(BaseNodeConfig):
    repo_name: str = Field(
        "", description="The full name of the repository (e.g. 'owner/repo')."
    )
    output_schema: Dict[str, str] = Field(
        default={"repository_details": "string"},
        description="The schema for the output of the node",
    )
    has_fixed_output: bool = True


class GitHubGetRepositoryNodeInput(BaseNodeInput):
    pass


class GitHubGetRepositoryNodeOutput(BaseNodeOutput):
    repository_details: str = Field(
        ..., description="Details of the requested repository in JSON format."
    )


class GitHubGetRepositoryNode(BaseNode):
    name = "github_get_repository_node"
    display_name = "GitHubGetRepository"
    logo = "/images/github.png"
    category = "GitHub"

    config_model = GitHubGetRepositoryNodeConfig
    input_model = GitHubGetRepositoryNodeInput
    output_model = GitHubGetRepositoryNodeOutput

    async def run(self, input: BaseModel) -> BaseModel:
        try:
            gh = GithubTools()
            repo_details = gh.get_repository(repo_name=self.config.repo_name)
            return GitHubGetRepositoryNodeOutput(repository_details=repo_details)
        except Exception as e:
            logging.error(f"Failed to get repository details: {e}")
            return GitHubGetRepositoryNodeOutput(repository_details="")

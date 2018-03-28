.. _quickstart: 

Quickstart
==========

Eager to get started? This page gives you a detailed introduction of how to use ``IGitt`` ineterfaces to access data from various git hosting services.

First, make sure that you have installed ``IGitt``::

    $ pip install IGitt

Also, each of the following example uses GitHub Token, So make sure you
have generated a GitHub Token of your own. You can follow
`this tutorial 
<https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`_
for the same.

Now, put your GitHub Token in a variable name GH_TOKEN::

    >>> GH_TOKEN = '3jfsdfhsdlfksdfvfvffgrgdfggg'

And make an ``IGitt`` GitHub Token object which will be used throughout
every example::

    >>> from IGitt.GitHub import GitHubToken
    >>> gh_token = GitHubToken(GH_TOKEN)

Now, Let's get going with the examples.

Organization
------------

This section will show you how to use ``Organization`` interface and its methods::

    >>> from IGitt.GitHub.GitHubOrganization import GitHubOrganization

Now get the ``Organization`` object as org::

    >>> org_name = 'coala'
    >>> org = GitHubOrganization(gh_token, org_name)

Get the web_url of the org::

    >>> org.web_url

Get the description of the org::

    >>> org.description

Get the number of registered users for the org::

    >>> org.billable_users

Get all the owners to the org::

    >>> owners = org.owners
    >>> owners

Get a single owner::

    >>> owners_list = []
    >>> for owner in owners:
            owners_list.append(owner)
    >>> owner = owners_list[0]

Get the id of the single owner::

    >>> owner.identifier

Get the username of the owner::

    >>> owner.username

Get install_repo of the owner::

    >>> owner.installed_repositories

Get the masters of the org::

    >>> org.masters

Get the name of the org::

    >>> org.name

Get the suborgs of the org::

    >>> org.suborgs

Get the set of repositories for the org::

    >>> repos = org.repositories
    >>> repos

Get a list of repositories for the org::

    >>> repos_list = []
    >>> for repo in repos:
	        repos_list.append(repo)

Get a single repo::

    >>> repo = repos_list[0]

For getting details of a single repo see ``Repository`` section.

Repository
----------

This section will show you how to use ``Repository`` interface and its methods::

    >>> from IGitt.GitHub.GitHubRepository import GitHubRepository

Get the ``Repository`` object as ``repo``::

    >>> repo_name = 'coala/commuity'
    >>> repo = GitHubRepository(gh_token, repo_name)

Get the id of the repo::

    >>> repo.identifier

Get the org of the repo::

    >>> repo.top_level_org

Get the name of the repo::

    >>> repo.full_name

Get set of commits to the repo::

    >>> commits = repo.commits

Get list of commits to the repo::

    >>> commits_list = []
    >>> for commit in commits:
            commits_list.append(commit)

Get a single commit::

    >>> commit = commits_list[0]

For more methods on a commit
See ``Commit`` section.

Get clone url of the repo::

   >>> repo.clone_url

Get the labels of the repo::

   >>> labels = repo.get_labels()
   >>> labels

Get set of issues to the repo::

   >>> repo.issues

Get a single issue by its number::

   >>> repo.get_issues(1)

For getting more details of a issue see ``Issue`` section.

Get set of MRs to the repo::

   >>> repo.merge_requests

Get a single MR of the repo by its number::

   >>> repo.get_mr(77)

For getting more details of a MR see ``MergeRequest`` section.

Get all the urls this repo is hooked to::

   >>> repo.hooks

MergeRequest
------------

This section will show you how to use ``MergeRequest`` interface and its methods::

   >>> from IGitt.GitHub.GitHubMergeRequest import GitHubMergeRequest

Get the ``MergeRequest`` object as ``mr``::

   >>> repo_name = 'coala/community'
   >>> mr_number = 52
   >>> mr = GitHubMergeRequest(gh_token, repo_name, mr_number)

Get the base commit as a commit object::

   >>> mr.base

Get the sha of the base::

   >>> mr.base.sha

Get the head commit as a commit object::

   >>> mr.head

Get the sha of the head::

   >>> mr.head.sha

Get the base branch name::

   >>> mr.base_branch_name

Get the head branch name::

   >>> mr.head_branch_name

Get the tuple of commit objects that are included in the mr::

   >>> mr.commits

Get the repository where this comes from::

   >>> mr.repository

Get the repository where this mr's head branch is located at::

   >>> mr.source_repository)

For getting more details of repo see `Repository` section.

Get the affected files by this mr::

   >>> mr.affected_files

Get the addition and deletion of the mr::

   >>> mr.diffstat

Get set of issue objects which would be closing upon merging this mr::

   >>> mr.closes_issues

Get set of issue obejects which are to this pull request::

   >>> mr.mentioned_issues

Get the author of the mr::

   >>> mr.author

Get the state of the mr::

   >>> mr.state

Get the comments on a mr::

   >>> comments = mr.comments
   >>> mr.comments

For getting more details of a comment see ``Comment`` section.

Issue
-----

This section will show you use ``Issue`` interface and its methods::

   >>> from IGitt.GitHub.GitHubIssue import GitHubIssue

Get the ``Issue`` obejct as ``issue``::

   >>> repo_name = 'coala/community'
   >>> issue_number = 1
   >>> issue = GitHubIssue(gh_token, repo_name, issue_number)

Get the repo where this issue belong::

   >>> issue.repository

For more details on a repo see `Repository` section.

Get the title of the issue::

   >>> issue.title

Get the number of the issue::

   >>> issue.number

Get the assignees to the issue::

   >>> issue.assignees

Get the description of the issue::

   >>> issue.description

Get the author of the issue::

   >>> issue.author

Get the comments to a issue::

   >>> comments = issue.comments
   >>> comments

For getting more details on a comment see ``Comment`` section.

Get the labels on a issue::

   >>> issue.labels

Get the available labels::

   >>> issue.available_labels

Get the time when issue was created::

   >>> issue.created

Get the time when issue was last updated::

   >>> issue.updated

Get the state of the issue::

   >>> issue.state

Get reactions to the issue::

   >>> issue.reactions

Get the mr which close this issue::

   >>> issue.mrs_closed_by

For getting more details on mr see ``MergeRequest`` section.

Comment
-------

This section will show you how to use ``Comment`` interface and its methods::

   >>> from IGitt.GitHub.GitHubComment import GitHubComment
   >>> from IGitt.Interfaces.Comment import CommentType

Get the ``Comment`` object as comment::

   >>> repo_name = 'coala/community'
   >>> comment_id = 373075029
   >>> issue = CommentType.ISSUE
   >>> comment = GitHubComment(gh_token, repo_name, issue , comment_id)

Get the id of the comment::

   >>> comment.number

Get the type of the comment::

   >>> comment.type

Get the descritption of the comment::

   >>> comment.body

Get the author of the comment::

   >>> comment.author

Get the time when this comment was created::

   >>> comment.created

Get the time when this comment was updated::

   >>> comment.updated

Get the repository where this comment belongs::

   >>> comment.repository

For more details on a repository see ``Repository`` section.

Commit
------

This section will show you how to use ``Commit`` interface and its methods::

   >>> from IGitt.GitHub.GitHubCommit import GitHubCommit

Get the ``Commit`` object as ``commit``::

   >>> repo_name = 'coala/community'
   >>> sha = 'b951ad95948112785522428d66a78785ffb7eebc'
   >>> commit = GitHubCommit(gh_token, repo_name, sha)

Get the commit message::

   >>> commit.message

Get sha of the commit::

   >>> commit.sha

Get the repository of the commit::

   >>> commit.repository

For more details of a repository please see ``Repository`` section.

Get the parent commit. In case of a merge commit the first parent will be returned::

   >>> commit.parent

Get all the commit statuses::

   >>> commit.statuses

Get combined status of all commits::

   >>> commit.combined_status

Get the patch for a given file::

   >>> commit.get_patch_for_file('README.md')

Get the unified diff for the commit excluding the diff index::

   >>> commit.unified_diff

User
----

This section will show you how to use ``User`` interface and its methods::

   >>> from IGitt.GitHub.GitHubUser import GitHubUser

Get the ``User`` object as user::

   >>> username = 'sks444'
   >>> user = GitHubUser(gh_token, username)

Get the username::

   >>> user.username

Get the id of the user::

   >>> user.identifier

Get installed repositories of the user::

   >>> user.installed_repositories

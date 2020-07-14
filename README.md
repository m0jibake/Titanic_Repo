# Titanic_Repo README

## git Workflow

development happens only on development branches, i.e. NOT the master branch. This means that you should not commit to the master branch.

If you start working on your code:
- git pull (to get the latest changes on your local master)
- git rebase (to integrate the changes which are on your master into your development branch)

If you created a feature, function, etc. and think it is worth sharing: 
- push your commits to the remote development branch. 
- on github, open a Pull Request. If there are no merge conflicts, everyone can integrate your contribution by pulling on the local master.




-------------------------------------------------------

## Link zu den den Videos:
https://www.youtube.com/user/schafer5/playlists

-------------------------------------------------------

## Important git commands

git status

git add <filename> --- add file to stageing area

git commit -m '<commit message>' --- commit all staged files on top of the current local branch

git push --- push all commits to the remote repo

git push -f --- force all commits on the remote repo. Required when local branch is behind -> remote repo will lose commits

git log --- display whole history of the current local branch

git log --oneline --- same as git log, but information is presented more consisely

git reflog --- show history, but also with merges and resets

git diff <filename> --- show differences between unstaged file and file that has been already commited

git revert <commit hash> --- Create new commit that undoes all of the changes made in <commit>, then apply it to the current branch

git fetch origin --- downloads new commits from the remote repo, but does NOT integrate them into the local repo. Required for git status to provide up todate info

git pull --- downloads new commits from the remote repo, and integrates them into the local repo

git commit --amend -m 'new commit message' --- change commit message of the last commit, if you haven't pushed yet. If you have already pushed, also do a git push -f

git reset --soft <commit hash> --- reset to <commit hash> and put all changes ever since into the stageing area

git reset --mixed <commit hash> --- reset to <commit hash> and put all changes ever since into the working directory 

git reset --hard --- reset to <commit hash> and throw all changes that happened ever since away. Also, working directory is cleaned. 

More info on git reset: https://stackoverflow.com/questions/3528245/whats-the-difference-between-git-reset-mixed-soft-and-hard

git checkout -b <mybranch> --- create a new local branch
  
git push --set-upstream origin <mybranch> --- register the local branch at the remote origin
  
git branch --- get a list of all local branches

git checkout <anybranch> --- change to another branch

git config --global --edit --- edit mail adress and name in editor

git Cheatsheet: https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet

learn git branching https://learngitbranching.js.org/?locale=de_DE

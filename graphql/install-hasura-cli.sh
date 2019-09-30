curl -L https://github.com/hasura/graphql-engine/raw/master/cli/get.sh | bash
echo "The hasura docker compose image will auto apply migrations, to run manually, cd into this directory and hasura migrate apply.";
echo "Anyhow, go run hasura console, do your thang and git commit metadata + migration folder changes.";

# # Bash
#     # Linux
#       # Add Bash completion file using:
#       $ sudo hasura completion bash --file=/etc/bash.completion.d/hasura
#     # Mac
#       # Install bash-completion using homebrew:
#       $ brew install bash-completion
#       # Add to your ~/.bash_profile:
#       if [ -f $(brew --prefix)/etc/bash_completion ]; then
#           . $(brew --prefix)/etc/bash_completion
#       fi
#       # Add the completion file:
#       $ sudo hasura completion bash --file=$(brew --prefix)/etc/bash_completion.d/hasura
#     # Windows (Git Bash)
#       # open git bash
#       $ mkdir -p ~/.bash_completion.d
#       # Add the completion file:
#       $ cd ~ && hasura completion bash --file=.bash_completion.d/hasura
#       # Add the following to ~/.bash_profile
#         if [ -f ~/.bash_completion.d/hasura ]; then
#           . ~/.bash_completion.d/hasura
#         fi
#       # restart git bash

#   # Zsh (using oh-my-zsh)
#     $ mkdir -p $HOME/.oh-my-zsh/completions
#     $ hasura completion zsh --file=$HOME/.oh-my-zsh/completions/_hasura

#   # Reload the shell for the changes to take effect!

# # * # * # * # * # * # * # * # * # * #
# To be placed in .zshrc or .bashrc.
# Line 7 must be changed accordingly
# Prints a table with al ssh-alias 
# entries within the .zshrc / .bashrc
# An alias needs to look like:
# alias ssh-<short-name>=<ssh-command>
# # * # * # * # * # * # * # * # * # * #
lssh(){
    cat ~/.zshrc | grep "alias ssh-" | sed -n -e 's/^alias.*\(ssh-.*\)\="\(.*\)"$/\1,| \2/p' | column -s ',' -t -N "alias, command"
}


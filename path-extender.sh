# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# To add a directory or file to the $PATH simply add
# the path to the file / directory to the paths-array
# it thenn will be added to the $PATH when sourcing
# this file
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
paths=( "/home/$USER/.cargo/bin"
        "/home/$USER/go/bin"
        )
for i in "${paths[@]}"  
do
  if [[ -d $i ]] || [[ -f $i ]] 
  then
  export PATH=$PATH:$i
  fi
done 

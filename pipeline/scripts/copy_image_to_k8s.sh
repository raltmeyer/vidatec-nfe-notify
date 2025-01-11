export image_name=$1
export image_version=$2
export ssh_username=$3
export KUBE_NODE=$4
export key_path=$5
export agent_temp_directory=$6

echo ----------------
echo Saving image to local storage
docker save --output ${agent_temp_directory}/${image_name}:${image_version}.tar ${image_name}:${image_version}
ls -l ${agent_temp_directory}/${image_name}:${image_version}.tar

echo ----------------
echo Copy image to k8s node
ssh -o StrictHostKeyChecking=no -i ${key_path} ${ssh_username}@${KUBE_NODE} "mkdir -p ~/images-tmp" 
scp -i ${key_path} "${agent_temp_directory}/${image_name}:${image_version}.tar" ${ssh_username}@${KUBE_NODE}:~/images-tmp/${image_name}:${image_version}.tar 

echo ----------------
echo Import image to k8s cluster
ssh -o StrictHostKeyChecking=no -i ${key_path} ${ssh_username}@${KUBE_NODE} "sudo k3s ctr images import ~/images-tmp/${image_name}:${image_version}.tar"

echo ----------------
echo Listing available ${image_name} on cluster
ssh -o StrictHostKeyChecking=no -i ${key_path} ${ssh_username}@${KUBE_NODE} "sudo k3s crictl images list | grep -i ${image_name}"

echo ----------------
echo cleanup node temporary image
ssh -o StrictHostKeyChecking=no -i ${key_path} ${ssh_username}@${KUBE_NODE} "rm -rf ~/images-tmp" 

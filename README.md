# ddf

## Passos

- Criar VM no Azure para dev
```sh
az vm create --resource-group fiapResourceGroup --name fiapDevVM --image UbuntuLTS --admin-username azureuser --generate-ssh-keys
```

- Criar VM no Azure para prod
```sh
az vm create --resource-group fiapResourceGroup --name fiapProdVM --image UbuntuLTS --admin-username azureuser --generate-ssh-keys
```

- Criar grupo de segurança
```sh
az network nsg create --resource-group fiapResourceGroup --name fiapSecurity
```

- Criar regra de segurança e aplicar no cluster
```sh
az network nsg rule create --resource-group fiapResourceGroup --nsg-name fiapSecurity --name AllowSSH --protocol Tcp direction Inbound priority 1000 --source-address-prefixes 192.0.15.0 --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 22 --access Allow

az network nsg rule create --resource-group fiapResourceGroup --nsg-name fiapSecurity --name AllowHTTP --protocol Tcp --direction Inbound --priority 1001 --source-address-prefixes 192.0.15.0 --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 80 --access Allow

az network nsg rule create --resource-group fiapResourceGroup --nsg-name fiapSecurity --name AllowHTTPS --protocol Tcp --direction Inbound --priority 1002 --source-address-prefixes 192.0.15.0 --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 443 --access Allow

az network nic update --resource-group fiapResourceGroup --name fiapSecureVMNic --network-security-group fiapSecurity
```

- Configurar monitoramento na VM
```sh
az vm extension set --resource-group fiapResourceGroup --vm-name fiapProdVM --name OmsAgentForLinux --publisher Microsoft.EnterpriseCloud.Monitoring --version 1.0
```

- Criar cluster AKS
```sh
az aks create --resource-group fiapResourceGroup --name fiapAKSCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys
```

- Setando escalabilidade automática
```sh
az aks nodepool update --resource-group fiapResourceGroup --cluster-name fiapAKSCluster --name nodepool1 --enable-cluster-autoscaler --min-count 1 --max-count 5
```

- Aplicar secret key
```sh
kubectl apply -f secret.yaml
```

- Deploy
```sh
kubectl apply -f k8s/deployment.yaml
```


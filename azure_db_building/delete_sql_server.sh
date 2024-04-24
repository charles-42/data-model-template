#!/bin/bash

# Set variables for resource group and server name
resourceGroupName="BENIAC_data_api"
serverName="DBServerNameOlistmodelapitemplate"
databaseName="olist"


# Remove the SQL database
az sql db delete --resource-group $resourceGroupName --server $serverName --name $databaseName --yes

# Remove the SQL server
az sql server delete --resource-group $resourceGroupName --name $serverName --yes
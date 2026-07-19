param(
    [Parameter(Mandatory = $true)]
    [string]$Ec2PublicIp,

    [string]$KeyPath = "D:\GitHub\LAB_GrupoA_EcossistemadeBigData\ingestao\aws_credentials_lab\labsuser.pem",

    [string]$Destination = "D:\GitHub\LAB_GrupoA_EcossistemadeBigData\ingestao\2-meltano\evidencias"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $KeyPath)) {
    throw "Chave SSH não encontrada: $KeyPath"
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null

scp `
    -i $KeyPath `
    -r `
    "ec2-user@${Ec2PublicIp}:/home/ec2-user/evidencias_tutorial2/*" `
    $Destination

Write-Host "Evidências copiadas para: $Destination"

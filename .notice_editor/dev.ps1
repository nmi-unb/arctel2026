param([Parameter(ValueFromRemainingArguments=$true)]$Args)
# Venv fora do OneDrive: evita corrupção de dist-info por sync em tempo real
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-envs\notice_editor"
uv @Args

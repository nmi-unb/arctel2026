Eu tenho as planilhas:

- [ArcTel 2026 - Confirmação](https://docs.google.com/spreadsheets/d/1rmQRpgQUqsy_XEGiHRVacEUlZou3zQ7WXcAO8jP04aU/edit?resourcekey=&gid=2056599558#gid=2056599558)
  - Cabeçalho: "Carimbo de data/hora","Nome Completo","E-mail Principal","Celular (com DDI e DDD)"
- [ArcTel2026 BRASIL](https://docs.google.com/forms/d/1Iet2fW3uQgOUAuRGaAgKyTf6WcNk2qbsnNu9kraLdFk/edit)
  - Cabeçalho: Carimbo de data/hora","Estrangeiro?","CPF","UF","Número do Passaporte","País (CPLP)","Nome Completo","Nome Social","Foi solicitado o uso do Nome Social nos documentos oficiais?","Data de Nascimento","CEP","Rua/Av.","Número","Bairro","Complemento","Município","Telefone Fixo","Celular","E-mail","Confirmação de E-mail".
- [ArcTel2026](https://docs.google.com/forms/d/1gTczBLKCq26l1mucEYUfI4cCp1qsfkNCW_0gub5COPA/edit)
  - Cabeçalho: Carimbo de data/hora","Estrangeiro?","CPF","UF","Número do Passaporte","País (CPLP)","Nome Completo","Nome Social","Foi solicitado o uso do Nome Social nos documentos oficiais?","Data de Nascimento","CEP","Rua/Av.","Número","Bairro","Complemento","Município","Telefone Fixo","Celular","E-mail","Confirmação de E-mail".

- [DADOS_ARCTEL](https://docs.google.com/spreadsheets/d/1vwwCa-VGHIpS64MzoYFNK7VHhB4uxtlLRqf7gvercOc/edit?gid=0#gid=0)

Eu tenho um total de quatro planilhas. As primeiras três são planilhas de onde a gente precisa extrair dados. E eu preciso compilar esses dados na quarta planilha. A quarta planilha está vazia.

# Como?

Desenvolver um único script em Python que autentique via Google Sheets API (Service Account), acesse simultaneamente três planilhas de origem no Google Drive, leia os dados necessários, processe e consolide essas informações conforme regras definidas e grave o resultado em uma planilha de saída (existente ou criada automaticamente, se necessário). O código deverá manter separados os parâmetros de configuração (IDs das planilhas) da lógica de processamento, permitindo fácil manutenção e futura expansão para novas planilhas, regras ou fontes de dados, sem alterar a estrutura principal do script.

# Onde?

Dentro da pasta `.\_drive`
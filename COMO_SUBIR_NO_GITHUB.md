# Como subir este projeto no GitHub

## Opção A – Pelo site (mais simples)

1. Em github.com, clique em **New repository**.
2. Nome: `orientar-whatsapp-n8n`. Marque **Public**. **Não** marque "Add a README".
3. Clique em **Create repository**.
4. Na página seguinte, clique em **uploading an existing file**.
5. Arraste **o conteúdo** desta pasta (as pastas `n8n`, `database`, `docs`, `tools` e os arquivos `README.md` e `.gitignore`).
   - O `.gitignore` começa com ponto e pode ficar oculto. No Windows, ative "Itens ocultos" no Explorador de Arquivos.
6. Escreva uma mensagem (ex.: "Versão inicial") e clique em **Commit changes**.

## Opção B – Pelo terminal (Git instalado)

Crie o repositório vazio no GitHub (passos 1 a 3 acima) e, dentro desta pasta, rode:

```bash
git init -b main
git add .
git commit -m "Versão inicial do atendimento automatizado via WhatsApp"
git remote add origin https://github.com/SEU_USUARIO/orientar-whatsapp-n8n.git
git push -u origin main
```

Na primeira vez, o GitHub pede login. Use o navegador ou um token pessoal (Settings → Developer settings → Personal access tokens).

## Antes de publicar, confira

- [ ] Nenhum arquivo `.vcf`, `.csv` ou exportação de contatos reais.
- [ ] Nenhuma conversa de WhatsApp.
- [ ] O fluxo está com `COLOQUE_SEU_VERIFY_TOKEN`, `SEU_PHONE_NUMBER_ID` e `55DDDNUMERO` (valores de exemplo).

Este arquivo pode ser apagado depois que o projeto estiver no GitHub.

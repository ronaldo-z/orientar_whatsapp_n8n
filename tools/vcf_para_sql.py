# Converte a agenda exportada do WhatsApp (.vcf) em SQL para a tabela contatos.
# Uso: python3 vcf_para_sql.py contatos.vcf saida.csv saida.sql
# ATENÇÃO: os arquivos gerados contêm dados pessoais. Não envie para o repositório.
import csv, quopri, re, sys

src, out_csv, out_sql = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(src, encoding="utf-8", errors="replace").read()
# junta linhas quebradas do quoted-printable (terminam com '=')
raw = re.sub(r"=\r?\n", "", raw)

def decode(line):
    head, _, val = line.partition(":")
    if "QUOTED-PRINTABLE" in head.upper():
        val = quopri.decodestring(val.encode()).decode("utf-8", "replace")
    return head.split(";")[0].upper(), val.strip()

def chave(tel):
    d = re.sub(r"\D", "", tel or "").lstrip("0")
    if len(d) >= 12 and d.startswith("55"):
        d = d[2:].lstrip("0")
    if len(d) < 10 or len(d) > 11:
        return None
    return d[:2] + d[-8:]

ORGAO = r"\b(pref|prefeitura|sec\.|secretaria|sema|smma|semur|iat|sanepar|incra|cart[oó]rio|vara|urbanismo|escrit[oó]rio regional|tributa|ger[eê]ncia de licenciamento)\b"
# Ajuste com nomes da equipe interna (o robô ignora esses contatos)
INTERNO = r"(orientar|estagi[aá]ri)"
IGNORAR = r"(siga me|tim exterior|cp no exterior)"

rows = []
for card in raw.split("BEGIN:VCARD")[1:]:
    fn, tels = "", []
    for line in card.splitlines():
        if not line or ":" not in line:
            continue
        k, v = decode(line)
        if k == "FN":
            fn = v
        elif k == "TEL":
            tels.append(v)
    if not fn and not tels:
        continue
    tel = tels[0] if tels else ""
    ch = chave(tel)
    low = fn.lower()
    if re.search(r"\d{5}-\d{3}$", tel.strip()):
        ch = None  # número truncado (ex.: 99960-224)
    if re.search(IGNORAR, low) or not ch:
        tipo = "revisar" if not re.search(IGNORAR, low) else "ignorar"
    elif re.search(INTERNO, low):
        tipo = "interno"
    elif re.search(ORGAO, low):
        tipo = "orgao"
    else:
        tipo = "cliente"
    rows.append({"nome": fn, "telefone": tel, "chave_whats": ch or "", "tipo_sugerido": tipo})

# remove duplicados pela chave (mantém o primeiro)
seen, uniq = set(), []
for r in rows:
    k = r["chave_whats"] or ("sem:" + r["nome"])
    if k in seen:
        continue
    seen.add(k)
    uniq.append(r)

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(uniq[0].keys()))
    w.writeheader()
    w.writerows(uniq)

esc = lambda s: re.sub(r"[\U00010000-\U0010FFFF]", "", s).strip().replace("'", "''")
with open(out_sql, "w", encoding="utf-8") as f:
    f.write("-- Importação dos contatos do WhatsApp (gerado a partir do .vcf)\n")
    f.write("-- Revise o tipo (cliente / orgao / interno) antes de rodar. Contatos sem DDD ficaram de fora (veja o CSV, tipo 'revisar').\n")
    f.write("-- Rodar no DBeaver com 'Executar script SQL' (Alt+X), depois do 01_criar_tabelas.sql.\n")
    f.write("USE `Orientar`;\n\n")
    f.write("-- INSERT IGNORE: se o número já estiver cadastrado, pula sem erro.\n")
    for r in uniq:
        if not r["chave_whats"] or r["tipo_sugerido"] == "ignorar":
            continue
        f.write(f"INSERT IGNORE INTO contatos (nome, telefone, chave_whats, tipo) VALUES ('{esc(r['nome'])}', '{esc(r['telefone'])}', '{r['chave_whats']}', '{r['tipo_sugerido']}');\n")
    f.write("\n-- Conferência:\n-- SELECT tipo, COUNT(*) FROM contatos GROUP BY tipo;\n")

from collections import Counter
print(len(rows), "cartões;", len(uniq), "únicos;", Counter(r["tipo_sugerido"] for r in uniq))
for r in uniq:
    if r["tipo_sugerido"] in ("revisar", "interno", "orgao", "ignorar"):
        print(r["tipo_sugerido"], "|", r["nome"], "|", r["telefone"])

-- Contatos FICTÍCIOS apenas para teste.
-- Os contatos reais devem ser importados localmente (veja tools/vcf_para_sql.py)
-- e NUNCA enviados para o repositório.
USE `Orientar`;

-- chave_whats = DDD + 8 últimos dígitos (sem 55 e sem o 9 inicial do celular)
INSERT IGNORE INTO contatos (nome, telefone, chave_whats, tipo) VALUES
('Cliente Exemplo Ltda',       '41 99999-0001', '4199990001', 'cliente'),
('Secretaria Municipal Exemplo','41 3333-0002',  '4133330002', 'orgao'),
('Colaborador Interno Exemplo', '41 99999-0003', '4199990003', 'interno');

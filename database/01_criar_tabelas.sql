-- =====================================================================
-- Orientar WhatsApp – estrutura do banco (DBeaver)
-- Como rodar: abra no editor SQL do DBeaver conectado ao servidor e use
--   "Executar script SQL" (Alt+X). NÃO use Ctrl+Enter (roda só 1 comando).
-- Pode rodar mais de uma vez: o script não duplica nada.
-- Cria as 3 tabelas do zero: mensagens, atendimentos e contatos.
-- =====================================================================

USE `Orientar`;

-- 1) Histórico de mensagens
CREATE TABLE IF NOT EXISTS mensagens (
  id         BIGINT AUTO_INCREMENT PRIMARY KEY,
  wamid      VARCHAR(128) NULL,
  chave      VARCHAR(12)  NOT NULL,
  telefone   VARCHAR(20)  NOT NULL,
  direcao    ENUM('in','out') NOT NULL,
  tipo       VARCHAR(20)  NULL,
  texto      TEXT         NULL,
  lote       VARCHAR(40)  NULL,
  criado_em  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_wamid (wamid),
  KEY idx_chave (chave, id),
  KEY idx_lote (lote)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 2) Estado do atendimento (triagem | coletando | humano | encerrado)
CREATE TABLE IF NOT EXISTS atendimentos (
  id            BIGINT AUTO_INCREMENT PRIMARY KEY,
  chave         VARCHAR(12) NOT NULL,
  telefone      VARCHAR(20) NOT NULL,
  categoria     VARCHAR(20) NULL,
  status        VARCHAR(20) NOT NULL,
  resumo        TEXT NULL,
  criado_em     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_chave_status (chave, status, atualizado_em)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 3) Contatos (cadastro de clientes, órgãos e equipe)
--    chave_whats = DDD + 8 últimos dígitos do telefone (ex.: 4199990001).
--    É por ela que o fluxo encontra o contato, com ou sem 55, 0 ou 9º dígito.
--    tipo: cliente | orgao | interno  (interno = equipe; o robô ignora)
CREATE TABLE IF NOT EXISTS contatos (
  id          BIGINT AUTO_INCREMENT PRIMARY KEY,
  nome        VARCHAR(150) NOT NULL,
  telefone    VARCHAR(40)  NULL,
  email       VARCHAR(150) NULL,
  chave_whats VARCHAR(12)  NULL,
  tipo        VARCHAR(20)  NOT NULL DEFAULT 'cliente',
  criado_em   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_chave_whats (chave_whats)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Conferência (rode separado, se quiser)
-- SELECT id, nome, telefone, chave_whats, tipo FROM contatos ORDER BY chave_whats IS NULL DESC, nome;

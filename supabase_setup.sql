-- COMANDO SQL PARA CRIAR AS TABELAS NO SUPABASE
-- Cole todo esse texto no "SQL Editor" do Supabase e clique em "Run" (Executar)

-- 1. Cria a tabela para o Histórico de Cargas
CREATE TABLE IF NOT EXISTS historico_cargas (
  id uuid default uuid_generate_v4() primary key,
  exercicio_id text not null,
  carga numeric not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Cria a tabela para as Receitas
CREATE TABLE IF NOT EXISTS receitas (
  id uuid default uuid_generate_v4() primary key,
  titulo text not null,
  url_link text,
  notas text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. Cria a tabela para as Conquistas
CREATE TABLE IF NOT EXISTS conquistas (
  id uuid default uuid_generate_v4() primary key,
  texto_conquista text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

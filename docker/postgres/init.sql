CREATE TABLE public.propriedades_aluguel (
	titulo text NULL,
	tipo varchar(20) NULL,
	subtipo _varchar NULL,
	valor float4 NULL,
	iptu float4 NULL,
	condominio float4 NULL,
	quartos int4 NULL,
	area int4 NULL,
	vagas_garagem int4 NULL,
	banheiros int4 NULL,
	cidade varchar(100) NULL,
	bairro varchar(100) NULL,
	regiao varchar(100) NULL,
	"data" date NULL,
	hash text NULL
);

CREATE TABLE public.propriedades_venda (
	titulo text NULL,
	tipo varchar(20) NULL,
	subtipo _varchar NULL,
	valor float4 NULL,
	iptu float4 NULL,
	condominio float4 NULL,
	quartos int4 NULL,
	area int4 NULL,
	vagas_garagem int4 NULL,
	banheiros int4 NULL,
	cidade varchar(100) NULL,
	bairro varchar(100) NULL,
	regiao varchar(100) NULL,
	"data" date NULL,
	hash text NULL
);

CREATE OR REPLACE FUNCTION public.calculate_hash_aluguel(new_row propriedades_aluguel)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    non_hash_fields text;
BEGIN
    non_hash_fields := COALESCE(new_row.titulo, '') || 
                       COALESCE(new_row.tipo, '') || 
                       COALESCE(new_row.valor::text, '') || 
                       COALESCE(new_row.iptu::text, '') || 
                       COALESCE(new_row.condominio::text, '') || 
                       COALESCE(new_row.quartos::text, '') || 
                       COALESCE(new_row.area::text, '') || 
                       COALESCE(new_row.vagas_garagem::text, '') || 
                       COALESCE(new_row.banheiros::text, '') || 
                       COALESCE(new_row.cidade, '') || 
                       COALESCE(new_row.bairro, '') || 
                       COALESCE(new_row.regiao, '') || 
                       COALESCE(new_row.data::text, '');

    RETURN MD5(non_hash_fields);
END;
$function$
;

CREATE OR REPLACE FUNCTION public.calculate_hash_venda(new_row propriedades_venda)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    non_hash_fields text;
BEGIN
    non_hash_fields := COALESCE(new_row.titulo, '') || 
                       COALESCE(new_row.tipo, '') || 
                       COALESCE(new_row.valor::text, '') || 
                       COALESCE(new_row.iptu::text, '') || 
                       COALESCE(new_row.condominio::text, '') || 
                       COALESCE(new_row.quartos::text, '') || 
                       COALESCE(new_row.area::text, '') || 
                       COALESCE(new_row.vagas_garagem::text, '') || 
                       COALESCE(new_row.banheiros::text, '') || 
                       COALESCE(new_row.cidade, '') || 
                       COALESCE(new_row.bairro, '') || 
                       COALESCE(new_row.regiao, '') || 
                       COALESCE(new_row.data::text, '');

    RETURN MD5(non_hash_fields);
END;
$function$
;

CREATE OR REPLACE FUNCTION public.prevent_duplicate_entry_aluguel()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
    existing_hash text;
    existing_subtipo varchar(100)[]; 
BEGIN
    NEW.hash := calculate_hash_aluguel(NEW);

    SELECT hash, subtipo
    INTO existing_hash, existing_subtipo
    FROM public.propriedades_aluguel
    WHERE hash = NEW.hash;

    IF existing_hash IS NOT NULL THEN
        IF (existing_subtipo @> NEW.subtipo or 'padrão' = ANY(NEW.subtipo)) THEN
            RETURN NULL;
        ELSE
            IF 'padrão' = ANY(existing_subtipo) THEN
                existing_subtipo := NEW.subtipo;
            ELSE
                existing_subtipo := existing_subtipo || NEW.subtipo;
            END IF;

            UPDATE public.propriedades_aluguel
            SET subtipo = existing_subtipo
            WHERE hash = existing_hash;

            RETURN NULL;
        END IF;
    END IF;

    RETURN NEW;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.prevent_duplicate_entry_venda()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
    existing_hash text;
    existing_subtipo varchar(100)[]; 
BEGIN
    NEW.hash := calculate_hash_venda(NEW);

    SELECT hash, subtipo
    INTO existing_hash, existing_subtipo
    FROM public.propriedades_venda
    WHERE hash = NEW.hash;

    IF existing_hash IS NOT NULL THEN
        IF (existing_subtipo @> NEW.subtipo or 'padrão' = ANY(NEW.subtipo)) THEN
            RETURN NULL;
        ELSE
            IF 'padrão' = ANY(existing_subtipo) THEN
                existing_subtipo := NEW.subtipo;
            ELSE
                existing_subtipo := existing_subtipo || NEW.subtipo;
            END IF;

            UPDATE public.propriedades_venda
            SET subtipo = existing_subtipo
            WHERE hash = existing_hash;

            RETURN NULL;
        END IF;
    END IF;

    RETURN NEW;
END;
$function$
;

create trigger prevent_duplicate_entry_trigger_venda before
insert
    on
    public.propriedades_venda for each row execute function prevent_duplicate_entry_venda();

create trigger prevent_duplicate_entry_trigger_aluguel before
insert
    on
    public.propriedades_aluguel for each row execute function prevent_duplicate_entry_aluguel();
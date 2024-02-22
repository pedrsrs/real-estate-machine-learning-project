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
    anuncio_data text NULL,
	anuncio_id text NULL,
    link text null,
    coleta_data date NULL
);
CREATE UNIQUE INDEX idx_aluguel_anuncio_id ON propriedades_aluguel (anuncio_id);
CREATE INDEX idx_aluguel_data ON propriedades_aluguel (anuncio_data);
CREATE INDEX idx_aluguel_valor ON propriedades_aluguel (valor);

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
    anuncio_data text NULL,
	anuncio_id text NULL,
    link text null,
    coleta_data date NULL
);
CREATE UNIQUE INDEX idx_venda_anuncio_id ON propriedades_venda (anuncio_id);
CREATE INDEX idx_venda_data ON propriedades_venda (anuncio_data);
CREATE INDEX idx_venda_valor ON propriedades_venda (valor);

CREATE OR REPLACE FUNCTION public.prevent_duplicate_entry_aluguel()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
    existing_id text;
    existing_subtipo varchar(100)[]; 
BEGIN

    SELECT anuncio_id, subtipo
    INTO existing_id, existing_subtipo
    FROM public.propriedades_aluguel
    WHERE anuncio_id = NEW.anuncio_id;

    IF existing_id IS NOT NULL THEN
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
            WHERE anuncio_id = existing_id;

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
    existing_id text;
    existing_subtipo varchar(100)[]; 
BEGIN

    SELECT anuncio_id, subtipo
    INTO existing_id, existing_subtipo
    FROM public.propriedades_venda
    WHERE anuncio_id = NEW.anuncio_id;

    IF existing_id IS NOT NULL THEN
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
            WHERE anuncio_id = existing_id;

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
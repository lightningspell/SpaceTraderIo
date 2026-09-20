-- Ausfuehrungsreihenfolge: 00 -> 01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 99
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE spacereset (
    reset_id    int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    started_at  timestamptz NOT NULL,
    ended_at    timestamptz,
    api_version text        NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT spacereset_ende_nach_start
        CHECK (ended_at IS NULL OR ended_at > started_at)
);

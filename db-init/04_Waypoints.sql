CREATE TABLE system (
    reset_id      int  NOT NULL,
    symbol        text NOT NULL,
    sector_symbol text NOT NULL,
    type          text NOT NULL,
    x             int  NOT NULL,
    y             int  NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, symbol),
    FOREIGN KEY (reset_id) REFERENCES spacereset (reset_id)
);

CREATE TABLE waypoint (
    reset_id        int  NOT NULL,
    symbol          text NOT NULL,
    system_symbol   text NOT NULL,
    type            text NOT NULL,
    x               int  NOT NULL,
    y               int  NOT NULL,
    orbits_waypoint text,                    
    created_at      timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, symbol),
    FOREIGN KEY (reset_id) REFERENCES spacereset (reset_id),
    FOREIGN KEY (reset_id, system_symbol)   REFERENCES system   (reset_id, symbol)
);

CREATE TABLE waypoint_trait (
    trait_symbol text PRIMARY KEY,
    name         text NOT NULL,
    description  text
);

CREATE TABLE waypoint_trait_link (
    reset_id        int       NOT NULL,
    waypoint_symbol text      NOT NULL,
    trait_symbol    text      NOT NULL,
    validity        tstzrange NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, waypoint_symbol, trait_symbol, validity),
    FOREIGN KEY (reset_id, waypoint_symbol) REFERENCES waypoint (reset_id, symbol),
    FOREIGN KEY (trait_symbol)              REFERENCES waypoint_trait (trait_symbol),
    EXCLUDE USING gist (
        reset_id        WITH =,
        waypoint_symbol WITH =,
        trait_symbol    WITH =,
        validity        WITH &&
    )
);

CREATE TABLE waypoint_state (
    reset_id              int       NOT NULL,
    waypoint_symbol       text      NOT NULL,
    validity              tstzrange NOT NULL,
    is_under_construction boolean   NOT NULL,
    faction_symbol        text,              
    charted_by_agent      text,              -- NULL = noch unkartiert
    created_at            timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, waypoint_symbol, validity),
    FOREIGN KEY (reset_id, waypoint_symbol)  REFERENCES waypoint (reset_id, symbol),
    FOREIGN KEY (reset_id, faction_symbol)   REFERENCES faction  (reset_id, symbol),
    FOREIGN KEY (reset_id, charted_by_agent) REFERENCES agent    (reset_id, symbol),
    EXCLUDE USING gist (
        reset_id        WITH =,
        waypoint_symbol WITH =,
        validity        WITH &&
    )
);

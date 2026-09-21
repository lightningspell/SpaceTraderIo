CREATE TABLE faction (
    reset_id      int  NOT NULL,
    symbol        text NOT NULL,
    name          text NOT NULL,
    description   text,
    hq_waypoint   text,
    isRecruiting boolean,
    created_at    timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, symbol),
    FOREIGN KEY (reset_id) REFERENCES spacereset (reset_id)
    -- FK auf waypoint siehe 99_constraints.sql (waypoint entsteht erst in 04)
);

CREATE TABLE faction_trait (
    trait_symbol      text PRIMARY KEY,
    trait_name        text NOT NULL,
    trait_description text
);

CREATE TABLE faction_trait_link (
    reset_id       int  NOT NULL,
    faction_symbol text NOT NULL,
    trait_symbol   text NOT NULL,
    created_at     timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, faction_symbol, trait_symbol),
    FOREIGN KEY (reset_id, faction_symbol) REFERENCES faction (reset_id, symbol),
    FOREIGN KEY (trait_symbol)             REFERENCES faction_trait (trait_symbol)
);

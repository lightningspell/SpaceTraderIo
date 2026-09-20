CREATE TABLE ship (
    reset_id       int  NOT NULL,
    ship_symbol    text NOT NULL,
    agent_symbol   text,
    faction_symbol text,
    type           text NOT NULL,
    name           text NOT NULL,
    created_at     timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, ship_symbol),
    FOREIGN KEY (reset_id) REFERENCES spacereset (reset_id),
    FOREIGN KEY (reset_id, agent_symbol)   REFERENCES agent   (reset_id, symbol),
    FOREIGN KEY (reset_id, faction_symbol) REFERENCES faction (reset_id, symbol)
);

-- Katalog mit Diskriminator statt fuenf fast gleicher Tabellen.
CREATE TABLE component (
    component_symbol  text PRIMARY KEY,
    kind              text NOT NULL,
    name              text NOT NULL,
    description       text,
    power_requirement int,
    crew_requirement  int,
    slot_requirement  int,
    attribute         jsonb,
    CONSTRAINT component_kind_gueltig
        CHECK (kind IN ('FRAME', 'REACTOR', 'ENGINE', 'MODULE', 'MOUNT'))
);

CREATE TABLE ship_component_install (
    reset_id         int       NOT NULL,
    ship_symbol      text      NOT NULL,
    slot_kind        text      NOT NULL,
    slot_index       int       NOT NULL,
    validity         tstzrange NOT NULL,
    component_symbol text      NOT NULL,
    condition        numeric,              -- API: Dezimalwert 0..1
    integrity        numeric,              -- API: Dezimalwert 0..1
    created_at       timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, ship_symbol, slot_kind, slot_index, validity),
    FOREIGN KEY (reset_id, ship_symbol) REFERENCES ship (reset_id, ship_symbol),
    FOREIGN KEY (component_symbol)      REFERENCES component (component_symbol),
    EXCLUDE USING gist (
        reset_id    WITH =,
        ship_symbol WITH =,
        slot_kind   WITH =,
        slot_index  WITH =,
        validity    WITH &&
    )
);

CREATE TABLE ship_state (
    reset_id            int  NOT NULL,
    ship_symbol         text NOT NULL,
    observed_at         timestamptz NOT NULL,
    nav_status          text NOT NULL,
    flight_mode         text NOT NULL,
    nav_waypoint        text NOT NULL,
    fuel_current        int  NOT NULL,
    fuel_capacity       int  NOT NULL,
    cargo_units         int  NOT NULL,
    cargo_capacity      int  NOT NULL,
    crew_current        int  NOT NULL,
    crew_morale         int,
    cooldown_expires_at timestamptz,       -- NULL = kein Cooldown aktiv
    created_at          timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, ship_symbol, observed_at),
    FOREIGN KEY (reset_id, ship_symbol)  REFERENCES ship (reset_id, ship_symbol),
    FOREIGN KEY (reset_id, nav_waypoint) REFERENCES waypoint (reset_id, symbol)
);

-- Detail zum Snapshot: haengt am ship_state, nicht am ship.
CREATE TABLE ship_cargo_item (
    reset_id     int  NOT NULL,
    ship_symbol  text NOT NULL,
    observed_at  timestamptz NOT NULL,
    trade_symbol text NOT NULL,
    units        int  NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, ship_symbol, observed_at, trade_symbol),
    FOREIGN KEY (reset_id, ship_symbol, observed_at)
        REFERENCES ship_state (reset_id, ship_symbol, observed_at),
    FOREIGN KEY (trade_symbol) REFERENCES trade_good (trade_symbol)
);

CREATE TABLE ship_nav_leg (
    reset_id           int  NOT NULL,
    ship_symbol        text NOT NULL,
    departure_waypoint text NOT NULL,
    departure_time     timestamptz NOT NULL,
    arrival_waypoint   text NOT NULL,
    arrival_time       timestamptz,
    flight_mode        text,
    created_at         timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, ship_symbol, departure_time),
    FOREIGN KEY (reset_id, ship_symbol)        REFERENCES ship (reset_id, ship_symbol),
    FOREIGN KEY (reset_id, departure_waypoint) REFERENCES waypoint (reset_id, symbol),
    FOREIGN KEY (reset_id, arrival_waypoint)   REFERENCES waypoint (reset_id, symbol),
    CONSTRAINT ship_nav_leg_ankunft_nach_abflug
        CHECK (arrival_time IS NULL OR arrival_time >= departure_time)
);

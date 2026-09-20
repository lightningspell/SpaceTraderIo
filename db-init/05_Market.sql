CREATE TABLE trade_good (
    trade_symbol text PRIMARY KEY,
    name         text NOT NULL,
    description  text
);

CREATE TABLE market (
    reset_id        int  NOT NULL,
    waypoint_symbol text NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, waypoint_symbol),
    FOREIGN KEY (reset_id) REFERENCES spacereset (reset_id),
    FOREIGN KEY (reset_id, waypoint_symbol) REFERENCES waypoint (reset_id, symbol)
);

CREATE TABLE market_listing (
    reset_id        int       NOT NULL,
    waypoint_symbol text      NOT NULL,
    trade_symbol    text      NOT NULL,
    validity        tstzrange NOT NULL,
    role            text      NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, waypoint_symbol, trade_symbol, validity),
    FOREIGN KEY (reset_id, waypoint_symbol) REFERENCES market (reset_id, waypoint_symbol),
    FOREIGN KEY (trade_symbol)              REFERENCES trade_good (trade_symbol),
    EXCLUDE USING gist (
        reset_id        WITH =,
        waypoint_symbol WITH =,
        trade_symbol    WITH =,
        validity        WITH &&
    )
);

CREATE TABLE market_observation (
    reset_id                int  NOT NULL,
    waypoint_symbol         text NOT NULL,
    trade_symbol            text NOT NULL,
    observed_at             timestamptz NOT NULL,
    purchase_price_per_unit int  NOT NULL,
    sell_price_per_unit     int  NOT NULL,
    supply                  text,            -- SCARCE / LIMITED / MODERATE / HIGH / ABUNDANT
    activity                text,            -- WEAK / GROWING / STRONG / RESTRICTED
    trade_volume            int  NOT NULL,
    created_at              timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, waypoint_symbol, trade_symbol, observed_at),
    FOREIGN KEY (reset_id, waypoint_symbol) REFERENCES market (reset_id, waypoint_symbol),
    FOREIGN KEY (trade_symbol)              REFERENCES trade_good (trade_symbol)
);

CREATE TABLE market_transaction (
    reset_id         int  NOT NULL,
    waypoint_symbol  text NOT NULL,
    ship_symbol      text NOT NULL,
    trade_symbol     text NOT NULL,
    transaction_at   timestamptz NOT NULL, 
    transaction_type text NOT NULL,
    units            int    NOT NULL,
    price_per_unit   int    NOT NULL,
    total_price      bigint NOT NULL,
    created_at       timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, waypoint_symbol, ship_symbol, trade_symbol, transaction_at),
    FOREIGN KEY (reset_id, waypoint_symbol) REFERENCES market (reset_id, waypoint_symbol),
    FOREIGN KEY (trade_symbol)              REFERENCES trade_good (trade_symbol),
    CONSTRAINT market_transaction_typ_gueltig
        CHECK (transaction_type IN ('PURCHASE', 'SELL'))
    -- FK auf ship siehe 99_constraints.sql (ship entsteht erst in 06)
);

CREATE TABLE shipyard (
    reset_id        int  NOT NULL,
    waypoint_symbol text NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, waypoint_symbol),
    FOREIGN KEY (reset_id) REFERENCES spacereset (reset_id),
    FOREIGN KEY (reset_id, waypoint_symbol) REFERENCES waypoint (reset_id, symbol)
);

CREATE TABLE shipyard_observation (
    reset_id        int  NOT NULL,
    waypoint_symbol text NOT NULL,
    ship_type       text NOT NULL,
    observed_at     timestamptz NOT NULL,
    purchase_price  int  NOT NULL,
    supply          text,
    activity        text,
    created_at      timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, waypoint_symbol, ship_type, observed_at),
    FOREIGN KEY (reset_id, waypoint_symbol) REFERENCES shipyard (reset_id, waypoint_symbol)
);

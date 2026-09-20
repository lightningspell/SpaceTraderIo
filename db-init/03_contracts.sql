CREATE TABLE contract (
    reset_id             int  NOT NULL,
    contract_id          text NOT NULL,         
    faction_symbol       text NOT NULL,
    agent_symbol         text NOT NULL,
    type                 text NOT NULL,
    deadline_to_accept   timestamptz,
    deadline_to_fulfill  timestamptz,
    payment_on_accept    bigint NOT NULL,
    payment_on_fulfill   bigint NOT NULL,
    accepted_at          timestamptz,            -- NULL = noch nicht angenommen
    fulfilled_at         timestamptz,            -- NULL = noch nicht erfuellt
    created_at           timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, contract_id),
    FOREIGN KEY (reset_id) REFERENCES spacereset (reset_id),
    FOREIGN KEY (reset_id, faction_symbol) REFERENCES faction (reset_id, symbol),
    FOREIGN KEY (reset_id, agent_symbol)   REFERENCES agent   (reset_id, symbol),
    CONSTRAINT contract_erfuellt_nach_annahme
        CHECK (fulfilled_at IS NULL OR accepted_at IS NOT NULL)
);

CREATE TABLE contract_deliver_good (
    reset_id             int  NOT NULL,
    contract_id          text NOT NULL,
    trade_symbol         text NOT NULL,
    destination_waypoint text NOT NULL,
    units_required       int  NOT NULL,
    created_at           timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, contract_id, trade_symbol),
    FOREIGN KEY (reset_id, contract_id) REFERENCES contract (reset_id, contract_id)
    -- FKs auf trade_good (05) und waypoint (04) siehe 99_constraints.sql
);

CREATE TABLE contract_delivery_progress (
    reset_id        int  NOT NULL,
    contract_id     text NOT NULL,
    trade_symbol    text NOT NULL,
    observed_at     timestamptz NOT NULL,
    units_fulfilled int  NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now(),
    -- observed_at MUSS in den Schluessel, sonst ist es keine Messreihe.
    -- destination_waypoint entfaellt hier: steht schon in contract_deliver_good.
    PRIMARY KEY (reset_id, contract_id, trade_symbol, observed_at),
    FOREIGN KEY (reset_id, contract_id, trade_symbol)
        REFERENCES contract_deliver_good (reset_id, contract_id, trade_symbol)
);

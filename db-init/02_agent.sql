-- 02_agent.sql — Muster A (agent) + Muster B (agent_state)

CREATE TABLE agent (
    reset_id                int  NOT NULL,
    symbol                  text NOT NULL,
    agent_token             text NOT NULL,
    starting_faction_symbol text NOT NULL,
    hq_waypoint             text,
    created_at              timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, symbol),
    FOREIGN KEY (reset_id) REFERENCES spacereset (reset_id),
    FOREIGN KEY (reset_id, starting_faction_symbol)
        REFERENCES faction (reset_id, symbol)
    -- FK auf waypoint siehe 99_constraints.sql
);

CREATE TABLE agent_state (
    reset_id      int       NOT NULL,
    agent_symbol  text      NOT NULL,
    agent_credits bigint    NOT NULL,
    ship_count    int       NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (reset_id, agent_symbol),
    FOREIGN KEY (reset_id, agent_symbol) REFERENCES agent (reset_id, symbol)
);

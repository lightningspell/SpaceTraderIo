-- 99_constraints.sql — Fremdschluessel, die ueber Dateigrenzen zeigen

ALTER TABLE faction
    ADD CONSTRAINT faction_hq_waypoint_fkey
    FOREIGN KEY (reset_id, hq_waypoint) REFERENCES waypoint (reset_id, symbol);

ALTER TABLE agent
    ADD CONSTRAINT agent_hq_waypoint_fkey
    FOREIGN KEY (reset_id, hq_waypoint) REFERENCES waypoint (reset_id, symbol);

ALTER TABLE contract_deliver_good
    ADD CONSTRAINT contract_deliver_good_trade_symbol_fkey
    FOREIGN KEY (trade_symbol) REFERENCES trade_good (trade_symbol);

ALTER TABLE contract_deliver_good
    ADD CONSTRAINT contract_deliver_good_destination_fkey
    FOREIGN KEY (reset_id, destination_waypoint) REFERENCES waypoint (reset_id, symbol);

ALTER TABLE market_transaction
    ADD CONSTRAINT market_transaction_ship_fkey
    FOREIGN KEY (reset_id, ship_symbol) REFERENCES ship (reset_id, ship_symbol);

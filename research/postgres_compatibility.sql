-- Additive DeviceIQ research tables for the existing PostgreSQL database.
-- Review before applying. Existing application tables and data are untouched.
-- Run the idempotent importer only after this migration succeeds.


CREATE TABLE IF NOT EXISTS research_manufacturers (
  manufacturer_id TEXT PRIMARY KEY,
  manufacturer_name TEXT NOT NULL UNIQUE,
  official_website TEXT,
  country_of_origin TEXT,
  parent_company_id TEXT REFERENCES research_manufacturers(manufacturer_id) DEFERRABLE INITIALLY DEFERRED,
  verification_status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS research_brands (
  brand_id TEXT PRIMARY KEY,
  brand_name TEXT NOT NULL UNIQUE,
  canonical_brand_name TEXT NOT NULL,
  manufacturer_id TEXT REFERENCES research_manufacturers(manufacturer_id) DEFERRABLE INITIALLY DEFERRED,
  official_website TEXT,
  alternative_names TEXT,
  brand_status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS research_device_categories (
  category_id TEXT PRIMARY KEY,
  category_name TEXT NOT NULL UNIQUE,
  category_description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS research_device_models (
  device_id TEXT PRIMARY KEY,
  manufacturer_id TEXT REFERENCES research_manufacturers(manufacturer_id) DEFERRABLE INITIALLY DEFERRED,
  brand_id TEXT NOT NULL REFERENCES research_brands(brand_id) DEFERRABLE INITIALLY DEFERRED,
  category_id TEXT NOT NULL REFERENCES research_device_categories(category_id) DEFERRABLE INITIALLY DEFERRED,
  model_name TEXT NOT NULL,
  canonical_model_name TEXT,
  product_line TEXT,
  model_number TEXT,
  model_code TEXT,
  global_announcement_date TEXT,
  global_release_date TEXT,
  global_release_year INTEGER,
  operating_system TEXT,
  device_status TEXT NOT NULL DEFAULT 'PENDING_VERIFICATION',
  is_base_model INTEGER NOT NULL DEFAULT 1 CHECK (is_base_model IN (0,1)),
  description TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(category_id, brand_id, model_name)
);

CREATE TABLE IF NOT EXISTS research_data_sources (
  source_id TEXT PRIMARY KEY,
  source_title TEXT NOT NULL,
  publisher TEXT NOT NULL,
  source_url TEXT UNIQUE,
  source_type TEXT NOT NULL,
  publication_date TEXT,
  access_date TEXT NOT NULL,
  source_reliability TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS research_device_configurations (
  configuration_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES research_device_models(device_id) DEFERRABLE INITIALLY DEFERRED,
  configuration_name TEXT NOT NULL,
  sku TEXT,
  model_code TEXT,
  processor TEXT,
  chipset TEXT,
  cpu TEXT,
  gpu TEXT,
  ram_gb DOUBLE PRECISION,
  internal_storage_gb DOUBLE PRECISION,
  display_inches DOUBLE PRECISION,
  display_resolution TEXT,
  display_type TEXT,
  refresh_hz DOUBLE PRECISION,
  battery_mah DOUBLE PRECISION,
  battery_wh DOUBLE PRECISION,
  charging_w DOUBLE PRECISION,
  rear_camera_mp DOUBLE PRECISION,
  front_camera_mp DOUBLE PRECISION,
  operating_system TEXT,
  connectivity TEXT,
  weight_g DOUBLE PRECISION,
  dimensions TEXT,
  price_php DOUBLE PRECISION,
  price_condition TEXT,
  price_observed_at TEXT,
  price_source_id TEXT REFERENCES research_data_sources(source_id) DEFERRABLE INITIALLY DEFERRED,
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(device_id, configuration_name)
);

CREATE TABLE IF NOT EXISTS research_device_specifications (
  specification_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES research_device_models(device_id) DEFERRABLE INITIALLY DEFERRED,
  configuration_id TEXT REFERENCES research_device_configurations(configuration_id) DEFERRABLE INITIALLY DEFERRED,
  spec_key TEXT NOT NULL,
  value_text TEXT NOT NULL,
  numeric_value DOUBLE PRECISION,
  unit TEXT,
  source_id TEXT REFERENCES research_data_sources(source_id) DEFERRABLE INITIALLY DEFERRED,
  UNIQUE(device_id, configuration_id, spec_key)
);

CREATE TABLE IF NOT EXISTS research_philippines_market_releases (
  release_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL UNIQUE REFERENCES research_device_models(device_id) DEFERRABLE INITIALLY DEFERRED,
  philippine_release_date TEXT,
  release_date_precision TEXT NOT NULL,
  philippine_release_year INTEGER,
  availability_date TEXT,
  availability_observed_at TEXT,
  availability_status TEXT NOT NULL,
  official_launch_status TEXT NOT NULL,
  authorized_distributor TEXT,
  market_availability_evidence TEXT,
  research_cutoff_date TEXT NOT NULL,
  inclusion_status TEXT NOT NULL,
  exclusion_reason TEXT,
  verification_status TEXT NOT NULL,
  claimed_release_year INTEGER,
  primary_source_id TEXT REFERENCES research_data_sources(source_id) DEFERRABLE INITIALLY DEFERRED,
  reviewer_notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS research_device_source_evidence (
  evidence_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES research_device_models(device_id) DEFERRABLE INITIALLY DEFERRED,
  release_id TEXT REFERENCES research_philippines_market_releases(release_id) DEFERRABLE INITIALLY DEFERRED,
  source_id TEXT NOT NULL REFERENCES research_data_sources(source_id) DEFERRABLE INITIALLY DEFERRED,
  evidence_type TEXT NOT NULL,
  supported_claim TEXT NOT NULL,
  evidence_excerpt TEXT,
  verification_result TEXT NOT NULL,
  confidence_level TEXT,
  reviewer_notes TEXT,
  created_at TEXT NOT NULL,
  UNIQUE(device_id, source_id, evidence_type)
);

CREATE TABLE IF NOT EXISTS research_raw_research_claims (
  claim_id TEXT PRIMARY KEY,
  source_file TEXT NOT NULL,
  source_line INTEGER NOT NULL,
  raw_text TEXT NOT NULL,
  research_year INTEGER,
  original_brand_name TEXT,
  original_model_text TEXT,
  original_category TEXT,
  original_release_claim TEXT,
  original_source_reference TEXT,
  normalized_brand_id TEXT REFERENCES research_brands(brand_id) DEFERRABLE INITIALLY DEFERRED,
  normalized_device_id TEXT REFERENCES research_device_models(device_id) DEFERRABLE INITIALLY DEFERRED,
  processing_status TEXT NOT NULL,
  verification_status TEXT NOT NULL,
  duplicate_of TEXT REFERENCES research_raw_research_claims(claim_id) DEFERRABLE INITIALLY DEFERRED,
  reviewer_notes TEXT,
  UNIQUE(source_file, source_line)
);

CREATE TABLE IF NOT EXISTS research_research_queue (
  queue_id TEXT PRIMARY KEY,
  claim_id TEXT REFERENCES research_raw_research_claims(claim_id) DEFERRABLE INITIALLY DEFERRED,
  device_id TEXT REFERENCES research_device_models(device_id) DEFERRABLE INITIALLY DEFERRED,
  candidate_name TEXT NOT NULL,
  brand_name TEXT,
  category_id TEXT NOT NULL REFERENCES research_device_categories(category_id) DEFERRABLE INITIALLY DEFERRED,
  claimed_release_year INTEGER,
  missing_evidence TEXT NOT NULL,
  verification_issue TEXT NOT NULL,
  required_action TEXT NOT NULL,
  priority TEXT NOT NULL,
  current_status TEXT NOT NULL,
  reviewer_notes TEXT
);

CREATE TABLE IF NOT EXISTS research_excluded_records (
  exclusion_id TEXT PRIMARY KEY,
  raw_claim_id TEXT REFERENCES research_raw_research_claims(claim_id) DEFERRABLE INITIALLY DEFERRED,
  original_record TEXT NOT NULL,
  device_name TEXT,
  brand_name TEXT,
  category_id TEXT REFERENCES research_device_categories(category_id) DEFERRABLE INITIALLY DEFERRED,
  exclusion_reason TEXT NOT NULL,
  supporting_evidence TEXT,
  date_reviewed TEXT
);

CREATE TABLE IF NOT EXISTS research_audit_log (
  audit_id TEXT PRIMARY KEY,
  table_name TEXT NOT NULL,
  record_id TEXT NOT NULL,
  action TEXT NOT NULL,
  previous_value TEXT,
  new_value TEXT,
  change_reason TEXT NOT NULL,
  changed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS research_scope_settings (
  setting_key TEXT PRIMARY KEY,
  setting_value TEXT NOT NULL,
  description TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS research_idx_models_category_brand ON research_device_models(category_id, brand_id);
CREATE INDEX IF NOT EXISTS research_idx_models_canonical ON research_device_models(category_id, canonical_model_name);
CREATE INDEX IF NOT EXISTS research_idx_release_year_status ON research_philippines_market_releases(philippine_release_year, inclusion_status, verification_status);
CREATE INDEX IF NOT EXISTS research_idx_claims_year_category ON research_raw_research_claims(research_year, original_category);
CREATE INDEX IF NOT EXISTS research_idx_queue_priority ON research_research_queue(priority, current_status);
CREATE INDEX IF NOT EXISTS research_idx_evidence_device ON research_device_source_evidence(device_id);
CREATE INDEX IF NOT EXISTS research_idx_specs_key ON research_device_specifications(spec_key, numeric_value);
CREATE UNIQUE INDEX IF NOT EXISTS research_models_casefold_unique
ON research_device_models(category_id, brand_id, lower(model_name));

PRAGMA foreign_keys = ON;

CREATE TABLE manufacturers (
  manufacturer_id TEXT PRIMARY KEY,
  manufacturer_name TEXT NOT NULL UNIQUE,
  official_website TEXT,
  country_of_origin TEXT,
  parent_company_id TEXT REFERENCES manufacturers(manufacturer_id),
  verification_status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE brands (
  brand_id TEXT PRIMARY KEY,
  brand_name TEXT NOT NULL UNIQUE COLLATE NOCASE,
  canonical_brand_name TEXT NOT NULL,
  manufacturer_id TEXT REFERENCES manufacturers(manufacturer_id),
  official_website TEXT,
  alternative_names TEXT,
  brand_status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE device_categories (
  category_id TEXT PRIMARY KEY,
  category_name TEXT NOT NULL UNIQUE,
  category_description TEXT NOT NULL
);

CREATE TABLE device_models (
  device_id TEXT PRIMARY KEY,
  manufacturer_id TEXT REFERENCES manufacturers(manufacturer_id),
  brand_id TEXT NOT NULL REFERENCES brands(brand_id),
  category_id TEXT NOT NULL REFERENCES device_categories(category_id),
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
  UNIQUE(category_id, brand_id, model_name COLLATE NOCASE)
);

CREATE TABLE data_sources (
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

CREATE TABLE device_configurations (
  configuration_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES device_models(device_id),
  configuration_name TEXT NOT NULL,
  sku TEXT,
  model_code TEXT,
  processor TEXT,
  chipset TEXT,
  cpu TEXT,
  gpu TEXT,
  ram_gb REAL,
  internal_storage_gb REAL,
  display_inches REAL,
  display_resolution TEXT,
  display_type TEXT,
  refresh_hz REAL,
  battery_mah REAL,
  battery_wh REAL,
  charging_w REAL,
  rear_camera_mp REAL,
  front_camera_mp REAL,
  operating_system TEXT,
  connectivity TEXT,
  weight_g REAL,
  dimensions TEXT,
  price_php REAL,
  price_condition TEXT,
  price_observed_at TEXT,
  price_source_id TEXT REFERENCES data_sources(source_id),
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(device_id, configuration_name)
);

CREATE TABLE device_specifications (
  specification_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES device_models(device_id),
  configuration_id TEXT REFERENCES device_configurations(configuration_id),
  spec_key TEXT NOT NULL,
  value_text TEXT NOT NULL,
  numeric_value REAL,
  unit TEXT,
  source_id TEXT REFERENCES data_sources(source_id),
  UNIQUE(device_id, configuration_id, spec_key)
);

CREATE TABLE philippines_market_releases (
  release_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL UNIQUE REFERENCES device_models(device_id),
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
  primary_source_id TEXT REFERENCES data_sources(source_id),
  reviewer_notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE device_source_evidence (
  evidence_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES device_models(device_id),
  release_id TEXT REFERENCES philippines_market_releases(release_id),
  source_id TEXT NOT NULL REFERENCES data_sources(source_id),
  evidence_type TEXT NOT NULL,
  supported_claim TEXT NOT NULL,
  evidence_excerpt TEXT,
  verification_result TEXT NOT NULL,
  confidence_level TEXT,
  reviewer_notes TEXT,
  created_at TEXT NOT NULL,
  UNIQUE(device_id, source_id, evidence_type)
);

CREATE TABLE raw_research_claims (
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
  normalized_brand_id TEXT REFERENCES brands(brand_id),
  normalized_device_id TEXT REFERENCES device_models(device_id),
  processing_status TEXT NOT NULL,
  verification_status TEXT NOT NULL,
  duplicate_of TEXT REFERENCES raw_research_claims(claim_id),
  reviewer_notes TEXT,
  UNIQUE(source_file, source_line)
);

CREATE TABLE research_queue (
  queue_id TEXT PRIMARY KEY,
  claim_id TEXT REFERENCES raw_research_claims(claim_id),
  device_id TEXT REFERENCES device_models(device_id),
  candidate_name TEXT NOT NULL,
  brand_name TEXT,
  category_id TEXT NOT NULL REFERENCES device_categories(category_id),
  claimed_release_year INTEGER,
  missing_evidence TEXT NOT NULL,
  verification_issue TEXT NOT NULL,
  required_action TEXT NOT NULL,
  priority TEXT NOT NULL,
  current_status TEXT NOT NULL,
  reviewer_notes TEXT
);

CREATE TABLE excluded_records (
  exclusion_id TEXT PRIMARY KEY,
  raw_claim_id TEXT REFERENCES raw_research_claims(claim_id),
  original_record TEXT NOT NULL,
  device_name TEXT,
  brand_name TEXT,
  category_id TEXT REFERENCES device_categories(category_id),
  exclusion_reason TEXT NOT NULL,
  supporting_evidence TEXT,
  date_reviewed TEXT
);

CREATE TABLE audit_log (
  audit_id TEXT PRIMARY KEY,
  table_name TEXT NOT NULL,
  record_id TEXT NOT NULL,
  action TEXT NOT NULL,
  previous_value TEXT,
  new_value TEXT,
  change_reason TEXT NOT NULL,
  changed_at TEXT NOT NULL
);

CREATE TABLE scope_settings (
  setting_key TEXT PRIMARY KEY,
  setting_value TEXT NOT NULL,
  description TEXT NOT NULL
);

CREATE INDEX idx_models_category_brand ON device_models(category_id, brand_id);
CREATE INDEX idx_models_canonical ON device_models(category_id, canonical_model_name);
CREATE INDEX idx_release_year_status ON philippines_market_releases(philippine_release_year, inclusion_status, verification_status);
CREATE INDEX idx_claims_year_category ON raw_research_claims(research_year, original_category);
CREATE INDEX idx_queue_priority ON research_queue(priority, current_status);
CREATE INDEX idx_evidence_device ON device_source_evidence(device_id);
CREATE INDEX idx_specs_key ON device_specifications(spec_key, numeric_value);

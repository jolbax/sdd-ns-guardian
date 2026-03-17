# US-4: Output Formats

## User Story
As a platform engineer, I want to choose between table, JSON, and YAML output formats, so I can integrate the tool with other automation.

## Acceptance Criteria
- [ ] A `--format` / `-f` flag accepts: `table` (default), `json`, `yaml`
- [ ] JSON output is a list of objects with keys: `namespace`, `resource_quota`, `limit_range`, `network_policy`, `compliant`
- [ ] YAML output has the same structure as JSON
- [ ] Table output remains the default and uses `rich` formatting
- [ ] JSON and YAML output goes to stdout cleanly (no extra decoration) so it can be piped

## Technical Notes
- Use `json.dumps` with `indent=2` for JSON output
- Use `yaml.dump` with `default_flow_style=False` for YAML output
- Use `rich.table.Table` with header style "bold cyan" for table output
- JSON and YAML should not include the summary line (only the data)

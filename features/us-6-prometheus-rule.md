# US-6: PrometheusRule YAML Generation

## User Story
As a platform engineer, I want to generate a PrometheusRule YAML that alerts on non-compliant namespaces, so I can integrate compliance checking into my monitoring stack.

## Acceptance Criteria
- [ ] A `generate-alert` subcommand outputs a PrometheusRule YAML to stdout
- [ ] The PrometheusRule contains one alert: `NamespaceMissingComplianceResources`
- [ ] Alert severity label: `warning`
- [ ] Alert includes the namespace name in labels
- [ ] The generated YAML is valid for OpenShift's monitoring stack (uses `monitoring.coreos.com/v1` API)
- [ ] A `--output` / `-o` flag allows writing to a file instead of stdout
- [ ] Works without cluster access (generates a static template)

## Technical Notes
- Use `monitoring.coreos.com/v1` API version for the PrometheusRule
- The alert is a static PromQL template that references `{{ $labels.namespace }}` at evaluation time
- Use `yaml.dump` to generate the YAML output
- The `--output` flag should write to the specified file path
- No cluster access is needed — this generates a template, not runtime data

"""Tests for the PrometheusRule generator."""

import yaml
from typer.testing import CliRunner

from ns_guardian.main import app
from ns_guardian.prometheus import generate_prometheus_rule

runner = CliRunner()


class TestGenerateAlertCommand:
    """Tests for the generate-alert CLI command."""

    def test_generate_alert_exits_0(self) -> None:
        """The generate-alert command should exit 0."""
        result = runner.invoke(app, ["generate-alert"])
        assert result.exit_code == 0

    def test_generate_alert_outputs_valid_yaml(self) -> None:
        """The output should be valid YAML."""
        result = runner.invoke(app, ["generate-alert"])
        data = yaml.safe_load(result.output)
        assert isinstance(data, dict)

    def test_generate_alert_has_correct_api_version(self) -> None:
        """The output should have the correct apiVersion."""
        result = runner.invoke(app, ["generate-alert"])
        data = yaml.safe_load(result.output)
        assert data["apiVersion"] == "monitoring.coreos.com/v1"

    def test_generate_alert_has_correct_kind(self) -> None:
        """The output should have kind PrometheusRule."""
        result = runner.invoke(app, ["generate-alert"])
        data = yaml.safe_load(result.output)
        assert data["kind"] == "PrometheusRule"

    def test_generate_alert_has_alert_name(self) -> None:
        """The alert should be named NamespaceMissingComplianceResources."""
        result = runner.invoke(app, ["generate-alert"])
        data = yaml.safe_load(result.output)
        rules = data["spec"]["groups"][0]["rules"]
        assert len(rules) == 1
        assert rules[0]["alert"] == "NamespaceMissingComplianceResources"

    def test_generate_alert_has_warning_severity(self) -> None:
        """The alert should have severity warning."""
        result = runner.invoke(app, ["generate-alert"])
        data = yaml.safe_load(result.output)
        rules = data["spec"]["groups"][0]["rules"]
        assert rules[0]["labels"]["severity"] == "warning"

    def test_generate_alert_references_namespace(self) -> None:
        """The alert should reference namespace in annotations."""
        result = runner.invoke(app, ["generate-alert"])
        data = yaml.safe_load(result.output)
        rules = data["spec"]["groups"][0]["rules"]
        annotations = rules[0]["annotations"]
        assert "namespace" in annotations["summary"]

    def test_generate_alert_has_expr(self) -> None:
        """The alert should have a PromQL expression."""
        result = runner.invoke(app, ["generate-alert"])
        data = yaml.safe_load(result.output)
        rules = data["spec"]["groups"][0]["rules"]
        assert "expr" in rules[0]
        assert "namespace" in rules[0]["expr"]

    def test_generate_alert_write_to_file(self, tmp_path) -> None:
        """The -o flag should write to a file."""
        output_file = tmp_path / "rule.yaml"
        result = runner.invoke(app, ["generate-alert", "-o", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()
        data = yaml.safe_load(output_file.read_text())
        assert data["kind"] == "PrometheusRule"

    def test_generate_alert_help(self) -> None:
        """Help should be available for generate-alert."""
        result = runner.invoke(app, ["generate-alert", "--help"])
        assert "--output" in result.output


class TestPrometheusModule:
    """Tests for the prometheus module directly."""

    def test_generate_prometheus_rule_returns_yaml(self) -> None:
        """The function should return a valid YAML string."""
        yaml_str = generate_prometheus_rule()
        data = yaml.safe_load(yaml_str)
        assert data["apiVersion"] == "monitoring.coreos.com/v1"
        assert data["kind"] == "PrometheusRule"

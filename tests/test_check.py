"""Tests for the check command using mock data."""

from typer.testing import CliRunner

from ns_guardian.filters import filter_results, is_system_namespace
from ns_guardian.main import app
from ns_guardian.mock import get_mock_data
from ns_guardian.models import NamespaceCheckResult

runner = CliRunner()


class TestCheckCommand:
    """Tests for the check CLI command."""

    def test_check_dry_run_succeeds(self) -> None:
        """The check command with --dry-run should exit 0."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert result.exit_code == 0

    def test_check_dry_run_shows_mock_message(self) -> None:
        """The check command with --dry-run should show the dry-run message."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "Running in dry-run mode with mock data" in result.output

    def test_check_dry_run_filters_system_by_default(self) -> None:
        """By default, system namespaces should not appear."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "kube-system" not in result.output
        assert "kube-public" not in result.output
        assert "openshift-monitoring" not in result.output

    def test_check_dry_run_shows_tenant_namespaces(self) -> None:
        """Tenant namespaces should appear by default."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "team-alpha" in result.output
        assert "team-beta" in result.output
        assert "staging" in result.output

    def test_check_dry_run_include_system(self) -> None:
        """--include-system should show all 8 namespaces."""
        result = runner.invoke(app, ["check", "--dry-run", "--include-system"])
        assert "kube-system" in result.output
        assert "openshift-monitoring" in result.output
        assert "team-alpha" in result.output
        assert "8" in result.output  # "X of 8 namespaces compliant"

    def test_check_dry_run_single_namespace(self) -> None:
        """--namespace should show only the specified namespace."""
        result = runner.invoke(app, ["check", "--dry-run", "-n", "team-alpha"])
        assert "team-alpha" in result.output
        assert "team-beta" not in result.output
        assert "1 of 1 namespaces compliant" in result.output

    def test_check_dry_run_shows_all_columns(self) -> None:
        """The check command should display all three check columns."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "ResourceQuota" in result.output
        assert "LimitRange" in result.output
        assert "NetworkPolicy" in result.output

    def test_check_dry_run_shows_summary(self) -> None:
        """The check command should display the compliance summary."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "namespaces compliant" in result.output

    def test_check_dry_run_filtered_summary_count(self) -> None:
        """Summary should reflect filtered results (2 of 5 tenant namespaces)."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "2 of 5 namespaces compliant" in result.output

    def test_check_help_shows_all_flags(self) -> None:
        """All flags should appear in help output."""
        result = runner.invoke(app, ["check", "--help"])
        assert "--dry-run" in result.output
        assert "--kubeconfig" in result.output
        assert "--include-system" in result.output
        assert "--namespace" in result.output


class TestFilters:
    """Tests for namespace filtering."""

    def test_is_system_namespace_exact_matches(self) -> None:
        """Exact system namespaces should be detected."""
        assert is_system_namespace("kube-system") is True
        assert is_system_namespace("kube-public") is True
        assert is_system_namespace("kube-node-lease") is True
        assert is_system_namespace("default") is True

    def test_is_system_namespace_prefix_match(self) -> None:
        """OpenShift namespaces should be detected by prefix."""
        assert is_system_namespace("openshift-monitoring") is True
        assert is_system_namespace("openshift-ingress") is True

    def test_is_not_system_namespace(self) -> None:
        """Tenant namespaces should not be detected as system."""
        assert is_system_namespace("team-alpha") is False
        assert is_system_namespace("staging") is False

    def test_filter_excludes_system_by_default(self) -> None:
        """Filtering should exclude system namespaces by default."""
        data = get_mock_data()
        filtered = filter_results(data)
        names = [r.name for r in filtered]
        assert "kube-system" not in names
        assert "openshift-monitoring" not in names
        assert "team-alpha" in names

    def test_filter_includes_system_when_requested(self) -> None:
        """include_system=True should return all namespaces."""
        data = get_mock_data()
        filtered = filter_results(data, include_system=True)
        assert len(filtered) == 8

    def test_filter_single_namespace(self) -> None:
        """namespace parameter should return only that namespace."""
        data = get_mock_data()
        filtered = filter_results(data, namespace="team-alpha")
        assert len(filtered) == 1
        assert filtered[0].name == "team-alpha"

    def test_filter_single_namespace_not_found(self) -> None:
        """namespace parameter for non-existent namespace returns empty list."""
        data = get_mock_data()
        filtered = filter_results(data, namespace="nonexistent")
        assert len(filtered) == 0


class TestMockData:
    """Tests for the mock data provider."""

    def test_mock_data_returns_8_namespaces(self) -> None:
        """Mock data should contain 8 namespaces."""
        data = get_mock_data()
        assert len(data) == 8

    def test_mock_data_returns_namespace_check_results(self) -> None:
        """Mock data should return NamespaceCheckResult instances."""
        data = get_mock_data()
        for item in data:
            assert isinstance(item, NamespaceCheckResult)

    def test_mock_data_includes_system_namespaces(self) -> None:
        """Mock data should include system namespaces for filtering demo."""
        data = get_mock_data()
        names = [d.name for d in data]
        assert "kube-system" in names
        assert "kube-public" in names
        assert "openshift-monitoring" in names

    def test_mock_data_compliance_status(self) -> None:
        """Mock data should have expected compliance states."""
        data = get_mock_data()
        by_name = {d.name: d for d in data}
        assert by_name["team-alpha"].compliant is True
        assert by_name["team-beta"].compliant is False
        assert by_name["team-gamma"].compliant is False
        assert by_name["team-delta"].compliant is False
        assert by_name["staging"].compliant is True


class TestModels:
    """Tests for data models."""

    def test_compliant_when_all_resources(self) -> None:
        """A namespace with all resources should be compliant."""
        result = NamespaceCheckResult(name="test", resource_quota=True, limit_range=True, network_policy=True)
        assert result.compliant is True

    def test_not_compliant_when_missing_quota(self) -> None:
        """A namespace without a ResourceQuota should not be compliant."""
        result = NamespaceCheckResult(name="test", resource_quota=False, limit_range=True, network_policy=True)
        assert result.compliant is False

    def test_not_compliant_when_missing_limit_range(self) -> None:
        """A namespace without a LimitRange should not be compliant."""
        result = NamespaceCheckResult(name="test", resource_quota=True, limit_range=False, network_policy=True)
        assert result.compliant is False

    def test_not_compliant_when_missing_network_policy(self) -> None:
        """A namespace without a NetworkPolicy should not be compliant."""
        result = NamespaceCheckResult(name="test", resource_quota=True, limit_range=True, network_policy=False)
        assert result.compliant is False

    def test_not_compliant_when_all_missing(self) -> None:
        """A namespace with no resources should not be compliant."""
        result = NamespaceCheckResult(name="test", resource_quota=False, limit_range=False, network_policy=False)
        assert result.compliant is False

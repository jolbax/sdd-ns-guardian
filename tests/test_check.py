"""Tests for the check command using mock data."""

from typer.testing import CliRunner

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

    def test_check_dry_run_shows_namespaces(self) -> None:
        """The check command with --dry-run should display namespace names."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "team-alpha" in result.output
        assert "team-beta" in result.output
        assert "kube-system" in result.output

    def test_check_dry_run_shows_all_columns(self) -> None:
        """The check command should display all three check columns."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "ResourceQuota" in result.output
        assert "LimitRange" in result.output
        assert "NetworkPolicy" in result.output

    def test_check_dry_run_shows_yes_no(self) -> None:
        """The check command should show Yes/No for each resource."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "Yes" in result.output
        assert "No" in result.output

    def test_check_dry_run_shows_summary(self) -> None:
        """The check command should display the compliance summary."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "of" in result.output
        assert "namespaces compliant" in result.output

    def test_check_dry_run_summary_count(self) -> None:
        """The summary should show correct compliant count (4 of 8)."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "4 of 8 namespaces compliant" in result.output

    def test_check_help_shows_dry_run(self) -> None:
        """The --dry-run flag should appear in help output."""
        result = runner.invoke(app, ["check", "--help"])
        assert "--dry-run" in result.output

    def test_check_help_shows_kubeconfig(self) -> None:
        """The --kubeconfig flag should appear in help output."""
        result = runner.invoke(app, ["check", "--help"])
        assert "--kubeconfig" in result.output


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

    def test_mock_data_has_expected_namespaces(self) -> None:
        """Mock data should include expected namespace names."""
        data = get_mock_data()
        names = [d.name for d in data]
        assert "team-alpha" in names
        assert "kube-system" in names
        assert "staging" in names

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

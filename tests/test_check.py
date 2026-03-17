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

    def test_check_dry_run_shows_quota_status(self) -> None:
        """The check command with --dry-run should show Yes/No for ResourceQuota."""
        result = runner.invoke(app, ["check", "--dry-run"])
        assert "Yes" in result.output
        assert "No" in result.output

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


class TestModels:
    """Tests for data models."""

    def test_compliant_when_has_quota(self) -> None:
        """A namespace with a ResourceQuota should be compliant."""
        result = NamespaceCheckResult(name="test", resource_quota=True)
        assert result.compliant is True

    def test_not_compliant_when_no_quota(self) -> None:
        """A namespace without a ResourceQuota should not be compliant."""
        result = NamespaceCheckResult(name="test", resource_quota=False)
        assert result.compliant is False

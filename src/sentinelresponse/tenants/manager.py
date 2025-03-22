from sentinelresponse.logmanager.log_manager import LogManager
from sentinelresponse.tenants.models import Tenant


class NotFoundError(Exception):
    """Exception raised when a tenant is not found."""

    def __init__(self, message: str):
        super().__init__(message)


class TenantManager:
    """Manages tenants with full CRUD operations.

    Stores Tenant objects in an internal dictionary keyed by tenant_id.
    """

    def __init__(self):
        """Initialize the TenantManager with empty storage."""
        self.tenants: dict[int, Tenant] = {}
        self.logger = LogManager.get_logger()

    def create_tenant(self, tenant: Tenant) -> None:
        """Create a new tenant or overwrite an existing one."""
        self.logger.info(f"Creating tenant: {tenant}")
        self.tenants[tenant.tenant_id] = tenant

    def read_tenant(self, tenant_id: int) -> Tenant:
        """Retrieve a tenant by its unique identifier.

        Raises NotFoundError if not found.
        """
        if tenant_id in self.tenants:
            return self.tenants[tenant_id]

        message = f"Tenant {tenant_id} not found."
        self.logger.warning(message)
        raise NotFoundError(message)

    def read_all_tenants(self) -> list[Tenant]:
        """Retrieve all tenants currently stored."""
        tenants = list(self.tenants.values())
        self.logger.debug(f"Retrieved {len(tenants)} tenants")
        return tenants

    def update_tenant(self, tenant: Tenant) -> None:
        """Update an existing tenant.

        Raises NotFoundError if the tenant does not exist.
        """
        if tenant.tenant_id in self.tenants:
            self.logger.info(f"Updating tenant: {tenant}")
            self.tenants[tenant.tenant_id] = tenant
        else:
            message = f"Tenant {tenant.tenant_id} not found for update."
            self.logger.warning(message)
            raise NotFoundError(message)

    def delete_tenant(self, tenant_id: int) -> None:
        """Delete a tenant by its unique identifier.

        Raises NotFoundError if the tenant does not exist.
        """
        if tenant_id in self.tenants:
            self.logger.info(f"Deleting tenant id={tenant_id}")
            del self.tenants[tenant_id]
        else:
            message = f"Tenant {tenant_id} not found for deletion."
            self.logger.warning(message)
            raise NotFoundError(message)

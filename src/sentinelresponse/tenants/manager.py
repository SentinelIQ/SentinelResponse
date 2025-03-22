import logging

from sentinelresponse.tenants.models import Tenant


class NotFoundError(Exception):
    """Exception raised when a tenant is not found.

    This exception is used by TenantManager methods to indicate that a tenant with a
    specified identifier does not exist in the internal storage.

    Examples
    --------
    >>> try:
    ...     raise NotFoundError("Tenant 1 não encontrado.")
    ... except NotFoundError as e:
    ...     print(e)
    Tenant 1 não encontrado.

    """


class TenantManager:
    """Manages tenants with support for CRUD operations.

    This class provides methods to create, read, update, and delete Tenant objects.
    Tenants are stored in an internal dictionary, using their unique tenant_id as keys.

    Attributes
    ----------
    tenants : dict[int, Tenant]
        A dictionary mapping tenant IDs to Tenant objects.

    Examples
    --------
    >>> from sentinelresponse.tenants.models import Tenant
    >>> tm = TenantManager()
    >>> tenant = Tenant(tenant_id=1, name="Financeiro")
    >>> tm.create_tenant(tenant)
    >>> tm.read_tenant(1)
    Tenant(id=1, name='Financeiro')

    """

    def __init__(self):
        """Initialize the TenantManager with an empty dictionary for tenants.

        Examples
        --------
        >>> tm = TenantManager()
        >>> tm.tenants
        {}

        """
        self.tenants: dict[int, Tenant] = {}

    def create_tenant(self, tenant: Tenant) -> None:
        """Create a new tenant and add it to the manager.

        This method adds the provided Tenant object to the internal dictionary using its
        tenant_id as the key. If a tenant with the same tenant_id already exists, it will
        be overwritten.

        Parameters
        ----------
        tenant : Tenant
            The Tenant object to be created.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.tenants.models import Tenant
        >>> tm = TenantManager()
        >>> tenant = Tenant(tenant_id=1, name="Financeiro")
        >>> tm.create_tenant(tenant)

        """
        logging.info(f"Criando tenant: {tenant}")
        self.tenants[tenant.tenant_id] = tenant

    def read_tenant(self, tenant_id: int) -> Tenant:
        """Retrieve a tenant by its unique identifier.

        This method searches the internal dictionary for a Tenant with the given tenant_id.
        If found, the Tenant object is returned; otherwise, a NotFoundError is raised.

        Parameters
        ----------
        tenant_id : int
            The unique identifier of the tenant to retrieve.

        Returns
        -------
        Tenant
            The Tenant object associated with the specified tenant_id.

        Raises
        ------
        NotFoundError
            If no tenant with the specified tenant_id exists.

        Examples
        --------
        >>> from sentinelresponse.tenants.models import Tenant
        >>> tm = TenantManager()
        >>> tenant = Tenant(tenant_id=1, name="Financeiro")
        >>> tm.create_tenant(tenant)
        >>> tm.read_tenant(1)
        Tenant(id=1, name='Financeiro')

        """
        if tenant_id in self.tenants:
            return self.tenants[tenant_id]
        raise NotFoundError(f"Tenant {tenant_id} não encontrado.")

    def read_all_tenants(self) -> list[Tenant]:
        """Retrieve all tenants stored in the manager.

        Returns
        -------
        list[Tenant]
            A list of all Tenant objects currently managed.

        Examples
        --------
        >>> from sentinelresponse.tenants.models import Tenant
        >>> tm = TenantManager()
        >>> tm.create_tenant(Tenant(tenant_id=1, name="Financeiro"))
        >>> tm.create_tenant(Tenant(tenant_id=2, name="RH"))
        >>> len(tm.read_all_tenants())
        2

        """
        return list(self.tenants.values())

    def update_tenant(self, tenant: Tenant) -> None:
        """Update an existing tenant.

        This method updates the Tenant object in the internal dictionary that matches the
        tenant_id of the provided Tenant. If the tenant is not found, a NotFoundError is raised.

        Parameters
        ----------
        tenant : Tenant
            The updated Tenant object. Its tenant_id must correspond to an existing tenant.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no tenant with the given tenant_id exists.

        Examples
        --------
        >>> from sentinelresponse.tenants.models import Tenant
        >>> tm = TenantManager()
        >>> tenant = Tenant(tenant_id=1, name="Financeiro")
        >>> tm.create_tenant(tenant)
        >>> tenant.name = "Financeiro - Atualizado"
        >>> tm.update_tenant(tenant)

        """
        if tenant.tenant_id in self.tenants:
            logging.info(f"Atualizando tenant: {tenant}")
            self.tenants[tenant.tenant_id] = tenant
        else:
            raise NotFoundError(
                f"Tenant {tenant.tenant_id} não encontrado para atualização."
            )

    def delete_tenant(self, tenant_id: int) -> None:
        """Delete a tenant by its unique identifier.

        This method removes the Tenant object associated with the given tenant_id from the
        internal dictionary. If the tenant is not found, a NotFoundError is raised.

        Parameters
        ----------
        tenant_id : int
            The unique identifier of the tenant to delete.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no tenant with the specified tenant_id exists.

        Examples
        --------
        >>> from sentinelresponse.tenants.models import Tenant
        >>> tm = TenantManager()
        >>> tm.create_tenant(Tenant(tenant_id=1, name="Financeiro"))
        >>> tm.delete_tenant(1)

        """
        if tenant_id in self.tenants:
            logging.info(f"Excluindo tenant com ID: {tenant_id}")
            del self.tenants[tenant_id]
        else:
            raise NotFoundError(f"Tenant {tenant_id} não encontrado para exclusão.")

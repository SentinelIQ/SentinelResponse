class Tenant:
    """Represents a tenant, which can be an organization or a team.

    This class encapsulates a tenant entity within the system, where each tenant is
    uniquely identified by a tenant_id and has an associated name. Tenants can be used
    to segregate data and operations in multi-tenant environments.

    Parameters
    ----------
    tenant_id : int
        Unique identifier for the tenant.
    name : str
        The name of the tenant.

    Attributes
    ----------
    tenant_id : int
        Unique identifier for the tenant.
    name : str
        The name of the tenant.

    Examples
    --------
    >>> tenant = Tenant(tenant_id=1, name="Financeiro")
    >>> print(tenant)
    Tenant(id=1, name='Financeiro')

    """

    def __init__(self, tenant_id: int, name: str):
        """Initialize a new Tenant instance.

        Parameters
        ----------
        tenant_id : int
            Unique identifier for the tenant.
        name : str
            The name of the tenant.

        """
        self.tenant_id = tenant_id
        self.name = name

    def __repr__(self) -> str:
        """Return the official string representation of the Tenant.

        Returns
        -------
        str
            A string representation of the Tenant, showing its tenant_id and name.

        Examples
        --------
        >>> tenant = Tenant(tenant_id=1, name="Financeiro")
        >>> repr(tenant)
        "Tenant(id=1, name='Financeiro')"

        """
        return f"Tenant(id={self.tenant_id}, name='{self.name}')"

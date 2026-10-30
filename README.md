# Microsoft Entra ID scripts

The `main.py` CLI uses Microsoft Graph v1.0 and app-only client-credentials
authentication. Operation modules expose parameterized functions and do not
parse arguments or start operations when run directly:

- `create_user.py` — expose the parameterized user-creation operation; `main.py` prompts for the temporary password without echoing it.
- `create_group.py` — create a security or Microsoft 365 group.
- `add_group_member.py` — add a user, group, or service principal to a group.
- `create_app_registration.py` — create an app registration without API permissions or credentials.
- `create_enterprise_app.py` — create the tenant's service principal for an app registration.
- `assign_enterprise_app.py` — assign a user or group to an enterprise app.

## Setup

1. Register an automation app in Entra ID and configure a client secret outside
   this repository. Grant only the Microsoft Graph **application permissions**
   needed for the scripts you intend to run, then grant tenant admin consent.
   Typical permissions are `User.ReadWrite.All`, `Group.ReadWrite.All`,
   `GroupMember.ReadWrite.All`, `Application.ReadWrite.All`, and
   `AppRoleAssignment.ReadWrite.All`. Microsoft Graph may require additional
   read permissions depending on tenant policy and the operation.
2. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

3. Set credentials in the current PowerShell session (do not put secrets in
   source files):

   ```powershell
   $env:ENTRA_TENANT_ID = "<tenant-id>"
   $env:ENTRA_CLIENT_ID = "<automation-app-client-id>"
   $env:ENTRA_CLIENT_SECRET = "<client-secret>"
   ```

## Examples

```powershell
py .\main.py create-user --display-name "Example User" --user-principal-name "example.user@contoso.com"
py .\main.py create-group --display-name "Engineering" --mail-nickname "engineering"
py .\main.py create-group --display-name "Project Team" --mail-nickname "project-team" --type microsoft-365
py .\main.py add-group-member --group-id "<group-object-id>" --member-id "<user-object-id>"
py .\main.py create-app-registration --display-name "Internal Service"
py .\main.py create-enterprise-app --app-id "<application-client-id>"
py .\main.py assign-enterprise-app --service-principal-id "<enterprise-app-object-id>" --principal-id "<user-or-group-object-id>"
```

Python callers can import the same parameterized operations directly, for
example:

```python
from graph_client import GraphClient
from create_group import create_group

group = create_group(
    GraphClient(),
    display_name="Engineering",
    mail_nickname="engineering",
)
```

The assignment script uses the all-zero app-role ID by default to grant the
enterprise app's default access. Supply `--app-role-id` to assign a specific
app role instead. Assignments grant access; verify the application and target
objects before running the command.

The app registration script intentionally creates no client secret, certificate,
redirect URI, or API permission. Configure those separately according to the
application's needs and security requirements. Graph errors are reported by
the scripts and are not suppressed.

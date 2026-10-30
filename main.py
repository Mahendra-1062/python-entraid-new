import argparse
import json
from getpass import getpass
from typing import Sequence

from add_group_member import add_group_member
from assign_enterprise_app import assign_enterprise_app
from create_app_registration import create_app_registration
from create_enterprise_app import create_enterprise_app
from create_group import create_group
from create_user import make_user
from graph_client import GraphClient, normalize_object_id


SIGN_IN_AUDIENCES = (
    "AzureADMyOrg",
    "AzureADMultipleOrgs",
    "AzureADandPersonalMicrosoftAccount",
    "PersonalMicrosoftAccount",
)


def parse_object_id(value: str) -> str:
    try:
        return normalize_object_id(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage Microsoft Entra ID objects through Microsoft Graph."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    user_parser = commands.add_parser("create-user", help="Create a user.")
    user_parser.add_argument("--display-name", required=True)
    user_parser.add_argument("--user-principal-name", required=True)
    user_parser.add_argument("--mail-nickname")

    group_parser = commands.add_parser("create-group", help="Create a group.")
    group_parser.add_argument("--display-name", required=True)
    group_parser.add_argument("--mail-nickname", required=True)
    group_parser.add_argument("--description", default="")
    group_parser.add_argument(
        "--type",
        choices=("security", "microsoft-365"),
        default="security",
    )

    member_parser = commands.add_parser(
        "add-group-member", help="Add a directory object to a group."
    )
    member_parser.add_argument("--group-id", required=True, type=parse_object_id)
    member_parser.add_argument("--member-id", required=True, type=parse_object_id)

    app_parser = commands.add_parser(
        "create-app-registration", help="Create an app registration."
    )
    app_parser.add_argument("--display-name", required=True)
    app_parser.add_argument(
        "--sign-in-audience",
        choices=SIGN_IN_AUDIENCES,
        default="AzureADMyOrg",
    )

    enterprise_app_parser = commands.add_parser(
        "create-enterprise-app",
        help="Create or retrieve an app's enterprise application.",
    )
    enterprise_app_parser.add_argument(
        "--app-id", required=True, type=parse_object_id
    )

    assignment_parser = commands.add_parser(
        "assign-enterprise-app",
        help="Assign a user or group to an enterprise app.",
    )
    assignment_parser.add_argument(
        "--service-principal-id", required=True, type=parse_object_id
    )
    assignment_parser.add_argument(
        "--principal-id", required=True, type=parse_object_id
    )
    assignment_parser.add_argument(
        "--app-role-id",
        default="00000000-0000-0000-0000-000000000000",
        type=parse_object_id,
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    password = None
    if args.command == "create-user":
        password = getpass("Temporary password (input hidden): ")
        confirmation = getpass("Confirm temporary password: ")
        if not password or password != confirmation:
            parser.error("Passwords must be non-empty and match.")

    graph = GraphClient()
    if args.command == "create-user":
        assert password is not None
        result = make_user(
            graph,
            args.display_name,
            args.user_principal_name,
            password,
            args.mail_nickname,
        )
        if result:
            print("User created successfully.")
    elif args.command == "create-group":
        result = create_group(
            graph,
            args.display_name,
            args.mail_nickname,
            args.description,
            args.type,
        )
    elif args.command == "add-group-member":
        add_group_member(graph, args.group_id, args.member_id)
        print(f"Added directory object {args.member_id} to group {args.group_id}.")
        return
    elif args.command == "create-app-registration":
        result = create_app_registration(
            graph, args.display_name, args.sign_in_audience
        )
    elif args.command == "create-enterprise-app":
        result = create_enterprise_app(graph, args.app_id)
    elif args.command == "assign-enterprise-app":
        result = assign_enterprise_app(
            graph,
            args.service_principal_id,
            args.principal_id,
            args.app_role_id,
        )
    else:
        parser.error(f"Unsupported command: {args.command}")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

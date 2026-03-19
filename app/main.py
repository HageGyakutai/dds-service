from __future__ import annotations


def healthcheck() -> str:
    return "ok"


def main() -> None:
    print(healthcheck())


if __name__ == "__main__":
    main()

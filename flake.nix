{
  description = "Circular Protocol Python API - Official blockchain SDK";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = {
            permittedInsecurePackages = [
              "python3.11-ecdsa-0.19.1"
            ];
          };
        };
        python = pkgs.python311;

        pythonEnv = python.withPackages (ps: with ps; [
          # Runtime dependencies
          requests
          ecdsa
          typing-extensions

          # Optional async support
          aiohttp

          # Development dependencies
          pytest
          pytest-timeout
          pytest-cov
          pytest-asyncio
          black
          mypy
          ruff
          types-requests

          # Build dependencies
          setuptools
          wheel
          setuptools-scm
        ]);
      in
      {
        packages = {
          default = pythonEnv;

          # Package for running tests
          test = pkgs.writeShellScriptBin "circular-test" ''
            cd ${./.}
            ${pythonEnv}/bin/python -m pytest tests/ -v --tb=short
          '';

          # Package for running tests with coverage
          test-cov = pkgs.writeShellScriptBin "circular-test-cov" ''
            cd ${./.}
            ${pythonEnv}/bin/python -m pytest tests/ -v --cov=circular_protocol_api --cov-report=term-missing
          '';

          # Package for linting
          lint = pkgs.writeShellScriptBin "circular-lint" ''
            cd ${./.}
            echo "Running black..."
            ${pythonEnv}/bin/black --check src/ tests/
            echo "Running ruff..."
            ${pythonEnv}/bin/ruff check src/ tests/
            echo "Running mypy..."
            ${pythonEnv}/bin/mypy src/
          '';

          # Package for formatting
          format = pkgs.writeShellScriptBin "circular-format" ''
            cd ${./.}
            ${pythonEnv}/bin/black src/ tests/
            ${pythonEnv}/bin/ruff check --fix src/ tests/
          '';
        };

        apps = {
          default = {
            type = "app";
            program = "${self.packages.${system}.test}/bin/circular-test";
          };

          test = {
            type = "app";
            program = "${self.packages.${system}.test}/bin/circular-test";
          };

          test-cov = {
            type = "app";
            program = "${self.packages.${system}.test-cov}/bin/circular-test-cov";
          };

          lint = {
            type = "app";
            program = "${self.packages.${system}.lint}/bin/circular-lint";
          };

          format = {
            type = "app";
            program = "${self.packages.${system}.format}/bin/circular-format";
          };
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [ pythonEnv ];

          shellHook = ''
            echo "Circular Protocol Python SDK Development Environment"
            echo "Python version: ${python.version}"
            echo ""
            echo "Available commands:"
            echo "  pytest tests/ -v          - Run tests"
            echo "  black src/ tests/         - Format code"
            echo "  ruff check src/ tests/    - Lint code"
            echo "  mypy src/                 - Type check"
            echo ""
            echo "Or use nix run:"
            echo "  nix run                   - Run tests (default)"
            echo "  nix run .#test            - Run tests"
            echo "  nix run .#test-cov        - Run tests with coverage"
            echo "  nix run .#lint            - Run linters"
            echo "  nix run .#format          - Format code"
          '';
        };
      }
    );
}

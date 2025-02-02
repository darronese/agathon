{ pkgs ? import <nixpkgs> { } }:

let
  python = pkgs.python3.withPackages (ps: with ps; [ pandas ]);
in
pkgs.mkShell {
  buildInputs = [
    python
  ];
  shellHook = ''
    PYTHONPATH=${python}/${python.sitePackages}
  '';
}

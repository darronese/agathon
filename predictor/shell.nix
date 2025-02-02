{ pkgs ? import <nixpkgs> { } }:

let
  python = pkgs.python3.withPackages (ps: with ps; [ matplotlib pandas scikit-learn ]);
in
pkgs.mkShell {
  buildInputs = [
    python
  ];
  shellHook = ''
    PYTHONPATH=${python}/${python.sitePackages}
  '';
}

let
  # channels/nixpkgs-unstable on 2019-01-10
  pkgs = import (fetchTarball {
    url = "https://github.com/nixos/nixpkgs/archive/7d864c6bd6391baa516118051ec5fb7e9836280e.tar.gz";
    sha256 = "0zh41p52vnk739cw5s12j4c4gg3bv90hqprp9h0w2k898l9sni5d";
  }) {};

  pythonDeps = pythonPackages: with pythonPackages; [
    numpy pytest pytest-benchmark
  ];

in (pkgs.python3.withPackages pythonDeps).env

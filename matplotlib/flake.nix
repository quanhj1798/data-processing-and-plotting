{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = { 
    self, nixpkgs 
  }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonEnv = pkgs.python3.withPackages (ps: with ps; [ pandas matplotlib pygobject3 ]);
    in {
      devShells.${system}.default = pkgs.mkShell {
        nativeBuildInputs = with pkgs; [ gobject-introspection ];
        packages = [ pythonEnv pkgs.gtk4 pkgs.texliveFull ];
        shellHook = '' export PYTHONPATH="./matplotlib:$PYTHONPATH" '';
      };
    };
}

{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
  };
  outputs = { 
    self, nixpkgs 
  }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonEnv = (
        pkgs.python312.override {
          packageOverrides = self: super: {
            #lmfitxps
            lmfitxps = self.buildPythonPackage {
              pname = "lmfitxps";
              version = "4.2.0";
              src = pkgs.fetchFromGitHub {
                owner = "Julian-Hochhaus";
                repo = "lmfitxps";
                rev = "4.2.0";
                sha256 = "sha256-SWtIbqZLTqFzAsizbrE00L11/SxRMKMQhTvyIJ26TRk=";
              };
              pyproject = true;
              build-system = [ self.setuptools self.wheel ];
              propagatedBuildInputs = [ self.scipy self.numpy self.lmfit ];
            };
          };
        }
      ).withPackages (ps: with ps; [ lmfitxps openpyxl pymatgen ase mdtraj ]);
    in { 
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pythonEnv ];
        shellHook = '' export PYTHONPATH="./data_processing:$PYTHONPATH" '';
      };
    };
}

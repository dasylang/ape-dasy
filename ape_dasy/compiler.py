import os
import dasy
from pathlib import Path
from typing import Dict, List, Optional, Set
from ape.api.compiler import CompilerAPI
from ape.types import ContractType
from semantic_version import Version

class DasyCompiler(CompilerAPI):

    @property
    def name(self) -> str:
        return "dasy"

    def compile(self, contracts_filepaths: List[Path], base_path: Optional[Path] = None) -> List[ContractType]:
        contract_types = []
        if base_path:
            for path in contracts_filepaths:
                with open(os.path.join(base_path, path)) as f:
                    src = f.read()
                    data = dasy.compile(src).__dict__
                    data["contractName"] = Path(path).stem
                    data["sourceId"] = path
                    data["deploymentBytecode"] = {"bytecode": data["bytecode"]}
                    data["runtimeBytecode"] = {"bytecode": data["bytecode_runtime"]}
                    contract_types.append(ContractType.parse_obj(data))
        return contract_types

    def get_compiler_settings(
            self, contract_filepaths: List[Path], base_path: Optional[Path] = None
        ) -> Dict[Version, Dict]:
        settings = {}
        settings["0.1.17"] = {"optimize": True}
        return settings

    def get_versions(self, all_paths: List[Path]) -> Set[str]:
        return set(['0.1.17'])

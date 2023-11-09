requirement_abi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "admin",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "licenseAddress",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "AccessControlBadConfirmation",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "bytes32",
                "name": "neededRole",
                "type": "bytes32"
            }
        ],
        "name": "AccessControlUnauthorizedAccount",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "EnforcedPause",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "ExpectedPause",
        "type": "error"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "evidenceID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "additionalData",
                "type": "bytes"
            }
        ],
        "name": "EvidenceRegistered",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "evidenceID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "additionalData",
                "type": "bytes"
            }
        ],
        "name": "EvidenceRevoked",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "requirementName",
                "type": "bytes"
            }
        ],
        "name": "LicenseRequirementRegistered",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "additionalData",
                "type": "bytes"
            }
        ],
        "name": "LicenseRequirementRevoked",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "Paused",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "previousAdminRole",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "newAdminRole",
                "type": "bytes32"
            }
        ],
        "name": "RoleAdminChanged",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            }
        ],
        "name": "RoleGranted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            }
        ],
        "name": "RoleRevoked",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "Unpaused",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "DEFAULT_ADMIN_ROLE",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "ISSUER_ROLE",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "PAUSER_ROLE",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "_licenseAddress",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            }
        ],
        "name": "getEvidences",
        "outputs": [
            {
                "internalType": "bytes[]",
                "name": "",
                "type": "bytes[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            }
        ],
        "name": "getRequirement",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "bytes",
                        "name": "requirementID",
                        "type": "bytes"
                    },
                    {
                        "internalType": "bytes",
                        "name": "requirementName",
                        "type": "bytes"
                    },
                    {
                        "internalType": "bytes",
                        "name": "state",
                        "type": "bytes"
                    },
                    {
                        "internalType": "bytes",
                        "name": "additionalData",
                        "type": "bytes"
                    }
                ],
                "internalType": "struct SharedStructs.RequirementStructBase",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            }
        ],
        "name": "getRoleAdmin",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "grantRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "hasRole",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "pause",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "paused",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "requirementName",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "additionalData",
                "type": "bytes"
            }
        ],
        "name": "register",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "evidenceID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "additionalData",
                "type": "bytes"
            }
        ],
        "name": "registerEvidence",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "callerConfirmation",
                "type": "address"
            }
        ],
        "name": "renounceRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "additionalData",
                "type": "bytes"
            }
        ],
        "name": "revoke",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "licenseID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "requirementID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "evidenceID",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "additionalData",
                "type": "bytes"
            }
        ],
        "name": "revokeEvidence",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "revokeRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes4",
                "name": "interfaceId",
                "type": "bytes4"
            }
        ],
        "name": "supportsInterface",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "unpause",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

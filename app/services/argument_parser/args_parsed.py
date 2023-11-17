"""
"""
import json

default_params = json.loads("""{
    "tests": {
        "alias": "-t",
        "value": [0]
    },
    "parameters": {
        "alias": "-P",
        "blockFrequencyTestBlockLength": {
            "id": "1",
            "value": 16384
        },
        "nonOverlappingTemplateTestBlockLength":{
            "id": "2",
            "value": 9
        },
        "overlappingTemplateTestBlockLength": {
            "id": "3",
            "value": 9
        },
        "approximateEntropyTestBlockLength": {
            "id": "4",
            "value": 10
        },
        "serialTestBlockLength": {
            "id": "5",
            "value": 16
        },
        "linearComplexityTestBlockLength": {
            "id": "6",
            "value": 500
        },
        "numberOfBitcountRuns": {
            "id": "7",
            "value": 1
        },
        "uniformityBins": {
            "id": "8",
            "value": 18.12
        },
        "bitsToProcessPerIteration": {
            "id": "9",
            "value": 1048576
        },
        "uniformityCutoffLevel": {
            "id": "10",
            "value": 0.0001
        },
        "alphaConfidenceLevel": {
            "id": "11",
            "value": 0.01
        }
    },
    "iterations": {
        "alias": "-i",
        "value": 1000
    },
    "workDir": {
        "alias": "-w",
        "value": "."
    },
    "createResultFiles": {
        "alias": "-s",
        "value": ""
    },
    "bitcount": {
        "alias": "-S",
        "value": 1048576
    },
    "numOfThreads": {
        "alias": "-T",
        "value": 1
    }
}""")

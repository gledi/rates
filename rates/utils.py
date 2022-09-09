from enum import Enum


class Environment(str, Enum):
    testing = "testing"
    development = "development"
    production = "production"
